import openai
import streamlit as st
from datetime import datetime
import pandas as pd

openai.api_key = st.secrets["api_secret"]
df = pd.DataFrame(columns=['Timestamp', 'Question', 'Response'])


from deta import Deta
# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
db = deta.Base("example-db3")
# db.put({"name": "test123", "age": 50})

"""
# Welcome to My Hospital Chatbot!

Feel free to ask any questions below:

"""

chatbot_input = st.text_input('Ask a question?','What is an angiogram?')
chatbot_input = chatbot_input + '?'

if st.button('Submit'):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H:%M:%S")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=chatbot_input,
        temperature=0.5
    )

    answer = response["choices"][0]["text"]
    st.write(answer)
    print(answer)
    db.put({"a_time_stamp": timestampStr,"b_input": chatbot_input,"c_answer": answer })

#     new_row = pd.Series([timestampStr, chatbot_input, answer], index=df.columns)
#     df = df.append(new_row,ignore_index=True) 
#     df.to_csv('submissions.csv', mode='a', index=False, header=False)

admin_input = st.text_input('Admin','Admin')

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False)

if st.button('Display') and admin_input == "1234":
    db_content = db.fetch().items
    df = pd.DataFrame.from_dict(db_content)
    csv = convert_df(df)
    st.dataframe(df)
    st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')
