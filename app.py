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
QTY = int(st.text_input('Please enter the quantity of parts:','100'))
Lot_num = st.text_input('Please enter the lot number','qwe')
OP = st.text_input('Please enter Operator name:','Sina')

st.write("Please start testing, Select 'Done' once you finish:")
if st.button("Done"):
    QTY_of_passed = st.text_input("Please enter the quantity of passed parts:  ",'90')

    QTY_of_failed = st.text_input("Please enter the quantity of failed parts:  ",'10')
    
    QP = int(QTY_of_passed)
    QF = int(QTY_of_failed)

    if (QP + QF) == QTY:    
        st.write(f"There are {QP} available parts to distributing ")
        Distributed = int(st.text_input("Please enter how many parts are distributed?  ",'40'))
        if Distributed <= QP:        
            Balance1 = QP - Distributed
            Balance = Balance1
            print(f"You have {Balance1} parts left as balance ")


    if st.button('Submit'):
        db.put({"a_operator": OP,"b_Lot_num": Lot_num,"c_QTY": QTY,"d_QTY_of_passed": QTY_of_passed,"e_QTY_of_failed": QTY_of_failed,"f_Available": QTY_of_passed,"g_Balance": Balance,"h_time": timestampStr })

#     new_row = pd.Series([timestampStr, chatbot_input, answer], index=df.columns)
#     df = df.append(new_row,ignore_index=True) 
#     df.to_csv('submissions.csv', mode='a', index=False, header=False)





@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False)

db_content = db.fetch().items
df = pd.DataFrame.from_dict(db_content)
df = df.sort_values(by=['h_time'])

df['d_QTY_of_passed'] = df['d_QTY_of_passed'].astype(int)

df['e_QTY_of_failed'] = df['e_QTY_of_failed'].astype(int)

df['f_Available'] = df['f_Available'].astype(int)

passed_sum = df['d_QTY_of_passed'].sum()
failed_sum = df['e_QTY_of_failed'].sum()
avail_sum = df['f_Available'].sum()


# df[4] = df[4].astype(int)
# st.write(df.sum())
csv = convert_df(df)
st.dataframe(df)

col1, col2, col3 = st.columns(3)
col1.metric(label="Sum of Quantity Passed", value=passed_sum)
col2.metric(label="Sum of Quantity Failed", value=failed_sum)
col3.metric(label="Sum of Quantity Available", value=avail_sum)

st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')
