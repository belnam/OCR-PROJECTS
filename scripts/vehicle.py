""""
ocr script extracting lp and transponders

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
                    transponder_re = re.findall(r"(\w+\s+\w+\s+\w+)\s+(\d{3})\s+(\w+)\s+(\w{8})\s+(.*)\s+(\d{3})",page_text)
                    
                    
                    for trans in transponder_re:
                        issu_auth = trans[0]
                        tag = trans[1]
                        number = trans [2]
                        style = trans[3]
                        status = trans[4]
                        class_tag = trans[5]
                        rowDict = {
                            "Issuing Authority":issu_auth,
                            "Tag":tag,
                            "Number":number,
                            "Style":style,
                            "Status":status,
                            "Class Tag Group":class_tag,
                            "Page_No": page_no
                        }
                        output_list.append(rowDict)
                        
                    lp_info_re = re.findall(r"(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d{4})\s+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})|(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d{4})(\s+)(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})",page_text)
                    for lpinfo in lp_info_re:
                        rn_data = []
                        for x in lpinfo:
                            if x != "":
                                rn_data.append(x)
                        lp =rn_data[0]
                        state = rn_data[1]
                        make = rn_data[2]
                        model = rn_data[3]
                        year = rn_data[4]
                        color =rn_data[5]
                        start_date = rn_data[6]
                        rowDict1 ={
                            "License Plate":lp,
                            "State":state,
                            "Make": make,
                            "Model":model,
                            "Year": year,
                            "Color": color,
                            "Start Date":start_date,
                            "Page_No": page_no

                        }
                        output_list.append(rowDict1)
                    page_no +=1
            df = pd.DataFrame(output_list) 
            with open("tezt.txt", "w") as file:
                file.write(text)
            print('Processing file ' + fname)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)
lpsextact()