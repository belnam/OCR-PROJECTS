'''
ocr bot extracting data from pay by plate ma agency
'''
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

def paybyplatemaprocess():
    try:
        username = getpass.getuser()
        input_path = f"input_files//"
        output_path = f"output_files//"
        files = os.listdir(input_path)
        for fname in files:
            text = "" 
            output_list = []  
            due_date = ""  
            non_ma_fee = 0  
            invoice_fee = 0  
            lp = ""  
            lp_state = ""
            invoice_no = ""  
            
            with pdfplumber.open(input_path + fname) as pdf:
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text

                    # Regex expressions to extract data from pdf
                    license_re = re.findall(r"License Plate\W+(\w+) Inv|Lic\w+.*Pl\w+\W+(\w+\d+)|Lic\w+.*Pl\w+\W+(\w+\W+\d+)",page_text)
                    state_re = re.findall(r"LicensePlateState\W+(\w+)|Lic\w+\W+Pl\w+\W+St\w+\W+(\w+)|License Plate State\W+(\w+) Inv| License Plate State\W+(\w+)",page_text)
                    invoice_re = re.findall(r"InvoiceNumber\W+(\w+)|In\w+\W+N\w+\W+(.*)[ ]|\woice\WNumber\W*(\d*)|Inv.*N\w+r(\w+)", page_text)
                    PreviousBal_re = re.findall(r"\$(\d+\.\d+[\)]*)\W+(\d+\.\d+)\W+(\d+\W+\w+)\W+(\d+\W+\d+)\W+(\d+\W+\d+)\W+(\d+\W+\d+\W+\d+|Immediately)|\$(\d+\.\d+[\)]*)\W+(\d+\.\d+)\W+(\d+\W+\w+)\W+(\d+\W+\d+)\W+(\d+\W+\d+)\W+(\d+\W+\d+\W+\d+|Immediately)\n", page_text)
                    invoice_fee_re = re.findall(r"InvoiceFee\s+\d+\W+\d+\W+\w+\W+\d+\W+\d+\s+[$81SIi]{1}(\d+\W+\d+)|I\w+\W*Fee\W*\d{2}\W*\d{2}\W*\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*(\d\W*\d*)|Invoice\W*Fee\W*\d{2}\W*\d{2}\W*\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*(\d\W*\d*)", page_text)
                    non_ma_fee_re = re.findall(r"NonMAFee\s+\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2}\s+[$| S81iI]{1}(\d+\W+\d+)", page_text)
                    for prev_bal_data in PreviousBal_re:
                        due_date = prev_bal_data[5]
                    for inv in invoice_re:
                        invoice_no = ''.join(inv).replace('S','9')
                    main_fees = []
                    for fee in invoice_fee_re:
                        for x in fee:
                            if x != '':
                                main_fees.append(x)
                        invoice_fee = main_fees[0] 
                    
                    for non in non_ma_fee_re:
                        non_ma_fee = non
                    index = 0
                    line_re = re.findall(r"PLATEMA\s+(.*)\W+(\w+)\s+\w+\W+\w+\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+\d+\s+[$8S5iI1| ]{1}(\d+\W+\d+)|PLATEMA\s+(.*)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+\d+\s+[$S58II| ]{1}(\d+\W+\d+)|LateFee\W+\w+\W+\s+(.*)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+\d+\s+[$S85| 1iI]{1}(\d+\W+\d+)|NOLFee\s+(.*)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+\d+\s+[$SI5| 8i]{1}(\d+\W+\d+)|PaymentFee\s+(.*)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+\d+\s+[$8S5I| ;]{1}(\d+\W+\d+)|TMA\s+(\w+)\W+(\w+)\W+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(.*)\s+[$SI851| ;]{1}(\d+\W+\d+)|PLATEMA\s+(\w+)\W+(\w+)\s+\W+\w+\W+\w+\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\W+(\w+\W+\w+\s+\w+)\W+\w+\W+\w+\W\s+[$8S5I| ;]{1}(\d+\W+\d+)|efs\W+(\w+)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(\w+\W+\w+\s+\w+)\s+[5$8SI| ;]{1}(\d+\W+\d+)|PLATEMA\s+(\w+)\W+(\w+)\s+\w+\W+\w+\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(\w+\W+\w+\s+\w+)\s+[5$8SI| ;]{1}(\w+\W+\w+)|PLATEMA\s+(\w+)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(\w+\W+\w+\s+\w+)\s+[$SI851| ;]{1}(\w+\W+\w+)|L\w+Fee\W+\w+\W+\s+(\w+)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})(\w+\W+\w+\s+\w+)\s+[$SI851| ;]{1}(\d+\W+\d+)|Feefs\W+(\w+)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\d{2})\s+(\w+\W+\w+\s+\w+)\s+[$SI851| ;](\d+\W+\d+)|Feefs\W+(\w+)\W+(\w+)\s+(\d{2}\W+\d{2}\W+\d{4}\d{2}\W+\d{2}\W+\w{2})(\w+\W+\w+\s+\w+)\s+[$SI851| ;]{1}(\d+\W+\d+)", page_text)
                   # print(line_re)
                    for ln_data in line_re:
                        line_data = []
                        for x in ln_data:
                            if x != '':
                                line_data.append(x)
                        lp_state = line_data[0].replace('ID-','ID').replace('(D','ID').replace('ID(cid:127)','ID').replace('(D-','ID').replace('ID-','ID').replace('IN-','IN').replace('(N','IN').replace('IN(cid:127)','IN').replace('tN-','IN')
                        lp = line_data[1]
                        trxn_date_time = f"{line_data[2][:10]} {line_data[2][10:]}"
                        exit_location = line_data[3].replace('Chariton', 'Charlton').replace('Chartton', 'Charlton').replace('Wiltiams', 'Williams')
                        trxn_charges = line_data[4].replace(',', '.').replace('1 -.00','1.00').replace('420\n03','4.20').replace('225\n03','2.25').replace('5^ 90','5.90').replace('3* 10','3.10')
                        exit_location = separate_and_insert_space(exit_location)
                        rowDict = {
                            "TOLL AGENCY": "PAY BY PLATE MA",
                            "LP": lp,
                            "LP STATE": lp_state,
                            "TRXN DATE & TIME":trxn_date_time,
                            "EXIT LANE/LOCATION": exit_location,
                            "ACCOUNT#": "",
                            "REFERENCE#": "",
                            "VIOLATION#": "",
                            "AMOUNT DUE": "",
                            "DUE DATE": due_date.upper(),
                            "PIN NO#": "",
                            "INVOICE#": invoice_no,
                            "CODE 1#": "",
                            "CODE 2#": "",
                            "BILL NO#": ""
                        }  
                        print(trxn_date_time,lp,trxn_charges)
                        try:
                            if index == len(line_re)-1:
                                rowDict["AMOUNT DUE"] = float(trxn_charges) + float(non_ma_fee) + float(invoice_fee)
                                non_ma_fee = 0  
                                invoice_fee = 0  
                            else:
                                rowDict["AMOUNT DUE"] = float(trxn_charges)
                        except Exception as e:
                            # Handle the exception here, e.g., print an error message or take appropriate action
                            print("Error occurred while calculating 'AMOUNT DUE':", e)
                        output_list.append(rowDict)
                        index += 1
                    for lic in license_re:
                        licence_plate = ''.join(lic) 
                    for sta  in state_re:
                        state = ''.join(sta).replace('TNS','TN5')
                    for prev_bal_data in PreviousBal_re:
                        amount_str = prev_bal_data[0]
                        if ')' in amount_str:
                            amount_str = amount_str.replace(')', '')
                            amount_due = -float(amount_str)
                        else:
                            amount_due = float(amount_str)
                        if amount_due != 0.00:
                            prev_bal_row = {
                                "TOLL AGENCY": "PAY BY PLATE MA",
                                "LP": licence_plate,  
                                "LP STATE": state,  
                                "TRXN DATE & TIME": "",
                                "EXIT LANE/LOCATION": "",
                                "ACCOUNT#": "",
                                "REFERENCE#": "",
                                "VIOLATION#": "",
                                "AMOUNT DUE": amount_due,
                                "DUE DATE": prev_bal_data[5].upper(),  
                                "PIN NO#": "",
                                "INVOICE#": invoice_no,  
                                "CODE 1#": "",
                                "CODE 2#": "",
                                "BILL NO#": ""
                            }
                            output_list.append(prev_bal_row)

            with open("text.txt", "w") as file:
                    file.write(text)       
            df = pd.DataFrame(output_list)
            df.to_excel(str(output_path + fname).replace('.pdf', '') + '.xlsx', index=False)
            print('Processing file ' + fname)
        return True, df.shape[0]
    except Exception as e:
        print(e)
        return False, 0
paybyplatemaprocess()

