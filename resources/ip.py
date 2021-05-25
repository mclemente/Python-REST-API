from flask_restful import Resource, reqparse
from sql_alchemy import banco
from models.ip import IpModel, WhitelistModel
import requests

class Blacklist (Resource):
    args = reqparse.RequestParser()

    def get(self):
        """
            1) Um endpoint GET que devolve todos os IPs de TOR obtidos das fontes externas
            - https://www.dan.me.uk/tornodes
            - https://onionoo.torproject.org/summary?limit=5000
        """
        return {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
    
    def post(self):
        tornodes = requests.get("https://www.dan.me.uk/torlist/")
        if tornodes.status_code == 200:
            for ip in tornodes.text.split("\n"):
                if IpModel.find_ip(ip):
                    continue
                _ip = IpModel(ip)
                _ip.save_ip()
        onionoo = requests.get("https://onionoo.torproject.org/summary?limit=5000")
        if onionoo.status_code == 200:
            for ip in onionoo.json()["relays"]:
                if IpModel.find_ip(ip["a"][0]):
                    continue
                _ip = IpModel(ip["a"][0])
                _ip.save_ip()
        return {'tornodes': tornodes.status_code, 'onionoo': onionoo.status_code}, 200

class Whitelist (Resource):
    args = reqparse.RequestParser()

    def get(self):
        return {'ips': [ip.json() for ip in WhitelistModel.query.all()]} # SELECT * FROM whitelist

class WhitelistIP (Resource):
    args = reqparse.RequestParser()
    
    def get(self, ip):
        _ip = WhitelistModel.find_ip(ip)
        if _ip:
            return _ip.json()
        return {'message': 'IP não encontrado'}, 404

    def post(self, ip):
        """
            2) Um endpoint POST que receba um IP e o agregue à uma base de dados onde se encontram todos os IPs que não queremos que apareçam no output do endpoint 3
        """
        if WhitelistModel.find_ip(ip):
            return {'message': 'IP {} já consta no banco de dados.'.format(ip)}, 400
        dados = WhitelistIP.args.parse_args()
        _ip = WhitelistModel(ip)
        _ip.save_ip()
        return _ip.json(), 200

class Filtro (Resource):
    """
        3) Um endpoint GET que devolve os IPs obtidos das fontes externas EXCETO os que se encontram na base de dados (IPs carregados utilizando o endpoint 2) 
    """
    def get(self):
        filter = banco.session.query(IpModel, WhitelistModel).filter(IpModel.ip != WhitelistModel.ip).all() # SELECT * FROM ips, whitelist WHERE ips.ip != whitelist.ip
        if (len(filter)): # Se Whitelist estiver vazio, retornar a blacklist inteira
            rows = {}
            i = 0
            for row in filter:
                rows[i] = dict(row)['IpModel'].json()
                i += 1
            return rows
        # return {'message': 'Não há IPs na whitelist'}, 404
        return {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
