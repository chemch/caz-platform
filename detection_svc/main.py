from flask import Flask, jsonify, request

from app.model.beacon import Beacon, BeaconSchema
from app.model.file_hash import FileHash, FileHashSchema
from app.model.detection_type import *

app = Flask(__name__)
app.config.from_object("detection_svc.config")

detections = [
    Beacon('Firewall', 'x.com', 100),
    FileHash('CrowdStrike', 'notepad.exe', 85, 'md5', 'c0202cf6aeab8437c638533d14563d35')
]

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