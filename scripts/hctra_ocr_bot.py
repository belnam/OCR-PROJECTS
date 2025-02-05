"""
OCR script extracting transactions from HCTRA
"""
from pathlib import Path
import os
import re
import pandas as pd
import pdfplumber
from datetime import datetime

def lpsextact():
    try:
        input_path = "input_files//"
        output_path = "output_files//"
        files = os.listdir(input_path)

        for fname in files:
            df = pd.DataFrame()
            output_list = []

            with pdfplumber.open(input_path + fname) as pdf:
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text(x_tolerance=1, y_tolerance=4)

                    # # Extract words with positional data
                    # words = page.extract_words()

                    # # Sort words by vertical position (rows) and horizontal position (columns)
                    # words = sorted(words, key=lambda w: (w['top'], w['x0']))

                    # row_tolerance = 2
                    # column_tolerance = 10

                    # # Group words into rows based on vertical position
                    # rows = []
                    # current_row = []
                    # for word in words:
                    #     if not current_row:
                    #         current_row.append(word)
                    #     else:
                    #         if abs(word['top'] - current_row[-1]['top']) <= row_tolerance:
                    #             current_row.append(word)
                    #         else:
                    #             rows.append(current_row)
                    #             current_row = [word]
                    # if current_row:
                    #     rows.append(current_row)

                    # new_rows = []
                    # # Analyze gaps between words in each row
                    # for row in rows:
                    #     row = sorted(row, key=lambda w: w['x0'])  # Sort words horizontally
                    #     # print(f"\nRow (top={row[0]['top']:.2f}):")
                    #     txt = ""
                    #     new_col = True
                    #     col = []
                    #     for i in range(len(row) - 1):
                    #         gap = row[i + 1]['x0'] - row[i]['x1']
                    #         # print(f"  Word: '{row[i]['text']}' -> '{row[i + 1]['text']}' | Gap: {gap:.2f}")
                    #         if gap > column_tolerance:
                    #             print(f"    ** Exceeds column tolerance ({column_tolerance}) **")
                    #             col.append(txt)
                    #             txt = row[i+1]['text']
                    #         else:
                    #             if new_col:
                    #                 txt += row[i]['text'] + " " + row[i+1]['text']
                    #                 new_col = False
                    #             else:
                    #                 txt += " " + row[i+1]['text']
                    #     new_rows.append(col)

                    # # Convert to DataFrame
                    # df = pd.DataFrame(new_rows)
                    # df.to_excel("test.xlsx", index=False)
                    # break


                    transaction_re = re.findall(r"(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+(\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d{2})\s+(\w+)\s+(\w+)(.*?)((?=SUPPORT|HCTRA-).*)[T]\w+.*[$](.*)(\W+[$]\d+\W+\d+\W)\W(.*)\s+(SERVICES.*)\W+(.*)",page_text)

                    for transaction in transaction_re:
                        rowDict = {
                            'POST DATE/TIME': transaction[0],
                            'TRXN DATE & TIME': transaction[1],
                            'ITEM ID': transaction[2],
                            'ITEM TYPE': transaction[3],
                            'ITEM DESCRIPTION': (transaction[4] + transaction[8]),
                            'LP': transaction[10],
                            'LOCATION': (transaction[5] + transaction[9] + transaction[10]).replace('TX',''),
                            'AMOUNT DUE': transaction[6],
                            'BALANCE': transaction[7],
                            
                        }
                        output_list.append(rowDict)

            # Save data to DataFrame and export to Excel
            df = pd.DataFrame(output_list)
            if not df.empty:
                output_file = str(output_path + fname).replace('.pdf', '') + '.xlsx'
                df.to_excel(output_file, index=False)
                print(f'Processed and saved: {output_file}')
            else:
                print(f'No transactions found in: {fname}')

    except Exception as e:
        print(f"Error: {e}")

lpsextact()
