from flask_restful import Resource, reqparse
from sql_alchemy import banco

class IpModel(banco.Model):
    __tablename__ = 'ips'

    ip_id = banco.Column(banco.String, primary_key = True)
    ip = banco.Column(banco.String(80))

    def __init__(self, ip_id, ip):
        self.ip_id = ip_id
        self.ip = ip
    
    def json(self):
        return {
            'ip_id': self.ip_id,
            'ip': self.ip
        }

    @classmethod
    def find_ip(cls, ip_id):
        ip = cls.query.filter_by(ip_id = ip_id).first() # SELECT * FROM ips WHERE ip_id = $ip_id
        if ip:
            return ip
        return None

    @classmethod
    def find_ip_by_ip(cls, ip):
        _ip = cls.query.filter_by(ip = ip).first() # SELECT * FROM ips WHERE ip_id = $ip_id
        if _ip:
            return _ip
        return None
    
    def save_ip(self):
        banco.session.add(self)
        banco.session.commit()
    
    def update_ip(self, ip_id, ip):
        self.ip = ip
    
    def delete_ip(self):
        banco.session.delete(self)
        banco.session.commit()
