# Local Setup & Operations Guide

## Quick Start
Run the entire platform with one command:

```bash
docker compose up -d
```
Or using `Makefile`:
```bash
make up
```

## Useful Makefile Commands

```bash
make up        # Build & launch all containers
make down      # Stop & remove containers
make logs      # Tail gateway container logs
make test      # Run pytest unit test suite
make benchmark # Execute k6 load test
make clean     # Stop containers & purge temporary files
```
