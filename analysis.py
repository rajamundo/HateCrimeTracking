from createDatabase import Session, States, Locations
from operator import itemgetter
import statistics
import numpy as np

# session = Session()

# for name, year, total_per_cap in session.query(States.name, States.year, States.total_per_cap).order_by((States.total_per_cap).desc()):
# 	print(name, year, total_per_cap)

POP_MEDIAN = 5367

def top_ten_dangerous(percent = 0):

	session = Session()
	years = ["2010", "2011", "2012", "2013", "2014"]
	top_dangerous = {}
	lowest_pop = percentile_calculator(percent)
	for year in years:
		# sqlalchemy returns a tuple and we only want the id 
		state_ids = [x[0] for x in session.query(States.id).filter(States.year == year).all()]

		top_locations = []
		for id in state_ids: 

			# may need to make it more than one for hate crime total
			top_locations.extend(session.query(Locations.name, Locations.total, Locations.total_per_cap,
			 Locations.population, Location.total_per_cap).filter(Locations.states_id == id).filter(Locations.total > 1)
			.filter(Locations.population > lowest_pop).all())
			top_locations = sorted(top_locations,key=itemgetter(4), reverse = True)

		top_dangerous[year] = top_locations[0:10]

	for year, top in top_dangerous.items():

		print("For the year %s the most dangerous cities are:" % (year))
		print(top)


def percentile_calculator(percent):

	session = Session()

	population = np.array([x[0] for x in session.query(Locations.population).all()])

	
	print("The population mean is %d" % statistics.mean(population))
	print("The population median is %d" % statistics.median(population))

	#print(p)
	#print(len(population))

	return np.percentile(population, percent)

if __name__ == "__main__":

	top_ten_dangerous(0)
	#percentile_calculator(50)
