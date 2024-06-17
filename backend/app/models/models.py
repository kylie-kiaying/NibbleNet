from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    profile_picture_url = Column(String, nullable=True)

class ListingStatus(enum.Enum):
    available = "available"
    reserved = "reserved"
    claimed = "claimed"

class FoodListing(Base):
    __tablename__ = 'food_listings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(Text)
    location = Column(String)
    status = Column(Enum(ListingStatus, name='listing_status'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="listings")

User.listings = relationship("FoodListing", order_by=FoodListing.id, back_populates="user")
