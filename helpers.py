from createDatabase import States, Locations


def generate_state(totals, pop):
	
	per_cap_totals = [float(total/pop) for total in totals[2:]]

	new_record = States(name = totals[0], year = totals[1], race_total = totals[2],
		religion_total = totals[3], sex_total = totals[4], ethnicity_total = totals[5],
		disability_total = totals[6], gender_total = totals[7], gender_identity_total = totals[8],
		total = totals[9], population = pop, race_per_cap = per_cap_totals[0],
		religion_per_cap = per_cap_totals[1], sex_per_cap = per_cap_totals[2],
		ethnicity_per_cap = per_cap_totals[3], disability_per_cap = per_cap_totals[4],
		gender_per_cap = per_cap_totals[5], gender_identity_per_cap = per_cap_totals[6], 
		total_per_cap = per_cap_totals[7])

	return new_record

def generate_location(state_id, location):

	# location[15] is total and location[14] is pop
	totals = location[3:10] +[location[15]]

	per_caps = [float(total/location[14]) for total in totals]
	new_record = Locations(states_id = state_id, agency_type = location[1], name = location[2], 
		race_count = location[3], religion_count = location[4], sex_count = location[5], 
		ethnicity_count = location[6], disability_count = location[7], gender_count = location[8],
		gender_identity_count = location[9], first_count = location[10], second_count = location[11],
		third_count = location[12], fourth_count = location[13], population = location[14], total = location[15],
		race_per_cap = per_caps[0], religion_per_cap = per_caps[1], sex_per_cap = per_caps[2],
		ethnicity_per_cap = per_caps[3], disability_per_cap = per_caps[4], gender_per_cap = per_caps[5],
		gender_identity_per_cap = per_caps[6], total_per_cap = per_caps[7], latitude = location[16], longitude = location[17])


	return new_record