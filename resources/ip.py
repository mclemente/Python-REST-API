from flask_restful import Resource, reqparse
from sql_alchemy import banco
from models.ip import IpModel

class IPS (Resource):
    def get(self):
        return {'ips': [ip.json() for ip in IpModel.query.all()]} # SELECT * FROM ips
    
class IP (Resource):
    args = reqparse.RequestParser()
    args.add_argument('ip')
    
    def get(self, ip_id):
        ip = IpModel.find_ip(ip_id)
        if ip:
            return ip.json()
        return {'message': 'IP não encontrado'}, 404

    def post(self, ip_id):
        if IpModel.find_ip(ip_id):
            return {'message': 'ID {} já existe.'.format(ip_id)}, 400
        dados = IP.args.parse_args()
        ip = IpModel(ip_id, **dados)
        if IpModel.find_ip_by_ip(ip.json()['ip']):
            return {'message': 'IP {} já consta no banco de dados.'.format(ip['ip'])}, 400
        ip.save_ip()
        return ip.json(), 200

    def put(self, ip_id):
        dados = IP.args.parse_args()
        ip_encontrado = IpModel.find_ip(ip_id)
        if ip_encontrado:
            ip_encontrado.update_ip(**dados)
            ip_encontrado.save_ip()
            return ip_encontrado.json(), 200
        ip = IpModel(ip_id, **dados)
        ip.save_ip()
        return ip.json(), 201

    def delete(self, ip_id):
        ip = IpModel.find_ip_by_ip(ip_id)
        if ip:
            ip.delete_ip()
            return {'message': 'IP deleted.'}
        return {'message': 'IP not found.'}, 404