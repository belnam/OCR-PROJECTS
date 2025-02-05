'''ocr bot extracting data from riverlink
 agency'''
from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def riverlinkprocess():
    try:
        username = getpass.getuser()
        input_path = f"input_files//"
        output_path = f"output_files//"
        text = ""
        files = os.listdir(input_path)

        for fname in files:
            df = pd.DataFrame()
            output_list = []
            unique_bills = set()
            unique_accounts = set()
            unique_lps = set()
            lp = ''
            bill_no = ''
            account_no = ''
            due_date = ''
            # Initialize a dictionary to store new_fees for each bill_no
            new_fees_dict = {}

            with pdfplumber.open(input_path + fname) as pdf:
                page_no = 1
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text
                    df = pd.DataFrame(output_list)

                    bill_no_re = re.findall(r"LI\w+.*M\w+.*B\w+.*#\s+(\w+)", page_text)
                    due_date_re = re.findall(r"Tot\w+.*Pa\w+\W+\s+(.*)", page_text)
                    prev_bal_re = re.findall(r"Forac.*\s+Pr.*B\w+\s+[$5S]{1}(\d+\W+\d+)|Lic.*P\w+\W+\w+\s+Pre.*B\w+\s+\W+(\d+\W+\d+)|Forac.*\W+com\s+Pre.*Ba.*[$5S]{1}(\d+\W+\d+)", page_text)
                    account_re = re.findall(r"Bill.*Acc.*nu\w+\W+(\w+)", page_text)
                    license_re = re.findall(r"Bill.*Acc.*nu\w+\W+\w+\s+Li.*Pl\w+\W+IN\W+(\w+)|Bill.*Acc.*nu\w+\W+\w+\s+Li.*Pl\w+\W+(\w+)", page_text)
                    new_fees_re = re.findall(r"Ne.*F\w+\s+[$5S]{1}(\d+\W+\d+)", page_text)
                    new_fees = 0.00
                    for bil in bill_no_re:
                        if bil:
                            bill_no = bil
                            if bill_no not in unique_bills:
                                unique_bills.add(bill_no)
                    for acc in account_re:
                        if acc:
                            account_no = acc
                            if account_no not in unique_accounts:
                                unique_accounts.add(account_no)
                    for match in due_date_re:
                        due_date = match
                    main_fees = []
                    for lic in license_re:
                        for x in lic:
                            if x != '':
                                main_fees.append(x)
                        if lic:
                            if len(main_fees) >= 1:
                                #lp_state = main_fees[0]
                                lp = main_fees[0]
                                if lp not in unique_lps:
                                    unique_lps.add(lp)
                    for fees in new_fees_re:
                        new_fees = fees
                        # if fees != '0.00':
                        #     new_fees_dict[bill_no] = fees

                    # index = 0
                    new_tolls_re = re.findall(r"(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\s+(.*)\s+[$S5]{1}(\d+\W+\d+)", page_text)
                    for tolls in new_tolls_re:
                        trxn_date = f"{tolls[0][:10]} {tolls[0][10:]}"
                        exit_loc = tolls[1]
                        trxn_charges = tolls[2]
                        rowDict = {
                            "TOLL AGENCY": "RIVERLINK",
                            "LP": lp,
                            "LP STATE":"",
                            "TRXN DATE & TIME": trxn_date,
                            "EXIT LANE/LOCATION": exit_loc,
                            "ACCOUNT#": account_no,
                            "REFERENCE#": "",
                            "VIOLATION#": "",
                            "AMOUNT DUE": float(trxn_charges.replace(",",".")),
                            "DUE DATE": due_date,
                            "PIN NO#": "",
                            "INVOICE#": "",
                            "CODE 1#": "",
                            "CODE 2#": "",
                            "BILL NO#": bill_no,
                        }
                        output_list.append(rowDict)
                        # if index == len(new_tolls_re) - 1:
                        #     new_fees = new_fees_dict.get(bill_no, '0.00')  
                        #     rowDict["AMOUNT DUE"] = float(trxn_charges) + float(new_fees)
                        #     new_fees = 0.00
                        # else:
                        #     rowDict["AMOUNT DUE"] = float(trxn_charges)
                        # output_list.append(rowDict)
                        # index += 1
                    for prev in prev_bal_re:
                        rn_data = []
                        for x in prev:
                            if x != '':
                                rn_data.append(x)
                        amount_due = rn_data[0]
                        if amount_due != '0.00':
                            prev_bal_row = {
                                "TOLL AGENCY": "RIVERLINK",
                                "LP": lp,
                                "LP STATE":"",
                                "TRXN DATE & TIME": "",
                                "EXIT LANE/LOCATION": "",
                                "ACCOUNT#": account_no,
                                "REFERENCE#": "",
                                "VIOLATION#": "",
                                "AMOUNT DUE": "",
                                "DUE DATE": due_date,
                                "PIN NO#": "",
                                "INVOICE#": "",
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": bill_no
                            }
                            try: 
                                new_fees= float(fees.replace(",","."))
                                amount_due = float(rn_data[0].replace(",","."))
                            except:
                                new_fees = 0  
                            if new_fees != 0:
                                total_amount = new_fees + amount_due
                                new_fees = 0
                            else:
                                total_amount = amount_due
                            prev_bal_row["AMOUNT DUE"] = total_amount
                            output_list.append(prev_bal_row) 
                            # if new_fees_dict.get(bill_no, '0.00') != '0.00' and not new_tolls_re:
                            #     new_fees = new_fees_dict.get(bill_no, '0.00')  
                            #     prev_bal_row["AMOUNT DUE"] = float(amount_due) + float(new_fees)
                            # else:
                            #     prev_bal_row["AMOUNT DUE"] = float(amount_due)

                            # output_list.append(prev_bal_row)
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
riverlinkprocess()
