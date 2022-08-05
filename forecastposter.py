import pandas as pd
import streamlit as st
from PIL import Image
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import glob
import plotly.express as px

st.set_page_config(age_title='heat-stressed-poultry')
st.set_page_config(layout="wide")

@st.cache
def readdata(file):
    van20all1 = pd.read_excel(file)
    time_plot1 = van20all1[['Section4','Section3','index']].set_index('index')
    time_plot1['deltaT'] = time_plot1['Section4'] -time_plot1['Section3']
    return van20all1, time_plot1

@st.cache
def loadimage(img):
   return Image.open(img)

fName = "van20jun.xlsx"
van20all,time_plot = readdata(fName)
header_container = st.container()
historical_container = st.container()

with st.sidebar:
    st.header('Choose File Controls')

    with st.expander("TXT Data file from CSGM"):
        weatherType1 = st.selectbox(
            'Select Weather variable being processed?',
            ('Humidity', 'Temperature', 'Rainfall', 'wind speed'))
        # st.write('You selected:', weatherType1)

with header_container:
    image = loadimage('conference logo2.png')
    # image2 = Image.open('FORECAST Logo 3.jpg')
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.image(image2)
    # with col2:
    st.image(image)

    st.title('NEARING A TIPPING POINT: HEAT-STRESS AND SMALL SCALE POULTRY FARMING IN JAMAICA')
    st.subheader('Abstract submitted to the FORECAST Conference 2022')

    with st.expander("View abstract"):
        st.text(
            "Background: Heat stress is the leading cause of high mortality and low production in small livestock farming")
        st.text(
            "in Jamaica. Additionally, the persistent warming of the Caribbean due to climate change worsens the problem")
        st.text(
            "in the sector. This paper presents a field investigation into the heat stress problem at the Vere Technical")
        st.text("High School in Clarendon Jamaica")

with historical_container:
    with st.expander(" Interactive graphs"):
        fig = px.scatter(van20all, x='date', y='hour', color='Sec3THI',
                         labels={'Sec3THI': 'Section3', 'hour': 'Time', 'date': 'Date'}
                         , marginal_y="box",
                         symbol='Sec3THI',
                         category_orders={'Sec3THI': ['No stress', 'Heat stressed', 'Severely stressed']},
                         color_discrete_sequence=["green", "blue", "red"], size_max=10,
                         width=1300, height=600

                         )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="right",
            x=1
        ))

        fig.update_layout(
            yaxis=dict(
                tickmode='array',
                range=[-0.5, len(van20all.hour.unique()) + 0.5],
                tickvals=van20all.hour.unique(),
                ticktext=van20all.time.unique(),
                # tickfont_family="Arial Black",
                # tickfont_size=15
            )
        )
        fig.update_layout(
            font_family="Arial Black",
            font_color="white",
            title_font_family="Times New Roman",
            title_font_color="white",
            legend_title_font_color="white",
            # font_size=15
        )

        # fig.update_xaxes(tickfont_family="Arial Black")
        # fig.update_xaxes(tickfont_size=15, ticks="outside")
        # fig.update_yaxes(tickfont_size=15, ticks="outside")
        st.plotly_chart(fig, use_container_width=True)