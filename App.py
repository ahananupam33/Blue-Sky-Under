import streamlit as st
import pandas as pd
import csv
import pickle
import numpy as np
import datetime
import darts
import matplotlib.pyplot as plt

from darts import TimeSeries

data = pd.read_csv("final.csv")

model1 = pickle.load(open('finalized_model1.pkl', 'rb'))
model2 = pickle.load(open('finalized_model2.pkl', 'rb'))

series1 = TimeSeries.from_dataframe(data, 'datetime', 'CO(GT)')
series2 = TimeSeries.from_dataframe(data, 'datetime', 'T')

his_ex1 = model1.historical_forecasts(
    series1, start=pd.Timestamp('2004-03-18 00:00:00')).pd_dataframe()
his_ex2 = model2.historical_forecasts(
    series2, start=pd.Timestamp('2004-03-18 00:00:00')).pd_dataframe()


def predictionCO(dt):
    begin = (dt-18)*24
    end = begin + 24
    return np.array(his_ex1[begin: end])


def predictionT(dt):
    begin = (dt-18)*24
    end = begin + 24
    return np.array(his_ex2[begin: end])


st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('Air Quality Prediction')
st.sidebar.subheader(
    "You can perform temporal forcasting of CO and Temperature of a particular day based on previous days where we show the graph and the predictions.")

app_mode = st.sidebar.selectbox('Choose the App mode',
                                ['Prediction of CO', 'Prediction of T']
                                )


if app_mode == 'Prediction of CO':
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    dt = st.date_input(
        "Select a date",
        datetime.date(2004, 3, 18), datetime.date(2004, 3, 18), datetime.date(2004, 3, 24))
    #18, 3, 2004
    dt = dt.day

    if st.button("Predict CO (mg/m3)"):
        st.balloons()
        output = predictionCO(dt)
        #st.success('CO amount is {}'.format(output))
        #plt.figure(101, figsize=(12, 8))
        #his_ex1.plot(label='forecast-fft', lw=3)
        df = pd.DataFrame(output)
        st.line_chart(df)
        df.columns = ['Prediction']
        st.dataframe(df, 400, 500)
        # plt.legend()


elif app_mode == 'Prediction of T':
    st.set_option('deprecation.showfileUploaderEncoding', False)
    #Start = st.sidebar.button('Plotttt')

    st.sidebar.markdown('---')
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    dt = st.date_input(
        "Select a date",
        datetime.date(2004, 3, 18), datetime.date(2004, 3, 18), datetime.date(2004, 3, 24))
    #18, 3, 2004
    dt = dt.day

    if st.button("Predict Temperature (°C)"):
        st.balloons()
        output = predictionT(dt)
        #st.success('CO amount is {}'.format(output))
        #plt.figure(101, figsize=(12, 8))
        #his_ex1.plot(label='forecast-fft', lw=3)
        df = pd.DataFrame(output)
        #df = df.set_index('date')
        st.line_chart(df)
        df.columns = ['Prediction']
        st.dataframe(df, 400, 500)
