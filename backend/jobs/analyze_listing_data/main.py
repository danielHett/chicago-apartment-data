import json

with open('data.txt', 'r') as f: 
     raw_data = f.read()

units = json.loads(raw_data)

rent_agg = 0

hoods = set()
bed_types = set()
bath_types = set()

valid_units = []

for unit in units:
    if unit['unit'] is not None:
        unit_info = unit['unit']

        valid_units.append(unit_info)

        rent_agg += unit_info['current_price']
        
        hoods = hoods | set(unit_info['neighborhoods'])
        bed_types.add(unit_info['num_beds'])
        bath_types.add(unit_info['num_baths'])


print('TOTAL NUMBER OF VALID LISTINGS: ' + str(len(valid_units)))
print('AVERAGE RENT IN THE CITY: $' + str(round(rent_agg / len(valid_units), 2)))

# Let's get all neighborhoods. 
print(hoods)
print(bed_types)
print(bath_types)

hood_to_avg = {}
for hood in hoods:
    hood_unit_rents = [hood_unit['current_price'] for hood_unit in valid_units if hood in hood_unit['neighborhoods']]
    
    rent_agg = 0
    for rent in hood_unit_rents:
        rent_agg += rent
    
    avg = round(rent_agg / len(hood_unit_rents), 2)
    hood_to_avg[hood] = avg
    print('THE AVERAGE RENT IN ' + hood + ' IS: $' + str(avg))

top_hood = ''
top_hood_avg = 0
for hood,avg in hood_to_avg.items():
    if avg > top_hood_avg:
        top_hood = hood 
        top_hood_avg = avg

print('THE NEIGHBORHOOD WITH THE HIGHEST RENT IS ' + top_hood + ' AT $' + str(top_hood_avg))

low_hood = ''
low_hood_avg = 10000000
for hood,avg in hood_to_avg.items():
    if avg < low_hood_avg:
        low_hood = hood 
        low_hood_avg = avg

print('THE NEIGHBORHOOD WITH THE LOWEST RENT IS ' + low_hood + ' AT $' + str(low_hood_avg))