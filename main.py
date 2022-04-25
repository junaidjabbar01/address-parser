import csv
import address_parser

states_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

with open('all_addresses.csv') as csvfile, open('formatted_address.csv', 'w') as csvoutput:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    writerCSV = csv.writer(csvoutput, lineterminator='\n')
    writerCSV.writerow(['object_id','geocoded_address', 'formatted_address'])

    for row in readCSV:
        digit_added = False
        address = row[1]
        address_split_spaces = address.replace(',',' ').replace('  ',' ').split()
        print ('splitted_address ' + str(address_split_spaces))
        for component in address_split_spaces:
            for state_key,state_value in states_dict.items():
                if component == state_value:
                    address_split_spaces[address_split_spaces.index(component)]= state_key
        address_to_parse = ' '.join(address_split_spaces)

        # print (address_to_parse)
        print('address_parse ' + address_to_parse)
        if (str(address)[0].isdigit() == False):
            address = '500 '+ address
            digit_added = True
        try:
            results = address_parser.tag(address_to_parse)
            # print(results)
            temp = results[0]
            street_address = ''
            place_name = ''
            state_name = ''
            zip_code = ''
            for key, value in results[0].items():
                if key not in ('PlaceName','StateName','ZipCode'):
                    street_address = street_address +' '+ value
                elif key == 'PlaceName':
                    place_name = value
                    #print ('Place Name is ' + value)
                elif key == 'StateName':
                    state_name = value
                    #print ('StateName is ' + value)
                elif key == 'ZipCode':
                    zip_code = value
                    #print ('ZipCode is ' + value)
                street_address = street_address.lstrip(' ')
                final_address_raw =  street_address + ', ' +  place_name + ', ' +  state_name + ', ' +  zip_code
            final_address_splitted = final_address_raw.replace(', ',',').split(',')
            print(final_address_splitted)
            for final_component in final_address_splitted:
                for state_key, state_value in states_dict.items():
                    if final_component == state_key:
                        final_address_splitted[final_address_splitted.index(final_component)] = state_value

            final_address = ', '.join(final_address_splitted)

            if digit_added is True:
                if (final_address[0:2] == '500 '):
                    final_address = final_address[2:]
            print('Records Processed: ' + row[0])
            final_address = final_address.lstrip(',').lstrip(' ')
            final_address = final_address.replace(', , ,',',')
            final_address = final_address.replace(', ,', ',')
            writerCSV.writerow([row[0], row[1], final_address])
        except:
            print('Records Not Parsed: ' + row[0])
            writerCSV.writerow([row[0], row[1], 'Ambigious Address'])
            pass



