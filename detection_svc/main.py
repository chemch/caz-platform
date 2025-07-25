from flask import Flask, jsonify, request
from app.model.beacon import Beacon, BeaconSchema
from app.model.file_hash import FileHash, FileHashSchema
from app.model.detection_type import *
from jaeger_client import Config
import logging
import atexit

app = Flask(__name__)
app.config.from_object("detection_svc.config")

# Configure logging cleanly
logging.getLogger('').handlers = []
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

# Initialize Jaeger tracer
def init_tracer(service_name):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
            'reporter_batch_size': 1,
            'local_agent': {
                'reporting_host': 'jaeger-agent.tracing.svc.cluster.local',
                'reporting_port': 6831,
            },
        },
        service_name=service_name,
    )
    return config.initialize_tracer()

tracer = init_tracer('detection-svc')

# Ensure trace is closed at shutdown so traces flush
atexit.register(tracer.close)

# Mock data
detections = [
    Beacon('Firewall', 'x.com', 100, '192.168.0.95', '167.89.76.91', 50878, 80, 'TCP'),
    FileHash('CrowdStrike', 'notepad.exe', 85, 'md5', 'c0202cf6aeab8437c638533d14563d35', '192.168.0.74')
]

# Traced endpoint
@app.route('/health')
def index():
    with tracer.start_span('health-span') as span:
        span.set_tag('endpoint', '/health')
        return "Up"

@app.route('/')
def get_detections():
    _detections = []
    for detection in detections:
        if detection.type == DetectionType.BEACON:
            _detections.append(BeaconSchema().dump(detection))
        elif detection.type == DetectionType.FILE_HASH:
            _detections.append(FileHashSchema().dump(detection))
    return jsonify(_detections)

@app.route('/beacons')
def get_beacons():
    schema = BeaconSchema(many=True)
    beacons = schema.dump(
        filter(lambda t: t.type == DetectionType.BEACON, detections)
    )
    return jsonify(beacons)

@app.route('/beacons', methods=['POST'])
def add_beacon():
    beacon = BeaconSchema().load(request.get_json())
    detections.append(beacon)
    return "", 204

@app.route('/file_hashes')
def get_file_hashes():
    schema = FileHashSchema(many=True)
    file_hashes = schema.dump(
        filter(lambda t: t.type == DetectionType.FILE_HASH, detections)
    )
    return jsonify(file_hashes)

@app.route('/file_hashes', methods=['POST'])
def add_file_hash():
    file_hash = FileHashSchema().load(request.get_json())
    detections.append(file_hash)
    return "", 204

if __name__ == "__main__":
    app.run()