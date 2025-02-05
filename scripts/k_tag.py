# """"
# ocr script extracting k-tag

# """
# from pathlib import Path
# import os
# import re
# import pandas as pd
# import pdfplumber
# import getpass
# from datetime import datetime

# def lpsextact():
#     try:
#         input_path = f"input_files//"
#         output_path = f"output_files//"
#         text =""
#         files = os.listdir(input_path)
#         for fname in files:
#             df = pd.DataFrame()
#             output_list = []
#             with pdfplumber.open(input_path+fname) as pdf:
#                 page_no = 1
#                 for page_number in range (len(pdf.pages)):
#                     page = pdf.pages[page_number]
#                     page_text = page.extract_text()
#                     text += page_text
#                     for line in page_text.split("\n"):

#                         #regex
#                         lp_state_re = re.findall(r"T.*e\s+(\w{2})\W+\w+.*\W+(\w+)\s+\W",line)
#                         # account_re = re.findall(r"ACCOUNT(\w+)|ACCOUNT\s+(\w+)",page_text)
#                         # statement_id_re = re.findall(r"ST.*I\w+\W+(\w+)",page_text)
#                         trans_re = re.findall(r"(\d{2}\W+\d{2}\W+\d{2}\s+\d{2}\W+\d{2}\s+\w{2})\s+(\w+)\s+(\w+)\s+(.*)KTA\s+\d+\s+\w+\s+\W+(\d+\W+\d+)",line)

#                         for lps in lp_state_re:
#                             lp_state = lps[0]                  
#                             lp = lps[1]
#                         # for acc in account_re:
#                         #     rn_data = []
#                         #     for x in acc:
#                         #         if x != "":
#                         #             rn_data.append(x)
#                         #     account = rn_data[0]
#                         for trxn in trans_re:
#                             tn_data = []
#                             for x in trxn:
#                                 if x != "":
#                                     tn_data.append(x)
#                             trx_date_time = tn_data[0]
#                             exit_loc = f"{tn_data[3]} {tn_data[2]} {tn_data[1]}"
#                             amount = tn_data[4]
#                         # for stmt in statement_id_re:
#                         #     statement_id = stmt
#                             rowDict = {
#                                 "AGENCY":"KTA",
#                                 "LP":lp,
#                                 "LP_STATE":lp_state,
#                                 "ACCOUNT":"4698302",
#                                 "STATEMENT ID":"24813667",
#                                 "TRXN DATE/TIME":trx_date_time,
#                                 "EXITLANE": exit_loc,
#                                 "AMOUNT":amount
#                             }
#                             output_list.append(rowDict)
#                 page_no +=1
#             df = pd.DataFrame(output_list) 
#             with open("ktag", "w") as file:
#                 file.write(text)
#             print('Processing file ' + fname)
#             df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
#     except Exception as e:
#         print(e)
# lpsextact()

from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber

def lpsextact():
    try:
        input_path = "input_files//"
        output_path = "output_files//"
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
                    for line in page_text.split("\n"):

                        # regex
                        lp_state_re = re.findall(r"T.*e\s+(\w{2})\W+\w+.*\W+(\w+)\s+\W", line)
                        trans_re = re.findall(
                            r"(\d{2}/\d{2}/\d{2}\d{2}:\d{2}\s+\w{2})\s+(\w+)\s+(\w+)\s+(.*)KTA\s+\d+\s+\w+\s+\W+(\d+\W+\d+)|(\d{2}/\d{2}/\d{4}\W+\d{2}\s+\w+)\s+(\w+)\s+(\w+)\s+(.*)K.*\s+\d+\s+\w+\s+\W+(\d+\W+\d+)",
                            line,
                        )

                        for lps in lp_state_re:
                            lp_state = lps[0]
                            lp = lps[1]

                        for trxn in trans_re:
                            tn_data = []
                            for x in trxn:
                                if x != "":
                                    tn_data.append(x)
                            trx_date_time = tn_data[0]

                            trx_date_time = re.sub(
                                r"(\d{2}/\d{2}/\d{2})(\d{2}:\d{2}\s+\w{2})",
                                r"\1 \2",
                                trx_date_time,
                            )

                            exit_loc = f"{tn_data[3]} {tn_data[2]} {tn_data[1]}"
                            amount = tn_data[4]

                            rowDict = {
                                "AGENCY": "KTA",
                                "LP": lp,
                                "LP_STATE": lp_state,
                                "ACCOUNT": "4698302",
                                "STATEMENT ID": "24813667",
                                "TRXN DATE/TIME": trx_date_time,  
                                "EXITLANE": exit_loc,
                                "AMOUNT": amount,
                            }
                            output_list.append(rowDict)
                page_no += 1
            df = pd.DataFrame(output_list)
            with open("ktag", "w") as file:
                file.write(text)
            print("Processing file " + fname)
            df.to_excel(
                str(output_path + fname).replace(".pdf", "") + ".xlsx", index=False
            )
    except Exception as e:
        print(e)

lpsextact()
