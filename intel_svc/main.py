from datetime import timedelta, datetime
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask, jsonify, request
from app.model.report import ReportSchema, Report
from app.model.indicator import IndicatorSchema, Indicator
from app.model.intel_type import *
from intel_svc.app.model.severity_type import SeverityType
from intel_svc.app.model.verdict_type import VerdictType
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)

# Default fallback
otlp_exporter = None
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4318/v1/traces")

try:
    health_check_url = otlp_endpoint.replace("/v1/traces", "/")
    response = requests.get(health_check_url, timeout=2)
    response.raise_for_status()
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
except Exception as e:
    logging.warning(f"Tracing setup failed, continuing without tracing: {e}")

if otlp_exporter:
    provider = TracerProvider(resource=Resource.create({"service.name": "intel-svc"}))
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    logging.info("Tempo tracing initialized.")

# Always after set_tracer_provider
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
app.config.from_object("intel_svc.config")

FlaskInstrumentor().instrument_app(app)

intel = [
    Report('Mallard Spider Update - 20250401', 'Mallard Spider Increases SoHo Coverage in US', 'UNC6786', 90, VerdictType.MALICIOUS, SeverityType.MEDIUM, 'VT', 67, datetime.now() - timedelta(days=10) ),
    Indicator('DNS Exfiltration', 'APT43', 68, VerdictType.UNKNOWN, SeverityType.LOW, 'AlienVault', 'I-89775678', 'x.com'),
]


@app.route('/')
def get_intel():
    with tracer.start_as_current_span("get_intel"):
        _intel = []
        for artifact in intel:
            print(artifact.type)
            if artifact.type == IntelType.REPORT:
                _intel.append(ReportSchema().dump(artifact))
            elif artifact.type == IntelType.INDICATOR:
                _intel.append(IndicatorSchema().dump(artifact))
        return jsonify(_intel)

@app.route('/indicators')
def get_indicators():
    schema = IndicatorSchema(many=True)
    indicators = schema.dump(
        filter(lambda t: t.type == IntelType.INDICATOR, intel)
    )

    return jsonify(indicators)


@app.route('/indicators', methods=['POST'])
def add_indicator():
    indicator = IndicatorSchema().load(request.get_json())
    intel.append(indicator)
    return "", 204


@app.route('/reports')
def get_reports():
    schema = ReportSchema(many=True)
    reports = schema.dump(
        filter(lambda t: t.type == IntelType.REPORT, intel)
    )

    return jsonify(reports)


@app.route('/reports', methods=['POST'])
def add_report():
    report = ReportSchema().load(request.get_json())
    intel.append(report)
    return "", 204


if __name__ == "__main__":
    app.run()