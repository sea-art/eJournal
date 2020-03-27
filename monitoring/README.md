# eJournal DevOps 2020

## Author: Maarten van Keulen

### Monitoring

Please note that all descriptions are relative from the monitoring directory.

```
monitoring
│   README.md
│   Makefile
│
└───ansible
│   │   hosts.yml
│   │   provision-monitoring.yml
│   │
│   └───roles
│       │   base.yml                # Update and install basic packages
│       │   docker.yml              # Install docker and compose
│       │   system_monitoring.yml   # System monitoring, creates monitoring network required for Sentry
│       │   sentry.yml              # Application monitoring
│
└───requirements
    │   base.txt
    │   local.txt
```

Provision a linux server with an onpremise configuration of:
- Sentry stack (~15 containers, see ansible/roles/sentry/templates/docker-compose.yml)
- System monitoring stack (8 containers, see ansible/roles/system_monitoring/templates/docker-compose.yml)

The monitoring service will reside behind Traefik as reverse-proxy, which handles all certificate management and
authentication. Domains are expected for the following services:
- Sentry
- Grafana
- Prometheus
- Alertmanager
- Pushgateway
- Traefik

Tested on an ubuntu 18.04 LTS server image, minimum of 2 cores and 4GB ram.

### Installation

`make setup`  
`make run provision-monitoring`
