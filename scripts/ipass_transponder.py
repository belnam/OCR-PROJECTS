""""
ocr script extracting express toll transactions

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
                    # for line in page_text.split("\n"):
                    
                        # # REGEX
                        # vehicle_info_re = re.findall(r"(T\w+\W+f\w+\W+D\w+\W+\d+\W+a\w+\W+P\w+\W+\w+)",line)
                        # txn_re = re.findall(r"(\d{10})\W+(\d{2}\W+\d{2}\W+\d{4}\W+\d{2}\W+\d{2}\W+\d{2})\W+(.*)\W+(\w+)\s+(\W+\d+\W+\d+)",line)

                        
                        # for device in vehicle_info_re:
                        #     rowDic = {
                        #         "Transaction No": device,
                        #         "Transaction Date / Time" : "",
                        #         "Location": "",
                        #         "Toll Status*": "",
                        #         "Amount": "",
                        #     }

                        #     output_list.append(rowDic)
               
                        # for txn in txn_re:
                        #     trxn_no = txn[0]
                        #     trxn_date = txn[1]
                        #     loca = txn[2]
                        #     toll = txn[3]
                        #     amt = txn [4]
                        #     rowDic = {
                        #     "Transaction No": trxn_no,
                        #     "Transaction Date / Time" : trxn_date,
                        #     "Location": loca,
                        #     "Toll Status*": toll,
                        #     "Amount": amt,
                        #     }

                        #     output_list.append(rowDic)

            df = pd.DataFrame(output_list) 
            with open("trat.txt", "w") as file:
                file.write(text)
            print('Processing file ' + fname)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)
lpsextact()