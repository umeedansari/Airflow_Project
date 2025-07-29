from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime

with DAG(
    dag_id='ETL_DAG',
    start_date=datetime(2025, 7, 28),
    schedule='@daily',
    tags=['ETL', 'NASA'],
    catchup=False
) as dag:

    @task
    def create_table():
        hook = PostgresHook(postgres_conn_id='mypostgres')
        query = '''
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        '''
        hook.run(query)

    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"},
        response_filter=lambda response: response.json(),
        do_xcom_push=True  # Keep this to push response to XCom, but we’ll use it in the next task
    )

    @task
    def transform_data(response):
        # The response comes as a dictionary, so you can directly map the keys to the data
        return {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }

    @task
    def load_data(apod_data):
        hook = PostgresHook(postgres_conn_id='mypostgres')
        query = '''
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        '''
        hook.run(query, parameters=[ 
            apod_data['title'], 
            apod_data['explanation'], 
            apod_data['url'], 
            apod_data['date'], 
            apod_data['media_type']
        ])

    # Task chaining, and using XCom data for transformation
    task1=create_table()
    task2=extract_apod.output
    task3=transform_data(task2)
    task4=load_data(task3)