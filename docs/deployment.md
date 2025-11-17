# Deployment Guide

## Prerequisites

- Python 3.10+
- Google Cloud Project with Vertex AI enabled
- gcloud CLI installed and configured
- Docker (for containerization)

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### Running Locally

```bash
# Development with ADK web UI
adk web agents/orchestrator.py

# Or run programmatically
python -m agents.orchestrator
```

## Deployment to Vertex AI

### Build Container

```bash
# Create Dockerfile
docker build -t agent-reliability-guardian:latest .

# Push to Google Container Registry
docker tag agent-reliability-guardian:latest \
  gcr.io/$PROJECT_ID/agent-reliability-guardian:latest

docker push gcr.io/$PROJECT_ID/agent-reliability-guardian:latest
```

### Deploy to Cloud Run

```bash
gcloud run deploy agent-reliability-guardian \
  --image=gcr.io/$PROJECT_ID/agent-reliability-guardian:latest \
  --platform=managed \
  --region=us-central1 \
  --memory=2Gi \
  --cpu=2 \
  --set-env-vars="GOOGLE_API_KEY=$GOOGLE_API_KEY"
```

### Deploy to Agent Engine

```bash
adk deploy agent_engine \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=us-central1 \
  --staging_bucket=gs://your-bucket \
  --trace_to_cloud \
  --enable_cloud_trace \
  agents/orchestrator.py
```

## Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your-api-key
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional
LOG_LEVEL=INFO
MONITORING_INTERVAL=60
RECOVERY_TIMEOUT=30
SLA_TARGET_UPTIME=99.7
```

### Configuration File

Edit `config.py` to customize:
- Monitoring thresholds
- Recovery policies
- Compliance settings
- Logging levels

## Monitoring Deployment

### Cloud Trace

```bash
gcloud trace list
gcloud trace describe <trace-id>
```

### Cloud Logging

```bash
gcloud logging read "resource.type=cloud_run_revision" \
  --limit 50 \
  --format json
```

### Metrics

View custom metrics in Cloud Monitoring:
- Agent reliability score
- SLA compliance status
- Incident count
- Recovery success rate

## Health Checks

### Readiness Probe

```bash
curl http://localhost:8080/health/ready
```

### Liveness Probe

```bash
curl http://localhost:8080/health/live
```

## Troubleshooting

### Common Issues

**Issue**: Import errors for google.adk
- **Solution**: Ensure google-adk is installed: `pip install google-adk>=0.3.0`

**Issue**: API key errors
- **Solution**: Verify GOOGLE_API_KEY is set and valid

**Issue**: Cloud Trace not working
- **Solution**: Enable Cloud Trace API and set proper IAM permissions

## Rollback Procedure

```bash
# Rollback to previous version
gcloud run deploy agent-reliability-guardian \
  --image=gcr.io/$PROJECT_ID/agent-reliability-guardian:previous \
  --update-env-vars="DISABLE_NEW_FEATURES=true"
```

## Maintenance

### Regular Tasks

- Review audit logs weekly
- Check SLA compliance daily
- Update baselines monthly
- Review and update anomaly thresholds

### Backup & Recovery

- Audit trails backed up daily to Cloud Storage
- Checkpoints retained for 30 days
- Emergency recovery procedures documented

## Support

For issues or questions:
1. Check logs: `gcloud logging read ...`
2. Review traces: `gcloud trace describe ...`
3. Check metrics in Cloud Monitoring
4. Open GitHub issue
