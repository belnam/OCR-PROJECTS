'''
ocr bot extracting data from deldot toll by plate
 agency
'''
from pathlib import Path 
import os 
import re
import pandas as pd 
import pdfplumber
import getpass 
from datetime import datetime

def deldotpbpprocess(): 
    try:
        username = getpass.getuser() 
        input_path = f"input_files//" 
        output_path = f"output_files//" 
        text = "" 
        files = os.listdir(input_path) 
        for fname in files: 
            crime_fee = 0

            df = pd.DataFrame()
            output_list = [] 
            crime_fee = 0
            due_date = ""

            with pdfplumber.open(input_path + fname) as pdf: 
                page_no =1
                for page in pdf.pages:
                    lines = page.extract_text().split('\n')
                    pre_balance_re = re.findall(r"Pri.*D\w+\s+[$S8;1I3]{1}(\d+\W+\d+)", page.extract_text())
                    for line in lines:
                        text += line + '\n'  
                        # regex expression to extract data from pdf
                        account_re = re.findall(r"Acc\w+.*Nu\w+\W+\s+(\w+)", line) 
                        invoice_re = re.findall(r"In\w+\s+Nu\w+\W+\s+(\w+\W+\w+)|In\w+Nu\w+\W+\s+(\w+\W+\w+)|In\w+Nu\w+\W+(\w+\W+\w+)", line) 
                        license_re = re.findall(r"L\w+\s+P\w+\W+S\w+\W+\s+(\w+)\W+(\w+)", line)
                        due_date_re = re.findall(r"Res.*\s+(\d{2}\W+\d{2}\W+\d{4})", line) 

                        for match in due_date_re:
                            due_date = 0
                            due_date = match         
                            # print(due_date)
                            # print("Page: ", page_no)
                        for acc in account_re:
                            account_no = acc
                        for inv in invoice_re:
                            in_data = []
                            for x in inv:
                                if x != '':
                                    if x.startswith('1-'):  
                                        x = 'I' + x[1:]
                                        in_data.append(x)
                            if in_data:
                                invoice_no = in_data[0]
                            else:
                                invoice_no = "N/A"
                        for line_data in license_re:
                            lp = line_data[0]
                            lp_state = line_data[1].replace('1','1')
                        transaction1_re = re.findall(r"\d+\W+\d+\W+\d+\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\w+\s+\w+\s+(\w+)\s+\W+(.*)|\d+\W+\d+\W+\d+\s+(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+\w+.*\s+(\w+)\s+[$5S38 1I|;]{1}(.*)", line)
                        for trans1 in transaction1_re:
                            trn_data = []
                            for x in trans1:
                                if x  != '':
                                    trn_data.append(x)
                            trxn_date_time = f"{trn_data[0][:10]} {trn_data[0][10:]}"
                            exit_lane = trn_data[1]
                            amount_due = trn_data[2]
                            rowDict = {
                                "TOLL AGENCY": "DELAWARE DEPARTMENT OF TRANSPORTATION (TOLL BY PLATE)",
                                "LP": lp,
                                "LP STATE": lp_state,
                                "TRXN DATE & TIME": trxn_date_time,
                                "EXIT LANE/LOCATION": exit_lane,
                                "ACCOUNT": account_no,
                                "REFERENCE#": "",
                                "VIOLATION": "",
                                "AMOUNT DUE": amount_due,
                                "DUE DATE": due_date,
                                "PIN NO#": "",
                                "INVOICE#": invoice_no,
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": "",
                                "PAGE NO #": page_no
                            }
                            output_list.append(rowDict)
                        transaction2_re = re.findall(r"(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\w+\s+\w+\W+\w+\W+\w+\W+\w+\s+(\w+)\s+[S5$3I1;!]{1}(\d+\W+\d+)\s+[S5$3I1;!]{1}(\d+\W+\d+)\s+[S5$3I1;!]{1}(\d+\W+\d+)|(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\w+\s+\w+\W+\w+\W+\w+\W+\w+\s+(\w+)\s+[S5$3I1;!]{1}(\d+\W+\d+)\s+[S5$3I1;!]{1}(\d+\W+\d+)|(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+\w+\s+\w+\W+\w+\s+\w+\W+\w+\W+\w+\s+(\w+)\s+[$S38I15]{1}(\d+\W+\d+)\s+[$S38I15]{1}(\d+\W+\d+)\s+[$S38I15]{1}(\d+\W+\d+)|(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+\w+\s+\w+\W+\w+\s+\w+\W+\w+\W+\w+\s+(\w+)\s+[$S38I15]{1}(\d+\W+\d+)\s+[$S38I15]{1}(\d+\W+\d+)", line)
                        for trans2 in transaction2_re:
                            rn_data =[]
                            for x in trans2:
                                if x != '':
                                    rn_data.append(x)
                            trxn_date = f"{rn_data[0][:10]} {rn_data[0][10:]}"
                            exit_loc = rn_data[1]
                           
                            rowDict = {
                                "TOLL AGENCY": "DELAWARE DEPARTMENT OF TRANSPORTATION (TOLL BY PLATE)",
                                "LP": lp,
                                "LP STATE": lp_state,
                                "TRXN DATE & TIME": trxn_date,
                                "EXIT LANE/LOCATION": exit_loc,
                                "ACCOUNT": account_no,
                                "REFERENCE#": "",
                                "VIOLATION": "",
                                "DUE DATE": due_date,
                                "PIN NO#": "",
                                "INVOICE#": invoice_no,
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": "",
                                "PAGE NO #": page_no
                            }
                            try:
                                adm_fee = float(rn_data[2].replace(",","."))
                                ambulance_fee = float(rn_data[3])
                                try: 
                                    crime_fee = float(rn_data[4])
                                except:
                                    crime_fee = 0  
                                if crime_fee != 0:
                                    total_amount = adm_fee + ambulance_fee + crime_fee
                                    crime_fee = 0                                        
                                else:
                                    total_amount = adm_fee + ambulance_fee

                                rowDict['AMOUNT DUE'] = total_amount
                            except Exception as e:
                                print(e)
                                pass
                            output_list.append(rowDict)
                    for prev in pre_balance_re:
                        amount_due= prev
                        if amount_due != '0.00':
                            prev_bal_row = {
                                "TOLL AGENCY": "DELAWARE DEPARTMENT OF TRANSPORTATION (TOLL BY PLATE)",
                                "LP": lp,  
                                "LP STATE": lp_state,  
                                "TRXN DATE & TIME": "",
                                "EXIT LANE/LOCATION": "",
                                "ACCOUNT": account_no,
                                "REFERENCE#": "",
                                "VIOLATION": "",
                                "AMOUNT DUE": amount_due,
                                "DUE DATE": due_date, 
                                "PIN NO#": "",
                                "INVOICE#":invoice_no, 
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": "",
                                "PAGE NO #": page_no
                            }
                            output_list.append(prev_bal_row)
                    page_no += 1
                      
            df = pd.DataFrame(output_list) 
            try:
                df['DUE DATE'] = pd.to_datetime(df['DUE DATE'], format='%m/%d/%Y')
                df['DUE DATE'] = df['DUE DATE'].dt.strftime('%m/%d/%Y')
            except Exception as e:
                print(e)
            print('Processing file ' + fname)
            df.to_excel(str(output_path+ fname).replace('.pdf', '') + '.xlsx', index=False) 
            with open("text.txt", "w") as file: 
                file.write(text) 
        return True, df.shape[0]  
    except Exception as e:
        print('error',e)
        return False, 0 
deldotpbpprocess()
