from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def nystatebridgeauthority():
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

                    #Regex pattern
                    # due_date_re = re.findall(r"S.*Tot.*D.*(I\w+)",page_text)
                    trxn_re = re.findall(r"(\w{13}\W+\w+)\s+(\w{2})(\w+)\s+(.*)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2})\s+[$5S;!81]{1}(\d+\W+\d+)|(\w{13}\W+\w+)\s+(\w+)\s+(\w+)\s+(.*)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2})\s+[$5S;!81]{1}(\d+\W+\d+)|(\w{13}\W+\w+)\s+(\w{2})(\w+)\s+(.*)\s+(\d+\W+\d+\s+\d+\W+\d+)\s+[$5S;!81]{1}(\d+\W+\d+)",page_text)
                    fee_re = re.findall(r"F.*D\w+\W+(\d+\W+\d+)",page_text)
                    
                    # process
                    index = 0
                    for ln_data in trxn_re:
                        line_data = []
                        for x in ln_data:
                            if x != '':
                                line_data.append(x)
                        violation_no = line_data[0]
                        lp_state = line_data[1]
                        lp = line_data[2]
                        exit_lane = line_data[3]
                        trxn_date_time = line_data[4]

                        # Replace date format in trxn_date_time
                        trxn_date_time = re.sub(r'0(\d{2})(\d{2}/\d{2})', r'\1/\2', trxn_date_time)
                        amount_due = line_data[5].replace(",", ".")
                        for fee in fee_re:
                            fee_due = fee.replace(",",".")
                            print(amount_due,violation_no,lp,fee_due)
                            rowDict = {
                                "TOLL AGENCY": "NEW YORK STATE BRIDGE AUTHORITY",
                                "LP": lp,
                                "LP STATE": lp_state,
                                "TRXN DATE & TIME": trxn_date_time,
                                "EXIT LANE/LOCATION": exit_lane,
                                "ACCOUNT": "",
                                "REFERENCE#": "",
                                "VIOLATION": violation_no,
                                "AMOUNT DUE": "",
                                "DUE DATE": "IMMEDIATELY",
                                "PIN NO#": "",
                                "INVOICE#": "",
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": ""
                            }
                            try:
                                if index == len(trxn_re)-1:
                                    rowDict["AMOUNT DUE"] = float(amount_due) + float(fee_due) 
                                    fee_due = 0    
                                else:
                                    rowDict["AMOUNT DUE"] = float(amount_due)
                            except Exception as e:
                                # Handle the exception here, e.g., print an error message or take appropriate action
                                print("Error occurred while calculating 'AMOUNT DUE':", e)
                        output_list.append(rowDict)
                        index += 1

            # Save data to DataFrame and then to Excel
            df = pd.DataFrame(output_list)
            df.drop_duplicates(inplace=True)
            with open("text.txt", "w") as file:
                file.write(text)
            print(f'Processing file {fname}')
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

nystatebridgeauthority()
