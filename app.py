from apiflask import APIFlask, Schema, input, output
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from json2xml import json2xml
from json2xml.utils import readfromjson
from google.cloud import bigquery

def query_stackoverflow():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10"""
    )

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))



class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))

class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


app = APIFlask(__name__, title='Wonderful API', version='1.0')

@app.get('/')
def index():
    query_stackoverflow()
    return {'message': 'hello'}

@app.get('/training/<int:pet_id>')
# @output(PetOutSchema)
def get_training(pet_id):
    data = readfromjson("sampledata.json")
    return json2xml.Json2xml(data).to_xml()


@app.post('/training')
@input(PetInSchema)
def create_pet(data):
    print(data)
    return {'message': 'created'}, 201


@app.put('/training/<int:pet_id>')
def update_pet(pet_id):
    return {'message': 'updated'}


@app.delete('/training/<int:pet_id>')
def delete_pet(pet_id):
    return '', 204