import streamlit as st
import pandas as pd
import plotly.express as px
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_connection

st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="🛡️",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.warning("Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

conn = get_connection()
data = get_all_cyber_incidents(conn)

data["timestamp"] = pd.to_datetime(data["timestamp"])
data["month"] = data["timestamp"].dt.to_period("M").astype(str)

st.title("Cybersecurity Incident Dashboard 🛡️")
st.write("This dashboard analyses cyber incidents to identify phishing trends and operational bottlenecks.")

with st.sidebar:
    st.header("Filters")
    selected_severity = st.multiselect(
        "Select Severity",
        options=data["severity"].unique(),
        default=list(data["severity"].unique())
    )

    selected_status = st.multiselect(
        "Select Status",
        options=data["status"].unique(),
        default=list(data["status"].unique())
    )

filtered_data = data[
    (data["severity"].isin(selected_severity)) &
    (data["status"].isin(selected_status))
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Incidents", len(filtered_data))

with col2:
    phishing_count = len(filtered_data[filtered_data["category"] == "Phishing"])
    st.metric("Phishing Incidents", phishing_count)

with col3:
    open_count = len(filtered_data[filtered_data["status"] == "Open"])
    st.metric("Open Incidents", open_count)

st.subheader("1. Incident Count by Category")
category_counts = filtered_data["category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]
fig1 = px.bar(category_counts, x="Category", y="Count", title="Incident Count by Category")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2. Severity Distribution")
severity_counts = filtered_data["severity"].value_counts().reset_index()
severity_counts.columns = ["Severity", "Count"]
fig2 = px.pie(severity_counts, names="Severity", values="Count", title="Severity Distribution")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Phishing Trend Over Time")
phishing_data = filtered_data[filtered_data["category"] == "Phishing"]
phishing_monthly = phishing_data.groupby("month").size().reset_index(name="Count")
fig3 = px.line(phishing_monthly, x="month", y="Count", markers=True, title="Monthly Phishing Trend")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Open/Unresolved Cases by Category")
open_data = filtered_data[filtered_data["status"].isin(["Open", "In Progress"])]
open_counts = open_data["category"].value_counts().reset_index()
open_counts.columns = ["Category", "Count"]
fig4 = px.bar(open_counts, x="Category", y="Count", title="Open / In Progress Incidents by Category")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Key Insights")
if phishing_count > 0:
    st.success(
        "Phishing is the most important threat trend in this dataset and should be prioritised for monitoring and faster response."
    )

if not open_counts.empty:
    top_bottleneck = open_counts.iloc[0]["Category"]
    st.info(
        f"The current response bottleneck appears to be in the '{top_bottleneck}' category because it has the highest number of unresolved incidents."
    )

st.subheader("6. Incident Data Table")
st.dataframe(filtered_data, use_container_width=True)