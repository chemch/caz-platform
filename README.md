# caz-alerting-svc
Cazadora - Alerting Microservice

## Running with Docker

This project is containerized using Docker and Docker Compose. It uses Python 3.12.8 (alpine) and manages dependencies with Pipenv. The main service runs on port `5002`.

### Build and Run

From the project root, run:

```sh
docker compose up --build
```

This will build the `cashman-flask-project` service from `./cashman-flask-project` and start it on [http://localhost:5002](http://localhost:5002).

### Ports
- `5002`: Exposed by the Flask application and mapped to the host.

### Configuration
- No environment variables are required by default. If you add a `.env` file to `./cashman-flask-project`, uncomment the `env_file` line in the `docker-compose.yml`.
- The service runs as a non-root user for security.

### Networks
- The service is attached to the `cashman-net` Docker network (bridge driver).

---

For development or troubleshooting, you can use the `bootstrap.sh` script as the container entrypoint. All dependencies are installed via Pipenv and included in the image.
