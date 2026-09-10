import os
from datetime import datetime
from io import BytesIO

import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="Chiller Plant Performance", page_icon="❄️", layout="wide")
st.markdown("""<style>
.block-container {max-width: 1400px; padding-top: 2rem;}
[data-testid='stMetric'] {background:#f8fafc; border:1px solid #e2e8f0; padding:14px; border-radius:12px;}
h1 {color:#0f172a;}
</style>""", unsafe_allow_html=True)


def get_url():
    try:
        return st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL"))
    except FileNotFoundError:
        return os.getenv("DATABASE_URL")


def connect():
    url = get_url()
    if not url:
        st.error("DATABASE_URL is missing in Streamlit Secrets.")
        st.stop()
    return psycopg2.connect(url, sslmode="require", connect_timeout=10)


def fetch(sql, params=None):
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def execute(sql, params):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()


def export_excel(frame):
    stream = BytesIO()
    with pd.ExcelWriter(stream, engine="openpyxl", datetime_format="m/d/yyyy h:mm AM/PM") as writer:
        frame.to_excel(writer, sheet_name="Sheet2", index=False)
        sheet = writer.book["Sheet2"]
        sheet.freeze_panes = "A2"
        for cell in sheet[1]:
            cell.font = __import__("openpyxl").styles.Font(bold=True, color="FFFFFF")
            cell.fill = __import__("openpyxl").styles.PatternFill("solid", fgColor="1F4E78")
        for column in sheet.columns:
            sheet.column_dimensions[column[0].column_letter].width = min(max(len(str(x.value or "")) for x in column) + 2, 28)
    return stream.getvalue()


st.title("Chiller Plant Performance")
st.caption("Daily operational readings • Sheet2 format")
page = st.sidebar.radio("Menu", ["Dashboard", "Add reading", "Download Excel"])

if page == "Dashboard":
    try:
        df = fetch("SELECT * FROM plant_readings ORDER BY reading_at DESC")
        if df.empty:
            st.info("No readings yet. Add the first Sheet2 reading.")
        else:
            latest = df.iloc[0]
            a, b, c, d = st.columns(4)
            a.metric("Latest total power", f"{float(latest.total_power_kw):,.2f} kW")
            b.metric("Latest refrigeration", f"{float(latest.total_refrigeration_ton):,.2f} TR")
            c.metric("Plant efficiency", f"{float(latest.plant_efficiency_kw_tr):,.2f} kW/TR")
            d.metric("Chillers running", int(latest.chillers_running))
            st.subheader("Performance trend")
            trend = df.sort_values("reading_at").set_index("reading_at")
            st.line_chart(trend[["total_power_kw", "total_refrigeration_ton"]])
            left, right = st.columns(2)
            with left:
                st.subheader("Plant efficiency")
                st.line_chart(trend[["plant_efficiency_kw_tr"]])
            with right:
                st.subheader("Delta T")
                st.line_chart(trend[["delta_t_c"]])
            st.subheader("Recent readings")
            st.dataframe(df[["reading_at", "total_power_kw", "total_refrigeration_ton", "delta_t_c", "plant_efficiency_kw_tr"]].head(10), use_container_width=True, hide_index=True)
    except Exception as err:
        st.error("Could not load the dashboard.")
        st.code(str(err))

elif page == "Add reading":
    st.header("Add Sheet2 reading")
    st.caption("Enter the same source values as Sheet2. Delta T, Chiller Load, and efficiency values are calculated exactly as in Excel.")
    with st.form("sheet2_form", clear_on_submit=True):
        st.subheader("Time and equipment")
        a, b, c, d = st.columns(4)
        date = a.date_input("Date")
        time = b.time_input("Time")
        ambient = c.number_input("Ambient temperature °C", min_value=0.0, value=0.0)
        primary_motors = d.number_input("Number of Primary Motors Running", min_value=0, step=1)
        a, b, c, d = st.columns(4)
        secondary_motors = a.number_input("Number of Secondary Motors running", min_value=0, step=1)
        chillers = b.number_input("Number of Chillers running", min_value=0, step=1)
        compressors = c.number_input("Number of Compressors running", min_value=0, step=1)
        motor_load = d.number_input("Motor load (KW)", min_value=0.0, help="Enter the same motor-load value used in Sheet2.")
        st.subheader("Power and cooling")
        a, b = st.columns(2)
        total_power = a.number_input("Total Power (KW)", min_value=0.0)
        total_tr = b.number_input("Total ton of refrigeration (TON)", min_value=0.0)
        st.subheader("Pressure and temperature")
        a, b, c, d = st.columns(4)
        primary_in = a.number_input("Primary In (Bar)", min_value=0.0)
        primary_out = b.number_input("Primary out (Bar)", min_value=0.0)
        secondary_in = c.number_input("Secondary In (Bar)", min_value=0.0)
        secondary_out = d.number_input("Secondary Out (Bar)", min_value=0.0)
        a, b = st.columns(2)
        return_temp = a.number_input("Return temperature (104) °C", min_value=0.0)
        supply_temp = b.number_input("Supply temperature (103) °C", min_value=0.0)
        submitted = st.form_submit_button("Save reading", type="primary")
    if submitted:
        # Sheet2 formulas: P = N-O, R = H-Q, S = R/I, T = H/I
        delta_t = return_temp - supply_temp
        chiller_load = total_power - motor_load
        chiller_efficiency = chiller_load / total_tr if total_tr else 0
        plant_efficiency = total_power / total_tr if total_tr else 0
        try:
            execute("""INSERT INTO plant_readings (reading_at,ambient_temp_c,primary_motors_running,secondary_motors_running,chillers_running,compressors_running,total_power_kw,total_refrigeration_ton,primary_in_bar,primary_out_bar,secondary_in_bar,secondary_out_bar,return_temp_c,supply_temp_c,delta_t_c,motor_load_kw,chiller_load_kw,chiller_efficiency_kw_tr,plant_efficiency_kw_tr)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (datetime.combine(date, time),ambient,primary_motors,secondary_motors,chillers,compressors,total_power,total_tr,primary_in,primary_out,secondary_in,secondary_out,return_temp,supply_temp,delta_t,motor_load,chiller_load,chiller_efficiency,plant_efficiency))
            st.success(f"Saved. Delta T: {delta_t:.2f} °C | Chiller Load: {chiller_load:,.2f} kW | Plant Efficiency: {plant_efficiency:.2f} kW/TR")
        except Exception as err:
            st.error("Could not save the reading.")
            st.code(str(err))

else:
    st.header("Download Sheet2 Excel")
    try:
        df = fetch("SELECT * FROM plant_readings ORDER BY reading_at")
        if df.empty:
            st.info("No readings available to download.")
        else:
            report = pd.DataFrame({
                "Date": pd.to_datetime(df.reading_at).dt.date,
                "Time": pd.to_datetime(df.reading_at).dt.strftime("%-I:%M%p"),
                "Ambient temperature °C": df.ambient_temp_c,
                "Number of Primary Motors Running": df.primary_motors_running,
                "Number of Secondary Motors running": df.secondary_motors_running,
                "Number of Chillers running": df.chillers_running,
                "Number of Compressors running": df.compressors_running,
                "Total Power (KW)": df.total_power_kw,
                "Total ton of refrigeration (TON)": df.total_refrigeration_ton,
                "Primary In (Bar)": df.primary_in_bar,
                "Primary out (Bar)": df.primary_out_bar,
                "Secondary In (Bar)": df.secondary_in_bar,
                "Secondary Out (Bar)": df.secondary_out_bar,
                "Return temperature (104) °C": df.return_temp_c,
                "Supply temperature (103)°C": df.supply_temp_c,
                "Delta T °C": df.delta_t_c,
                "Motor load (KW)": df.motor_load_kw,
                "Chiller Load (KW)": df.chiller_load_kw,
                "Chiller Efficiency (Chiller KW/TR)": df.chiller_efficiency_kw_tr,
                "Plant Efficiency (Total KW/TR)": df.plant_efficiency_kw_tr,
            })
            st.dataframe(report, use_container_width=True, hide_index=True)
            st.download_button("Download Excel (.xlsx)", export_excel(report), "Daily_Readings_Sheet2.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")
    except Exception as err:
        st.error("Could not prepare the Excel file.")
        st.code(str(err))
