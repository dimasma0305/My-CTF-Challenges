#!/bin/sh

export SECRET_KEY=$(python -c "import os;print(os.urandom(16).hex(),end='')")

gunicorn \
    main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 \
    --threads 4 \
    --max-requests 100 \
    --timeout 10 \
    --bind 0.0.0.0:8000
