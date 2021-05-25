from flask_restful import Resource, reqparse
from sql_alchemy import banco
from models.ip import IpModel

class IPS (Resource):
    def get(self):
        return {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
    
class IP (Resource):
    args = reqparse.RequestParser()
    
    def get(self, ip):
        _ip = IpModel.find_ip(ip)
        if _ip:
            return _ip.json()
        return {'message': 'IP não encontrado'}, 404

    def post(self, ip):
        if IpModel.find_ip(ip):
            return {'message': 'IP {} já consta no banco de dados.'.format(ip)}, 400
        dados = IP.args.parse_args()
        _ip = IpModel(ip)
        _ip.save_ip()
        return _ip.json(), 200

    def put(self, ip):
        dados = IP.args.parse_args()
        ip_encontrado = IpModel.find_ip(ip)
        if ip_encontrado:
            ip_encontrado.update_ip(**dados)
            ip_encontrado.save_ip()
            return ip_encontrado.json(), 200
        _ip = IpModel(ip, **dados)
        _ip.save_ip()
        return _ip.json(), 201

    def delete(self, ip):
        _ip = IpModel.find_ip_by_ip(ip)
        if _ip:
            _ip.delete_ip()
            return {'message': 'IP deleted.'}
        return {'message': 'IP not found.'}, 404