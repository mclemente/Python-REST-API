import flask
from flask_restful import Api
from resources.ip import IPS, IP
from sql_alchemy import banco

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

api = Api(app)
api.add_resource(IPS, '/ips')
api.add_resource(IP, '/ips/<string:ip>')

@app.before_first_request
def cria_banco():
    banco.create_all()

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run()