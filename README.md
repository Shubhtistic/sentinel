# Sentinel 🛡️
### Distributed VPC Uptime & Observability Engine

[cite_start]**Sentinel** is a self-hosted, open-source uptime monitoring service. [cite_start]It is specifically architected to run inside a company's private network (VPC) to health-check internal microservices and databases that are invisible to the public internet[cite: 5, 6].

## 📢 Project Identity & Open Source
* [cite_start]**Open Source:** This project is free to use, modify, and distribute.
* **Attribution:** While the code is free, you **must** provide credit to the author (Shubham Pawar) in any derivative works or deployments.
* **Name Disclaimer:** The name "Sentinel" is used as a project codename. I do not claim any trademark over the name "Sentinel."

## 🚀 The Mission
[cite_start]Most monitoring tools live on the public web and cannot reach "private subnets" behind a corporate firewall[cite: 8, 12]. Sentinel lives inside the network to monitor:
* [cite_start]**Internal APIs:** Heartbeat checks for services like Payment and Auth[cite: 12, 16].
* [cite_start]**Deep Health:** Verifying DB connectivity and Redis status internally[cite: 16].
* [cite_start]**Dead Man's Switch:** Monitoring silent background jobs and backups[cite: 24, 84].

## 🏗️ High-Level Architecture
[cite_start]Sentinel is built as a distributed system to ensure scalability[cite: 28]:
* [cite_start]**Control Plane:** FastAPI + PostgreSQL with PASETO v4.local authentication[cite: 30, 42].
* [cite_start]**Scheduler:** Celery Beat + Redbeat for persistent task dispatching[cite: 30, 108].
* [cite_start]**Worker Layer:** Distributed Celery Workers for HTTP and TCP socket checks[cite: 30, 90].



---
## 📜 License
This project is open-source, but **attribution is mandatory**. Failure to credit the author constitutes a copyright violation. See the `LICENSE` file for details.
