from createDatabase import Session, States, Locations
from helpers import generate_state, generate_location


def states_insertion_test():
	
	session = Session()

	alabama_2011_counts = ["ALABAMA", "2011", float(58), float(5), float(7), float(11), float(2), float(-1), float(-1)]
	alabama_2011_pop = float(4801695)
	alabama_2011_counts.append(sum(alabama_2011_counts[2:7]))

	alabama_2011_record = generate_state(alabama_2011_counts, alabama_2011_pop)
	alabama_2011_db_entry = session.query(States).filter(States.name == "ALABAMA").filter(States.year == "2011").one()
	
#***********************************************************************************#


	new_york_2013_counts = ["NEW YORK", "2013", float(150), float(294), float(122), float(36), float(2), float(6), float(5)]
	new_york_2013_pop = float(19695680)
	new_york_2013_counts.append(sum(new_york_2013_counts[2:9]))

	new_york_2013_record  = generate_state(new_york_2013_counts, new_york_2013_pop)
	new_york_2013_db_entry = session.query(States).filter(States.name == "NEW YORK").filter(States.year == "2013").one()

#***********************************************************************************#

	connecticut_2014_counts = ["CONNECTICUT", "2014", float(57), float(31), float(23), float(11), float(1), float(0), float(0)]
	connecticut_2014_pop = float(3596677)
	connecticut_2014_counts.append(sum(connecticut_2014_counts[2:9]))

	connecticut_2014_record = generate_state(connecticut_2014_counts, connecticut_2014_pop)	
	connecticut_2014_db_entry = session.query(States).filter(States.name == "CONNECTICUT").filter(States.year == "2014").one()

#***********************************************************************************#

	comparisons = [[alabama_2011_record, alabama_2011_db_entry], [new_york_2013_record, new_york_2013_db_entry], 
	[connecticut_2014_record, connecticut_2014_db_entry]]

	for record, db_entry in comparisons:

		print("For %s:" % record.name )

		try:
			assert(record == db_entry)
			print("SUCCESS")
		except:
			print("NOT EQUIVALENT")
			print(record)
			print(db_entry)


def run_tests():

	states_insertion_test()


if __name__ == "__main__":

	run_tests()