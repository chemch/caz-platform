from flask import Flask, jsonify, request

from app.model.detection import DetectionSchema, Detection
from app.model.incident import IncidentSchema, Incident
from app.model.alert_type import *


app = Flask(__name__)

alerts = [
    Detection('Malware Installation', 2),
    Detection('C2 Beacon', 1),
    Incident('Accounts Hijacked', 5),
]

@app.route('/')
def get_alerts():
    _alerts = []
    for alert in alerts:
        if alert.type == AlertType.DETECTION:
            _alerts.append(DetectionSchema().dump(alert))
        elif alert.type == AlertType.INCIDENT:
            _alerts.append(IncidentSchema().dump(alert))
    return jsonify(_alerts)

@app.route('/detections')
def get_detections():
    schema = DetectionSchema(many=True)
    detections = schema.dump(
        filter(lambda t: t.type == AlertType.DETECTION, alerts)
    )

    return jsonify(detections)


@app.route('/detections', methods=['POST'])
def add_detection():
    detection = DetectionSchema().load(request.get_json())
    alerts.append(detection)
    return "", 204


@app.route('/incidents')
def get_incidents():
    schema = IncidentSchema(many=True)
    incidents = schema.dump(
        filter(lambda t: t.type == AlertType.INCIDENT, alerts)
    )

    return jsonify(incidents)


@app.route('/incidents', methods=['POST'])
def add_incident():
    incident = IncidentSchema().load(request.get_json())
    alerts.append(incident)
    return "", 204


if __name__ == "__main__":
    app.run()