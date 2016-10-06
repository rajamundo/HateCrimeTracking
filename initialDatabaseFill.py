from databaseMigration import parse_records, get_zero_locations, insert_state_totals_into_database, insert_location_records_into_database, get_state_populations
from createDatabase import build_database
import os

try:
	os.remove('hatecrimes.db')
except OSError:
	pass

build_database()

data_folder = os.getcwd() + "/Data/"
f = []
for (dirpath, dirnames, filenames) in os.walk(data_folder):
    f.extend(filenames)

state_populations = get_state_populations()

for file_name in f:
	file_path = data_folder + file_name
	year = ''.join([letter for letter in file_name if letter.isdigit()][2:])
	
	print(year)

	# locations with hate crimes
	if "Table_13" in file_name:
		state_totals, location_records = parse_records(file_name = file_path)
		insert_state_totals_into_database(state_totals, year, state_populations)
		insert_location_records_into_database(location_records, year)

	# for the cities with zero hate crimes
	else:
		zero_location_records = get_zero_locations(file_name = file_path)
		insert_location_records_into_database(zero_location_records, year)




# TO-DO:
# 1. Get States Populations for each year
