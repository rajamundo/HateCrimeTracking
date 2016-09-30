from databaseMigration import parse_records, get_zero_locations, insert_state_totals_into_database, insert_location_records_into_database
import os
print(os.getcwd())
data_folder = os.getcwd() + "/Data/"
f = []
for (dirpath, dirnames, filenames) in os.walk(data_folder):
    f.extend(filenames)
#print(f)

for file_name in f:
	file_path = data_folder + file_name
	year = ''.join([letter for letter in file_name if letter.isdigit()][2:])
	
	print(year)

	# locations with hate crimes
	if "Table_13" in file_name:
		state_totals, location_records = parse_records(file_name = file_path)
		insert_state_totals_into_database(state_totals)
		insert_location_records_into_database(location_records, year)

	# for the cities with zero hate crimes
	else:
		zero_location_records = get_zero_locations(file_name = file_path)
		insert_location_records_into_database(zero_location_records, year)




# TO-DO:
# 1. Write script to see which hate crime files don't have all the states
# 2. Check to see if the states that don't exist in the hate crime exist in the zero records
# 3. For territories like Guam that don't belong to a state, dont include them and write some sort of error if the code can't find matching state id for location record
# 4. Get States Populations for each year
# 5. add create database to this file