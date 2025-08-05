FROM apache/airflow:slim-3.0.2-python3.10

USER root
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install \
    flask_appbuilder==4.5.0 \
    psycopg2-binary==2.9.9 \
    asyncpg==0.29.0 \
    apache-airflow-providers-postgres \
    apache-airflow-providers-mongo \
    apache-airflow-providers-docker \
    requests==2.31.0

WORKDIR /opt/airflow