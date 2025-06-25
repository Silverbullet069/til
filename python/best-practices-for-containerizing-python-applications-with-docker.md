# Best Practices For Containerizing Python Applications With Docker

<!-- tl;dr starts -->

<!-- tl;dr ends -->

```py
# Flask
@app.route('/health', methods=['GET'])
def health():
	# Handle here any business logic for ensuring you're application is healthy (DB connections, etc...)
    return "Healthy: OK"
```

```Dockerfile
# Build
FROM python:latest as build
RUN apt-get update && \
  apt-get install -y --no-install-recommends build-essential gcc && \
  rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

# Production
# FROM python:alpine
FROM python:slim-bullseye
RUN groupadd -g 1000 python && useradd -r -u 1000 -g python python
RUN mkdir /app && chown python:python /app
WORKDIR /app
COPY --chown=python:python --from=build /app/.venv ./.venv
COPY --chown=python:python . .
ENV PATH="/app/.venv/bin:$PATH"
USER 1000
CMD ["gunicorn", "--bind", "0.0.0.0:5000"]
# be mindful of unhandled events or problems that could set the app to unhealthy states
# e.g. it won't work anymore yet it won't kill the process => a running Python app server
# that doesn't respond to HTTP Request anymore
# Solution: implement a health check API endpoint `/health` or `/monitoring` + Docker HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health
# NOTE: HEALTHCHECK directives are ignored in K8s.
```

## References

- [Liran Tal, Daniel Campos Olivares, Snyk Blog "Best practices for containerizing Python applications with Docker"](https://snyk.io/blog/best-practices-containerizing-python-docker/)
