# coding=utf-8
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from validate_email import validate_email
import bcrypt

import config


Base = declarative_base()
engine = create_engine(config.db_url, echo=False)
plugin = sqlalchemy.Plugin(engine, None, keyword='db')

vote_table = Table(
    'vote',
    Base.metadata,
    Column('restriction_id', Integer, ForeignKey('restriction.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Restriction(Base):
    __tablename__ = 'restriction'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.current_timestamp())
    modified = Column(DateTime, server_default=func.current_timestamp())
    title = Column(String)
    body = Column(String)
    state = Column(Enum('NEW', 'APPROVED', 'REJECTED'))

    approver_id = Column(Integer, ForeignKey('user.id'))
    approver = relationship('User', foreign_keys=approver_id)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=user_id)

    user_name = Column(String)
    user_city = Column(String)

    voters = relationship('User', secondary=vote_table, backref='restrictions')

    def __repr__(self):
        return '<Restriction: %s>' % self.title

    def toDict(self, full=False, user=None):
        ret = {}
        ret['id'] = self.id
        ret['created'] = self.created
        ret['votes'] = len(self.voters)
        ret['title'] = self.title
        ret['body'] = self.body
        ret['user_name'] = self.user_name
        ret['user_city'] = self.user_city
        ret['state'] = self.state
        if full:
            if self.approver:
                ret['approver'] = self.approver.toDict()
            else:
                ret['approver'] = None
            ret['modified'] = self.modified
        if user:
            ret['voted'] = user in self.voters
        return ret

    @validates('title')
    def validate_title(self, key, title):
        assert title and len(title) <= 50
        return title

    @validates('body')
    def validate_body(self, key, body):
        assert body and len(body) <= (512 * 1024)
        return body

    @validates('user_name')
    def validate_name(self, key, name):
        assert name and len(name) <= 50
        return name

    @validates('user_city')
    def validate_city(self, key, city):
        assert city and len(city) <= 30
        return city


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    verified = Column(Boolean, server_default='FALSE')
    password = Column(String)
    city = Column(String)
    admin = Column(Boolean, server_default='FALSE')
    registered = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return '<User: %s>' % self.email

    def toDict(self, full=False):
        ret = {}
        ret['name'] = self.name
        ret['city'] = self.city
        if full:
            ret['id'] = self.id
            ret['email'] = self.email
            ret['registered'] = self.registered
            ret['admin'] = self.admin
        return ret

    @validates('email')
    def validate_email(self, key, email):
        assert email and len(email) <= 100 and validate_email(email)
        return email

    @validates('name')
    def validate_name(self, key, name):
        # turn empty values into Nones and check length for others
        if name is not None:
            if not name:
                name = None
            else:
                assert name and len(name) <= 50
        return name

    @validates('city')
    def validate_city(self, key, city):
        # turn empty values into Nones and check length for others
        if city is not None:
            if not city:
                city = None
            else:
                assert city and len(city) <= 30
        return city

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >= 8
        return bcrypt.hashpw(password, bcrypt.gensalt())


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created = Column(DateTime, server_default=func.current_timestamp())
    modified = Column(DateTime, server_default=func.current_timestamp())

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=user_id)

    def __repr__(self):
        return '<News: %s>' % self.title

    def toDict(self, full=False):
        ret = {}
        ret['title'] = self.title
        ret['body'] = self.body
        ret['created'] = self.created
        if full:
            ret['id'] = self.id
            ret['user'] = self.user.toDict()
            ret['modified'] = self.modified
        return ret
