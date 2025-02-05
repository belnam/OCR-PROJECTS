"""
ocr bot extracting lps from pdf
"""

from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def lpsextact():
    try:
        input_path = f"input_files//"
        output_path = f"output_files//"
        text =""
        files = os.listdir(input_path)
        for fname in files:
            df = pd.DataFrame()
            output_list = []
            with pdfplumber.open(input_path+fname) as pdf:
                page_no = 1
                for page_number in range (len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text
                    
                    # REGEX
                    acc_re = re.findall(r"Acc\w+.*Nu\w+\W+(\w+)\s+N",page_text)
                    transaction_re = re.findall(r"(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+(\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+\s+\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\W+\d+\W+\d+)\s+(\W+\d+\W+\d+)\s+(\W+\d+\W+\d+)\s+(\W+\d+\W+\d+)",page_text)

                    for acc in acc_re:
                        account_no = acc
                    for trans in transaction_re:
                        trxn_date = trans[0]
                        transponder = trans[1]
                        lp = trans[2]
                        lp_state = trans[3]
                        agen_pla = trans[4]
                        plaza_id = trans[5]
                        cit = trans[6]
                        seq = trans[7]
                        det = trans[8]
                        recv  =trans[9]
                        rec = trans[10]
                        cit_lev = trans[11]
                        amt_due = trans[12]
                        amt_pd = trans[13]
                        amt_dis = trans[14]
                        amount_due = trans[15]
                        rowDict = {
                            "TOLL AGENCY":"MTA B&T",
                            "Tx Date Tx Time": trxn_date,
                            "Device #": transponder,
                            "Plate #": lp,
                            "Plate state": lp_state,
                            "Plaza agency": agen_pla,
                            "lane ID": plaza_id,
                            "Citation #": cit,
                            "Seq #": seq,
                            "Detail Status": det,
                            "Recv Status":recv,
                            "Recv Type":rec,
                            "Citation Level":cit_lev,
                            "Amount Due":amt_due,
                            "Amount Paid": amt_pd,
                            "Amount Dismissed": amt_dis,
                            "Balance Due": amount_due,
                            "Page No": page_no

                        }
                        output_list.append(rowDict)
                        
                    page_no +=1
            df = pd.DataFrame(output_list) 
            with open("tezt.txt", "w") as file:
                file.write(text)
            print('Processing file ' + fname)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)
lpsextact()