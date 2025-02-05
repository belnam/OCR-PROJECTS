from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def separate_and_insert_space(text):
    new_text = ""
    for i in range(len(text)):
        if i > 0 and text[i].isupper() and text[i-1].islower():
            new_text += " "
        new_text += text[i]
    return new_text

def insert_hyphen(input_str):
    if len(input_str) < 2:
        return input_str  
    modified_str = input_str[:-2] + '-' + input_str[-2:]
    return modified_str

# Creating a dictionary to append data extracted from the pdf
def atlanticprocess():
    try:
        username = getpass.getuser()
        input_path = f"input_files//"
        output_path = f"output_files//"
        text = ""
        files = os.listdir(input_path)
        for fname in files:
            df = pd.DataFrame()
            output_list = []
            with pdfplumber.open(input_path + fname) as pdf:
                page_no = 1
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text
                    df = pd.DataFrame(output_list)
                    # regex expression
                    due_date_re = re.findall(r"Pay.*due.*(\d{2}\W+\d{2}\W+\d{4})|Pay.*Due(\w+)", page_text)
                    admin_fee_re = re.findall(r"Ad.*Fee\s[$5S>]{1}(\d+\W+\d+)", page_text)
                    
                    for adm in admin_fee_re:
                        admin_fee = adm
                    for match in due_date_re:
                        ai_data = []
                        for x in match:
                            if x != '':
                                ai_data.append(x)
                        due_date = ai_data[0].replace("I", "1").replace("1mmediately", "Immediately")
                    index = 0
                    line_re = re.findall(r"(\w{13}\W+\d{2})\s+\W+(\w+)\W+(\w+)\s+(\w+.*\d+)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\W+\d{2})\s+[S$�!;5>1i38]{1}(\d+\W+\d+)|(\w{13}\W+\d{2})\s+\W+(\w+)\W+(\w+)\s+(\w+\s\d+)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\W+\d{2})\s+[S$�!;5>1i38]{1}(\w+)|(\w{13}\W+\d{2})\s+\W+(\w+)\W+(\w+)\s+(\w+.*\d+)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\W+\d{2})\s+(\d+\W+\d+)|(\w{15})\s+\W+(\w+)\W+(\w+)\s+(\w+\s+\d+)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\W+\d{2})\s+[S$�!;5>1i38](\d+\W+\d+)|(\w{13}\W+\d+)\s+\w{1}(\w+)\W+(\w+)\s+(\w+\s+\d+)\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+[S$�!;5>1i38]{1}(\d+\W+\d+)", page_text)
                    for ln_data in line_re:
                        line_data = []
                        for x in ln_data:
                            if x != '':
                                line_data.append(x)
                        violation_no = insert_hyphen(line_data[0]).replace("--","-").replace("- -","-")
                        lp_state = line_data[1]
                        lp = line_data[2]
                        exit_lane = line_data[3]
                        trxn_date = line_data[4]
                        amount_due = line_data[5].replace("Z55", "2.55").replace("075", "0.75").replace("140", "1.40").replace(",", ".")
                        print(amount_due,admin_fee, lp, lp_state, violation_no, trxn_date)

                        exit_lane = separate_and_insert_space(exit_lane) 
                        rowDict = {
                            "TOLL AGENCY": "ATLANTIC CITY EXPRESSWAY",
                            "LP": lp,
                            "LP STATE": lp_state,
                            "TRXN DATE & TIME": trxn_date,
                            "EXIT LANE/LOCATION": exit_lane,
                            "ACCOUNT": "",
                            "REFERENCE#": "",
                            "VIOLATION": violation_no,
                            "AMOUNT DUE": "",
                            "DUE DATE": due_date,
                            "PIN NO#": "",
                            "INVOICE#": "",
                            "CODE 1#": "",
                            "CODE 2#": "",
                            "BILL NO#": "",
                        }
                        if index == len(line_re) - 1:  
                            rowDict["AMOUNT DUE"] = float(amount_due) + float(admin_fee)
                            admin_fee = 0.00
                        else:
                            rowDict["AMOUNT DUE"] = float(amount_due)
                        output_list.append(rowDict)
                        index += 1 
                page_no += 1
            df = pd.DataFrame(output_list) 
            # df['DUE DATE'] = pd.to_datetime(df['DUE DATE'], format='%m/%d/%Y')
            # df['DUE DATE'] = df['DUE DATE'].dt.strftime('%m/%d/%Y')
            with open("text.txt", "w") as file:
                file.write(text)
            print('Processing file ' + fname)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

atlanticprocess()
