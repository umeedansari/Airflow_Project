# ETL DAG Project on Astro using Apache Airflow 🚀

Welcome! This is a data engineering project built with [Apache Airflow](https://airflow.apache.org/) using the Astronomer CLI. It demonstrates an end-to-end ETL pipeline that fetches data from NASA's Astronomy Picture of the Day (APOD) API and stores it in a PostgreSQL database hosted on Google Cloud Platform (GCP).

---

## 📦 Setup Instructions

### 1. Install Astro CLI

Follow the [Astro CLI installation guide](https://docs.astronomer.io/astro/install-cli) for your OS.

### 2. Initialize Astro Project

In an empty project directory, run:

```bash
astro dev init
```

This sets up the basic folder structure and files to start developing Airflow DAGs.

### 3. Start Airflow with Docker

Astro uses Docker under the hood. To start your Airflow environment locally, run:

```bash
astro dev start
```

This spins up 5 containers:
- **Postgres** – Metadata DB
- **Scheduler**
- **Webserver** – UI at [localhost:8080](http://localhost:8080)
- **DAG Processor**
- **Triggerer**

> 💡 If ports are already in use, follow [this guide](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

---

## 📂 Project Structure

Astro project includes:

- **`dags/`**: Contains your Airflow DAGs, including:
  - `ETL_DAG.py`: A daily ETL pipeline that:
    - Creates a PostgreSQL table (if not exists)
    - Extracts APOD data from NASA's API
    - Transforms the response
    - Loads it into a GCP-hosted PostgreSQL DB
- **`Dockerfile`**: Astro Runtime image configuration.
- **`include/`**: Placeholder for extra data or scripts.
- **`requirements.txt`**: Add Python packages if needed.
- **`packages.txt`**: For OS-level dependencies.
- **`plugins/`**: Add custom Airflow plugins here.
- **`airflow_settings.yaml`**: Define local Airflow Variables, Connections, etc.

---

## ⚙️ How to Run Locally

1. **Start Airflow locally:**

   ```bash
   astro dev start
   ```

   This spins up 5 containers:
   - **Postgres** – Metadata DB
   - **Scheduler**
   - **Webserver** – UI at [localhost:8080](http://localhost:8080)
   - **DAG Processor**
   - **Triggerer**

2. **Access PostgreSQL DB:**
   - Hosted on: **Google Cloud Platform**
   - DB: `postgres`
   - User/Pass: provided via Airflow connection
   - Note: Configure the connection in the Airflow UI or via `airflow_settings.yaml`

---

## 🛠️ DAG Breakdown: `ETL_DAG`

| Step            | Description                                  |
|-----------------|----------------------------------------------|
| `create_table`  | Initializes the `apod_data` table in Postgres|
| `extract_apod`  | Fetches JSON data from NASA APOD API         |
| `transform_data`| Extracts and formats relevant fields         |
| `load_data`     | Inserts the cleaned data into Postgres table |

**Technologies Used:**
- Python
- Apache Airflow (TaskFlow + SimpleHttpOperator)
- PostgresHook
- NASA APOD API
- Docker via Astro Runtime
- PostgreSQL on Google Cloud Platform

---

Happy Scheduling! ⏰
