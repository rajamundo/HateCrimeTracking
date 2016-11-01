import pyexcel as pe
from createDatabase import Session, States, Locations
from helpers import generate_state, generate_location
from datetime import date
import re
import os
import decimal

STATES = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'DISTRICT OF COLUMBIA', 'FLORIDA', 'GEORGIA', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']

def get_indicies(location_records):
	# get rid of header notes and footnotes 
	front_idx = 0
	for x in location_records:
		front_idx += 1
		if x[0] == 'STATE':
			break

	back_idx = 0
	_digits = re.compile('\d')
	for x in reversed(location_records):
		if not _digits.search(x[0]):
			break
		back_idx -= 1

	return front_idx, back_idx	

def get_state_record(sheet, idx, state, year):

	nums = [float(num) for num in sheet.row[idx] if isinstance(num, (int,float))]
	total = sum(nums)
	if year == "2010" or year == "2011" or year == "2012":
		# negatives to indicate that this type of data was not collected these years
		nums = nums + [-1, -1]

	nums.insert(0, state)
	nums.insert(1, year)
	nums.append(total) # total

	return nums

def get_location_record(sheet, idx, state, year, region):

	location_crimes = []
	location_crimes.append(state)
	location_crimes.append(region)
	location = sheet[idx, 2]
	location_crimes.append(location)
	nums = [float(num) for num in [0 if not elt else elt for elt in sheet.row[idx]] if isinstance(num, (int,float))]
	# remove the two blanks that occur due to the blank fields for state and region type
	nums = nums[2:]

	if year == "2013" or year == "2014":
		location_total = sum(nums[:7])

	else:
		# these years do not have gender or gender_identity so use neg values
		location_total = sum(nums[:5])
		nums.insert(5, -1)
		nums.insert(6, -1)

	# remove the trailing blanks from the ends of rows in some of the spreadsheets
	nums = nums[:12]

	location_crimes = location_crimes + nums
	location_crimes.append(location_total)

	return location_crimes


def parse_records(file_name):

	sheet = pe.get_sheet(file_name = file_name)
	year = ''.join([letter for letter in file_name if letter.isdigit()][2:])
	total_column = (sheet.column[1])
	# state name, race, religion, sex orientation, ethnicity, disability
	state_totals = []
	location_records = []
	region = None
	state = None
	for idx, row in enumerate(total_column):
		if sheet[idx,0]:
			# if the column has a state value, assign the new state value
			state = sheet[idx, 0].upper()

		if row == "Total":

			nums = get_state_record(sheet, idx, state, year)
			state_totals.append(nums)

		elif row:
			# if the field is not null (aka cities, metro counties, universities)
			region = row
		else:
			location_crimes = get_location_record(sheet, idx, state, year, region)
			
			# only adds records that have a population and are the correct size, gets rid of header and footer
			try:
				if location_crimes[14] > 0:
					location_records.append(location_crimes)
			except:
				continue

	return state_totals, location_records

def get_zero_locations(file_name):
	sheet = pe.get_sheet(file_name = file_name)
	agency_column = (sheet.column[1])

	state = None 
	region = None
	zero_location_records = []

	for idx, row in enumerate(agency_column):
		location_record = [0]*16
		pop_exists = True
		if sheet[idx, 0]:
			state = sheet[idx, 0].upper()

		if row:
			region = row

		location = sheet[idx, 2]
		population = sheet[idx, 7]

		if not isinstance(population, int) or population == 0:
			pop_exists = False
			population = 0
		else:
			population = float(population)
	
		location_record[0] = state
		location_record[1] = region
		location_record[2] = location
		location_record[14] = population

		if pop_exists:
			zero_location_records.append(location_record)
	
	return zero_location_records

def get_state_populations():

	file_name = "NST_EST2014_ALLDATA.csv"
	main_folder = os.getcwd() + "/"
	sheet = pe.get_sheet(file_name=main_folder + file_name)
	years = [2010, 2011, 2012, 2013, 2014]
	headers = sheet.row[0]

	states = sheet.column[4]
	first_state_idx = states.index("Alabama")
	last_state_idx = states.index("Wyoming")
	hawaii_index = states.index('Hawaii')
	states.remove('Hawaii')
	states = states[first_state_idx:last_state_idx]
	state_populations = {}

	for year in years:
		column_name = "POPESTIMATE"
		population_nums = sheet.column[(headers.index(column_name + str(year)))]
		del population_nums[hawaii_index]
		population_nums = population_nums[first_state_idx:last_state_idx]
		
		state_populations[year] = {}

		for idx, state in enumerate(states):

		 	state_populations[year][state.upper()] = population_nums[idx]

	return state_populations


#**************************************INSERTING**************************************#

def insert_state_totals_into_database(state_totals, current_year, state_populations):
	session = Session()

	if len(STATES) != len(state_totals):

		differences = set(STATES) - set([name[0] for name in state_totals])
		for difference in differences:
			state_totals.append([difference.upper(), current_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	
	for entry in state_totals:
		assert(entry[1] == current_year)
		population = state_populations[int(current_year)][entry[0]]
		
		new_record = generate_state(entry, population)
		session.add(new_record)
	session.commit()

def insert_location_records_into_database(location_records, current_year):
	# location: [state, agency_type, name, race_count, religion_count, sex_count, ethnicity_count, disability_count, first_count, second_count, third_count, fourth_count, population, total]
	session = Session()
	current_state = None
	state_id = None
	for location in location_records:
		state = location[0]

		if state != current_state:
			current_state = state
			for state_entry in session.query(States).filter(States.name == current_state).filter(States.year == current_year):
				state_id = state_entry.id
		
		new_record = generate_location(state_id, location, per_caps)

		session.add(new_record)
	session.commit()

#***********************************************************************************#


if __name__ == "__main__":

	parse_records()





