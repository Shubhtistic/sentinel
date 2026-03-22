# Sentinel 🛡️
### Self-Hosted Uptime Monitoring Service

**Sentinel** is a self-hosted, open-source uptime monitoring service that runs
on any server — a $5 VPS, an on-premise machine, or inside a private network (VPC).

---

## The Idea

While working on backend projects, I kept running into the same problem — I needed
to know if my services were down, but I didn't want to pay for an external monitoring
tool or expose internal endpoints to the public internet. I built Sentinel to solve
this: a monitoring service you own, deploy anywhere, and pay nothing for.

---

## Features

- **HTTP Health Checks** — ping any API with configurable intervals
- **TCP Socket Pinging** — check databases (PostgreSQL, Redis) without HTTP
- **Dead Man's Switch** — monitor background cron jobs via heartbeat pings
- **Outbound Webhooks** — alert Slack/Discord on state changes
- **Exponential Backoff** — reliable alert delivery during network degradation
- **Consecutive Failure Thresholds** — eliminate false alerts from temporary blips
- **PASETO v4.local Auth** — secure admin control plane with Argon2id password hashing
- **Redbeat Scheduler** — persistent Celery Beat schedule that survives restarts

---

## Architecture

| Component | Technology | Role |
|-----------|------------|------|
| Control Plane | FastAPI + PostgreSQL | Dashboard API, auth, monitor management |
| Scheduler | Celery Beat + Redbeat | Dispatches health-check tasks on schedule |
| Workers | Celery + httpx | Execute HTTP, TCP, keyword, SSL checks |
| Alert Engine | Celery Tasks | Outbound webhooks with retry logic |
| State Store | Redis | Broker, Redbeat schedule, rate limiting |

---

## Tech Stack

Python 3.12, FastAPI, PostgreSQL, Redis, Celery, Redbeat, PASETO v4.local,
Argon2id, Docker Compose, Linux

---

## License

MIT License. Free to use and modify.

---

Built by [Shubham Pawar](https://github.com/Shubhtistic)
