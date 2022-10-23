import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Pengaruh COVID-19 Terhadap Perekonomian Negara-Negara di Dunia')
st.markdown('#')
st.subheader('COVID-19')
text1 = """<span style="word-wrap:break-word;">
Sejarah Coronavirus bermula pada laporan pertama wabah COVID-19 yang berasal dari sekelompok kasus pneumonia manusia di Kota Wuhan, China, sejak akhir Desember 2019. Tanggal paling awal timbulnya kasus adalah 1 Desember 2019.
Penyakit COVID-19 yang disebabkan oleh virus SARS-CoV-2 atau yang dikenal juga dengan coronavirus masih satu keluarga dengan coronavirus penyebab wabah Severe Acute Respiratory Syndrome (SARS) dan Middle East Respiratory Syndrome (MERS).<br>

Menurunnya berbagai aktivitas ini berdampak pada kondisi sosial-ekonomi masyarakat, khususnya masyarakat rentan dan miskin. Oleh sebab itu, pemerintah, baik di tingkat pusat maupun daerah, mengeluarkan berbagai kebijakan untuk menanggulangi penyebaran COVID-19 serta kebijakan-kebijakan yang bersifat penanggulangan dampak sosial dan ekonomi akibat pandemi ini. Kendati demikian, pelaksanaan berbagai kebijakan ini perlu dipantau dan dievaluasi untuk mengetahui efektivitasnya. <br>

Turunnya aktivitas masyarakat di dunia ini disebabkan oleh COVID-19 yang tidak kunjung selesai dari awal kasus COVID-19.
Tentunya hal ini memiliki pengaruh terhadap berbagai sektor seperti pendidikan, sosial budaya, dan pastinya perekonomian.
Negara-negara di dunia sudah mulai merasakan dampak dari COVID-19 yang dapat dilihat dari berita-berita seputar tingkat inflasi dan juga tingkat perekonomian suatu negara yang bisa sangat tionggi.
Bahkan ada negara yang disebut-sebut hingga mengal;ami kebangkrutan. <br>

Kita bersama-sama akan melihat pengaruh COVID-19 dengan menggunakan data mengenai COVID-19 yang didapatkan dari Kaggle (https://www.kaggle.com/) dan juga data mengenai perekonomian yang didapatkan dari Organisation for Economic
Co-operation and Development (https://data.oecd.org/). Tingkat perekonomian akan dilihat beberapa komponen yaitu QGDP (Quaterly Gross Domestic Product) dan Tingkat Inflasi menggunakan CPI.
</span>"""
st.markdown(text1, unsafe_allow_html=True)

st.header('Grafik Total Kasus COVID-19 di Seluruh Dunia')
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
plt.xlabel('Tanggal (per Bulan)')
plt.ylabel('Total Kasus Terkonfirmasi (satuan 10 miliar)')
st.pyplot(fig)

st.subheader('Data 10 Negara Teratas Jumlah Kasus COVID-19 Terbaru (5 Oktober 2022)')
st.markdown('#')

confirmed_global['Total Confirmed'] = confirmed_global.iloc[:,-1]
confirmed_global = confirmed_global.groupby('Country/Region').sum().reset_index()

latest_confirmed_global = confirmed_global[['Country/Region', 'Total Confirmed']]
top_10_confirmed = latest_confirmed_global.sort_values('Total Confirmed', ascending=False)[:10][['Country/Region', 'Total Confirmed']].reset_index(drop=True)
st.dataframe(top_10_confirmed)


st.subheader('Grafik Kenaikan Jumlah Kasus COVID-19 untuk 10 Negara Teratas')

list_top_10_confirmed_country = top_10_confirmed['Country/Region'].to_list()
confirmed_cases_country = confirmed_global.groupby('Country/Region').sum().reset_index()

ax = plt.figure(figsize=(16,6))
plt.title('Comparison of Top 10 Confirmed Cases')
plt.xlabel('Date Confirmed Cases (per Month)')
plt.ylabel('Total Confirmed Cases (in Billion)')

for top_10_confirmed_country in list_top_10_confirmed_country:
    country_confirmed_cases = confirmed_cases_country[confirmed_cases_country['Country/Region'] == top_10_confirmed_country].reset_index(drop=True)
    total_country_cases = country_confirmed_cases.sum(axis=0).to_frame()
    total_country_cases = total_country_cases.iloc[2:-1].rename(columns={0: 'Total Confirmed Cases'})

    total_country_cases.index = pd.to_datetime(total_country_cases.index)

    resetidx_total_country_cases = total_country_cases.reset_index()

    newdf_country = resetidx_total_country_cases.groupby([resetidx_total_country_cases['index'].dt.year.rename('year'),resetidx_total_country_cases['index'].dt.month.rename('month')])['Total Confirmed Cases'].sum()

    newsdf_country = newdf_country.to_frame()
    newsdf_country = newsdf_country.reset_index()

    newsdf_country['date'] = pd.to_datetime(newsdf_country[['year', 'month']].assign(DAY=1))
    newsdf_country = newsdf_country[newsdf_country['date']<'2022-10-01']
    newsdf_country = newsdf_country.drop(columns=['year', 'month'])

    plt.plot(newsdf_country['date'],newsdf_country['Total Confirmed Cases'])
    plt.xticks(rotation='vertical')
plt.legend(list_top_10_confirmed_country)
st.pyplot(ax)
