import csv
import numpy as np

CHILDREN_FAMILY_MAX = 100

def minmax(x, min, max):
    return (x - min) / (max - min)

sets = ["validation","testing"]

for curr_name in sets:

    annual_income_list=[]
    #bday_list=[]
    employee_days_list=[]

    with open(curr_name+'_dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                annual_income_list.append(float(row[5]))
                #bday_list.append(float(row[10]))
                employee_days_list.append(float(row[11]))
            line_count+=1

    minimum_employee_days = min(employee_days_list)

    # log transform
    annual_income_list = [np.log(income+1) for income in annual_income_list]
    #bday_list = [np.log(abs(bday)+1) for bday in bday_list]
    employee_days_list = [np.sign(days)*np.log(abs(days)+1) for days in employee_days_list]

    with open('statistics.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                income_mean = float(row[0])
                income_std = float(row[1])
                employee_days_mean = float(row[2])
                employee_days_std = float(row[3])
            line_count+=1
    #print(income_mean,income_std,employee_days_mean,employee_days_std)

    # z-score standardization
    annual_income_list = [(income - income_mean)/income_std for income in annual_income_list]
    #bday_list = [(bday - bday_mean)/bday_std for bday in bday_list]
    employee_days_list = [(days - employee_days_mean)/employee_days_std for days in employee_days_list]



    encoded_data=[]
    inc_empl_cntr=0
    with open(curr_name+'_dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            encoded_row=[]
            if line_count == 0:
                header = [
                    "Gender","Car Owner","Property Owner","Children","Annual Income",
                    "Type Income 1","Type Income 2","Education 1","Education 2","Education 3",
                    "Marital Status 1","Marital Status 2","Marital Status 3","Housing Type 1","Housing Type 2",
                    "Housing Type 3","Birthday Count","Employee Days","Work Phone","Phone",
                    "Email","Type Occupation 1","Type Occupation 2","Type Occupation 3","Type Occupation 4",
                    "Type Occupation 5","Family Members","Label"
                    ]
                encoded_data.append(header)
            else:
                # 0 - index in dataset (do not encode)
                # 1 - gender - HAS MISSING 
                    # 0-M
                    # 0.5-U
                    # 1-F
                if row[1] == "M":
                    encoded_row.append(0)
                elif row[1] == "F":
                    encoded_row.append(1)
                else:
                    encoded_row.append(0.5)
                # 2 - car owner
                    # 0-N
                    # 1-Y
                if row[2] == "N":
                    encoded_row.append(0)
                elif row[2] == "Y":
                    encoded_row.append(1)
                # 3 - property owner
                    # 0-N
                    # 1-Y
                if row[3] == "N":
                    encoded_row.append(0)
                elif row[3] == "Y":
                    encoded_row.append(1)
                # 4 - children
                    # Min-Max Sampling
                encoded_row.append(minmax(int(row[4]),0,CHILDREN_FAMILY_MAX))
                # 5 - annual income - HAS MISSING
                    # Log transform, due to right skewedness
                    # Standardization
                encoded_row.append(annual_income_list[inc_empl_cntr])
                # 6 - type income
                    # 00 - Pensioner
                    # 01 - Commercial associate
                    # 10 - Working
                    # 11 - State servant
                if row[6] == "Pensioner":
                    encoded_row.append(0)
                    encoded_row.append(0)
                elif row[6] == "Commercial associate":
                    encoded_row.append(0)
                    encoded_row.append(1)
                elif row[6] == "Working":
                    encoded_row.append(1)
                    encoded_row.append(0)
                elif row[6] == "State servant":
                    encoded_row.append(1)
                    encoded_row.append(1)
                # 7 - education
                    # 000 - Higher education
                    # 001 - Secondary / secondary special
                    # 010 - Lower secondary
                    # 011 - Incomplete higher
                    # 100 - Academic degree
                if row[7] == "Higher education":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(0)
                elif row[7] == "Secondary / secondary special":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(1)
                elif row[7] == "Lower secondary":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(0)
                elif row[7] == "Incomplete higher":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(1)
                elif row[7] == "Academic degree":
                    encoded_row.append(1)
                    encoded_row.append(0)
                    encoded_row.append(0)
                # 8 - marital status
                    # 000 - Married
                    # 001 - Single / not married
                    # 010 - Civil marriage
                    # 011 - Separated
                    # 100 - Widow
                if row[8] == "Married":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(0)
                elif row[8] == "Single / not married":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(1)
                elif row[8] == "Civil marriage":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(0)
                elif row[8] == "Separated":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(1)
                elif row[8] == "Widow":
                    encoded_row.append(1)
                    encoded_row.append(0)
                    encoded_row.append(0)
                # 9 - housing type
                    # 000 - House / apartment
                    # 001 - With parents
                    # 010 - Rented apartment
                    # 011 - Municipal apartment
                    # 100 - Co-op apartment
                    # 101 - Office apartment
                if row[9] == "House / apartment":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(0)
                elif row[9] == "With parents":
                    encoded_row.append(0)
                    encoded_row.append(0)
                    encoded_row.append(1)
                elif row[9] == "Rented apartment":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(0)
                elif row[9] == "Municipal apartment":
                    encoded_row.append(0)
                    encoded_row.append(1)
                    encoded_row.append(1)
                elif row[9] == "Co-op apartment":
                    encoded_row.append(1)
                    encoded_row.append(0)
                    encoded_row.append(0)
                elif row[9] == "Office apartment":
                    encoded_row.append(1)
                    encoded_row.append(0)
                    encoded_row.append(1)
                # 10 - birthday count - HAS MISSING
                    # Convert to positive
                    # Log transform
                    # Standardization
                    # OR
                    # Min-Max Scaling
                encoded_row.append(minmax(abs(int(row[10])),0,47450))
                # 11 - employee days - HAS VALUE PRESUMED EQUIVALENT TO MISSING
                    # Get absolute, then later return sign
                    # Log transform
                    # Standardization
                encoded_row.append(employee_days_list[inc_empl_cntr])
                # 12 - work phone
                    # 0 - 0
                    # 1 - 1
                if row[12] == "0":
                    encoded_row.append(0)
                elif row[12] == "1":
                    encoded_row.append(1)
                # 13 - phone
                    # 0 - 0
                    # 1 - 1
                if row[13] == "0":
                    encoded_row.append(0)
                elif row[13] == "1":
                    encoded_row.append(1)
                # 14 - email id
                    # 0 - 0
                    # 1 - 1
                if row[14] == "0":
                    encoded_row.append(0)
                elif row[14] == "1":
                    encoded_row.append(1)
                # 15 - type occupation - HAS MISSING
                    # 00000 - Unknown
                    # 00001 - Core staff
                    # 00010 - Cooking staff
                    # 00011 - Laborers
                    # 00100 - Sales staff
                    # 00101 - Accountants
                    # 00110 - High skill tech staff
                    # 00111 - Managers
                    # 01000 - Cleaning staff
                    # 01001 - Drivers
                    # 01010 - Low-skill Laborers
                    # 01011 - IT staff
                    # 01100 - Waiters/barmen staff
                    # 01101 - Security staff
                    # 01110 - Medicine staff
                    # 01111 - Private service staff
                    # 10000 - HR staff
                    # 10001 - Secretaries
                    # 10010 - Realty agents
                if row[15] == "Unknown":
                    encoded_row.extend([0,0,0,0,0])
                elif row[15] == "Core staff":
                    encoded_row.extend([0,0,0,0,1])
                elif row[15] == "Cooking staff":
                    encoded_row.extend([0,0,0,1,0])
                elif row[15] == "Laborers":
                    encoded_row.extend([0,0,0,1,1])
                elif row[15] == "Sales staff":
                    encoded_row.extend([0,0,1,0,0])
                elif row[15] == "Accountants":
                    encoded_row.extend([0,0,1,0,1])
                elif row[15] == "High skill tech staff":
                    encoded_row.extend([0,0,1,1,0])
                elif row[15] == "Managers":
                    encoded_row.extend([0,0,1,1,1])
                elif row[15] == "Cleaning staff":
                    encoded_row.extend([0,1,0,0,0])
                elif row[15] == "Drivers":
                    encoded_row.extend([0,1,0,0,1])
                elif row[15] == "Low-skill Laborers":
                    encoded_row.extend([0,1,0,1,0])
                elif row[15] == "IT staff":
                    encoded_row.extend([0,1,0,1,1])
                elif row[15] == "Waiters/barmen staff":
                    encoded_row.extend([0,1,1,0,0])
                elif row[15] == "Security staff":
                    encoded_row.extend([0,1,1,0,1])
                elif row[15] == "Medicine staff":
                    encoded_row.extend([0,1,1,1,0])
                elif row[15] == "Private service staff":
                    encoded_row.extend([0,1,1,1,1])
                elif row[15] == "HR staff":
                    encoded_row.extend([1,0,0,0,0])
                elif row[15] == "Secretaries":
                    encoded_row.extend([1,0,0,0,1])
                elif row[15] == "Realty agents":
                    encoded_row.extend([1,0,0,1,0])
                # 16 - family members
                    # Min-Max Sampling
                encoded_row.append(minmax(int(row[16]),0,CHILDREN_FAMILY_MAX))
                # 17 - label / output
                encoded_row.append(int(row[17]))

                encoded_data.append(encoded_row)
                inc_empl_cntr+=1
            
            line_count+=1

    with open('encoded_'+curr_name+'_dataset.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(encoded_data)
