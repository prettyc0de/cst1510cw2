import streamlit as st
import pandas as pd
import plotly.express as px
from app_model.db import get_connection
from app_model.metadatas import get_all_datasets_metadata

st.set_page_config(
    page_title="Data Science Dashboard",
    page_icon="📊",
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
data = get_all_datasets_metadata(conn)

data["upload_date"] = pd.to_datetime(data["upload_date"])
data["month"] = data["upload_date"].dt.to_period("M").astype(str)

st.title("Data Science Dashboard 📊")
st.write("This dashboard analyses uploaded datasets to support data governance, storage planning, and archive decisions.")

with st.sidebar:
    st.header("Filters")

    selected_uploaded_by = st.multiselect(
        "Uploaded By",
        options=data["uploaded_by"].unique(),
        default=list(data["uploaded_by"].unique())
    )

    min_rows = int(data["rows"].min())
    max_rows = int(data["rows"].max())

    row_range = st.slider(
        "Rows Range",
        min_value=min_rows,
        max_value=max_rows,
        value=(min_rows, max_rows)
    )

filtered_data = data[
    (data["uploaded_by"].isin(selected_uploaded_by)) &
    (data["rows"] >= row_range[0]) &
    (data["rows"] <= row_range[1])
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Datasets", len(filtered_data))

with col2:
    st.metric("Total Rows", int(filtered_data["rows"].sum()))

with col3:
    st.metric("Average Columns", round(filtered_data["columns"].mean(), 2))

st.subheader("1. Dataset Rows by Dataset Name")
fig1 = px.bar(
    filtered_data,
    x="name",
    y="rows",
    title="Rows by Dataset",
    text="rows"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2. Dataset Columns by Dataset Name")
fig2 = px.bar(
    filtered_data,
    x="name",
    y="columns",
    title="Columns by Dataset",
    text="columns"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Upload Activity Over Time")
monthly_uploads = filtered_data.groupby("month").size().reset_index(name="count")
fig3 = px.line(
    monthly_uploads,
    x="month",
    y="count",
    markers=True,
    title="Dataset Upload Trend"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Dataset Ownership Distribution")
owner_counts = filtered_data["uploaded_by"].value_counts().reset_index()
owner_counts.columns = ["uploaded_by", "count"]
fig4 = px.pie(
    owner_counts,
    names="uploaded_by",
    values="count",
    title="Datasets by Uploaded By"
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Governance Insights")

largest_dataset = filtered_data.sort_values("rows", ascending=False).iloc[0]["name"]
largest_rows = int(filtered_data.sort_values("rows", ascending=False).iloc[0]["rows"])

st.info(
    f"The largest dataset in the current filtered view is '{largest_dataset}' with {largest_rows} rows. "
    f"This dataset may require stronger storage planning, validation, or archiving review."
)

top_owner = filtered_data["uploaded_by"].value_counts().idxmax()
st.success(
    f"The main dependency appears to be on '{top_owner}', because this uploader owns the highest number of datasets "
    f"in the current view."
)

st.write("Recommended governance actions:")
st.write("- Review very large datasets for storage efficiency.")
st.write("- Monitor departments or users uploading the most datasets.")
st.write("- Archive old or low-priority datasets where appropriate.")
st.write("- Apply regular validation checks before long-term storage.")

st.subheader("6. Dataset Metadata Table")
st.dataframe(filtered_data, use_container_width=True)