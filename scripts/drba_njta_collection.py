'''
ocr bot extracting data from drpa njta collection agency
'''

from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass

#creating a dictionary to append data extracted from the pdf
def drpaprocess():
    rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN.DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT#":"", "REFERENCE # OR INVOICE #":"","VIOLATION#":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":""}
    username = getpass.getuser()
    input_path = f"C:\\Users\\{username}\\Documents\\py\\input1_files\\"
    output_path = f"C:\\Users\\{username}\\Documents\\py\\output1_files\\"
    
    files = os.listdir(input_path)
    for fname in files:
        text = ""
        #empty dataframe
        df = pd.DataFrame()
        output_list = []
        with pdfplumber.open(input_path + fname) as pdf:
            for page_number in range(len(pdf.pages)):
                page = pdf.pages[page_number]
                text += page.extract_text()
        with open("test.txt", "w") as file:
            file.write(text)
            # regular expression to extract text
            all_re = re.findall(r"(\w+\W+\d+)\s+\W+(\w+)\W+(\w+)\s+(.*)\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)\s+\W+(\d+\W+\d+)|(\w+\W+\d+)\s+\W+(\w+)\W+(\w+)\s+(.*)\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)\s+(\d+\W+\d+)|(\w+\W+\d+)\s+\W+(\w+)\W+(\w+)\s+([\w\- ]*)\W+(\d{2}\/\d{2}\/\d{2}\W*\d{2}:\d{2}:\d{2})\s{1}[$I1]{1}([\d.]*)\s{1}[$18]{1}([\d.]*)|(\w+\W+\d+)\s+\W+(\w{2})\w(\w{7})\s+([\w\- ]*)\s(\d{2}\/\d{2}\/\d{2}\W*\d{2}:\d{2}:\d{2})\s+\W+(\d+\W+\d+)\s+\W+(\d+\W+\d+)",text)

            for line_data in all_re:
                violation_no = line_data[0]
                lp_state = line_data[1]
                lp = line_data[2]
                exit_lane = line_data[3]
                trxn_date = line_data[4]
                toll_due = float(line_data[5]) if line_data[5] else 0.0
                admin_fee = float(line_data[6]) if line_data[6] else 0.0
                amount_due = toll_due + admin_fee 

                rowDict["VIOLATION#"] = violation_no
                rowDict["LP STATE"] = lp_state
                rowDict["LP"] = lp
                rowDict["EXIT LANE/LOCATION"] = exit_lane
                rowDict["TRXN.DATE & TIME"] = trxn_date
                rowDict["AMOUNT DUE"] = amount_due
                rowDict["TOLL AGENCY"] = "DELAWARE RIVER AND BAY AUTHORITY"
                rowDict["DUE DATE"] = "IMMEDIATELY"

                
                output_list.append(rowDict)
                dff = pd.DataFrame(output_list)
                df = pd.concat([df, dff]) 
                df.drop_duplicates(inplace=True)
    
    
    df.to_excel(str(output_path+ fname).replace('.pdf', '') + '.xlsx', index=False)

drpaprocess()