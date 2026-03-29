#!/usr/bin/env bash
set -euo pipefail

# Boilerworks — Django Micro
# Usage: ./run.sh [command]

COMPOSE_FILE=""

if [ -f "docker-compose.yml" ]; then
    COMPOSE_FILE="docker-compose.yml"
elif [ -f "docker-compose.yaml" ]; then
    COMPOSE_FILE="docker-compose.yaml"
fi

compose() {
    if [ -n "$COMPOSE_FILE" ]; then
        docker compose -f "$COMPOSE_FILE" "$@"
    else
        echo "No docker-compose file found"
        exit 1
    fi
}

case "${1:-help}" in
    up|start)
        compose up -d --build
        echo "Waiting for services..."
        sleep 5
        compose exec -T api python manage.py migrate --noinput 2>&1 | tail -3
        echo ""
        echo "Services running. Check status with: ./run.sh status"
        ;;
    down|stop)
        compose down
        ;;
    restart)
        compose down
        compose up -d --build
        ;;
    status|ps)
        compose ps
        ;;
    logs)
        compose logs -f "${2:-}"
        ;;
    seed)
        echo "No seed command configured for this template"
        ;;
    test)
        compose exec api python -m pytest --cov --cov-report=term-missing -v
        ;;
    lint)
        compose exec api python -m ruff check . && compose exec api python -m ruff format --check .
        ;;
    shell)
        compose exec api bash
        ;;
    migrate)
        compose exec api python manage.py migrate
        ;;
    help|*)
        echo "Usage: ./run.sh <command>"
        echo ""
        echo "Commands:"
        echo "  up, start     Start all services"
        echo "  down, stop    Stop all services"
        echo "  restart       Restart all services"
        echo "  status, ps    Show service status"
        echo "  logs [svc]    Tail logs (optionally for one service)"
        echo "  seed          Seed the database"
        echo "  test          Run tests"
        echo "  lint          Run linters"
        echo "  shell         Open a shell in the API container"
        echo "  migrate       Run database migrations"
        echo "  help          Show this help"
        ;;
esac
