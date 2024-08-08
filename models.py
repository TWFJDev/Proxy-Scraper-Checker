from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from uuid import uuid4

engine = create_engine('sqlite:///bot.sqlite', echo=False)

base = declarative_base()

class Proxies(base):
    __tablename__ = 'proxies'

    id = Column(String(150), primary_key=True, default=lambda: str(uuid4()))
    ip_address = Column(String(150), nullable=True)
    port = Column(String(150), nullable=True)
    http = Column(String(150), nullable=True)
    https = Column(String(150), nullable=True)
    socks4 = Column(String(150), nullable=True)
    socks5 = Column(String(150), nullable=True)
    ssl = Column(String(150), nullable=True)
    country = Column(String(150), nullable=True)
    anonymity = Column(String(150), nullable=True)
    status = Column(String(150), nullable=True, default='Not Checked')
    last_checked = Column(String(150), nullable=True)

    def __init__(self, ip_address, port, http, https, socks4, socks5, ssl, country, anonymity, status, last_checked):
        self.ip_address = ip_address
        self.port = port
        self.http = http
        self.https = https
        self.socks4 = socks4
        self.socks5 = socks5
        self.ssl = ssl
        self.country = country
        self.anonymity = anonymity
        self.status = status
        self.last_checked = last_checked

base.metadata.create_all(engine)