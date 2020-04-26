from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, ForeignKey, CHAR, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

sys.path.append('..')
import config as conf

engine = create_engine("mysql://" + conf.mysql["user"] + ":" + conf.mysql["passwd"] + "@" + conf.mysql["host"] + "/" + conf.mysql["db"])

base = declarative_base(engine)

class softballGameStats(base):
    __tablename__ = "baseballGameStats"
    __table_args__ = {"autoload": True}

class baseballGameStats(base):
    __tablename__ = "baseballGameStats"
    __table_args__ = {"autoload": True}

class wbbGameStats(base):
    __tablename__ = "mbbGameStats"
    __table_args__ = {"autoload": True}

class mbbGameStats(base):
    __tablename__ = "mbbGameStats"
    __table_args__ = {"autoload": True}

class baseballPitchingStats(base):
    __tablename__ = "baseballPitchingStats"
    __table_args__ = {"autoload": True}

class softballFieldingStats(base):
    __tablename__ = "softballFieldingStats"
    __table_args__ = {"autoload": True}

class wbbPlayerStats(base):
    __tablename__ = "wbbPlayerStats"
    __table_args__ = {"autoload": True}

class baseballBattingStats(base):
    __tablename__ = "baseballBattingStats"
    __table_args__ = {"autoload": True}

class softballPitchingStats(base):
    __tablename__ = "baseballFieldingStats"
    __table_args__ = {"autoload": True}

class baseballFieldingStats(base):
    __tablename__ = "baseballFieldingStats"
    __table_args__ = {"autoload": True}

class mbbPlayerStats(base):
    __tablename__ = "mbbPlayerStats"
    __table_args__ = {"autoload": True}

class mbbTeamStats(base):
    __tablename__ = "mbbTeamStats"
    __table_args__ = {"autoload": True}

class wbbTeamStats(base):
    __tablename__ = "wbbTeamStats"
    __table_args__ = {"autoload": True}

class softballBattingStats(base):
    __tablename__ = "softballBattingStats"
    __table_args__ = {"autoload": True}

class softballRoster(base):
    __tablename__ = "softballRoster"
    __table_args__ = {"autoload": True}

class mbbRoster(base):
    __tablename__ = "mbbRoster"
    __table_args__ = {"autoload": True}

class wbbRoster(base):
    __tablename__ = "wbbRoster"
    __table_args__ = {"autoload": True}

class baseballRoster(base):
    __tablename__ = "baseballRoster"
    __table_args__ = {"autoload": True}