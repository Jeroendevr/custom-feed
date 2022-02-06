from apiflask import APIFlask, Schema, input, output
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from json2xml import json2xml
from json2xml.utils import readfromjson


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
    return {'message': 'hello'}

@app.get('/pets/<int:pet_id>')
# @output(PetOutSchema)
def get_pet(pet_id):
    data = readfromjson("sampledata.json")
    return json2xml.Json2xml(data).to_xml()


@app.post('/pets')
@input(PetInSchema)
def create_pet(data):
    print(data)
    return {'message': 'created'}, 201


@app.put('/pets/<int:pet_id>')
def update_pet(pet_id):
    return {'message': 'updated'}


@app.delete('/pets/<int:pet_id>')
def delete_pet(pet_id):
    return '', 204