'''
ocr bot extracting data from atlantic city express njta collection agency
'''

from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass

#creating a dictionary to append data extracted from the pdf
def atlanticprocess():
    rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN.DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT#":"", "REFERENCE # OR INVOICE #":"","VIOLATION#":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":""}
    username = getpass.getuser()
    input_path = f"C:\\Users\\{username}\\Documents\\py\\input4_files\\"
    output_path = f"C:\\Users\\{username}\\Documents\\py\\output4_files\\"
    
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
            # reGEX to extract data from pdf

            line_re = re.findall(r"(\w+\W+\d+)\s+\W+(\w+)\W+(\w+)\s+(.*)\s+((\d{2}\/\d{2}\/\d{2}\W*\d{2}:\d{2}:\d{2}))\s+(\w+)",text)
            for line_data in line_re:
                violation_no = line_data[0]
                lp_state = line_data[1]
                lp = line_data[2]
                exit_lane = line_data[3]
                trxn_date = line_data[4]
                amount_due = line_data[5]

                rowDict["VIOLATION#"] = violation_no
                rowDict["LP STATE"] = lp_state
                rowDict["LP"] = lp
                rowDict["EXIT LANE/LOCATION"] = exit_lane
                rowDict["TRXN.DATE & TIME"] = trxn_date
                rowDict["AMOUNT DUE"] = amount_due
                rowDict["TOLL AGENCY"] = "ATLANTIC CITY EXPRESSWAY"
                rowDict["DUE DATE"] = "IMMEDIATELY"

                output_list.append(rowDict)
                dff = pd.DataFrame(output_list)
                df = pd.concat([df, dff]) 
                df.drop_duplicates(inplace=True)
    
    
    df.to_excel(str(output_path+ fname).replace('.pdf', '') + '.xlsx', index=False)


atlanticprocess()