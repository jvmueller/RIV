from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Metro(Base):
    __tablename__ = 'cities'

    #defines each column
    id = Column(Integer, primary_key=True)  # Auto-incrementing ID number
    name = Column(String(100), nullable=False)  # Metro name, max 100 chars, required
    population = Column(Integer, nullable=False)  # Population number, required  
    latitude = Column(Float, nullable=False)  # Decimal number for latitude
    longitude = Column(Float, nullable=False)  # Decimal number for longitude

    #to string function
    def __repr__(self):
        return f"<Metro(name='{self.name}', population={self.population}, lat={self.latitude}, lon={self.longitude})>"
