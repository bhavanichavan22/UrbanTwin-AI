import json
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from urbantwin.simulation import run_simulation
from urbantwin.recommendations import recommend
from urbantwin.ai_engine import analyse_with_ai
from urbantwin.database import init_db, save_scenario, list_scenarios, get_scenario, delete_scenario
from urbantwin.report import build_pdf_report

st.set_page_config(page_title="UrbanTwin AI", page_icon="🏙️", layout="wide", initial_sidebar_state="expanded")
init_db()

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#f4f8fc 0%,#eef4f8 100%);}
.block-container {padding-top:1.3rem; max-width:1450px;}
.hero {padding:1.35rem 1.6rem;border-radius:18px;background:linear-gradient(110deg,#102a43,#176b87);color:white;margin-bottom:1rem;box-shadow:0 8px 24px #173f6720;}
.hero h1 {color:white;font-size:2.1rem;margin:0;}
.hero p {color:#d8edf5;margin:.35rem 0 0;}
div[data-testid="stMetric"] {background:white;border:1px solid #dce7ef;padding:14px;border-radius:13px;box-shadow:0 3px 10px #163b5509;}
section[data-testid="stSidebar"] {background:#eaf1f6;}
.small-note {color:#587080;font-size:.85rem;}
</style>
<div class="hero"><h1>🏙️ UrbanTwin AI</h1><p>Simulate Today. Shape Tomorrow. &nbsp; | &nbsp; Smart City Scenario Simulator</p></div>
""", unsafe_allow_html=True)

st.sidebar.title("UrbanTwin AI")
page = st.sidebar.radio("Navigation", ["City Dashboard", "Scenario Simulator", "Scenario History", "About & Help"])
st.sidebar.caption("Academic prototype • illustrative scenario models")

def render_metrics(result):
    cols = st.columns(3)
    cols[0].metric("Baseline", f'{result["baseline"]:.1f} {result["unit"]}')
    cols[1].metric("Projected", f'{result["projected"]:.1f} {result["unit"]}', delta=f'{result["change"]:+.1f} {result["unit"]}')
    cols[2].metric("Status", result["severity"])

def scenario_form():
    category = st.selectbox("Select urban challenge", ["Traffic Congestion", "Water Shortage", "Waste Accumulation"])
    with st.form("scenario_form"):
        name = st.text_input("Scenario name", value=f"{category} scenario")
        st.markdown("#### Configure city conditions")
        if category == "Traffic Congestion":
            c1,c2,c3 = st.columns(3)
            vehicles = c1.number_input("Vehicles per hour", 100, 50000, 8500, 100)
            capacity = c2.number_input("Road capacity / hour", 100, 50000, 6000, 100)
            population = c3.number_input("Population density (people/km²)", 100, 100000, 12000, 500)
            c4,c5,c6 = st.columns(3)
            transit = c4.slider("Public transport usage (%)", 0, 100, 28)
            signals = c5.slider("Smart signal improvement (%)", 0, 60, 15)
            road = c6.slider("Road capacity expansion (%)", 0, 50, 0)
            carpool = st.slider("Carpool / private vehicle reduction (%)", 0, 50, 5)
            params = dict(vehicles=vehicles, capacity=capacity, population_density=population,
                          public_transport_usage=transit, smart_signals=signals,
                          road_expansion=road, carpool_reduction=carpool)
            interventions = {"public_transport": transit, "smart_signals": signals,
                             "road_expansion": road, "carpool_reduction": carpool}
        elif category == "Water Shortage":
            c1,c2,c3 = st.columns(3)
            demand = c1.number_input("Daily water demand (MLD)", 1.0, 2000.0, 180.0, 5.0)
            supply = c2.number_input("Available water supply (MLD)", 1.0, 2000.0, 145.0, 5.0)
            reservoir = c3.slider("Reservoir availability (%)", 0, 100, 65)
            c4,c5,c6 = st.columns(3)
            population = c4.number_input("Population", 1000, 50000000, 850000, 10000)
            consumption = c5.number_input("Consumption (litres/person/day)", 20.0, 500.0, 135.0, 5.0)
            conservation = c6.slider("Water conservation (%)", 0, 60, 10)
            rain = st.slider("Rainwater harvesting contribution (%)", 0, 60, 12)
            leakage = st.slider("Distribution leakage reduction (%)", 0, 60, 10)
            params = dict(demand_mld=demand, supply_mld=supply, reservoir_availability=reservoir,
                          population=population, consumption_lpcd=consumption,
                          conservation=conservation, rainwater=rain, leakage_reduction=leakage)
            interventions = {"conservation": conservation, "rainwater": rain, "leakage_reduction": leakage}
        else:
            c1,c2,c3 = st.columns(3)
            generated = c1.number_input("Daily waste generation (tonnes)", 1.0, 10000.0, 350.0, 10.0)
            capacity = c2.number_input("Collection capacity (tonnes/day)", 1.0, 10000.0, 270.0, 10.0)
            population = c3.number_input("Population", 1000, 50000000, 850000, 10000)
            c4,c5,c6 = st.columns(3)
            recycling = c4.slider("Recycling rate (%)", 0, 90, 18)
            segregation = c5.slider("Waste segregation improvement (%)", 0, 80, 20)
            efficiency = c6.slider("Collection efficiency improvement (%)", 0, 80, 15)
            composting = st.slider("Composting / organic diversion (%)", 0, 80, 15)
            params = dict(waste_tpd=generated, collection_capacity=capacity, population=population,
                          recycling=recycling, segregation=segregation, collection_efficiency=efficiency,
                          composting=composting)
            interventions = {"recycling": recycling, "segregation": segregation,
                             "collection_efficiency": efficiency, "composting": composting}
        submitted = st.form_submit_button("▶ Run scenario", type="primary", use_container_width=True)
    if submitted:
        result = run_simulation(category, params)
        result["recommendations"] = recommend(category, result, params)
        ai_text = analyse_with_ai(category, params, result)
        result["ai_analysis"] = ai_text
        result["problem_description"] = result["explanation"]
        sid = save_scenario(name or category, category, params, result)
        st.session_state["active_scenario_id"] = sid
        st.session_state["active_scenario"] = {"name": name, "category": category, "params": params, "result": result}
        st.success(f"Scenario saved successfully (ID: {sid}).")
    return category

def show_result(item):
    result = item["result"]
    st.subheader(f'📍 {item["name"]}')
    st.caption(item["category"])
    render_metrics(result)
    st.info(result["explanation"])
    df = pd.DataFrame({"Stage":["Baseline","After interventions"],"Value":[result["baseline"],result["projected"]]})
    fig = px.bar(df,x="Stage",y="Value",color="Stage",text_auto=".2f",
                 title=f'{result["metric"]} — before and after')
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("#### Input parameters")
    st.json(item["params"])
    st.markdown("#### AI scenario analysis")
    st.markdown(result.get("ai_analysis","AI analysis unavailable."))
    st.markdown("#### Prioritised recommendations")
    for i, rec in enumerate(result.get("recommendations",[]),1):
        st.markdown(f"**{i}. {rec['title']}** — {rec['reason']}")
    st.caption("Estimates are generated from simplified assumptions and illustrative inputs. Validate with local data and domain experts.")
    pdf = build_pdf_report(item["name"], item["category"], item["params"], result)
    st.download_button("⬇ Download scenario report (PDF)", pdf,
                       file_name=f"UrbanTwin_{item['category'].replace(' ','_')}_report.pdf",
                       mime="application/pdf")

if page == "City Dashboard":
    st.subheader("City overview")
    history = list_scenarios(limit=100)
    total = len(history)
    counts = {x: sum(1 for row in history if row["category"] == x) for x in
              ["Traffic Congestion","Water Shortage","Waste Accumulation"]}
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Saved scenarios", total)
    c2.metric("Traffic scenarios", counts["Traffic Congestion"])
    c3.metric("Water scenarios", counts["Water Shortage"])
    c4.metric("Waste scenarios", counts["Waste Accumulation"])
    st.markdown("### Urban service indicators")
    st.caption("These are latest saved simulation outcomes, not live sensor readings.")
    latest = {}
    for row in history:
        latest.setdefault(row["category"], row)
    cols = st.columns(3)
    for col, cat in zip(cols, ["Traffic Congestion","Water Shortage","Waste Accumulation"]):
        row = latest.get(cat)
        with col:
            st.markdown(f"**{cat}**")
            if row:
                res = row["result"]
                st.metric(res["metric"], f'{res["projected"]:.1f} {res["unit"]}', delta=f'{res["change"]:+.1f}')
                st.caption(f'Latest: {row["created_at"]}')
            else:
                st.info("No saved scenario yet.")
    if history:
        st.markdown("### Scenario activity")
        chart = pd.DataFrame([{"Category":r["category"],"Scenario":r["name"],"Created":r["created_at"]} for r in history])
        st.plotly_chart(px.histogram(chart,x="Category",color="Category",title="Saved scenarios by category"),use_container_width=True)
        st.markdown("### Recent scenarios")
        st.dataframe(pd.DataFrame([{"ID":r["id"],"Name":r["name"],"Category":r["category"],"Created":r["created_at"],"Severity":r["result"]["severity"]} for r in history[:10]]),use_container_width=True,hide_index=True)
    else:
        st.info("Run your first simulation from the Scenario Simulator page.")

elif page == "Scenario Simulator":
    st.subheader("Scenario simulator")
    st.write("Change the inputs, choose interventions and run a hypothetical urban scenario.")
    scenario_form()
    active = st.session_state.get("active_scenario")
    if active:
        st.divider()
        show_result(active)

elif page == "Scenario History":
    st.subheader("Saved scenario history")
    history = list_scenarios(limit=250)
    if not history:
        st.info("No scenarios saved yet. Run a simulation first.")
    else:
        df = pd.DataFrame([{"ID":r["id"],"Name":r["name"],"Category":r["category"],"Created":r["created_at"],"Baseline":r["result"]["baseline"],"Projected":r["result"]["projected"],"Severity":r["result"]["severity"]} for r in history])
        st.dataframe(df,use_container_width=True,hide_index=True)
        ids = [r["id"] for r in history]
        selected = st.selectbox("Select scenario to inspect or delete",ids,format_func=lambda x: f'#{x} — {next(r["name"] for r in history if r["id"]==x)}')
        item = get_scenario(selected)
        if item:
            show_result(item)
            if st.button("🗑 Delete selected scenario"):
                delete_scenario(selected)
                st.success("Scenario deleted.")
                st.rerun()
        st.markdown("### Compare saved scenarios")
        if len(ids) >= 2:
            chosen = st.multiselect("Choose two or more scenarios",ids,default=ids[:2],
                                    format_func=lambda x: f'#{x} — {next(r["name"] for r in history if r["id"]==x)}')
            if len(chosen) >= 2:
                compare = []
                for sid in chosen:
                    r = get_scenario(sid)
                    compare.append({"Scenario":r["name"],"Category":r["category"],"Metric":r["result"]["metric"],
                                    "Baseline":r["result"]["baseline"],"Projected":r["result"]["projected"],
                                    "Severity":r["result"]["severity"]})
                st.dataframe(pd.DataFrame(compare),use_container_width=True,hide_index=True)
                st.caption("Compare values within the same category and metric for meaningful numerical comparison.")
        else:
            st.caption("Save at least two scenarios to compare them.")

else:
    st.subheader("About UrbanTwin AI")
    st.markdown("""
**UrbanTwin AI – Smart City Scenario Simulator** demonstrates a digital-twin-inspired approach to exploring urban challenges.

**Technology:** Python, Streamlit, Pandas, NumPy, Plotly, SQLite, Gemini API (optional), ReportLab.

**Modules:** City dashboard, traffic simulator, water simulator, waste simulator, AI analysis, recommendation engine, scenario history and PDF report generation.

**Important academic scope:** This project uses simplified mathematical models and user-entered sample values. It is not connected to live city infrastructure, and its outputs are not engineering forecasts or official municipal advice.
""")
    with st.expander("How to configure Gemini"):
        st.code("GEMINI_API_KEY=your_api_key_here\nGEMINI_MODEL=gemini-2.5-flash",language="bash")
        st.write("Copy `.env.example` to `.env`, add your key, then restart Streamlit. Never upload your key to GitHub.")
