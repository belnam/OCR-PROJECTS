from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def deldotprocess():
    try:
        username = getpass.getuser()
        input_path = "input_files//"
        output_path = "output_files//"
        text = ""

        files = os.listdir(input_path)
        for fname in files:
            output_list = []
            with pdfplumber.open(input_path + fname) as pdf:
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text if page_text else ""

                    # Initialize lists to hold matched data
                    license_plate_re = re.findall(r"Li\w+.*Pl\w+\:\W+(\w+)(.*)|License Plate\W+State\W+(\w+)\W+(\w{2})|Plate\W+(\w+)\s+(\w+)", page_text)
                    exit_lane_re = re.findall(r"Pl\w+\W+(\w+)\W+La\w+\W+(\w+)", page_text)
                    trxn_date_time_re = re.findall(r"Da\w+\W+(\w+\W+\w+\W+\w+)\W+Tim\w+\W+(\w+\W+\w+\W+\d+)|Date\W+\s+(\d{2}\W+\d{2}\W+\d{4})\s+T\w+\W+\s+(.*)", page_text)
                    due_date_re = re.findall(r"PA\w+\W+(\d+\W+\d+\W+\d+)|PA\w+\W+D\w+\W+B\w+\W+(\d+\W+\d+\W+\d+)|PA\w+\W+D\w+\w+\W+(\d+\W+\d+\W+\d+)|PA\w+\w+\W+B\w+\W+(\d+\W+\d+\W+\d+)", page_text)
                    violation_no_re = re.findall(r"FORVIOLATION(\w+\W+\w+)|F\w+\W+VIOLATION(\w+\W+\w+)|FO\w+\W+V\w+\W+(\w+\W+\w+)|F\w+VIO\w+\W+(\w+\W+\w+)", page_text)
                    amount_due_re = re.findall(r"BALANCE.*DUE\W+(.*)|BAL\w+\D\w+\W+\s+[$S |8Ii]{1}\s+(\d{2}\W+\d{2})", page_text)

                    # Process extracted data
                    date_time = ''
                    for match in trxn_date_time_re:
                        date_time = match[0].replace('I', '1') + ' ' + match[1].replace('I', '1') if match[0] and match[1] else ''

                    exit_location = ''
                    for loc in exit_lane_re:
                        exit_location = loc[0] + ' ' + loc[1] if len(loc) == 2 else loc[0]

                    lp, lp_state = '', ''
                    for lic in license_plate_re:
                        lin = [x for x in lic if x]
                        if len(lin) >= 2:
                            lp = lin[0].replace('I', '1')
                            lp_state = lin[1].replace('FN', 'IN').replace('ID J', 'ID')

                    due_date = ''
                    for dat in due_date_re:
                        due_date = ''.join(dat) if dat else ''

                    violation_no = ''
                    for ref in violation_no_re:
                        violation_no = ''.join(ref)

                    amount_due = ''
                    for amt in amount_due_re:
                        amount_due = ''.join(amt).replace(",", ".").replace("S", "").replace(" ", "") if amt else ''

                    # Append to the list if all necessary data is present
                    if date_time and exit_location and lp and lp_state and due_date and amount_due and violation_no:
                        rowDict = {
                            "TOLL AGENCY": "DELAWARE DEPARTMENT OF TRANSPORTATION",
                            "LP": lp,
                            "LP STATE": lp_state,
                            "TRXN DATE & TIME": date_time,
                            "EXIT LANE/LOCATION": exit_location,
                            "ACCOUNT": "",
                            "REFERENCE#": "",
                            "VIOLATION": violation_no,
                            "AMOUNT DUE": amount_due,
                            "DUE DATE": due_date,
                            "PIN NO#": "",
                            "INVOICE#": "",
                            "CODE 1#": "",
                            "CODE 2#": "",
                            "BILL NO#": ""
                        }
                        output_list.append(rowDict)

            # Save data to DataFrame and then to Excel
            df = pd.DataFrame(output_list)
            df.drop_duplicates(inplace=True)
            with open("text.txt", "w") as file:
                file.write(text)
            print(f'Processing file {fname}')
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

deldotprocess()
