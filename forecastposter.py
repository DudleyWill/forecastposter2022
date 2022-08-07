import pandas as pd
import streamlit as st
from PIL import Image
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import glob
import plotly.express as px

# st.set_page_config(age_title='heat-stressed-poultry')
st.set_page_config(layout="wide")

mystyle = '''
    <style>
        p {
            text-align: justify;
        }
    </style>
    '''

st.markdown(mystyle, unsafe_allow_html=True)

@st.cache
def readdata(file):
    van20all1 = pd.read_excel(file)
    time_plot1 = van20all1[['Section4','Section3','index','Outdoor']].set_index('index')
    time_plot1['s3out'] = time_plot1['Section3'] -time_plot1['Outdoor']
    time_plot1['s4out'] = time_plot1['Section4'] - time_plot1['Outdoor']
    return van20all1, time_plot1

@st.cache
def loadimage(img):
   return Image.open(img)

fName = "van20all.xlsx"
van20all,time_plot = readdata(fName)
header_container = st.container()
method_container = st.container()
historical_container = st.container()
conclusion_container = st.container()
reference_container = st.container()

def graphs20 (thi,section):
    fig1 = px.scatter(van20all, x='date', y='hour', color=thi,
                     labels={thi: section, 'hour': 'Time', 'date': 'Date'}
                     , marginal_y="box",
                     symbol=thi,
                     category_orders={thi: ['No stress', 'Heat stressed', 'Severely stressed']},
                     color_discrete_sequence=["#70bb2a", "#ffb814", "#ff1120"], size_max=10,
                     width=1300, height=600

                     )
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="right",
        x=1
    ))

    fig1.update_layout(
        yaxis=dict(
            tickmode='array',
            range=[-0.5, len(van20all.hour.unique()) + 0.5],
            tickvals=van20all.hour.unique(),
            ticktext=van20all.time.unique(),
            # tickfont_family="Arial Black",
            # tickfont_size=15
        )
    )
    fig1.update_layout(
        font_family="Arial Black",
        font_color="white",
        title_font_family="Times New Roman",
        title_font_color="white",
        legend_title_font_color="white",
        # font_size=15
    )
    return  fig1


def timeseries(section,outt):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.3, 0.7], )

    fig.add_trace(
        go.Scatter(x=time_plot.index, y=time_plot[section], name='inTemp', line_color='red'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=time_plot.index, y=time_plot['Outdoor'], name='OutTemp', line_color='blue'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=time_plot.index, y=time_plot[outt], name='tempDiff'),
        row=1, col=1
    )

    fig.update_yaxes(
        title_text="Temperature \N{DEGREE SIGN} C ",
        title_standoff=25)

    fig.update_layout(height=600, width=1300,
                      )
    return fig


with header_container:
    image = loadimage('conference logo2.png')
    col1, col2,col3 = st.columns([1,3,1])
    with col1:
        st.write(' ')
    with col2:
        st.image(image)
    with col3:
        st.write(' ')

    st.title('NEARING A TIPPING POINT: HEAT-STRESS AND SMALL SCALE POULTRY FARMING IN JAMAICA')
    st.subheader('Abstract submitted to the FORECAST Conference 2022')

    with st.expander("Research Background"):
        st.info(
            """This project reports on work done at the Vere Technical 
            High School chicken farm in Clarendon Jamaica. This chicken farm is used to supply meat to the school's
            canteen, whose profitability was being threaten by high mortality. The research team with funding from 
            the Environmental Foundation of Jamaica provided assistance to the school to investigate the cause of 
            the high mortality and provide mitigation options.""")
        st.write(" ")
        st.write(
            " The growth of livestock such as chicken is affected by "
            "temperature as it dictates the quantity of water lost through sweating and urination. Where a large"
            " number of livestock are kept in the same location, fans are used to control the temperature in the "
            "building, which becomes less effective with increasing temperatures from climate change. "
            "If a new solution is not found: there will be increase death of livestock from heat stroke,"
            " smaller livestock in terms of body mass after the normal growing period as they lose water weight to "
            "survive the heat." 
            "Heat stress is the leading cause of high mortality and low production in small livestock farming in [1]"
            "  Jamaica. Additionally, the persistent warming of the Caribbean due to climate change worsens the problem"
            "in the sector. This paper presents a field investigation into the heat stress problem at ")

with method_container:
    with st.expander('Experimental setup'):

        cola, colb =st.columns(2)
        with cola:
            st.write('A typical open ventilated poultry house, made of galvanized zinc roof, timber framing and meshed sides '
                     'was chosen as the test site. Measuring instruments were installed inside to record temperature and humidity, '
                     'along with an external weather station. Baseline data was collected in 2019. A radiant barrier was '
                     'installed in the ceiling of one section of the poultry house in 2020, to reduce heat ingress from the '
                     ' zinc roof. The Temperature Humidity Index (THI) was used to assess the thermal comfort of the '
                     'broiler chickens using Eqn.1 and the following THI classifications: no stress < 26, heat-stressed'
                     '26-29 and severely stressed > 30 [2]. The project also explored nighttime radiative cooling by '
                     ' modifying a solar water heater to reduce the temperature of 30 gallons of water during the night '
                     'with a 3W circulating pump. This experiment was conducted at the Department of Physics of the '
                     'University of the West Indies, Mona Campus. Eqn.1 THI = 0.85 ∗ T_drybulb + 0.15 ∗ T_wetbulb')
        with colb:
            image4 = loadimage('inside.jpg')
            st.image(image4,caption='Radiant barrier installed in section 3 of the Poultry house. Direct sunlight heats'
                                    ' up the floor on the left side in the morning focusing the chickens to migrate to '
                                    ' the other side')

with historical_container:
    with st.expander(" Results"):
        graphs = st.radio(" ",
                          ('Section 4 compared with outdoor',
                           'Section 3 compared with outdoor',
                           'Section 4 hourly THI',
                           'Section 3 hourly THI',
                           'Chicken mortality stats')
                          ,horizontal=True)
        if graphs =='Section 4 compared with outdoor':
            fig = timeseries('Section4', 's4out')
            st.plotly_chart(fig, use_container_width=True)
            st.write("Shows the temperature of inside of section 4, where no interventon was done, compared to outdoor temperature. "
            "Note worthy, section 4 achieved lower temperatures during the night than section 3" )
        elif graphs=='Section 3 compared with outdoor':

            fig2 = timeseries('Section3', 's3out')
            st.plotly_chart(fig2, use_container_width=True)
            st.write(
                "Compares the temperature of section 3 where the radiant barrier was installed with respect to outdoor temperatures. "
                "Section 3 maintained a temperature difference of 0\N{DEGREE SIGN} C to 4\N{DEGREE SIGN} C in the daytime while section 4"
                "could go as high as ~5.6\N{DEGREE SIGN} C.  ")
        elif graphs =='Section 4 hourly THI':
            fig = graphs20('Sec4THI', 'Section4')
            st.plotly_chart(fig, use_container_width=True)
            st.write(
                'Shows the hourly variation of the temperature hunmidity index which is used to estimate the level of heat stress expereinced by '
                'chickens in section 4 of the poultry house')
        elif graphs =='Section 3 hourly THI':

            fig = graphs20('Sec3THI', 'Section3')
            st.plotly_chart(fig, use_container_width=True)
            st.write(
                'Shows the hourly variation of temperature hunmidity index which is used to estimate the level of heat stress expereinced by '
                'chickens in section 4 of the poultry house')
        else:
            image1 = loadimage('chickendeath.png')
            st.image(image1)

with conclusion_container:
    with st.expander('Conclusion'):
        st.write('The radiant Barrier reduced convective and radiative  heating inside the Poultry farm. '
                 'The section with the radiant barrier was on average 2 \N{DEGREE SIGN} C lower that the other sections.  '
                 'Improving the thermal performance of the building may not be sufficient to reduce'
                 ' the number of hours spent in severe THI conditions. Methods that can '
                 'reduce the temperature of the air without being energy intensive '
                 'are needed to address the heat stress problems '
                 'of small farmers. Based')


with reference_container:
    with st.expander('References'):
        st.write ('[1] C. Lallo et al, “Characterizing heat stress on livestock using the temperature humidity index'
              '  (THI)—prospects for a warmer Caribbean” Regional Environmental Change,'
              ' vol. 18, , pp. 2329–2340, Dec.2018.')
        st.write('[2] O.Omomowo, F. Falayi, “Temperature-humidity index and thermal comfort of broilers in humid'
             '  tropics” CIGR, vol.23(3): pp. 101-110, Sep 2021.')