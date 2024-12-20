import pandas as pd
import streamlit as st
#from streamlit_extras.app_logo import add_logo
#import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests
import logging
logger = logging.getLogger()
from datetime import datetime as dt
import urllib.parse


# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()


politician = requests.get(f'http://api:4000/po/politicians_dropdown').json()
logger.info(f'politician: {politician}')
politicians = []
for p in politician:
     politicians.append(p['item'])
#dropdown_list = pd.DataFrame(politician).values.astype(str)
search_query = st.selectbox('Search for a politician...', politicians, index=None)
if search_query:
    search_query = (search_query.split(" -")[0])
    results = requests.get(f'http://api:4000/po/{search_query}').json()
    if results:
        for politician in results:
            if st.button(politician['name'],
                        type='primary',
                        use_container_width=True):
                politician_name = politician['name']
                politician_response = requests.get(f'http://api:4000/po/politician_stock_details/{politician_name}').json()
                st.session_state.politician_stock = politician_response
                st.session_state.payload = politician
                st.switch_page('pages/09_Politician_Detail.py')
    else:
        st.write('no politicians found... check spelling')
    
else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Trending Politicians:")

        # SQL query to grab 5 most searched politicians ... eventually
        results = requests.get(f'http://api:4000/po/politicians').json()
        for politician in results:
                if st.button('🔥 ' + politician['name'],
                            type='primary',
                            use_container_width=True,
                            key=f"{politician['name']}_name_trending"):
                    politician_name = politician['name']
                    politician_response = requests.get(f'http://api:4000/po/politician_stock_details/{politician_name}').json()
                    st.session_state.politician_stock = politician_response
                    st.session_state.payload = politician
                    st.switch_page('pages/09_Politician_Detail.py')

    with col2:
        st.write("Politicians with Highest Volume:")

        # SQL query to grab 5 most searched politicians ... eventually
        results = requests.get(f'http://api:4000/po/politicians_volume').json()
        for politician in results:
                if st.button(politician['name'],
                            type='primary',
                            use_container_width=True,
                            key=f"{politician['name']}_name_volume"):
                    politician_name = politician['name']
                    politician_response = requests.get(f'http://api:4000/po/politician_stock_details/{politician_name}').json()
                    st.session_state.politician_stock = politician_response
                    st.session_state.payload = politician
                    st.switch_page('pages/09_Politician_Detail.py')
