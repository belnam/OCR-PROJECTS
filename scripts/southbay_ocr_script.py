from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
import getpass
from datetime import datetime

def separate_and_insert_space(text):
    new_text = ""
    for i in range(len(text)):
        if i > 0 and text[i].isupper() and text[i-1].islower():
            new_text += " "
        new_text += text[i]
    return new_text

def deldotprocess():
    try:
        username = getpass.getuser()
        input_path = "input_files//"
        output_path = "output_files//"
        text = ""

        files = os.listdir(input_path)
        for fname in files:
            output_list = []
            with pdfplumber.open(input_path + fname) as pdf:
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text if page_text else ""

                    #Regex pattern
                    reference_re = re.findall(r"(\d{10})\s+(\w+)\s+(\w+)\s+AM",page_text)
                    due_date_re = re.findall(r"\W+\d+\W+\d+\s+(\d{2}\W+\d{2}\W+\d{4})",page_text)
                    transaction_re = re.findall(r"(\w{9})\s+(\d{4}\W+\d{2}\W+\d{2}\d{2}\W+\d{2}\W+\d{2})\s+(.*)\s+[$S5I;83]{1}(\d+\W+\d+)\s+[$S5I;83]{1}(\d+\W+\d+)\s+[$S5I;83]{1}\d+\W+\d+",page_text)
                    #process
                    for match in due_date_re:
                        due_date = match
                    for ref in reference_re:
                        reference_no = ref[0]
                        lp = ref[1]
                        lp_state = ref[2]
                    for trns in transaction_re:
                        violation_no = trns[0]
                        # trxn_date_time  = f"{trns[1][:10]} {trns[1][10:]}"
                        trxn_date_time = trns[1]
                        print(trxn_date_time)
                        exit_lane = trns[2].replace("OlayMainlineTollPlaza","OtayMainlineTollPlaza SB").replace("OtayMainlineTollPlaza","OtayMainlineTollPlaza SB")
                        tot_due = trns[3]
                        fine_due = trns[4]
            # Save data to DataFrame and then to Excel
            # df = pd.DataFrame(output_list)
            # df.drop_duplicates(inplace=True)
            with open("text.txt", "w") as file:
                file.write(text)
            print(f'Processing file {fname}')
            # df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
    except Exception as e:
        print(e)

deldotprocess()