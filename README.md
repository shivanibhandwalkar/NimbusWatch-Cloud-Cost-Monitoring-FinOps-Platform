# NimbusWatch: Multi-Cloud Cost Monitoring & Anomaly Detection Platform

NimbusWatch is a modern, containerized multi-cloud financial operations (FinOps) dashboard designed to track, analyze, and monitor daily expenditures across major cloud providers (**AWS, Azure, and GCP**). It features automated background synchronization, real-time budget tracking, intelligent cost anomaly detection, and a responsive dark-mode UI.
## Key Features
- **Multi-Cloud Ingestion Engine**: Collects and normalizes daily telemetry across AWS, Azure, and GCP. Includes an environment-aware **AWS Boto3** client that interfaces with AWS Cost Explorer with a seamless local simulation fallback.
- **Automated Background Sync**: Powered by **APScheduler** inside a FastAPI worker thread to periodically sync billing metrics and run anomaly detection routines.
- **Cost Anomaly Detection**: Statistical sliding-window analysis to identify unusual spending spikes and notify users.
- **Interactive Dark-Mode Dashboard**: Built with **React, Vite, and Recharts** featuring real-time budget progress gauges, customizable spending thresholds, and historical cost trends.
- **Containerized Architecture**: Fully dockerized using **Docker Compose** with persistent SQLite volume storage.
## Tech Stack
* **Backend**: Python, FastAPI, Uvicorn, APScheduler, SQLite, Boto3 / Botocore
* **Frontend**: React, Vite, Recharts, CSS3 (Custom Dark Theme)
* **Infrastructure**: Docker, Docker Compose
## Project Structure

NimbusWatch-cloud-cost-monitor-platform/
│
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── cost_fetcher.py
│   ├── anomaly_detector.py
│   ├── alerter.py
│   ├── database.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
└── docker-compose.yml