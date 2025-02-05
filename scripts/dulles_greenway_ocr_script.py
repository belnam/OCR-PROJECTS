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
        if i > 0 and ((text[i].isupper() and text[i-1].islower()) or (text[i].isdigit() and text[i-1].isalpha()) or (text[i].isalpha() and text[i-1].isdigit())):
            new_text += " "
        new_text += text[i]
    return new_text
# Creating a dictionary to append data extracted from the pdf
def dullesgreenway():
    try:
        username = getpass.getuser()
        input_path = f"input_files//"
        output_path = f"output_files//"
        text = ""
        files = os.listdir(input_path)
        for fname in files:
            df = pd.DataFrame()
            output_list = []
            lp = ""
            lp_state = ""
            with pdfplumber.open(input_path + fname) as pdf:
                page_no = 1
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text
                    df = pd.DataFrame(output_list)
                    # regex expression
                    account_re = re.findall(r"D.*o.*un\w+.*to\w+\W+(\w+)|Un\w+.*To\w+.*D\w+\W+\s+(\d{8})", page_text)
                    license_re = re.findall(r"Lic.*Pl\w+\W+(\w{2})(\w+)", page_text)
                    due_date_re = re.findall(r"Du.*G\w+\s+D.*D\w+\W+(.*)", page_text)
                    transaction_re = re.findall(r"(\w{1}\d+)\s+(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\w+\s+(.*)\s+[$53S1!;&]{1}(\d+\W+\d+)\s+[$53S1!;&]{1}(\d+\W+\d+)", page_text)
                    for acc in account_re:
                        acc_data = []
                        for x in acc:
                            if x  != '':
                                acc_data.append(x)
                        account_no = acc_data[0]
                    for lic in license_re:
                        lp_state = lic[0]
                        lp = lic[1]
                    for due in due_date_re:
                        due_date = due
                    for trns in transaction_re:
                        reference_no = trns[0]  
                        trxn_date_time = trns[1]
                        exit_plaza = trns[2]
                        toll_charges = trns[3]
                        admin_fee = trns[4]
                        amount_due = float(toll_charges) + float(admin_fee)
                        exit_plaza = separate_and_insert_space(exit_plaza)
                        rowDict = {
                            "TOLL AGENCY": "DULLES GREENWAY",
                            "LP": lp,
                            "LP STATE": lp_state,
                            "TRXN DATE & TIME":trxn_date_time,
                            "EXIT LANE/LOCATION": exit_plaza,
                            "ACCOUNT": account_no,
                            "REFERENCE#": reference_no,
                            "VIOLATION": "",
                            "AMOUNT DUE": amount_due,
                            "DUE DATE": due_date,
                            "PIN NO#": "",
                            "INVOICE#": "",
                            "CODE 1#": "",
                            "CODE 2#": "",
                            "BILL NO#": ""
                        } 
                        output_list.append(rowDict) 
                page_no += 1
             # Save data to DataFrame and then to Excel
            df = pd.DataFrame(output_list)
            df.drop_duplicates(inplace=True)
            with open("text.txt", "w") as file:
                file.write(text)
            print(f'Processing file {fname}')
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

dullesgreenway()