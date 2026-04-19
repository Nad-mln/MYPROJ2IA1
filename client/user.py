import streamlit as st

def user_input():
    Temperature = st.sidebar.slider('Temperature', 0.0, 50.0, 25.0)
    Humidity = st.sidebar.slider('Humidity', 0.0, 100.0, 50.0)
    PM25 = st.sidebar.slider('PM2.5', 0.0, 500.0, 50.0)
    PM10 = st.sidebar.slider('PM10', 0.0, 500.0, 80.0)
    NO2 = st.sidebar.slider('NO2', 0.0, 200.0, 40.0)
    SO2 = st.sidebar.slider('SO2', 0.0, 200.0, 20.0)
    CO = st.sidebar.slider('CO', 0.0, 10.0, 1.0)
    Industrie = st.sidebar.slider('Proximité industrielle', 0.0, 10.0, 5.0)
    Population = st.sidebar.slider('Densité population', 0.0, 1000.0, 300.0)


    data = {
        'Temperature': Temperature,
        'Humidity': Humidity,
        'PM2.5': PM25,
        'PM10': PM10,
        'NO2': NO2,
        'SO2': SO2,
        'CO': CO,
        'Proximite_zones_industrielles': Industrie,
        'Densite_population': Population
    }
    return data