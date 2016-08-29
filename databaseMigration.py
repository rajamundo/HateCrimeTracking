import pyexcel as pe
from createDatabase import Session, States
from datetime import date


def parse_records(file_name):

	sheet = pe.get_sheet(file_name = file_name)
	year = ''.join([letter for letter in file_name if letter.isdigit()][2:])
	print(year)
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
	return state_totals, location_records

def insert_into_database(state_records, location_records):
	session = Session()
	
	for entry in state_records:
		new_record = States(name = entry[0], year = entry[1], race_total = entry[2], religion_total = entry[3], sex_total = entry[4], ethnicity_total = entry[5], disability_total = entry[6], population = entry[7])
		session.add(new_record)
	session.commit()
if __name__ == "__main__":
	file_name = "Table_13_Hate_Crime_Incidents_per_Bias_Motivation_and_Quarter_by_State_and_Agency_2011.xls"
	parse_records(file_name = file_name)
	#record = [["test", date.today(), 0, 0, 0, 0, 0, 0]]
	#insert_into_database(record, record)


# the counties and other agencies don't have a population total, which is rather confusing 