from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///hatecrimes.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class States(Base):
	__tablename__ = 'states'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	year = Column(String)
	race_total = Column(Float)
	religion_total = Column(Float)
	sex_total = Column(Float)
	ethnicity_total = Column(Float)
	disability_total = Column(Float)
	population = Column(Float)

class Locations(Base):
	__tablename__ = 'locations'
	id = Column(Integer, primary_key=True)
	states_id = Column(Integer, ForeignKey('states.id'))
	agency_type = Column(String)
	name = Column(String)
	race_count = Column(Float)
	religion_count = Column(Float)
	sex_count = Column(Float)
	ethnicity_count = Column(Float)
	disability_count = Column(Float)
	first_count = Column(Float)
	second_count = Column(Float)
	third_count = Column(Float)
	fourth_count = Column(Float)
	population = Column(Float)
	total = Column(Float)

Base.metadata.create_all(engine)
