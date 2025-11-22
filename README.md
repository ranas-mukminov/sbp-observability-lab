# SBP Observability Lab 🔍

![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![CI](https://img.shields.io/badge/build-passing-brightgreen.svg)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov) | **Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Overview

SBP Observability Lab is a production-grade monitoring toolkit for Linux servers handling integrations with the Russian Faster Payments System (Sistema Bystrykh Platezhey, СБП). It provides log parsers, a lightweight HTTP proxy, Prometheus exporter, Grafana dashboards, and AI-powered weekly reports to help DevOps engineers and payment system integrators monitor latency, error rates, and payment gateway health in real time.

The toolkit addresses the observability gap for SBP integrations, enabling businesses to detect payment failures early, analyze error patterns by bank and channel, and generate actionable insights without exposing sensitive payment data.

---

## Key Features

- **Multi-format log parsing**: Parse NGINX access logs, JSON logs, and CSV exports from SBP gateways
- **Prometheus metrics exporter**: Pre-configured metrics for request counts, error rates, latency histograms, and gateway uptime
- **Grafana dashboards**: Business and technical operations dashboards with drill-down by bank, channel, and operation type
- **Prometheus alert rules**: Out-of-the-box alerts for error spikes, latency degradation, and gateway downtime
- **AI-generated weekly reports**: Automated Markdown reports summarizing top issues and actionable recommendations (Russian language)
- **Lightweight HTTP proxy**: Optional transparent proxy for live request monitoring and metric collection
- **Privacy-first design**: Automatic masking of sensitive fields (PAN, account numbers); synthetic data in examples
- **Production-ready**: Type-safe Python 3.11+, pytest-based test suite, CI/CD with GitHub Actions

---

## Architecture

The lab consists of four main components:

```
┌─────────────────┐
│  SBP Gateway    │  (Your payment gateway/integration layer)
│  Logs & Traffic │
└────────┬────────┘
         │
         ├──▶ Log Parsers (NGINX/JSON/CSV)
         │        │
         │        ▼
         │   Normalized Events ──▶ Prometheus Exporter (:8000/metrics)
         │                                  │
         └──▶ HTTP Proxy (optional)        │
                    │                       │
                    ▼                       ▼
              Live Metrics ──────▶  Prometheus ──▶ Grafana Dashboards
                                         │
                                         ▼
                              Alert Manager ──▶ Notifications
                                         │
                                         ▼
                                    AI Reports (weekly)
```

**Components**:
- **Parsers** (`sbp_observability/parsing`): Extract structured events from logs
- **Exporter** (`sbp_observability/exporter`): Expose metrics in Prometheus format
- **Proxy** (`sbp_observability/proxy`): Optional HTTP proxy for live traffic instrumentation
- **AI Layer** (`sbp_observability/ai`): Generate human-readable weekly reports from error logs
- **Grafana assets** (`grafana/`): Pre-built dashboards and Prometheus alert rules

---

## Requirements

### Operating System
- **Ubuntu** 20.04+ / **Debian** 11+
- **RHEL** / **Rocky Linux** / **AlmaLinux** 8+
- **Any Linux** with Python 3.11+ and systemd

### Hardware
- **CPU**: 1+ cores
- **RAM**: 512 MB minimum (1 GB recommended for production)
- **Disk**: 100 MB for application, additional space for logs and metrics storage

### Software Dependencies
- **Python**: 3.11 or higher
- **pip**: Latest version
- **Optional**: Docker and Docker Compose (for containerized Prometheus/Grafana stack)
- **Optional**: systemd (for service management)

### Network
- Outbound HTTPS access to GitHub and PyPI (for installation)
- Open port 8000 for Prometheus scraping (or configure custom port)
- Open port 8080 for HTTP proxy (if enabled)

### Access Rights
- Standard user with virtualenv capabilities (no root required for installation)
- Root/sudo required only for systemd service setup and firewall configuration

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ranas-mukminov/sbp-observability-lab.git
cd sbp-observability-lab
```

### 2. Install Dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### 3. Parse Sample Logs

```bash
sbp-observability parse-logs examples/logs/sbp_gateway_nginx_sample.log --format nginx
```

Expected output: JSON array of normalized transaction events.

### 4. Run Prometheus Exporter

```bash
sbp-observability run-exporter --port 8000
```

The exporter is now available at `http://localhost:8000/metrics`.

### 5. Configure Prometheus

Add this scrape config to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'sbp-observability'
    static_configs:
      - targets: ['localhost:8000']
```

Restart Prometheus:

```bash
sudo systemctl restart prometheus
```

### 6. Import Grafana Dashboards

1. Log in to Grafana (default: `http://localhost:3000`, admin/admin)
2. Go to **Dashboards → Import**
3. Upload JSON files from `grafana/dashboards/`:
   - `sbp_business.json` — Business metrics (payment success rates, error trends)
   - `sbp_tech_ops.json` — Technical operations (latency histograms, gateway health)

### 7. Load Prometheus Alerts (Optional)

Copy `grafana/alerts/sbp_alert_rules.yml` to your Prometheus rules directory:

```bash
sudo cp grafana/alerts/sbp_alert_rules.yml /etc/prometheus/rules/
sudo systemctl reload prometheus
```

---

## Detailed Installation

### Install on Ubuntu / Debian

```bash
# Update package index
sudo apt update

# Install Python 3.11 (if not present)
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Clone repository
git clone https://github.com/ranas-mukminov/sbp-observability-lab.git
cd sbp-observability-lab

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install package
pip install --upgrade pip
pip install -e .

# Verify installation
sbp-observability --help
```

### Install on RHEL / Rocky / AlmaLinux

```bash
# Install Python 3.11 from AppStream
sudo dnf install -y python3.11 python3.11-pip git

# Clone and install (same as Ubuntu)
git clone https://github.com/ranas-mukminov/sbp-observability-lab.git
cd sbp-observability-lab
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Install with Docker Compose (Full Stack)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  sbp-exporter:
    build: .
    command: sbp-observability run-exporter --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ./examples/logs:/logs:ro
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
```

Start the stack:

```bash
docker-compose up -d
```

### Systemd Service Setup (Production)

Create `/etc/systemd/system/sbp-observability.service`:

```ini
[Unit]
Description=SBP Observability Prometheus Exporter
After=network.target

[Service]
Type=simple
User=sbp-monitor
WorkingDirectory=/opt/sbp-observability-lab
Environment="PATH=/opt/sbp-observability-lab/.venv/bin"
ExecStart=/opt/sbp-observability-lab/.venv/bin/sbp-observability run-exporter --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo useradd -r -s /bin/false sbp-monitor
sudo cp -r sbp-observability-lab /opt/
sudo chown -R sbp-monitor:sbp-monitor /opt/sbp-observability-lab
sudo systemctl daemon-reload
sudo systemctl enable sbp-observability.service
sudo systemctl start sbp-observability.service
sudo systemctl status sbp-observability.service
```

---

## Configuration

### Main Configuration File

Create `/etc/sbp_observability/config.yaml`:

```yaml
# Upstream URL for HTTP proxy (optional)
upstream_url: "https://sbp-gateway.example.com"

# Parser configuration for CSV logs
parser:
  column_mapping:
    timestamp: ts
    bank_id: bank_alias
    channel: channel_name
    operation_type: op_type
    status: result_code
    latency_ms: duration_ms

  # Fields to mask in logs (privacy protection)
  mask_keys:
    - pan
    - card
    - account
    - phone
```

### Environment Variables

You can override configuration via environment variables:

- `SBP_CONFIG_PATH`: Path to custom config file (default: `/etc/sbp_observability/config.yaml`)
- `SBP_EXPORTER_PORT`: Prometheus exporter port (default: `8000`)
- `SBP_PROXY_PORT`: HTTP proxy port (default: `8080`)

Example:

```bash
export SBP_CONFIG_PATH=/opt/sbp-observability/my-config.yaml
export SBP_EXPORTER_PORT=9100
sbp-observability run-exporter
```

### Prometheus Scrape Configuration

Example `prometheus.yml` snippet:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'sbp-observability'
    static_configs:
      - targets: ['localhost:8000']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'sbp-prod-gateway'
```

---

## Usage & Common Tasks

### Parse Logs from Different Formats

**NGINX access logs**:

```bash
sbp-observability parse-logs /var/log/nginx/sbp-access.log --format nginx
```

**JSON logs**:

```bash
sbp-observability parse-logs /var/log/sbp-gateway/events.json --format json
```

**CSV logs**:

```bash
sbp-observability parse-logs /var/log/sbp-gateway/export.csv --format csv --config-path /etc/sbp_observability/config.yaml
```

### Run the Prometheus Exporter

```bash
# Default: listen on 0.0.0.0:8000
sbp-observability run-exporter

# Custom host and port
sbp-observability run-exporter --host 127.0.0.1 --port 9100
```

Access metrics:

```bash
curl http://localhost:8000/metrics
```

### Run the HTTP Proxy (Optional)

```bash
# Start proxy on port 8080
sbp-observability run-proxy --port 8080
```

Configure your SBP gateway to route requests through `http://localhost:8080`.

### Generate Weekly Reports

Create a file with error codes and messages:

```bash
cat > errors.txt <<EOF
GATEWAY_TIMEOUT
BANK_DECLINE
RATE_LIMIT_EXCEEDED
EOF

sbp-observability generate-weekly-report errors.txt > weekly_report.md
```

Example output (in Russian):

```markdown
## Итоги недели по СБП

### Топ проблем
- GATEWAY_TIMEOUT: 3
- BANK_DECLINE: 2

### Рекомендации
- Проверить доступность внешнего шлюза
- Уточнить лимиты и правила антифрода в банках
```

### Access Grafana Dashboards

1. Open Grafana: `http://<YOUR_SERVER_IP>:3000`
2. Default credentials: `admin` / `admin` (change on first login)
3. Navigate to **Dashboards → Browse**
4. Select:
   - **SBP Business Metrics** — for business stakeholders
   - **SBP Tech Ops** — for DevOps and on-call engineers

---

## Update / Upgrade

### Update from Git Repository

```bash
cd sbp-observability-lab
source .venv/bin/activate
git pull origin main
pip install --upgrade -e .
```

### Restart Services

If running as systemd service:

```bash
sudo systemctl restart sbp-observability.service
```

If running with Docker Compose:

```bash
docker-compose pull
docker-compose up -d --force-recreate
```

### Migration Notes

- **v0.1.0 → v0.2.0**: No breaking changes expected
- Always check `CHANGELOG.md` for version-specific upgrade notes

---

## Logs, Monitoring, and Troubleshooting

### View Application Logs

**Systemd service**:

```bash
sudo journalctl -u sbp-observability.service -f
```

**Docker Compose**:

```bash
docker-compose logs -f sbp-exporter
```

### Common Issues

#### 1. Service Fails to Start

**Symptom**: `systemctl status sbp-observability` shows `failed` state.

**Solution**:

```bash
# Check logs for errors
sudo journalctl -u sbp-observability.service -n 50

# Verify Python path and permissions
sudo -u sbp-monitor /opt/sbp-observability-lab/.venv/bin/sbp-observability --help
```

#### 2. Port Already in Use

**Symptom**: `Address already in use` error when starting exporter.

**Solution**:

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process or use a different port
sbp-observability run-exporter --port 8001
```

#### 3. No Data in Grafana Dashboards

**Symptom**: Dashboards show "No data" panels.

**Solution**:

```bash
# Verify Prometheus is scraping the exporter
curl http://localhost:8000/metrics

# Check Prometheus targets
curl http://localhost:9090/targets

# Verify metric names in Prometheus query browser
# Expected metrics: sbp_requests_total, sbp_request_latency_seconds, etc.
```

#### 4. Permission Denied on Log Files

**Symptom**: Parser fails with `PermissionError`.

**Solution**:

```bash
# Add sbp-monitor user to log group
sudo usermod -a -G adm sbp-monitor

# Or copy logs to accessible location
sudo cp /var/log/nginx/sbp-access.log /tmp/ && sudo chown sbp-monitor /tmp/sbp-access.log
```

---

## Security Notes

### Data Privacy

- **Never commit real payment data** to the repository. All examples use synthetic logs.
- **Mask sensitive fields**: Configure `mask_keys` in `config.yaml` to anonymize PAN, account numbers, and phone numbers.
- **No PII in metrics**: Prometheus metrics aggregate data without exposing individual user identifiers.

### Access Control

- **Change default passwords**: If using Grafana, change the default `admin/admin` credentials immediately.
- **Restrict exporter port**: Use firewall rules to allow Prometheus access only from trusted IPs:

```bash
sudo ufw allow from <PROMETHEUS_IP> to any port 8000
sudo ufw deny 8000
```

- **Use HTTPS**: In production, place Grafana and Prometheus behind a reverse proxy (nginx, Caddy) with TLS.

### Security Scanning

Run security checks before deploying:

```bash
# Activate dev environment
pip install -e .[dev]

# Run bandit (Python security linter)
./scripts/security_scan.sh

# Run pip-audit (dependency vulnerability scanner)
pip-audit
```

### Legal Compliance

- This toolkit is **not** affiliated with the Bank of Russia, NSPK, or any specific bank.
- Deploying this tool **does not** exempt you from regulatory compliance (e.g., 152-FZ on personal data protection).
- Review `LEGAL.md` for additional disclaimers.

---

## Project Structure

```
sbp-observability-lab/
├── sbp_observability/         # Main Python package
│   ├── parsing/               # Log parsers (NGINX, JSON, CSV)
│   ├── exporter/              # Prometheus exporter and metrics
│   ├── proxy/                 # HTTP proxy for live traffic
│   ├── ai/                    # AI report generator
│   ├── cli/                   # Typer-based CLI
│   ├── models.py              # Domain models (TransactionEvent, etc.)
│   └── config.py              # Configuration loader
├── grafana/                   # Grafana assets
│   ├── dashboards/            # JSON dashboard definitions
│   └── alerts/                # Prometheus alert rules (YAML)
├── examples/                  # Sample data and configs
│   ├── logs/                  # Synthetic log files
│   ├── configs/               # Example YAML configs
│   └── reports/               # Sample weekly report
├── tests/                     # Pytest test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── scripts/                   # Development and CI scripts
│   ├── lint.sh                # Ruff + mypy
│   ├── dev_run_all_tests.sh   # Pytest runner
│   └── security_scan.sh       # Bandit + pip-audit
├── pyproject.toml             # Python package metadata
├── LICENSE                    # Apache-2.0 license
├── CONTRIBUTING.md            # Contribution guidelines
├── SECURITY.md                # Security policy
└── LEGAL.md                   # Legal disclaimers
```

---

## Roadmap

- [ ] Support for additional log formats (Apache, HAProxy)
- [ ] Built-in log rotation and archival helpers
- [ ] Telegram bot for alert delivery
- [ ] Extended AI reports with trend analysis and forecasting
- [ ] Helm chart for Kubernetes deployment
- [ ] Integration with OpenTelemetry for distributed tracing

---

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

### Development Workflow

1. Fork the repository and create a feature branch
2. Write tests first (TDD approach)
3. Run linters and tests locally:

```bash
./scripts/lint.sh
./scripts/dev_run_all_tests.sh
./scripts/security_scan.sh
```

4. Submit a pull request with clear description
5. Address Codex Code Review feedback

### Code Style

- **Python**: PEP 8, enforced by Ruff
- **Type hints**: Required for all public functions (mypy strict mode enabled)
- **Docstrings**: PEP 257 style
- **Max line length**: 100 characters

---

## License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for the full text.

---

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

### Professional Services

For production deployments, custom integrations, and ongoing support, visit [run-as-daemon.ru](https://run-as-daemon.ru) or contact the author via GitHub.

We offer:
- **SBP Integration Audits**: Analyze your payment gateway logs and architecture to identify bottlenecks and failure points
- **Observability Stack Setup**: Turnkey deployment of Prometheus, Grafana, and this lab toolkit on your infrastructure
- **Custom Dashboards and Alerts**: Tailored monitoring for your specific SBP use cases and SLA requirements
- **Weekly Report Customization**: AI-powered insights tuned to your business KPIs
- **DevOps / SRE Consulting**: Ongoing support, incident response, and infrastructure optimization

---

## Disclaimer

This project is an independent open-source tool and is **not** an official product of the Bank of Russia, NSPK, or any payment system operator. It does not provide payment services and does not replace regulatory compliance obligations. Use at your own risk and ensure your deployment complies with all applicable laws and agreements.
