import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image

st.title('NFL Football Stats (Rushing) Explorer')
image = Image.open('/app/NFL_logos.jpg')
st.image(image, use_column_width=True, caption='NFL Football team logos')

st.markdown("""
This app performs simple web-scraping of NFL Football players stats data (mainly Rushing data)
* **Python Libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, lxml
* **Data Source:** [pro-football-reference.com](https://www.pro-football-reference.com)
""")

st.sidebar.header('User Inputs')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2021))))

# web-scraping NFL player stats
# https://www.pro-football-reference.com/years/2020/rushing.htm
@st.cache
def load_data(year):
    url = 'https://www.pro-football-reference.com/years/' + str(year) + '/rushing.htm'
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team Selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Player Position Selection
unique_player_position = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_player_position, unique_player_position)

# Filtering Data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Displaying Player Stats for Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team.astype(str))

# Download NFL Player Stats Data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def downloadfile(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # string <-> byte conversion
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(downloadfile(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('heatmap.csv', index=False)
    corr = pd.read_csv('heatmap.csv').corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style('white'):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)