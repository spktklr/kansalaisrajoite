# coding=utf-8
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()
engine = create_engine('postgresql+psycopg2:///kansalaisrajoite', echo=False)
plugin = sqlalchemy.Plugin(engine, None, keyword='db')


kannatustaulu = Table('kannatus', Base.metadata,
	Column('rajoite_id', Integer, ForeignKey('rajoite.id')),
	Column('kayttaja_id', Integer, ForeignKey('kayttaja.id'))
)

class Rajoite(Base):
	__tablename__ = 'rajoite'
	
	id = Column(Integer, primary_key=True)
	luontiaika = Column(DateTime, server_default=func.current_timestamp())
	muokkausaika = Column(DateTime, server_default=func.current_timestamp())
	otsikko = Column(String)
	sisalto = Column(String)
	perustelut = Column(String)
	vahvistettu = Column(Boolean, server_default='FALSE')
	
	vahvistaja_id = Column(Integer, ForeignKey('kayttaja.id'))
	vahvistaja = relationship('Kayttaja', foreign_keys=vahvistaja_id)
	
	kayttaja_id = Column(Integer, ForeignKey('kayttaja.id'))
	kayttaja = relationship('Kayttaja', foreign_keys=kayttaja_id)
	
	kannattajat = relationship('Kayttaja', secondary=kannatustaulu, backref='rajoitteet')
	
	def __repr__(self):
		return '<Rajoite: %s>' % self.otsikko
	
	def toDict(self, full=False):
		ret = {}
		ret['id'] = self.id
		ret['luontiaika'] = self.luontiaika
		ret['otsikko'] = self.otsikko
		ret['kannattajamaara'] = len(self.kannattajat)
		ret['sisalto'] = self.sisalto
		ret['perustelut'] = self.perustelut
		ret['vireillepanija'] = self.kayttaja.toDict()
		ret['vahvistettu'] = self.vahvistettu
		if full:
			ret['vahvistaja'] = self.vahvistaja.toDict()
			ret['muokkausaika'] = self.muokkausaika
		return ret

class Kayttaja(Base):
	__tablename__ = 'kayttaja'
	
	id = Column(Integer, primary_key=True)
	email = Column(String)
	nimi = Column(String)
	salasana = Column(String)
	kaupunki = Column(String)
	yllapitaja = Column(Boolean, server_default='FALSE')
	rekisteroitymisaika = Column(DateTime, server_default=func.current_timestamp())
	
	def __repr__(self):
		return '<Käyttäjä: %s>' % self.email
	
	def toDict(self, full=False):
		ret = {}
		ret['nimi'] = self.nimi
		ret['kaupunki'] = self.kaupunki
		if full:
			ret['id'] = self.id
			ret['email'] = self.email
			ret['rekisteroitymisaika'] = self.rekisteroitymisaika
			ret['yllapitaja'] = self.yllapitaja
		return ret
