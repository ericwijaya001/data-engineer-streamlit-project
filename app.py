import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Pengaruh COVID-19 Terhadap Perekonomian Negara-Negara di Dunia')
st.header('AAAAAAAAAA NAISUUUUUUUUUUU')
confirmed_global = pd.read_csv('time_series_covid19_confirmed_global.csv', index_col=None, header=0)
confirmed_global = confirmed_global.drop(columns=['Lat', 'Long','Province/State'])
confirmed_global = confirmed_global.groupby('Country/Region').sum().reset_index()

total_global_cases = confirmed_global.sum(axis=0).to_frame()
total_global_cases = total_global_cases.iloc[2:-1].rename(columns={0: 'Total Confirmed Cases'})
total_global_cases.index = pd.to_datetime(total_global_cases.index)
resetidx_total_global_cases = total_global_cases.reset_index()
newdf = resetidx_total_global_cases.groupby([resetidx_total_global_cases['index'].dt.year.rename('year'),resetidx_total_global_cases['index'].dt.month.rename('month')])['Total Confirmed Cases'].sum()
newsdf = newdf.to_frame()
newsdf = newsdf.reset_index()
newsdf['date'] = pd.to_datetime(newsdf[['year', 'month']].assign(DAY=1))
newsdf = newsdf[newsdf['date']<'2022-10-01']
newsdf = newsdf.drop(columns=['year', 'month'])

fig = plt.figure() 
plt.plot(newsdf['date'],newsdf['Total Confirmed Cases'])
plt.xticks(rotation='vertical')
st.pyplot(fig)


confirmed_global['Total Confirmed'] = confirmed_global.iloc[:,-1]
confirmed_global = confirmed_global.groupby('Country/Region').sum().reset_index()

latest_confirmed_global = confirmed_global[['Country/Region', 'Total Confirmed']]
top_10_confirmed = latest_confirmed_global.sort_values('Total Confirmed', ascending=False)[:10][['Country/Region', 'Total Confirmed']].reset_index(drop=True)
st.dataframe(top_10_confirmed)

import numpy as np
with st.container():
   st.write("This is inside the container")
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")