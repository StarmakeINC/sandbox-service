from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Scenario(Base):
    __tablename__ = "sandbox_scenario"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True) 
    text = Column(Text, nullable=False)
    temp_id = Column(String(36), nullable=True)

    def __repr__(self):
        return f"<Scenario {self.text[:50]}>"