import streamlit as st
import pandas as pd
import os

col1, col2 = st.columns([1, 1])  # two equal-width columns

with col1:
    st.image("logo.png", width=300)  # your logo

with col2:
    st.image("novo_nordisk_logo.png", width=300)  # Novo Nordisk logo



st.markdown(
    "<h1 style='text-align: center;'>Supplier CO₂ Reporting Portal</h1>",
    unsafe_allow_html=True
)


st.info(
    "This portal helps suppliers improve sustainability performance, "
    "increase data quality, and strengthen their partnership with Novo Nordisk."
)


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
    st.markdown(f"<span style='color:green; font-weight:bold;'>Tier {score}</span>", unsafe_allow_html=True)


    st.info("📈 How to improve your score:")


    if confidence != "High":
        st.write("• Provide energy consumption data to improve data quality.")
    if carbon_intensity > 4:
        st.write("• Reduce energy intensity or switch to renewable electricity.")
    if score == "A":
        st.write("• Maintain current performance to retain preferred supplier status.")

    industry_avg = EMISSION_FACTORS[industry]

    st.subheader("Benchmark vs Industry")
    st.write(f"**Industry average:** {industry_avg} kgCO₂ / unit")
    st.write(f"**Your intensity:** {carbon_intensity:.2f} kgCO₂ / unit")

    st.success(
    "Improving your sustainability tier can increase your credibility with Novo Nordisk "
    "and unlock potential preferred-supplier status."
    )




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


st.subheader("Data Quality Overview")

if os.path.exists("supplier_data.csv"):
    reported_share = (df_all["Confidence"] == "High").mean() * 100
    st.write(f"**Reported data coverage:** {reported_share:.0f}%")

    st.subheader("Supplier Tiers Overview")
    tier_counts = df_all["Tier"].value_counts()
    st.bar_chart(tier_counts)

    st.subheader("Industry Emission Comparison")
    industry_avg = df_all.groupby("Industry")["Emissions_tCO2"].mean()
    st.bar_chart(industry_avg)
else:
    st.write("No supplier data submitted yet.")
    
st.markdown("<br>", unsafe_allow_html=True)


st.download_button(
    "Download supplier data",
    data=open("supplier_data.csv", "rb"),
    file_name="supplier_data.csv"
)

if st.button("Reset Portal / Clear Data"):
    if os.path.exists("supplier_data.csv"):
        os.remove("supplier_data.csv")
        st.success("Data cleared. The page will now refresh.")
    st.experimental_rerun()

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    **Scalable system for thousands of suppliers:**  
    - Automatically estimates missing emissions  
    - Calculates tiers in real-time  
    - Aggregates results for corporate dashboards  
    - Can integrate with ERP and supply chain systems
    """)



