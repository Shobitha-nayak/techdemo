# System Architecture

## Overview

The Stock Market Data Ingestion and Monitoring System consists of a backend service that ingests and processes stock data and a frontend service that displays reports and alerts.

## Components

1. **Backend**
   - **Language:** Python
   - **Framework:** Flask
   - **Database:** SQLite
   - **Responsibilities:** Data ingestion, KPI calculations, API endpoints.

2. **Frontend**
   - **Language:** JavaScript
   - **Framework:** Next.js
   - **Responsibilities:** Displaying stock data, reports, and alerts.

## Deployment

The system is containerized using Docker and deployed on Kubernetes for scalability and reliability.
