from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean,
    Enum, Float
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


# ------------------------
# Typy eventów
# ------------------------
class EventType(str, enum.Enum):
    # SYSTEM
    LOGIN = "login"
    LOGOUT = "logout"

    # PLAYER STATE / MOVEMENT
    CROUCH = "crouch"              # wciśnięcie/przytrzymanie/zwolnienie
    SKILL_INCREASE = "skill_increase"
    SKILL_DECREASE = "skill_decrease"

    # COMBAT
    DAMAGE_DEALT = "damage_dealt"
    DAMAGE_RECEIVED = "damage_received"
    DEATH = "death"

    # ITEMS
    ITEM_CRAFT = "item_craft"
    ITEM_DROP = "item_drop"
    ITEM_PICKUP = "item_pickup"
    ITEM_EQUIP = "item_equip"
    ITEM_USE = "item_use"
    ITEM_USE_ON_PIECE = "item_use_on_piece"

    # BUILDING
    PIECE_PLACED = "piece_placed"
    PIECE_DESTROYED = "piece_destroyed"

    # INTERACTIONS
    INTERACTION = "interaction"
    GRAVE_INTERACTION = "grave_interaction"

    # SOCIAL / COMMUNICATION
    PLAYER_PING = "player_ping"



# ------------------------
# Player
# ------------------------
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("PlayerSession", back_populates="player")
    events = relationship("EventLog", back_populates="player")
    stats = relationship("PlayerStats", uselist=False, back_populates="player")


# ------------------------
# Player Sessions
# ------------------------
class PlayerSession(Base):
    __tablename__ = "player_sessions"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime, nullable=True)
    session_length = Column(Integer, nullable=True)  # w sekundach

    player = relationship("Player", back_populates="sessions")


# ------------------------
# Event Log (ważne eventy)
# ------------------------
class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))

    session_id = Column(Integer, ForeignKey("player_sessions.id"), nullable=True)
    event_type = Column(Enum(EventType))
    value = Column(Float, nullable=True)  
    # Np:
    # - DAMAGE = liczba obrażeń
    # - HEAL = ilość leczenia
    # - QUEST_COMPLETE = xp / nagroda
    # - LEVEL_UP = nowy poziom
    # - KILL/DEATH bez value

    timestamp = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="events")
    session = relationship("PlayerSession")


# ------------------------
# Aggregated Player Stats
# ------------------------
class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), unique=True)

    total_play_time = Column(Integer, default=0)  # sekundy
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    damage_dealt = Column(Float, default=0.0)
    damage_taken = Column(Float, default=0.0)
    quests_completed = Column(Integer, default=0)
    level = Column(Integer, default=1)

    player = relationship("Player", back_populates="stats")
