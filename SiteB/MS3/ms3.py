from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse 


app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('DB-B.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()
    description = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def masukkeindeks():
    return "MS3 Server Ready"

class CAR(Resource):
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]

        for row in rows:
            datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice,
            'description':row.description
        })
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')
        fDescription = parserAmbilData.get('description')

        car_simpan = TBCarsWeb.create(
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice,
            description = fDescription
            )

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice,
                'description':row.description
            })
        return jsonify(datas)

class CARbyID(Resource):
    def put(self, id):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')
        parserAmbilData = parserData.parse_args()

        try:
            mobil = TBCarsWeb.get(TBCarsWeb.id == id)
            mobil.carname = parserAmbilData.get('carname')
            mobil.carbrand = parserAmbilData.get('carbrand')
            mobil.carmodel = parserAmbilData.get('carmodel')
            mobil.carprice = parserAmbilData.get('carprice')
            mobil.description = parserAmbilData.get('description')
            mobil.save()

            return jsonify({
                'message': 'Data updated',
                'data': {
                    'id': mobil.id,
                    'carname': mobil.carname,
                    'carbrand': mobil.carbrand,
                    'carmodel': mobil.carmodel,
                    'carprice': mobil.carprice,
                    'description': mobil.description
                }
            })
        except TBCarsWeb.DoesNotExist:
            return jsonify({'message': 'Car not found'}), 404

    def delete(self, id):
        try:
            mobil = TBCarsWeb.get(TBCarsWeb.id == id)
            mobil.delete_instance()
            return jsonify({'message': f'Car with id {id} deleted.'})
        except TBCarsWeb.DoesNotExist:
            return jsonify({'message': 'Car not found'}), 404


api.add_resource(CAR, '/cars/', endpoint="cars/")
api.add_resource(CARbyID, '/cars/<int:id>', endpoint="car_by_id")


if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5053
        )