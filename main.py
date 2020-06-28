import streamlit as st
import pandas as pd
import requests, json

st.title('Claim Money')

def max_width():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.markdown(f'<style>{open("style.css").read()}</style>', unsafe_allow_html=True)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://api.moneysmart.gov.au/UnclaimedMoneyService/Simple?accountName='

st.markdown(f'<font size="2">Enter a name:</font>', unsafe_allow_html=True)
name = st.text_input('', '')
st.markdown('</font>', unsafe_allow_html=True)

if st.button('Search'):
    if name is None:
        st.error('Please enter a name.')
    else:
        url += name
        response = requests.get(url, headers=header)
        code = response.status_code
        if code == 200:
            max_width()
            json_response = response.json()
            hits = int(json_response['body']['hitCount'])
            if (hits>1 and hits<501):
                entries = json_response['body']['UnclaimedBasic']
                data = json.dumps(entries)
                df = pd.read_json(data)
                df = df.sort_values(by=['amount'], ascending=False)
                st.dataframe(df)
            elif (hits>500):
                st.error('Error: Too many responses. Try narrowing the search down.')
            elif (hits<2):
                st.error('Error: No records found.')
        elif code == 403:
            st.error('Error: No Response.')
        elif code == 404:
            st.error('Error: No Response.')