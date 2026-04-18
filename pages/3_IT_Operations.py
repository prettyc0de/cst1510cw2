import streamlit as st
import pandas as pd
import plotly.express as px
from app_model.db import get_connection
from app_model.it_tickets import get_all_it_tickets

st.set_page_config(
    page_title="IT Operations Dashboard",
    page_icon="🖥️",
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
data = get_all_it_tickets(conn)

data["created_at"] = pd.to_datetime(data["created_at"])
data["month"] = data["created_at"].dt.to_period("M").astype(str)

st.title("IT Operations Dashboard 🖥️")
st.write("This dashboard analyses IT support tickets to identify delays, staff workload, and process bottlenecks.")

with st.sidebar:
    st.header("Filters")

    selected_priority = st.multiselect(
        "Select Priority",
        options=data["priority"].unique(),
        default=list(data["priority"].unique())
    )

    selected_status = st.multiselect(
        "Select Status",
        options=data["status"].unique(),
        default=list(data["status"].unique())
    )

filtered_data = data[
    (data["priority"].isin(selected_priority)) &
    (data["status"].isin(selected_status))
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tickets", len(filtered_data))

with col2:
    st.metric("Average Resolution Time", round(filtered_data["resolution_time_hours"].mean(), 2))

with col3:
    open_count = len(filtered_data[filtered_data["status"] == "Open"])
    st.metric("Open Tickets", open_count)

st.subheader("1. Tickets by Status")
status_counts = filtered_data["status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig1 = px.bar(status_counts, x="Status", y="Count", title="Ticket Count by Status")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2. Average Resolution Time by Staff")
staff_time = filtered_data.groupby("assigned_to")["resolution_time_hours"].mean().reset_index()
fig2 = px.bar(
    staff_time,
    x="assigned_to",
    y="resolution_time_hours",
    title="Average Resolution Time by Staff",
    text="resolution_time_hours"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Ticket Priority Distribution")
priority_counts = filtered_data["priority"].value_counts().reset_index()
priority_counts.columns = ["Priority", "Count"]
fig3 = px.pie(priority_counts, names="Priority", values="Count", title="Priority Distribution")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Ticket Creation Trend Over Time")
monthly_tickets = filtered_data.groupby("month").size().reset_index(name="Count")
fig4 = px.line(monthly_tickets, x="month", y="Count", markers=True, title="Ticket Trend Over Time")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Operational Insights")

slowest_staff = staff_time.sort_values("resolution_time_hours", ascending=False).iloc[0]["assigned_to"]
slowest_time = round(staff_time.sort_values("resolution_time_hours", ascending=False).iloc[0]["resolution_time_hours"], 2)

st.info(
    f"The staff member with the highest average resolution time is '{slowest_staff}' at {slowest_time} hours. "
    f"This may indicate a workload issue or performance bottleneck."
)

top_status = filtered_data["status"].value_counts().idxmax()
st.success(
    f"The most common ticket status is '{top_status}'. This suggests that this stage should be reviewed for process efficiency."
)

st.write("Recommended actions:")
st.write("- Review staff workload and ticket assignment balance.")
st.write("- Monitor long-resolution tickets more closely.")
st.write("- Investigate the most common ticket status for process delays.")
st.write("- Prioritise high and critical tickets for faster handling.")

st.subheader("6. IT Ticket Table")
st.dataframe(filtered_data, use_container_width=True)