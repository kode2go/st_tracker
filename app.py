import streamlit as st
from datetime import datetime
import pandas as pd

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H:%M:%S")

from deta import Deta
# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
db = deta.Base("example-db4_tracker")
# db.put({"name": "test123", "age": 50})

"""
# Welcome to My Tracker App

Tracking the parts test processing

"""
QTY_of_failed = 0
QTY_of_passed = 0
QTY = int(st.text_input('Tracking the parts test processing:',''))
Lot_num = st.text_input('Please enter the lot number','')
OP = st.text_input('Please enter Operator name:','')

QTY_of_passed = st.text_input("Please enter the quantity of passed parts:  ")

QTY_of_failed = st.text_input("Please enter the quantity of failed parts:  ")

QP = int(QTY_of_passed)
QF = int(QTY_of_failed)

if (QP + QF) == QTY:    
    st.write(f"There are {QP} available parts to distributing ")
    Distributed = int(st.text_int("Please enter how many parts are distributed?  "))
    if Distributed <= QP:        
        Balance1 = QP - Distributed
        Balance = Balance1
        print(f"You have {Balance1} parts left as balance ")


db.put({"a_operator": OP,"b_Lot_num": Lot_num,"c_QTY": QTY,"d_QTY_of_passed": QTY_of_passed,"e_QTY_of_failed": QTY_of_failed,"f_Available": Available,"g_Balance": Balance,"h_time": timestampStr })

#     new_row = pd.Series([timestampStr, chatbot_input, answer], index=df.columns)
#     df = df.append(new_row,ignore_index=True) 
#     df.to_csv('submissions.csv', mode='a', index=False, header=False)



@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False)

db_content = db.fetch().items
df = pd.DataFrame.from_dict(db_content)
csv = convert_df(df)
st.dataframe(df)
st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')
