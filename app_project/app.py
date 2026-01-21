import streamlit as st
import pandas as pd
import os

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("novo_nordisk_logo.png", width=200)



st.title("Supplier CO₂ Reporting Portal")

st.header("Supplier Information")

supplier_name = st.text_input("Supplier name")

industry = st.selectbox(
    "Industry",
    ["Pharmaceutical API", "Packaging (Plastic)", "Logistics"]
)

production_volume = st.number_input(
    "Annual production volume (units)",
    min_value=0.0
)

energy_kwh = st.number_input(
    "Annual energy consumption (kWh)",
    min_value=0.0
)

submit = st.button("Submit")

EMISSION_FACTORS = {
    "Pharmaceutical API": 4.2,
    "Packaging (Plastic)": 2.1,
    "Logistics": 0.9
}

ELECTRICITY_FACTOR = 0.0004  # tons CO2 per kWh

if submit:
    if energy_kwh > 0:
        emissions = energy_kwh * ELECTRICITY_FACTOR
        method = "Reported (energy-based)"
        confidence = "High"
    else:
        emissions = production_volume * EMISSION_FACTORS[industry]
        method = "Estimated (industry average)"
        confidence = "Medium"

    st.subheader("Estimated CO₂ Emissions")
    st.write(f"**Total emissions:** {emissions:.2f} tons CO₂/year")
    st.write(f"**Calculation method:** {method}")
    st.write(f"**Confidence level:** {confidence}")

    # Sustainability score
    carbon_intensity = emissions / production_volume if production_volume > 0 else 0

    if confidence == "High" and carbon_intensity < 3:
        score = "A"
    elif carbon_intensity < 5:
        score = "B"
    else:
        score = "C"

    st.subheader("Your Sustainability Rating")
    st.write(f"**Tier:** {score}")

    # Save data (THIS is where 'data' must be)
    data = {
        "Supplier": supplier_name,
        "Industry": industry,
        "Volume": production_volume,
        "Energy_kWh": energy_kwh,
        "Emissions_tCO2": emissions,
        "Method": method,
        "Confidence": confidence,
        "Tier": score
    }

    df = pd.DataFrame([data])

    if os.path.exists("supplier_data.csv"):
        df.to_csv("supplier_data.csv", mode="a", header=False, index=False)
    else:
        df.to_csv("supplier_data.csv", index=False)

st.header("Novo Nordisk – Supply Chain Emissions Overview")

if os.path.exists("supplier_data.csv"):
    df_all = pd.read_csv("supplier_data.csv")

    st.dataframe(df_all)

    st.bar_chart(
        df_all.groupby("Supplier")["Emissions_tCO2"].sum()
    )
else:
    st.write("No supplier data submitted yet.")


st.download_button(
    "Download supplier data",
    data=open("supplier_data.csv", "rb"),
    file_name="supplier_data.csv"
)


