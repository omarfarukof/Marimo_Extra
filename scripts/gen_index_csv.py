import os
import shutil
import marimo_extra as me
import pandas as pd

def gen_index_csv():
    
    index_csv_path = os.path.join("public", "index.csv")
    index_csv = me.record_csv(["notebooks", "apps"], output_csv=index_csv_path, replace=True, output=True)

    index_csv.loc[index_csv['Name'] == 'Penguins', 'Type'] = 'edit'

    index_csv = me.add_row_csv(
        index_csv, 
        ["Home", "index.py", "index.html", "edit", "", ""])


    # index_csv.loc[index_csv['Name'] == 'Penguins', 'Type'] = 'edit'


    me._save_record_csv(index_csv, index_csv_path)
    

if __name__ == "__main__":
    gen_index_csv()



