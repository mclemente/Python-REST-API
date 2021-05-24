from flask_restful import Resource, reqparse
from sql_alchemy import banco

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

    @classmethod
    def find_ip(cls, ip_id):
        ip = cls.query.filter_by(ip_id = ip_id).first # SELECT * FROM ips WHERE ip_id = $ip_id
        if ip:
            return ip
        return None
    
    @classmethod
    def find_ip_by_ip(cls, ip):
        ip = cls.query.filter_by(ip = ip).first # SELECT * FROM ips WHERE ip = $ip
        if (ip):
            return ip
        return None
    
    def save_ip(self):
        banco.session.add(self)
        banco.session.commit()
    
    def update_ip(self, ip_id, ip, whitelist):
        self.ip = ip
        self.whitelist = whitelist
    
    def delete_ip(self):
        banco.session.delete(self)
        banco.session.commit()
