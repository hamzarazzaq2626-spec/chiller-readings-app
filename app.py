import os
from datetime import datetime

import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="Chiller Plant Readings", page_icon="❄️", layout="wide")


def get_database_url():
    try:
        return st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL"))
    except FileNotFoundError:
        return os.getenv("DATABASE_URL")


def connect():
    url = get_database_url()
    if not url:
        st.error("DATABASE_URL is missing. Add it in Streamlit Secrets and reboot the app.")
        st.stop()
    return psycopg2.connect(url, sslmode="require", connect_timeout=10)


def query(sql, params=None):
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def save(sql, params):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()


def number(value, suffix=""):
    return "—" if pd.isna(value) else f"{float(value):,.2f}{suffix}"


st.title("❄️ Chiller Plant Readings")
st.caption("Record plant and chiller performance readings.")
page = st.sidebar.radio("Navigate", ["Dashboard", "Add plant reading", "Add chiller reading", "Reports"])

if page == "Dashboard":
    st.header("Dashboard")
    try:
        data = query("""SELECT COUNT(*) AS reading_count, AVG(total_power_kw) AS avg_power,
                        AVG(total_refrigeration_ton) AS avg_tr,
                        AVG(plant_efficiency_kw_tr) AS avg_efficiency
                        FROM plant_readings""").iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Plant readings", int(data["reading_count"]))
        c2.metric("Average power", number(data["avg_power"], " kW"))
        c3.metric("Average refrigeration", number(data["avg_tr"], " TR"))
        c4.metric("Plant efficiency", number(data["avg_efficiency"], " kW/TR"))
        trend = query("""SELECT reading_at, total_power_kw, total_refrigeration_ton,
                         plant_efficiency_kw_tr FROM plant_readings ORDER BY reading_at""")
        if trend.empty:
            st.info("No readings saved yet. Use ‘Add plant reading’ to create the first record.")
        else:
            st.subheader("Power and refrigeration")
            st.line_chart(trend.set_index("reading_at")[["total_power_kw", "total_refrigeration_ton"]])
            st.subheader("Plant efficiency")
            st.line_chart(trend.set_index("reading_at")[["plant_efficiency_kw_tr"]])
    except Exception as error:
        st.error("Database connection failed. Check the Streamlit secret DATABASE_URL.")
        st.code(str(error))

elif page == "Add plant reading":
    st.header("Add plant reading")
    with st.form("plant_reading", clear_on_submit=True):
        a, b, c = st.columns(3)
        reading_date = a.date_input("Date")
        reading_time = b.time_input("Time")
        ambient = c.number_input("Ambient temperature (°C)", min_value=0.0)
        a, b, c, d = st.columns(4)
        primary = a.number_input("Primary motors running", min_value=0, step=1)
        secondary = b.number_input("Secondary motors running", min_value=0, step=1)
        chillers = c.number_input("Chillers running", min_value=0, step=1)
        compressors = d.number_input("Compressors running", min_value=0, step=1)
        a, b, c = st.columns(3)
        power = a.number_input("Total power (kW)", min_value=0.0)
        refrigeration = b.number_input("Total refrigeration (TR)", min_value=0.0)
        motor_load = c.number_input("Motor load (kW)", min_value=0.0)
        a, b, c, d = st.columns(4)
        primary_in = a.number_input("Primary inlet (bar)", min_value=0.0)
        primary_out = b.number_input("Primary outlet (bar)", min_value=0.0)
        secondary_in = c.number_input("Secondary inlet (bar)", min_value=0.0)
        secondary_out = d.number_input("Secondary outlet (bar)", min_value=0.0)
        a, b = st.columns(2)
        return_temp = a.number_input("Return temperature (°C)", min_value=0.0)
        supply_temp = b.number_input("Supply temperature (°C)", min_value=0.0)
        submitted = st.form_submit_button("Save plant reading", type="primary")
    if submitted:
        delta_t = return_temp - supply_temp
        chiller_load = power - motor_load
        chiller_efficiency = chiller_load / refrigeration if refrigeration else None
        plant_efficiency = power / refrigeration if refrigeration else None
        try:
            save("""INSERT INTO plant_readings (reading_at, ambient_temp_c, primary_motors_running,
            secondary_motors_running, chillers_running, compressors_running, total_power_kw,
            total_refrigeration_ton, primary_in_bar, primary_out_bar, secondary_in_bar,
            secondary_out_bar, return_temp_c, supply_temp_c, delta_t_c, motor_load_kw,
            chiller_load_kw, chiller_efficiency_kw_tr, plant_efficiency_kw_tr)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (datetime.combine(reading_date, reading_time), ambient, primary, secondary, chillers,
             compressors, power, refrigeration, primary_in, primary_out, secondary_in, secondary_out,
             return_temp, supply_temp, delta_t, motor_load, chiller_load, chiller_efficiency,
             plant_efficiency))
            st.success("Plant reading saved successfully.")
        except Exception as error:
            st.error("Could not save the reading.")
            st.code(str(error))

elif page == "Add chiller reading":
    st.header("Add chiller reading")
    with st.form("chiller_reading", clear_on_submit=True):
        a, b, c, d = st.columns(4)
        reading_date = a.date_input("Date")
        reading_time = b.time_input("Time")
        chiller_number = c.text_input("Chiller number", placeholder="Chiller 01")
        is_on = d.toggle("Chiller ON", value=True)
        a, b, c, d = st.columns(4)
        compressors = a.number_input("Compressors running", min_value=0, step=1)
        load_percent = b.number_input("Load (%)", min_value=0.0, max_value=100.0)
        ewt = c.number_input("EWT (°C)", min_value=0.0)
        lwt = d.number_input("LWT (°C)", min_value=0.0)
        a, b, c, d = st.columns(4)
        flow = a.number_input("Flow", min_value=0.0)
        power = b.number_input("Power (kW)", min_value=0.0)
        calibration_1 = c.number_input("Calibration 1", min_value=0.0)
        calibration_2 = d.number_input("Calibration 2", min_value=0.0)
        submitted = st.form_submit_button("Save chiller reading", type="primary")
    if submitted:
        if not chiller_number.strip():
            st.error("Enter a chiller number.")
        else:
            delta_t = ewt - lwt
            far = delta_t * 1.8
            total_tr = (flow * delta_t) / 24 if flow else 0
            try:
                save("""INSERT INTO chiller_readings (reading_at, chiller_number, is_on,
                compressors_running, load_percent, ewt_c, lwt_c, flow, calibration_1, power_kw,
                delta_t_c, far, calibration_2, total_tr)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (datetime.combine(reading_date, reading_time), chiller_number.strip(), is_on,
                 compressors, load_percent, ewt, lwt, flow, calibration_1, power, delta_t, far,
                 calibration_2, total_tr))
                st.success("Chiller reading saved successfully.")
            except Exception as error:
                st.error("Could not save the reading.")
                st.code(str(error))

else:
    st.header("Reports")
    try:
        readings = query("SELECT * FROM plant_readings ORDER BY reading_at DESC")
        st.dataframe(readings, use_container_width=True, hide_index=True)
        st.download_button("Download plant readings (CSV)", readings.to_csv(index=False).encode("utf-8"),
                           file_name="plant_readings.csv", mime="text/csv")
    except Exception as error:
        st.error("Could not load the report.")
        st.code(str(error))
