# Energy Consumption Forecasting Pipeline

# Project Overview
The objective of this project is to build a **scalable and reliable data engineering pipeline** that supports energy consumption analytics and forecasting while demonstrating modern **data lakehouse architecture and ETL best practices**.
The **Energy Consumption Forecasting Pipeline** is a data engineering project that processes household energy consumption data using **Databricks, PySpark, and Delta Lake**.
The pipeline ingests raw CSV files from **AWS S3**, performs data cleaning and transformations, and produces aggregated datasets used for **analytics and forecasting**.
The architecture follows the **Medallion Architecture (Bronze → Silver → Gold)** pattern commonly used in modern data lakehouse systems.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![PySpark](https://img.shields.io/badge/PySpark-3.x-orange?logo=apache-spark)](https://spark.apache.org)
[![Databricks](https://img.shields.io/badge/Databricks-Serverless-red?logo=databricks)](https://databricks.com)
[![AWS](https://img.shields.io/badge/AWS-ap--south--1-FF9900?logo=amazonaws)](https://aws.amazon.com)
[![Airflow](https://img.shields.io/badge/Airflow-MWAA-017CEE?logo=apacheairflow)](https://airflow.apache.org)
---

#  Dataset  

## Dataset Source  

Kaggle – **Energy Consumption Forecasting**

The dataset consisting of **energy consumption, grid, weather related data** collected from multiple Indian cities and regions.

##  Datasets Used  

- `energy_usage_stream_v2.csv` → Historical household energy consumption data  
- `device_metrics_stream_v2.csv` → Device-level energy usage and performance metrics  
- `grid_load_stream_v2.csv` → Power grid load and distribution data  
- `tariff_metrics_stream_v2.csv` → Electricity pricing and tariff information  
- `weather_stream_v2.csv` → Weather conditions affecting energy consumption  

These datasets simulate a **real-world energy analytics environment**, where multiple data sources are combined to generate insights such as consumption trends, load forecasting, and cost optimization.

---

# End-to-End Pipeline Architecture

<p align="center">
  <img src="https://github.com/user-attachments/assets/9e421b59-149d-4127-bac4-2de2beff8085" alt="Architecture Diagram" width="800"/>
</p>

# Medallion Data Architecture

## Bronze Layer

### Purpose

- Store raw ingested data  
- Preserve source records  
- Enable reprocessing  

### Operations

- CSV ingestion from S3  
- Schema inference  
- Ingestion timestamp creation

### Tables

```
raw.bronze_energy_usage
raw.bronze_weather
raw.bronze_device_metrics
raw.bronze_grid_load
raw.bronze_tariff_metrics
```

---

## Silver Layer

### Purpose

- Clean and standardize raw data  
- Prepare structured datasets for analytics  

### Transformations

- Remove duplicate records  
- Handle missing values  
- Standardize timestamps  
- Convert data types  
- Normalize column names

### Output Table Example

```
processed.silver_energy_usage
```

---

## Gold Layer

### Star Schema
<img width="953" height="609" alt="image" src="https://github.com/user-attachments/assets/eb105858-1162-4320-a39e-1a06f8f21113" />


### Purpose

- Provide aggregated analytics datasets  
- Generate forecasting features  

### Operation

- Hourly energy consumption metrics  
- Daily consumption aggregation  
- Peak load calculations  
- Forecast feature generation

### Features Generated

- Regional energy consumption metrics
- Device efficiency rankings
- Grid health and stress indicators
- Household billing analytics
- Weather impact on energy demand
- Tariff plan cost comparison

### Output Table Example

```
analytics.metrics_weather_energy_correlation
```

---

# Airflow Orchestration

<p align="center">
  <img src="https://github.com/user-attachments/assets/89d38545-aafe-4b10-922d-5da7f0779f4b" alt="Airflow Diagram" width="700"/>
</p>

The ETL workflow can be orchestrated using **Apache Airflow DAGs** to automate pipeline execution.

Apache Airflow is used to orchestrate the end-to-end ETL pipeline by defining workflows as Directed Acyclic Graphs (DAGs).

- **Workflow Scheduling**: Automates pipeline execution at defined intervals  
- **Task Orchestration**: Manages dependencies between ingestion, transformation, and loading tasks  
- **Scalability**: Uses executors and workers to run tasks in parallel  
- **Monitoring**: Provides UI for tracking job status, logs, and failures  
- **Error Handling**: Supports retries, failure handling, and alerting (Slack integration)  

### Outcome

Airflow ensures reliable, automated, and scalable execution of the data pipeline from **S3 → Bronze → Silver → Gold**, improving data availability and consistency.

### Schedule

Daily at **04:00 AM UTC**

---

# Data Quality Checks

The pipeline includes multiple data quality validations to ensure reliability and accuracy of the data across Bronze, Silver, and Gold layers:

- **Null Checks**: Identifies missing values in critical columns such as timestamps and meter readings.  
- **Duplicate Detection**: Ensures no duplicate records are processed across datasets.  
- **Schema Validation**: Verifies column names and data types match expected schema definitions.  
- **Range Validation**: Detects invalid values (e.g., negative energy consumption).  
- **Data Consistency**: Ensures consistent formatting and standardized values across datasets.    

**Example validation logic**

```python
if df.filter(col("global_active_power").isNull()).count() > 0:
    raise Exception("Data Quality Issue Detected")
```
## Data Quality Alerts

The pipeline generates alerts when data quality issues are detected:

- Missing or null values found in critical fields  
- Duplicate records detected  
- Schema mismatches or missing columns  
- Invalid or out-of-range values identified

## Error Handling and Monitoring

Pipeline failures and anomalies are logged in

`energy_catalog.logs.etl_errors`

Monitoring includes

- Logging ETL failures  
- Capturing malformed records  
- Data validation alerts  
- Job execution monitoring  

---

# Slack Notifications

The pipeline integrates with Slack to provide real-time alerts and monitoring updates.

## Features

- Sends alerts for data quality issues (nulls, duplicates, schema mismatches)  
- Notifies on pipeline failures or task errors  
- Provides success notifications after pipeline completion  
- Enables quick visibility for data engineers and stakeholders

## Use Cases

- Immediate alerting for failed jobs or broken pipelines  
- Monitoring data quality issues before they impact downstream systems  
- Keeping teams informed about pipeline execution status  

## Benefit

Slack integration ensures **real-time monitoring, faster issue resolution, and improved pipeline reliability**.

---

# Analytics Dashboards & Artifacts

This section contains **dashboards generated from the analytics (Gold layer) dataset**.

---

## Energy consumption dashboard

Tracks total and average energy usage across regions, cities, and customer categories.

<img width="1901" height="934" alt="image" src="https://github.com/user-attachments/assets/11928336-f0c2-4f9c-9f05-a9bb4931921e" />

---

## Weather impact dashboard

Correlates temperature and humidity with energy demand to quantify how climate drives consumption.

<img width="1902" height="931" alt="image" src="https://github.com/user-attachments/assets/8ad9b146-bfc4-4777-8698-3c5b74f01b94" />

---

## Device monitoring dashboard

Analyzes device runtime, efficiency, and maintenance status across categories and brands.

<img width="1898" height="931" alt="image" src="https://github.com/user-attachments/assets/002c90ab-02f4-4e00-8122-d4c5ab932ca4" />

---

## Grid monitoring dashboard

Monitors grid load, transformer stress, and line loss percentage by region to identify infrastructure risks.

<img width="1896" height="926" alt="image" src="https://github.com/user-attachments/assets/00bca798-5ee8-4396-a610-e74430ce24ff" />

---

## Billing analytics dashboard

Compares monthly billing across tariff plans, cities, and household tiers to surface cost patterns.

<img width="1894" height="928" alt="image" src="https://github.com/user-attachments/assets/8359924e-42d2-4cbc-9b4f-603002b0b919" />

---

# Technology Stack

| Component | Technology |
|----------|------------|
| Data Storage | AWS S3 |
| AWS tools    | Glue / Crawler / MWAA |
| Processing Engine | Apache Spark / PySpark |
| Platform | Databricks |
| Data Format | Delta Lake |
| Orchestration | Apache Airflow / Databricks Workflows |
| Programming Language | Python |
| Testing | pytest |
| Version Control | Git |

---

# Business Insights Generated

The pipeline enables insights such as

- Peak electricity consumption hours  
- Daily and seasonal energy usage trends  
- Grid load monitoring  
- Tariff efficiency analysis  

These insights support **better energy forecasting and resource planning**.

---

# Future Enhancements

- Support real-time data processing using streaming  
- Improve data quality checks with advanced validation tools  
- Add multi-channel alerts (Slack, Email)  
- Implement CI/CD for automated deployments  
- Enhance dashboards for better insights  
- Optimize performance and reduce costs
