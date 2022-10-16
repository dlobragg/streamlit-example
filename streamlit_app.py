from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import snowflake.connector
from snowflake.connector import ProgrammingError

# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.experimental_singleton
#def init_connection():
 #   return snowflake.connector.connect(
  #      **st.secrets["snowflake"], client_session_keep_alive=True
   # )
@st.experimental_singleton
def snowflakeconnect():
  connect=snowflake.connector.connect(
      user=st.secrets['user'],password=st.secrets['password'],
      account=st.secrets['account'] ,
      database = st.secrets['database'],
      schema = st.secrets['schema'],
      warehouse = st.secrets['warehouse'])
  cx=connect.cursor()
  return cx                  

conn = snowflakeconnect()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query('select distinct "brandName" from pleasantrees_erp.leaflogix."Products" limit 10;')

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")

product = run_query('select distinct "brandName" from pleasantrees_erp.leaflogix."Products" limit 10;')

option = st.selectbox("Select Brand:", product)
