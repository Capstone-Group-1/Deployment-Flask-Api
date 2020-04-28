from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, ForeignKey, CHAR, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *
import json

engine = create_engine("mysql://" + conf.mysql["user"] + ":" + conf.mysql["passwd"] + "@" + conf.mysql["host"] + "/" + conf.mysql["db"])
base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#player methods
def GetPlayerData(id, sport):
    try:
        playerQuery = ""
        PlayerData = {}

        if sport == "mbb":
            playerQuery = session.query(mbbRoster).filter(mbbRoster.jerseyNo == id).first()
        elif sport == "wbb":
            playerQuery = session.query(wbbRoster).filter(wbbRoster.jerseyNo == id).first()
        elif sport == "baseball":
            playerQuery = session.query(baseballRoster).filter(baseballRoster.jerseyNo == id).first()
        elif sport == "softball":
            playerQuery = session.query(softballRoster).filter(softballRoster.jerseyNo == id).first()

        session.close()

        if playerQuery is not None:
            PlayerData = playerQuery.__dict__
            print(PlayerData)
            PlayerData.pop('_sa_instance_state', None)

            return json.dumps(PlayerData)

        return "No player with that jersey number."
    except:
        session.rollback()
        return "mysql error"


def GetPlayerStats(id, sport):
    try:
        TeamStatsQuery = ""
        PitchingStats = ""
        BattingStats = ""
        FieldingStats = ""

        PitchingItem = ""
        BattingItem = ""
        FieldingItem = ""

        PlayerStatsQuery = ""

        if sport == "baseball":
            PitchingStats = session.query(baseballPitchingStats).filter(baseballPitchingStats.jerseyNo == id).first()
            BattingStats = session.query(baseballBattingStats).filter(baseballBattingStats.jerseyNo == id).first()
            FieldingStats = session.query(baseballFieldingStats).filter(baseballFieldingStats.jerseyNo == id).first()
        elif sport == "softball":
            PitchingStats = session.query(softballPitchingStats).filter(softballPitchingStats.jerseyNo == id).first()
            BattingStats = session.query(softballBattingStats).filter(softballBattingStats.jerseyNo == id).first()
            FieldingStats = session.query(softballFieldingStats).filter(softballFieldingStats.jerseyNo == id).first()
        elif sport == "wbb":
            PlayerStatsQuery = session.query(wbbPlayerStats).filter(wbbPlayerStats.jerseyNo == id).first()
        elif sport == "mbb":
            PlayerStatsQuery = session.query(mbbPlayerStats).filter(mbbPlayerStats.jerseyNo == id).first()

        if sport in ("wbb", "mbb"):
            Basketball = PlayerStatsQuery.__dict__
            Basketball.pop('_sa_instance_state', None)

            return json.dumps(Basketball)

        if sport in ("baseball", "softball"):
            #for pitItem in PitchingStats:
            if PitchingStats != None:
                PitchingItem = PitchingStats.__dict__
                PitchingItem.pop('_sa_instance_state', None)

            #for batItem in BattingStats:
            if BattingStats != None:
                BattingItem = BattingStats.__dict__
                BattingItem.pop('_sa_instance_state', None)

            #for fieldItem in FieldingStats:
            if FieldingStats != None:
                FieldingItem = FieldingStats.__dict__
                FieldingItem.pop('_sa_instance_state', None)

            return json.dumps([{"Pitching": PitchingItem}, {"Batting": BattingItem}, {"Fielding": FieldingItem}])

        return None
    except:
        session.rollback()
        return "mysql error"

#team methods
def GetTeamRoster(sport):
    try: 
        TeamRoster = []
        TeamQuery = ""

        if sport == "mbb":
            TeamQuery = session.query(mbbRoster).all()
        elif sport == "wbb":
            TeamQuery = session.query(wbbRoster).all()
        elif sport == "baseball":
            TeamQuery = session.query(baseballRoster).all()
        elif sport == "softball":
            TeamQuery = session.query(softballRoster).all()

        for item in TeamQuery:
            TeamMember = {
                "jerseyNum": item.jerseyNo,
                "pictureFile": item.picFileName,
                "firstname": item.firstName,
                "lastname": item.lastName
            }
            TeamRoster.append(TeamMember)
            
        session.close()

        return json.dumps(TeamRoster)
    except:
        session.rollback()
        return "mysql error"

def GetTeamStats(sport):
    try:
        TeamStatsQuery = ""
        PitchingStats = ""
        BattingStats = ""
        FieldingStats = ""
        
        Basketball = {}
        Picthing = []
        Batting = []
        Fielding = []

        if sport == "mbb":
            TeamStatsQuery = session.query(mbbTeamStats).first()
        elif sport == "wbb":
            TeamStatsQuery = session.query(wbbTeamStats).first()
        elif sport == "baseball":
            PitchingStats = session.query(baseballPitchingStats).all()
            BattingStats = session.query(baseballBattingStats).all()
            FieldingStats = session.query(baseballFieldingStats).all()
        elif sport == "softball":
            PitchingStats = session.query(softballPitchingStats).all()
            BattingStats = session.query(softballBattingStats).all()
            FieldingStats = session.query(softballFieldingStats).all()

        session.close()

        if sport in ("wbb", "mbb"):
            Basketball = TeamStatsQuery.__dict__
            Basketball.pop('_sa_instance_state', None)

            return json.dumps(Basketball)

        if sport in ("baseball", "softball"):
            for pitItem in PitchingStats:
                PitchingItem = pitItem.__dict__
                PitchingItem.pop('_sa_instance_state', None)
                Picthing.append(PitchingItem)

            for batItem in BattingStats:
                BattingItem = batItem.__dict__
                BattingItem.pop('_sa_instance_state', None)
                Batting.append(BattingItem)

            for fieldItem in FieldingStats:
                FieldingItem = pitItem.__dict__
                FieldingItem.pop('_sa_instance_state', None)
                Fielding.append(FieldingItem)

            return json.dumps([{"Pitching": Picthing}, {"Batting": Batting}, {"Fielding": Fielding}])

        return None
    except:
        session.rollback()
        return "mysql error"


def GetTeamStatsPerformance(sport, stat):
    try:
        data = ""
        dataList = []
        Result = ""

        if sport == "mbb":
            data = session.query(mbbGameStats).all()
        elif sport == "wbb":
            data = session.query(wbbGameStats).all()
        elif sport == "baseball":
            data = session.query(baseballGameStats).all()
        elif sport == "softball":
            data = session.query(softballGameStats).all()

        for item in data:
            Result = item.__dict__
            Game = {
                "date": item.date,
                "stat": Result.get(stat)
            }
            dataList.append(Game)

        return json.dumps(dataList)
    except:
        session.rollback()
        return "mysql error"

def GetStats(sport):
    try:
        columns = ""
        Stats = []
        StatDict = {}

        if sport == "mbb":
            columns = mbbGameStats.__table__.columns
        elif sport == "wbb":
            columns = wbbGameStats.__table__.columns
        elif sport == "baseball":
            columns = baseballGameStats.__table__.columns
        elif sport == "softball":
            columns = softballGameStats.__table__.columns

        for item in columns:
            colValue = str(item).split('.')
            colName = colValue[1]

            if colName == "fieldGoalsMade":
                StatDict = {"statAbrv": colName, "statName": "Field Goals Made"}
                Stats.append(StatDict)
            elif colName == "fieldGoalAttempts":
                StatDict = {"statAbrv": colName, "statName": "Field Goal Attempts"}
                Stats.append(StatDict)
            elif colName == "3ptMade":
                StatDict = {"statAbrv": colName, "statName": "3 PT Made"}
                Stats.append(StatDict)
            elif colName == "3ptAttempted":
                StatDict = {"statAbrv": colName, "statName": "3 PT Attempted"}
                Stats.append(StatDict)
            elif colName == "ftMade":
                StatDict = {"statAbrv": colName, "statName": "Free Throw Made"}
                Stats.append(StatDict)
            elif colName == "ftAttempted":
                StatDict = {"statAbrv": colName, "statName": "Free Throw Attempted"}
                Stats.append(StatDict)
            elif colName == "oRebs":
                StatDict = {"statAbrv": colName, "statName": "Offensive Rebounds"}
                Stats.append(StatDict)
            elif colName == "dRebs":
                StatDict = {"statAbrv": colName, "statName": "Defensive Rebounds"}
                Stats.append(StatDict)
            elif colName == "totalRebs":
                StatDict = {"statAbrv": colName, "statName": "Total Rebounds"}
                Stats.append(StatDict)
            elif colName == "personalFouls":
                StatDict = {"statAbrv": colName, "statName": "Personal Fouls"}
                Stats.append(StatDict)
            elif colName == "assists":
                StatDict = {"statAbrv": colName, "statName": "Assists"}
                Stats.append(StatDict)
            elif colName == "turnovers":
                StatDict = {"statAbrv": colName, "statName": "Turnovers"}
                Stats.append(StatDict)
            elif colName == "blocks":
                StatDict = {"statAbrv": colName, "statName": "Blocks"}
                Stats.append(StatDict)
            elif colName == "steals":
                StatDict = {"statAbrv": colName, "statName": "Steals"}
                Stats.append(StatDict)
            elif colName == "points":
                StatDict = {"statAbrv": colName, "statName": "Points"}
                Stats.append(StatDict)
            elif colName == "outcome":
                StatDict = {"statAbrv": colName, "statName": "Outcome"}
                Stats.append(StatDict)
            elif colName == "atBats":
                StatDict = {"statAbrv": colName, "statName": "At Bats"}
                Stats.append(StatDict)
            elif colName == "runs":
                StatDict = {"statAbrv": colName, "statName": "Runs"}
                Stats.append(StatDict)
            elif colName == "hits":
                StatDict = {"statAbrv": colName, "statName": "Hits"}
                Stats.append(StatDict)
            elif colName == "rbis":
                StatDict = {"statAbrv": colName, "statName": "Runs Batted In"}
                Stats.append(StatDict)
            elif colName == "doubles":
                StatDict = {"statAbrv": colName, "statName": "Doubles"}
                Stats.append(StatDict)
            elif colName == "triples":
                StatDict = {"statAbrv": colName, "statName": "Triple"}
                Stats.append(StatDict)
            elif colName == "homeruns":
                StatDict = {"statAbrv": colName, "statName": "Homeruns"}
                Stats.append(StatDict)
            elif colName == "walks":
                StatDict = {"statAbrv": colName, "statName": "Walks"}
                Stats.append(StatDict)
            elif colName == "ibbs":
                StatDict = {"statAbrv": colName, "statName": "Intentional Base on Balls"}
                Stats.append(StatDict)
            elif colName == "stolenBases":
                StatDict = {"statAbrv": colName, "statName": "Stolen Bases"}
                Stats.append(StatDict)
            elif colName == "caughtStealing":
                StatDict = {"statAbrv": colName, "statName": "Caught Stealing"}
                Stats.append(StatDict)
            elif colName == "hbps":
                StatDict = {"statAbrv": colName, "statName": "Hits by Ptich"}
                Stats.append(StatDict)
            elif colName == "sacrificeHits":
                StatDict = {"statAbrv": colName, "statName": "Sacrifice Hits"}
                Stats.append(StatDict)
            elif colName == "gdps":
                StatDict = {"statAbrv": colName, "statName": "Grounding Into Double Plays"}
                Stats.append(StatDict)
            elif colName == "strikeouts":
                StatDict = {"statAbrv": colName, "statName": "Strikeouts"}
                Stats.append(StatDict)
            elif colName == "putouts":
                StatDict = {"statAbrv": colName, "statName": "Putouts"}
                Stats.append(StatDict)
            elif colName == "errors":
                StatDict = {"statAbrv": colName, "statName": "Errors"}
                Stats.append(StatDict)

        return json.dumps(Stats)
    except:
        session.rollback()
        return "mysql error"