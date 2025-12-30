# AI-LogAnalyzer

## Project: Log Anomaly Detection & Alerting Service (DevOps)
## Overview

This project is a containerized, Kubernetes-deployed log analysis service designed to continuously ingest application logs, analyze them in time windows, and detect abnormal error patterns based on historical baselines.

The focus of this project is DevOps system design and operability, not heavy ML.
The service is designed to behave like a real production background worker.

## Problem Statement
In production environments, static alert rules (for example, alert on every ERROR log) create excessive noise and lead to alert fatigue.

This project addresses that problem by:

- Treating logs as a continuous stream

- Analyzing logs over time windows

- Detecting abnormal behavior relative to historical baselines

- Triggering alerts only when anomalies persist, not on single events

## High-Level Architecture

- No request/response API

- No manual triggering

- Runs as a long-lived background service

## Key Features

- Continuous log ingestion (stream-based, not file-based batch processing)

- Time-window based log analysis

- Stateful baseline tracking using historical windows

- Alert noise reduction using cooldowns and persistence checks

- Fully configurable via environment variables

- Containerized and Kubernetes-ready

- Graceful shutdown handling for Docker/Kubernetes

## Technology Stack

- Language: Python 3

- Containerization: Docker

- Orchestration: Kubernetes (Minikube)

- Configuration: Environment variables / ConfigMaps

- Alerting: Webhook (Slack-compatible)

## How It Works
### 1. Log Ingestion

- Logs are treated as a stream

- The service continuously tails a log file mounted into the container

- Designed to survive restarts and delayed log availability

### 2. Time Windows

- Logs are grouped into fixed-duration windows (e.g., 30 seconds)

- Metrics extracted per window:

- Total log count

- ERROR log count

### 3. Baseline Tracking

- Maintains historical error counts across previous windows

- Computes a rolling baseline (average error rate)

### 4. Anomaly Detection
An anomaly is detected when:
```bash
current_error_count > baseline_error_rate × threshold
```

This approach is:

- Explainable

- Easy to tune

- Operationally reliable

### 5. Alert Control

- Alerts are sent only if:

- An anomaly persists

- Cooldown period has expired

- Prevents alert storms and false positives

### Configuration

All behavior is configurable via environment variables:

| Variable               | Description                    |
| ---------------------- | ------------------------------ |
| LOG_FILE_PATH          | Path to log file               |
| WINDOW_SIZE_SECONDS    | Analysis window size           |
| BASELINE_WINDOWS       | Number of windows for baseline |
| ERROR_SPIKE_MULTIPLIER | Anomaly sensitivity            |
| ALERT_COOLDOWN_SECONDS | Alert suppression window       |

In Kubernetes, these are injected using a ConfigMap.

### Running Locally (Docker)
```bash
docker build -t log-analyzer:1.0 .
mkdir -p logs
touch logs/app.log

docker run -it \
  -v $(pwd)/logs:/var/log/app \
  log-analyzer:1.0
```

### Generate logs:
```bash
echo "ERROR Database connection failed" >> logs/app.log
```

### Write logs on the Minikube node:
```bash
minikube ssh
sudo mkdir -p /tmp/app-logs
sudo chmod 666 /tmp/app-logs/app.log
echo "ERROR DB failure" >> /tmp/app-logs/app.log
```

## Design Decisions (Important)

- No heavy ML: Baseline-based detection is more explainable and reliable for ops

- Single replica: Stateful baseline tracking avoids duplicate alerts

- Non-root container: Reduces security risk

- Silent by default: Avoids log noise during normal operation

## What This Project Demonstrates

- Real-world DevOps system design

- Long-running service behavior

- Log ingestion and analysis pipelines

- Docker and Kubernetes fundamentals

- Operational reliability and alert hygiene

## Future Improvements

- Replace print statements with structured logging

- Add HTTP /health endpoint

- Support multiple log sources

- Externalize state (Redis) for HA deployments

- Integrate with Prometheus metrics