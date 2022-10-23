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
st.markdown('#')

st.subheader('Grafik Total Kasus COVID-19 di Seluruh Dunia')
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
plt.ylabel('Total Kasus Terkonfirmasi (Satuan 10 Miliar)')
st.pyplot(fig)
st.markdown('#')

st.subheader('Data 10 Negara Teratas Jumlah Kasus COVID-19 Terbaru (5 Oktober 2022)')

confirmed_global['Total Confirmed'] = confirmed_global.iloc[:,-1]
confirmed_global = confirmed_global.groupby('Country/Region').sum().reset_index()

latest_confirmed_global = confirmed_global[['Country/Region', 'Total Confirmed']]
top_10_confirmed = latest_confirmed_global.sort_values('Total Confirmed', ascending=False)[:10][['Country/Region', 'Total Confirmed']].reset_index(drop=True)
st.dataframe(top_10_confirmed)

st.markdown('#')
st.subheader('Grafik Kenaikan Jumlah Kasus COVID-19 untuk 10 Negara Teratas')

list_top_10_confirmed_country = top_10_confirmed['Country/Region'].to_list()
confirmed_cases_country = confirmed_global.groupby('Country/Region').sum().reset_index()

ax = plt.figure(figsize=(16,6))
plt.ylabel('Total Kasus Terkonfirmasi (Satuan Miliar)')

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

st.markdown('#')
st.subheader('Gross domestic product (GDP)')
text2 = """<span style="word-wrap:break-word;">
Gross domestic product (GDP) is the standard measure of the value added created through the production of goods and services in a country during a certain period. As such, it also measures the income earned from that production, or the total amount spent on final goods and services (less imports). While GDP is the single most important indicator to capture economic activity, it falls short of providing a suitable measure of people's material well-being for which alternative indicators may be more appropriate. This indicator is based on nominal GDP (also called GDP at current prices or GDP in value) and is available in different measures: US dollars and US dollars per capita (current PPPs). All OECD countries compile their data according to the 2008 System of National Accounts (SNA). This indicator is less suited for comparisons over time, as developments are not only caused by real growth, but also by changes in prices and PPPs.
</span>"""
st.markdown(text2, unsafe_allow_html=True)

st.markdown('#')
st.subheader('Grafik Total QGDP (Quaterly Gross Domestic Product)')

qgdp_total_PC_CHGPP = pd.read_csv('DP_LIVE_23102022054035282.csv')
top_10_confirmed_country3alphacodes = ['USA', 'IND', 'FRA', 'BRA', 'DEU', 'KOR', 'GBR', 'ITA', 'JPN', 'RUS']
axx = plt.figure(figsize=(16,6))
plt.ylabel('Perubahan persentase periode sebelumnya QGDP')

for top_10_confirmed_country3alphacode in top_10_confirmed_country3alphacodes:
    country_top_10_confirmed_country3alphacode = qgdp_total_PC_CHGPP[qgdp_total_PC_CHGPP['LOCATION'] == top_10_confirmed_country3alphacode]
    plt.plot(country_top_10_confirmed_country3alphacode['TIME'],country_top_10_confirmed_country3alphacode['Value'])
    plt.xticks(rotation='vertical')
plt.legend(top_10_confirmed_country3alphacodes)
st.pyplot(axx)


st.markdown('#')
st.subheader('Grafik Index QGDP (Quaterly Gross Domestic Product)')

qgdp_index_PC_CHGPP = pd.read_csv('DP_LIVE_23102022054016532.csv')

axxx = plt.figure(figsize=(16,6))
plt.ylabel('Index QGDP')

for top_10_confirmed_country3alphacode in top_10_confirmed_country3alphacodes:
    country_top_10_confirmed_country3alphacode = qgdp_index_PC_CHGPP[qgdp_index_PC_CHGPP['LOCATION'] == top_10_confirmed_country3alphacode]
    plt.plot(country_top_10_confirmed_country3alphacode['TIME'],country_top_10_confirmed_country3alphacode['Value'])
    plt.xticks(rotation='vertical')
plt.legend(top_10_confirmed_country3alphacodes)
st.pyplot(axxx)


st.markdown('#')
st.subheader('Inflasi CPI (Consumer Price Index )')
text3 = """<span style="word-wrap:break-word;">
Inflation measured by consumer price index (CPI) is defined as the change in the prices of a basket of goods and services that are typically purchased by specific groups of households. Inflation is measured in terms of the annual growth rate and in index, 2015 base year with a breakdown for food, energy and total excluding food and energy. Inflation measures the erosion of living standards. A consumer price index is estimated as a series of summary measures of the period-to-period proportional change in the prices of a fixed set of consumer goods and services of constant quantity and characteristics, acquired, used or paid for by the reference population. Each summary measure is constructed as a weighted average of a large number of elementary aggregate indices. Each of the elementary aggregate indices is estimated using a sample of prices for a defined set of goods and services obtained in, or by residents of, a specific region from a given set of outlets or other sources of consumption goods and services.
</span>"""
st.markdown(text3, unsafe_allow_html=True)

st.markdown('#')

cpi_total_annual_growth = pd.read_csv('DP_LIVE_23102022054442626.csv')

axxxx = plt.figure(figsize=(16,6))
plt.ylabel('Index Inflasi')

for top_10_confirmed_country3alphacode in top_10_confirmed_country3alphacodes:
    country_top_10_confirmed_country3alphacode = cpi_total_annual_growth[(cpi_total_annual_growth['LOCATION'] == top_10_confirmed_country3alphacode) & (cpi_total_annual_growth['TIME'] >= '2020-01')]
    plt.plot(country_top_10_confirmed_country3alphacode['TIME'],country_top_10_confirmed_country3alphacode['Value'])
    plt.xticks(rotation='vertical')
plt.legend(top_10_confirmed_country3alphacodes)
st.pyplot(axxxx)


st.markdown('#')
st.subheader('Penutup')
text3 = """<span style="word-wrap:break-word;">
COVID-19 memiliki pengaruh terhadap perekonomian negara-negara di dunia. Terlihat dari Grafik Total QGDP dan Grafik Index QGDP yang mengalami penurunan signifikan pada kuartal kedua pada tahun 2020.
Namun seiring berjalannya waktu, kesepuluh negara dengan total kasus COVID-19 terbanyak di dunia sudah mengalami 'recovery' dalam hal GDP dan cenderung mengalami kenaikan nilai yang sedikit hingga kuartal kedua tahun 2022.
Di sisi lain, performa CPI pada masing-masing 10 negara teratas dengan kasus COVID-19 mengalami kenaikan hingga pada bulan Agustus 2022 yang berarti tingkat inflasi juga selama COVID-19 berlangsung.
</span>"""
st.markdown(text3, unsafe_allow_html=True)
