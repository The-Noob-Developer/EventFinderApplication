from sqlalchemy import Boolean , Column , Integer , String , ForeignKey , DateTime , Float
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime , timezone

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)  
    password_hash = Column(String(200), nullable=False)      
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    favorites = relationship("FavoriteEvent", back_populates="user", cascade="all, delete-orphan")

class FavoriteEvent(Base):
    __tablename__ = 'favorite_events'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(String(100), nullable=False)  # Ticketmaster Event ID
    name = Column(String(200))
    url = Column(String(300))
    date = Column(DateTime)
    image_url = Column(String(500))

    user = relationship("User", back_populates="favorites")
