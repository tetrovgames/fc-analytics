#!/bin/sh

# uvicorn app.main:app --host 0.0.0.0 --port "$PORT"

# https://fastapi.tiangolo.com/deployment/docker/#behind-a-tls-termination-proxy
uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port "$PORT"
