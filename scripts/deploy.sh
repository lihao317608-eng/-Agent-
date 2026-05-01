#!/usr/bin/env bash
set -e

if [ -f .env ]; then
  set -a; source .env; set +a
fi

docker compose pull || true
docker compose up -d --build

echo "Backend: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
