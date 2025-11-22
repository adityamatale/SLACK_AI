from sqlalchemy import Column, Integer, String, TIMESTAMP
from SLLACK.db.database import Base

class User(Base):

    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    encrypted_password = Column(String)
    created_at = Column(TIMESTAMP)