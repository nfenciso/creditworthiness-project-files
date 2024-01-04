import numpy as np
import csv
import random

data=[]
with open('original_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    annual_list = []
    bday_list = []
    for row in csv_reader:
        if line_count != 0:
            try:
                annual_list.append(float(row[5]))
                bday_list.append(float(row[10]))
            except:
                pass
        line_count+=1
    median_annual = round(np.median(annual_list))
    mean_bday = round(np.mean(bday_list))

# print(median_annual)
# print(mean_bday)

with open('original_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    new_row=[]
    line_count = 0
    for row in csv_reader:
        # 0 - index in dataset
        # 1 - gender - HAS MISSING
        # 2 - car owner
        # 3 - property owner
        # 4 - children
        # 5 - annual income - HAS MISSING
        # 6 - type income
        # 7 - education
        # 8 - marital status
        # 9 - housing type
        # 10 - birthday count - HAS MISSING
        # 11 - employee days - HAS VALUE PRESUMED EQUIVALENT TO MISSING
        # 12 - mobile phone - EXCLUDE DUE TO ONLY HAVING 1 OBSERVED UNIQUE VALUE IN THE WHOLE DATASET
        # 13 - work phone
        # 14 - phone
        # 15 - email id
        # 16 - type occupation - HAS MISSING
        # 17 - family members
        # 18 - label / output

        #if line_count != 0:
        for i in range(0,len(row)):
            if i == 0:
                if (len(row[i]) == 0):
                    break
                else:
                    new_row.append(row[i])
            elif i == 1:
                if (len(row[i]) == 0):
                    new_row.append("U")
                else:
                    new_row.append(row[i])
            elif i == 5:
                if (len(row[i]) == 0):
                    new_row.append(median_annual)
                else:
                    new_row.append(row[i])
            elif i == 10:
                if (len(row[i]) == 0):
                    new_row.append(mean_bday)
                else:
                    new_row.append(row[i])
            elif i == 12:
                pass
            elif i == 16:
                if (len(row[i]) == 0):
                    # Unknown
                    # Laborers
                    new_row.append(
                            random.choices(
                            [
                            "Core staff",
                            "Cooking staff",
                            "Laborers",
                            "Sales staff",
                            "Accountants",
                            "High skill tech staff",
                            "Managers",
                            "Cleaning staff",
                            "Drivers",
                            "Low-skill Laborers",
                            "IT staff",
                            "Waiters/barmen staff",
                            "Security staff",
                            "Medicine staff",
                            "Private service staff",
                            "HR staff",
                            "Secretaries",
                            "Realty agents"
                            ], 
                            [
                            0.1641509434,
                            0.01981132075,
                            0.2528301887,
                            0.1150943396,
                            0.04150943396,
                            0.06132075472,
                            0.1283018868,
                            0.02075471698,
                            0.08113207547,
                            0.008490566038,
                            0.001886792453,
                            0.004716981132,
                            0.02358490566,
                            0.04716981132,
                            0.01603773585,
                            0.002830188679,
                            0.008490566038,
                            0.001886792453
                            ], k=1)[0]
                    )
                else:
                    new_row.append(row[i])
            else:
                new_row.append(row[i])
        
        data.append(new_row)
        new_row=[]
        line_count += 1

with open('filled_dataset.csv', 'w', newline='') as csv_file:
     writer = csv.writer(csv_file)
     writer.writerows(data)

