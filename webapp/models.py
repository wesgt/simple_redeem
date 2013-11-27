import datetime
from sqlalchemy import Column, Integer, String, DateTime
from webapp.database import Base, db_session


class User(Base):
    __tablename__ = 'user'
    #__table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    redeem_code = Column(String(50))
    redeem_count = Column(Integer)
    register_date = Column(DateTime)

    def __init__(self, email, redeem_code, redeem_count,
                 register_date=datetime.datetime.today()):
        self.email = email
        self.redeem_code = redeem_code
        self.redeem_count = redeem_count
        self.register_date = register_date

    def __repr__(self):
        return '<User email {0}>'.format(self.email)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class RedeemGift(Base):
    __tablename__ = 'redeem_gift'
    #__table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    redeem_code = Column(String(50))
    redeem_date = Column(DateTime)

    def __init__(self, email, redeem_code,
                 redeem_date=datetime.datetime.today()):
        self.email = email
        self.redeem_code = redeem_code
        self.redeem_date = redeem_date

    def __repr__(self):
        return '<RedeemGift email:{0} redeem_code:{1}>'.format(
            self.email, self.redeem_code)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()