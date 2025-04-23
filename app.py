import streamlit as st
import wntr
import tempfile
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EPANET Simulation API", layout="wide")
st.title("💧 EPANET Simulation with WNTR")

uploaded_file = st.file_uploader("Upload your EPANET .inp file", type=["inp"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as temp:
        temp.write(uploaded_file.read())
        inp_path = temp.name

    st.success("File uploaded. Starting simulation...")

    wn = wntr.network.WaterNetworkModel(inp_path)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    st.subheader("Simulation Complete")
    pressure = results.node["pressure"]
    st.line_chart(pressure)

    st.download_button("Download Pressure Data (CSV)", data=pressure.to_csv().encode('utf-8'),
                       file_name="pressure_results.csv", mime="text/csv")
