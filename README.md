# Azure-Container-Lab

A hands-on progression through Azure's container services, deployed via Terraform.

## What this is

A learning lab that takes a single containerized application and progressively
deploys it across Azure's container offerings — from the simplest (ACI) to the
most powerful (AKS) — to build practical understanding of when to reach for
each one.

## The app

`platform-inspector` — a small Python Flask app that reports back the
container hostname, detected Azure platform, uptime, and a request count.
Same image, different runtimes — different behavior.

## Stages

- [x] **1. Local** — Build and run with Docker Desktop ✅
- [ ] **2. Azure Container Registry (ACR)** — Private image storage
- [ ] **3. Azure Container Instances (ACI)** — Run a single container, fast
- [ ] **4. Azure Container Apps (ACA)** — Serverless containers with autoscaling
- [ ] **5. Azure Kubernetes Service (AKS)** — Full Kubernetes, full control

Stages 2–5 will live in their own Terraform modules under `/infra` and can be
applied or destroyed independently to keep costs in check.

## Naming convention

All resources prefixed with `bkr` (e.g., `bkr-acr-lab`, `bkr-aci-lab`).

## Cost guardrails

A budget alert is configured at the subscription level before any deployments.
Each stage includes a `terraform destroy` cleanup step in its README.

## Stack

- Terraform (azurerm provider)
- Docker
- Python 3.12 / Flask
- GitHub Actions (later stages)
