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
	gender_total = Column(Float)
	gender_identity_total = Column(Float)
	total = Column(Float)
	population = Column(Float)
	race_per_cap = Column(Float)
	religion_per_cap = Column(Float)
	sex_per_cap = Column(Float)
	ethnicity_per_cap = Column(Float)
	disability_per_cap = Column(Float)
	gender_per_cap = Column(Float)
	gender_identity_per_cap = Column(Float)
	total_per_cap = Column(Float)

	def __repr__(self):

		return str(self.__dict__)

	def __eq__(self, other):

		self_dict = self.__dict__
		other_dict = other.__dict__
		
		# the test record doesnt have an id
		if "id" in self_dict:
			del self_dict["id"]
		else:
			del other_dict["id"]

		del self_dict["_sa_instance_state"]	
		del other_dict["_sa_instance_state"]

		return self_dict == other_dict


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
	gender_count = Column(Float)
	gender_identity_count = Column(Float)
	first_count = Column(Float)
	second_count = Column(Float)
	third_count = Column(Float)
	fourth_count = Column(Float)
	population = Column(Float)
	total = Column(Float)
	race_per_cap = Column(Float)
	religion_per_cap = Column(Float)
	sex_per_cap = Column(Float)
	ethnicity_per_cap = Column(Float)
	disability_per_cap = Column(Float)
	gender_per_cap = Column(Float)
	gender_identity_per_cap = Column(Float)
	total_per_cap = Column(Float)

	def __repr__(self):

		return str(self.__dict__)


	def __eq__(self, other):

		self_dict = self.__dict__
		other_dict = other.__dict__
		
		# the test record doesnt have an id
		if "id" in self_dict:
			del self_dict["id"]
		else:
			del other_dict["id"]

		del self_dict["_sa_instance_state"]	
		del other_dict["_sa_instance_state"]

		return self_dict == other_dict

def build_database():

	Base.metadata.create_all(engine)
