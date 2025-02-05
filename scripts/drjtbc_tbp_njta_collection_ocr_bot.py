'''
ocr bot extracting data from drjtbc toll by plate
'''

#importing required libraries
import re
import pandas as pd
import pdfplumber
import getpass
from collections import namedtuple
import datetime
import os

# Define a named tuple for the row data
rowDict = {"TOLL AGENCY":"","LP":"","LP STATE":"","TRXN.DATE & TIME":"","EXIT LANE/LOCATION":"","ACCOUNT#":"", "REFERENCE # OR INVOICE #":"","VIOLATION#":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":""}

inputdir = f"input_files\\"
outputdir = f"output_files\\"
files = os.listdir(inputdir)
for fname in files:
#empty dataframefiles = os.listdir(input_path)
    for fname in files:
        text = ""
        #empty dataframe
        df = pd.DataFrame()
        output_list = []
        with pdfplumber.open(inputdir + fname) as pdf:
            for page_number in range(len(pdf.pages)):
                page = pdf.pages[page_number]
                text += page.extract_text()
            with open("test.txt", "w") as file:
                file.write(text)

            # regular expression to extract text
            account_re = re.findall(r'Account\s+Number\W+(\d+)',text)
            reference_re = re.findall(r'Toll\s+Bill\s+Number\W+(\w+\d+)',text)
            duedate_re = re.findall(r'\$\d{2}\W+\d{2}\s+\W+[\d.]*\s+\W+[\d.]*\s+\W+[\d.]*\s+(\d+\W+\d+\W+\d+)',text)
            line1_re =  re.findall(r'\W+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\s+\W+\s+(.*)\s+\d+\s+(.*)\s+\W+(\d+\W+\d+)|\W+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\s+\W+\s+(.*)\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\W+\s+(\W+\d+\W+\d+)|\W+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\s+\W+\s+(.*)\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)|\w+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\s+(.*)\s+\d+\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)|\W+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\s+(.*)\s+(\d+\W+\d+\W+\d+\s+\W+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)|\W+(\w+)\W+\s+(\w+)\s+\d+\W+\d+\W+\d+\s+\w+\W+\s+(.*)\s+\d+\s+(\d+\W+\d+\W+\d+\s+\d+\W+\d+\W+\d+)\s+\W+(\d+\W+\d+)', text)

            for match in duedate_re:
                due_date_match = match
                rowDict["DUE DATE"]=due_date_match
            for ref in reference_re:
                reference_no = ref
                rowDict["REFERENCE # OR INVOICE #"] = reference_no
            for acc in account_re:
                account_no = acc
                rowDict["ACCOUNT#"] = account_no
            for line_data in line1_re:
                Lp=line_data[1]
                LPState=line_data[0]
                Trxn_date_time=line_data[3]
                Exit_lane_location=line_data[2]
                Amount_due=line_data[4]

                rowDict["LP"] = Lp
                rowDict["LP STATE"] = LPState
                rowDict["TRXN.DATE & TIME"]= Trxn_date_time
                rowDict["EXIT LANE/LOCATION"]= Exit_lane_location
                rowDict["TOLL AGENCY"] = "DELAWARE RIVER JOINT TOLL BRIDGE COMMISSION (TOLL BY PLATE)"
                rowDict["AMOUNT DUE"] = Amount_due
                output_list.append(rowDict)
                dff = pd.DataFrame(output_list)
                df = pd.concat([df, dff]) 
                df.drop_duplicates(inplace=True)  


    df.to_excel(str(outputdir + fname).replace('.pdf', '') + '.xlsx', index=False)
    










    






            
            
                            
                        