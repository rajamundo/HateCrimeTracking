import pyexcel as pe
from createDatabase import Session, States, Locations
from datetime import date


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
			state = sheet[idx, 0]

		if row == "Total":

			nums = [float(num) for num in sheet.row[idx] if isinstance(num, (int,float))]
			nums.insert(0, state)
			nums.insert(1, year)
			state_totals.append(nums)

		elif row:
			# if the field is not null (aka cities, metro counties, universities)
			region = row
		else:
			location_crimes = []
			location_crimes.append(state)
			location_crimes.append(region)
			location = sheet[idx, 2]
			location_crimes.append(location)
			nums = [float(num) for num in [0 if not elt else elt for elt in sheet.row[idx]] if isinstance(num, (int,float))]
			# remove the two blanks that occur due to the blank fields for state and region type
			nums = nums[2:]
			location_total = sum(nums[:5])
			location_crimes = location_crimes + nums
			location_crimes.append(location_total)
			location_records.append(location_crimes)
	# get rid of header notes and footnotes 
	location_records = location_records[4:-4]
	print(location_records)
	return state_totals, location_records

def get_zero_locations(file_name):
	sheet = pe.get_sheet(file_name = file_name)
	agency_column = (sheet.column[1])

	state = None 
	region = None
	zero_location_records = []

	for idx, row in enumerate(agency_column):
		location_record = [0]*14
		if sheet[idx, 0]:
			state = sheet[idx, 0]

		if row:
			region = row

		location = sheet[idx, 2]
		population = sheet[idx, 7]
		location_record[0] = state
		location_record[1] = region
		location_record[2] = location
		location_record[12] = population
		zero_location_records.append(location_record)
	
	zero_location_records = zero_location_records[4:-3]
	print(zero_location_records)

	return zero_location_records

def insert_into_database(state_records, location_records, current_year):
	session = Session()
	
	for entry in state_records:
		new_record = States(name = entry[0], year = entry[1], race_total = entry[2], religion_total = entry[3], sex_total = entry[4], ethnicity_total = entry[5], disability_total = entry[6], population = entry[7])
		session.add(new_record)
	session.commit()


	# location: [state, agency_type, name, race_count, religion_count, sex_count, ethnicity_count, disability_count, first_count, second_count, third_count, fourth_count, population, total]
	current_state = None
	state_id = None
	for location in location_records:
		state = location[0]
		if state != current_state:
			current_state = state
			for state_entry in session.query(States).filter(States.name == current_state).filter(States.year == current_year):
				state_id = state_entry.id
		new_record = Locations(states_id = state_id, agency_type = location[1], name = location[2], race_count = location[3], religion_count = location[4], sex_count = location[5], ethnicity_count = location[6], disability_count = location[7], first_count = location[8], second_count = location[9], third_count = location[10], fourth_count = location[11], population = location[12], total = location[13])
		session.add(new_record)
	session.commit()

	#TO-DO: get the state populations for each year
if __name__ == "__main__":
	file_name = "Table_13_Hate_Crime_Incidents_per_Bias_Motivation_and_Quarter_by_State_and_Agency_2011.xls"
	state_totals, location_records = parse_records(file_name = file_name)
	insert_into_database(state_totals, location_records, '2011')
	#file_name = "Table_14_Hate_Crime_Zero_Data_Submitted_per_Quarter_by_State_and_Agency_2011.xls"
	#get_zero_locations(file_name = file_name)
	#record = [["test", date.today(), 0, 0, 0, 0, 0, 0]]
	#insert_into_database(record, record)


# the counties and other agencies don't have a population total, which is rather confusing 