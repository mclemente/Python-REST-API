from flask_restful import Resource, reqparse
from sql_alchemy import banco
from models.ip import IpModel, WhitelistModel
import requests

class Filtro (Resource):
    def get(self):
        filter = banco.session.query(IpModel, WhitelistModel).filter(IpModel.ip != WhitelistModel.ip).all() # SELECT * FROM ips, whitelist WHERE ips.ip != whitelist.ip
        if (len(filter)):
            rows = {}
            i = 0
            for row in filter:
                rows[i] = dict(row)['IpModel'].json()
                i += 1
        else:
            rows = {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
        return rows

class Blacklist (Resource):
    args = reqparse.RequestParser()

    def get(self):
        return {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
    
    def post(self):
        tornodes = requests.get("https://www.dan.me.uk/torlist/")
        if tornodes.status_code == 200:
            for ip in tornodes.text().split("\n"):
                if IpModel.find_ip(ip):
                    continue
                _ip = IpModel(ip)
                _ip.save_ip()
        onionoo = requests.get("https://onionoo.torproject.org/summary?limit=5000")
        if onionoo.status_code == 200:
            for ip in onionoo.json()["relays"]["a"][0]:
                if IpModel.find_ip(ip):
                    continue
                _ip = IpModel(ip)
                _ip.save_ip()
        return 200

class Whitelist (Resource):
    args = reqparse.RequestParser()
    # args.add_argument('ip')
    
    def get(self):
        return {'ips': [ip.json() for ip in WhitelistModel.query.all()]} # SELECT * FROM whitelist

class WhitelistIP (Resource):
    args = reqparse.RequestParser()
    # args.add_argument('ip')
    
    def get(self, ip):
        _ip = WhitelistModel.find_ip(ip)
        if _ip:
            return _ip.json()
        return {'message': 'IP não encontrado'}, 404

    def post(self, ip):
        if WhitelistModel.find_ip(ip):
            return {'message': 'IP {} já consta no banco de dados.'.format(ip)}, 400
        dados = WhitelistIP.args.parse_args()
        _ip = WhitelistModel(ip)
        _ip.save_ip()
        return _ip.json(), 200
