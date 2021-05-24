from flask_restful import Resource, reqparse
from sql_alchemy import banco

ips = []

class IpModel:
    __tablename__ = 'ips'

    ip_id = banco.Column(banco.String, primary_key = True)
    ip = banco.Column(banco.String(80))
    whitelist = banco.Column(banco.Boolean())

    def __init__(self, ip_id, ip, whitelist):
        self.ip_id = ip_id
        self.ip = ip
        self.whitelist = whitelist
    
    def json(self):
        return {
            'ip_id': self.ip_id,
            'ip': self.ip,
            'whitelist': self.whitelist
        }

class IPS (Resource):
    def get(self):
        return {'ips': ips}
    
class IP (Resource):
    args = reqparse.RequestParser()
    args.add_argument('ip')
    args.add_argument('whitelist')

    def acha_ip(ip_id):
        for ip in ips:
            if (ip['ip_id'] == ip_id):
                return ip
        return None

    def get(self, ip_id):
        ip = IP.acha_ip(ip_id)
        if ip:
            return ip
        return {'message': 'IP não encontrado'}, 404

    def post(self, ip_id):
        dados = IP.args.parse_args()
        novo_ip = IpModel(ip_id, **dados).json()
        ips.append(novo_ip)
        return novo_ip, 200

    def put(self, ip_id):
        ip = IP.acha_ip(ip_id)
        dados = IP.args.parse_args()

        novo_ip = IpModel(ip_id, **dados).json()
        if ip:
            ip.update(novo_ip)
            return novo_ip, 200
        ips.append(novo_ip)
        return novo_ip, 201

    def delete(self, ip_id):
        global ips
        ips = [ip for ip in ips if ip['ip_id'] != ip_id]
        return {'message': 'IP deleted'}