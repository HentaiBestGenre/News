import requests
import pymongo
import datetime as dt
import json

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
db = mongo_client["news_classification"]
spark_config = {
    "executor_cores": 1,
    "num_executors": 1,
}

@task
def _last_article():
    print("LOOKING FOR THE LAST ARTICLE")
    last_article = db['GameSpotHeaders'].find({}).sort('_id', pymongo.DESCENDING)[0]
    print("THE LAST ACTICLE: ", last_article)
    return last_article

@task
def _parse_new(last_article: dict):
    print("LOOKING FOR NEW ARTICLES")
    isFound, page, res, last_index = False, 1, [], last_article['_id']

    while not isFound:
        headers = requests.get(f"http://localhost:8000/parse/gamespot/get/headers/page/{page}", headers=HEADERS)
        if headers.status_code != 200:
            print(f"ERROR with parsing article id - {i['_id']}:\n", json.loads(headers.content))
            raise Exception("request Error: ", json.loads(headers.content))
        headers = json.loads(headers.content)
        for i in headers:
            print("HEADER INFO: ", i)
            if i['title'] == last_article['title'] or i['url'] == last_article['url']:
                isFound = True
                break
            res.insert(0, i)
        page += 1

    print("RESAULT: ")
    for i in range(len(res)):
        res[i]["_id"] = last_index + i + 1
        print(f"№{i}:\t{res[i]}")
    print("NUMBER OF ELEMENTS: ", len(res))

    with open('/tmp/new_headers.json', 'w') as f:
        json.dump(res, f)

def _write_headers():
    with open('/tmp/new_headers.json', 'r') as f:
        headers = json.load(f)
    
    print("WRITEING: ")
    for i in headers:
        print(i)
    
    db['GameSpotHeaders'].insert_many(headers)

def _parse_articles():
    with open('/tmp/new_headers.json', 'r') as f:
        headers = json.load(f)
    
    articles=[]
    for i in headers:
        try:
            article = requests.get(f"http://localhost:8000/parse/gamespot/get/article?url={i['url']}", headers=HEADERS)

            if article.status_code != 200:
                print(f"ERROR with parsing article id - {i['_id']}:\n", json.loads(article.content))
                continue

            article = json.loads(article.content)
            article['_id'] = i['_id']
            db['GameSpotArticles'].insert_one(article)
            articles.append(article)

        except Exception as e:
            print(f"==========================\n{e}\n==========================")

    with open('/tmp/new_articles.json', 'w') as f:
        json.dump(articles, f)


def _save_clean_articles():
    with open('/tmp/clean_articles.json', 'r') as f:
        data = json.load(f)
    db['Texts'].insert_many(data)


default_args = {
    'owner': 'vadim',
    'start_date': dt.datetime(2023, 6, 17),
    'retry_delay': dt.timedelta(days=1),
}

with DAG(
    dag_id="news_parser",
    default_args = default_args,
    template_searchpath="/tmp",
    max_active_runs=1,
) as dag:

    last_article = _last_article()
    parse_new = _parse_new(last_article)
    
    write_headers = PythonOperator(
        task_id="write_headers",
        python_callable=_write_headers,
        dag=dag,
    )
    
    parse_articles = PythonOperator(
        task_id="parse_articles",
        python_callable=_parse_articles,
        dag=dag,
    )

    prepare_article = SparkSubmitOperator(
        application="/home/vadim/airflow/dags/NEWS/pyspark_data_transformation.py", 
        task_id="prepare_article",
        dag=dag,
        executor_cores = 1,
        num_executors = 1,
        driver_memory = '1g',
        executor_memory = '1g',
    )
    
    save_clean_articles = PythonOperator(
        task_id="save_clean_articles",
        python_callable=_save_clean_articles,
        dag=dag,
        
    )

prepare_article >> save_clean_articles
parse_new >> write_headers
parse_new >> parse_articles >> prepare_article >> save_clean_articles