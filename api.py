import flask
from flask_restful import Api
from resources.ip import Blacklist, Filtro, Whitelist, WhitelistIP
from sql_alchemy import banco

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

api = Api(app)
api.add_resource(Blacklist, '/blacklist')
api.add_resource(Whitelist, '/whitelist')
api.add_resource(WhitelistIP, '/whitelist/<string:ip>')
api.add_resource(Filtro, '/filtro')

@app.before_first_request
def cria_banco():
    banco.create_all()

banco.init_app(app)

if __name__ == '__main__':
    banco.init_app(app)
    app.run()