'''
ocr bot extracting data from bcbc agency
'''
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

#creating a dictionary to append data extracted from the pdf
def bcbcprocess():
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
                    # regex 
                    admin_fee_re = re.findall(r"Ad.*Fee\s[$5S]{1}(\d+\W+\d+)\s+A|Ad.*Fee\s[$5S]{1}(\d+\W+\d+)\s+\W+",page_text)
                    due_date_re = re.findall(r"E.*cal.*Pay.*\W+(\d{2}\W+\d{2}\W\d{4})|Pay.*due.*(\d{2}\W+\d{2}\W+\d{4})",page_text)
                    for adm in admin_fee_re:
                        rn_data =[]
                        for x in adm:
                            if x != '':
                                rn_data.append(x)
                        admin_fee = rn_data[0]
                    for match in due_date_re:
                        ai_data = []
                        for x in match:
                            if x != '':
                                ai_data.append(x)
                        due_date = ai_data[0]
                    index = 0
                    line_re = re.findall(r"(\w+\W+\d+)\s+\W+(\w+)\W+(\w+)\s+(.*)\s+(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\W+\d{2}).*[$S5i;]{1}(\d+\W+\d+)",page_text) 
                    for line_data in line_re:
                        violation_no = line_data[0]
                        lp_state = line_data[1]
                        lp = line_data[2]
                        exit_lane = line_data[3].replace('Taconv', ' Tacony')
                        trxn_date = line_data[4]
                        amount_due = line_data[5]
                        exit_lane = separate_and_insert_space(exit_lane)  
                        rowDict = {
                            "TOLL AGENCY": "BURLINGTON COUNTY BRIDGE COMMISSION",
                            "LP": lp,
                            "LP STATE": lp_state,
                            "TRXN DATE & TIME": trxn_date,
                            "EXIT LANE/LOCATION": exit_lane,
                            "ACCOUNT": "",
                            "REFERENCE#": "",
                            "VIOLATION": violation_no,
                            "AMOUNT DUE":"",
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
            df['DUE DATE'] = pd.to_datetime(df['DUE DATE'], format='%m/%d/%Y')
            df['DUE DATE'] = df['DUE DATE'].dt.strftime('%m/%d/%Y')
            with open("text.txt", "w") as file:
                file.write(text)
            print('Processing file ' + fname)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

bcbcprocess()
