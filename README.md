# caz-alerting-svc
Cazadora - Alerting Microservice

# caz-detection-svc
Cazadora - Detection Microservice

## Running with Docker and EKS

This project is containerized using Docker and Docker Compose. It uses Python 3.12.8 (alpine) and manages dependencies with Pipenv. The main service runs on port `5002`.

### Build and Run

From the project root, run:

```sh
docker compose up --build
```

This will build the `alert-svc` service from `./alert-svc` and start it on [http://localhost:5002](http://localhost:5002).

### Ports
- `5002`: Exposed by the Flask application and mapped to the host.

### Configuration
- No environment variables are required by default. If you add a `.env` file to `./alert-svc`, uncomment the `env_file` line in the `compose.yaml`.
- The service runs as a non-root user for security.
- All dependencies are installed via Pipenv and included in the image.
- The container uses `bootstrap.sh` as its entrypoint.

### Networks
- The service is attached to the `alert-net` Docker network (bridge driver).

---

For development or troubleshooting, you can use the `bootstrap.sh` script as the container entrypoint. All dependencies are installed via Pipenv and included in the image.
