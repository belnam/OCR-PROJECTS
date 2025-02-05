'''
ocr bot extracting data from drpa  new jersey , deldot llp agency
'''

from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

#creating a dictionary to append data extracted from the pdf
def drpaprocess():
    # rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN.DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT#":"", "REFERENCE # OR INVOICE #":"","VIOLATION#":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":""}
    username = getpass.getuser()
    input_path = f"input_files//"
    output_path = f"output_files//"
    
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
            reference_re = re.findall(r"Reference#\W+(\w+)",text)
            line1_re = re.findall(r"(\w+)\s+(\w+\W+\d+)\s+(\d+\W+\d+\W+\d+)\s+\w+\s+\d+\W+\d+\s+\d+\W+\d+\s+(\d+\W+\d+)",text)
            line2_re = re.findall(r"(\w+)\s+(\d+\W+\d+\W+\d+)\s+(\w+)\s+\W+\d+\W+\d+\s+\W+\d+\W+\d+\s+\W+\d+\W+\d+\d+\W+\d+\W+\d+\s+\W+\d+\W+\d+\s+\W+\d+\W+\d+\s+\W+(\d+\W+\d+)",text)
            plate_re = re.findall(r"Philadelphia\W+PA19103\s+(\w{7})(\w{2})",text)
            if line1_re:
                for line_data in line1_re:
                    Lp = line_data[0]
                    violation_id = line_data[1].replace(".","-")
                    trxn_date = line_data[2]
                    amount_due = line_data[3]
                    rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT":"", "REFERENCE#":"","VIOLATION":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":"","INVOICE#":"","CODE 1#":"","CODE 2#":"","BILL NO#":""}
                    rowDict["LP"] = Lp
                    rowDict["VIOLATION"] = violation_id
                    rowDict["TRXN DATE & TIME"] = trxn_date
                    rowDict["AMOUNT DUE"] = amount_due
                    rowDict["TOLL AGENCY"] = "NEW JERSEY TURNPIKE AUTHORITY (LINEBARGER GOGGAN BLAIR & SAMPSON)"
                    rowDict["LP STATE"] =  "IN"
                    rowDict["DUE DATE"] = "IMMEDIATELY"

                    output_list.append(rowDict)
                    dff = pd.DataFrame(output_list)
                    df = pd.concat([df, dff]) 
                    df.drop_duplicates(inplace=True) 
                for ref in reference_re:
                    reference_no = ref
                    rowDict["REFERENCE#"] = reference_no
            
               

            if line2_re:     
                for line1_data in line2_re:
                    violation_id = line1_data[0]
                    trxn_date = line1_data[1]
                    exit_location = line1_data[2]
                    amount_due = line1_data[3]
                    rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT":"", "REFERENCE#":"","VIOLATION":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":"","INVOICE#":"","CODE 1#":"","CODE 2#":"","BILL NO#":""}
                    rowDict["VIOLATION"] = violation_id
                    rowDict["TRXN DATE & TIME"] = trxn_date
                    rowDict["AMOUNT DUE"] = amount_due
                    rowDict["EXIT LANE/LOCATION"] = exit_location
                    rowDict["DUE DATE"] = "IMMEDIATELY"
                    rowDict["TOLL AGENCY"]= "DELAWARE DEPARTMENT OF TRANSPORTATION (LINEBARGER GOGGAN BLAIR & SAMPSON)"
                for plate in plate_re:
                    Lp = plate[0]
                    Lp_State = plate[1]
                    rowDict["LP"] = Lp
                    rowDict["LP STATE"] = Lp_State

                    output_list.append(rowDict)
                    dff = pd.DataFrame(output_list)
                    df = pd.concat([df, dff]) 
                    df.drop_duplicates(inplace=True)

                else:
                    pass
        with open("test.txt", "w") as file:
            file.write(text)       
        df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False) 
    

drpaprocess()