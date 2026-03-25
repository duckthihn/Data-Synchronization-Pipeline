# Data Synchronization Pipeline

![Data Engineering](https://img.shields.io/badge/Data_Engineering-Portfolio_Project-blue)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-PySpark-E25A1C)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-231F20)
![MySQL](https://img.shields.io/badge/MySQL-CDC_Source-4479A1)
![MongoDB](https://img.shields.io/badge/MongoDB-Target_DB-47A248)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D)

## 📌 Introduction
This project is an end-to-end data synchronization pipeline built to move and validate data across multiple storage systems. It combines **MySQL**, **MongoDB**, **Redis**, **Apache Kafka**, and **PySpark** to demonstrate a practical flow for schema creation, trigger-based change capture, streaming, and distributed writes.

The pipeline uses sample GitHub event JSON as input data, writes structured user records into operational databases, captures table changes from MySQL trigger logs, streams them through Kafka, and prepares the data for downstream Spark processing.

## 🏗️ Architecture & Data Flow
![Data Synchronization Architecture](docs/diagram.jpg)

1. **Source Data**
   - Raw JSON data is stored in the `data/` folder.
   - `src/spark/main.py` reads nested GitHub event data and extracts `actor` fields into a user dataset.
2. **Database Bootstrap**
   - `src/main.py` creates schemas in **MySQL** and **MongoDB**.
   - MySQL tables and audit tables are initialized from `sql/schema.sql` and `sql/trigger.sql`.
3. **Change Data Capture Simulation**
   - MySQL triggers write insert, update, and delete events into `Users_log_before` and `Users_log_after`.
   - `src/kafka/producer.py` polls the MySQL log table and publishes new records to Kafka topic `users`.
4. **Streaming Layer**
   - `src/kafka/consumer.py` consumes messages from `users` and forwards them to `spark-consumer`.
5. **Processing & Sync**
   - PySpark transforms JSON into a tabular user DataFrame.
   - `src/spark/spark_write_data.py` writes the result to **MySQL** and **MongoDB** and validates that the writes succeeded.
6. **Caching Layer**
   - Redis connection utilities are included for cache-oriented extensions and validation scenarios.

## 🎯 Technical Objectives
* Build a multi-database synchronization workflow using Python.
* Practice schema management across **MySQL**, **MongoDB**, and **Redis**.
* Simulate **change data capture** with MySQL triggers and Kafka topics.
* Use **PySpark** to transform nested JSON and write data into operational databases.
* Add validation logic to verify that Spark writes match persisted records.

## 🛠️ Tech Stack
* **Languages:** Python, SQL
* **Processing:** PySpark
* **Streaming:** Apache Kafka, Zookeeper
* **Databases:** MySQL, MongoDB, Redis
* **Infrastructure:** Docker Compose
* **Utilities:** `python-dotenv`, `mysql-connector-python`, `pymongo`, `redis`, `kafka-python`

## 📂 Project Structure
```text
.
├── config/               # Environment and Spark configuration
├── data/                 # Sample JSON input files
├── database/             # Database clients and schema helpers
├── docker/               # Docker Compose and environment file
├── docs/                 # Architecture diagrams and images
├── sql/                  # MySQL schema, trigger, and update scripts
├── src/
│   ├── kafka/            # Kafka producer and consumer
│   ├── spark/            # Spark jobs and database writers
│   ├── drop_table_users.py
│   └── main.py           # Bootstrap schemas and seed data
├── Makefile
└── requirements.txt
```

## 🚀 How to Run Locally

### 1. Prerequisites
* Docker and Docker Compose installed
* Python 3.12+ recommended
* Java available locally for Spark

### 2. Configure Environment Variables
This repo already includes a local env file at `docker/.env`. The application expects variables like:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DB=github_data

MONGO_URI=mongodb://duckthihn:rootpassword@localhost:27017/github_data?authSource=admin
MONGO_INITDB_ROOT_USERNAME=duckthihn
MONGO_INITDB_ROOT_PASSWORD=rootpassword
MONGO_DB=github_data
MONGO_PORT=27017

REDIS_HOST=localhost
REDIS_USER=root
REDIS_PASSWORD=rootpassword
REDIS_PORT=6379
REDIS_DB=0
```

If you change these values, update `docker/.env` so the Python config loader can find them.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Infrastructure
```bash
make up
```

This starts:
* MySQL
* MongoDB
* Redis
* Zookeeper
* Kafka

### 5. Bootstrap Schemas and Seed Records
```bash
python src/main.py
```

This step:
* creates the MySQL database
* creates the `Users` table
* creates MySQL trigger log tables
* creates MongoDB collection validation rules
* inserts seed data for validation

### 6. Run the Kafka Producer
```bash
python src/kafka/producer.py
```

The producer reads new records from `Users_log_after` and publishes them to Kafka topic `users`.

### 7. Run the Kafka Consumer
```bash
python src/kafka/consumer.py
```

The consumer forwards messages from `users` to `spark-consumer`.

### 8. Run the Spark Job
```bash
python src/spark/main.py
```

This job reads JSON data from `data/2015-03-01-17.json`, extracts user fields, and writes validated results into MySQL and MongoDB.

## 🧪 Useful Commands
```bash
make up
make down
make mysql
make mongo
make redis
```

## 🖼️ Demo
![Pipeline Preview](docs/img.png)

## ⚠️ Current Notes
* The project currently uses local sample data rather than an external API.
* Several file paths and imports are still tightly coupled to the local development structure.
* Kafka is used as a streaming bridge, while trigger tables simulate a CDC-style workflow instead of using Debezium or native binlog capture.

## 🤝 Connect
This project is part of my data engineering learning journey and highlights practical work with distributed processing, streaming, and multi-database synchronization.

* 💼 **LinkedIn:** [duc-thinh-pham](https://www.linkedin.com/in/duc-thinh-pham-8705b0249/)
* 📧 **Email:** [thinhpham1807@gmail.com](mailto:thinhpham1807@gmail.com)
