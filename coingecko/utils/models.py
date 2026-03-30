from sqlalchemy import Column, DateTime, Float, Integer, String

from coingecko.utils.base import Base


class Coin(Base):
    __tablename__ = "coins"

    coin_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class Price(Base):
    __tablename__ = "prices"

    coin_id = Column(String, primary_key=True)
    price = Column(Float, nullable=False)
    last_updated = Column(DateTime)


class MarketData(Base):
    __tablename__ = "market_data"

    coin_id = Column(String, primary_key=True)
    market_cap = Column(Float)
    total_volume = Column(Float)
    market_cap_rank = Column(Integer)
