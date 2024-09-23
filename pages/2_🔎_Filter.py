import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🔎 Filter")
st.markdown("##")

# ----- SIDEBAR -----
st.sidebar.header("Please Filter Here:")

@st.cache_data
def get_dataset():
    data = pd.read_csv("CustomerChurn.csv")
    return data

data = get_dataset()

# Filter for Payment Method
payment_method = st.sidebar.multiselect(
    "Select the Payment Method:",
    options = data["Payment Method"].unique(),
    default = data["Payment Method"].unique()
)

# Filter for Senior Citizen
senior_citizen = st.sidebar.multiselect(
    "Select the Senior Citizen Status:",
    options = data["Senior Citizen"].unique(),
    default = data["Senior Citizen"].unique()
)

# Filter for Partner
partner = st.sidebar.multiselect(
    "Select the Partner Status:",
    options = data["Partner"].unique(),
    default = data["Partner"].unique()
)

# Filter for Dependents
dependents = st.sidebar.multiselect(
    "Select Dependents Status:",
    options = data["Dependents"].unique(),
    default = data["Dependents"].unique()
)

# Filter for Internet Service
internet_service = st.sidebar.multiselect(
    "Select Internet Service Type:",
    options = data["Internet Service"].unique(),
    default = data["Internet Service"].unique()
)

# Filter for Contract Type
contract_type = st.sidebar.multiselect(
    "Select Contract Type:",
    options = data["Contract"].unique(),
    default = data["Contract"].unique()
)

# Filter for Monthly Charges (You can customize the range)
monthly_charges = st.sidebar.slider(
    "Select Monthly Charges Range:",
    min_value=float(data["Monthly Charges"].min()),
    max_value=float(data["Monthly Charges"].max()),
    value=(float(data["Monthly Charges"].min()), float(data["Monthly Charges"].max()))
)

# Filter for Monthly Charges (You can customize the range)
tenure = st.sidebar.slider(
    "Select Tenure Range:",
    min_value=float(data["Tenure"].min()),
    max_value=float(data["Tenure"].max()),
    value=(float(data["Tenure"].min()), float(data["Tenure"].max()))
)

# Apply filters
filtered_data = data.copy()

if payment_method:
    filtered_data = filtered_data[filtered_data["Payment Method"].isin(payment_method)]

if senior_citizen:
    filtered_data = filtered_data[filtered_data["Senior Citizen"].isin(senior_citizen)]

if partner:
    filtered_data = filtered_data[filtered_data["Partner"].isin(partner)]

if dependents:
    filtered_data = filtered_data[filtered_data["Dependents"].isin(dependents)]

if internet_service:
    filtered_data = filtered_data[filtered_data["Internet Service"].isin(internet_service)]

if contract_type:
    filtered_data = filtered_data[filtered_data["Contract"].isin(contract_type)]

filtered_data = filtered_data[
    (filtered_data["Monthly Charges"] >= monthly_charges[0]) & 
    (filtered_data["Monthly Charges"] <= monthly_charges[1])
]

filtered_data = filtered_data[
    (filtered_data["Tenure"] >= tenure[0]) & 
    (filtered_data["Tenure"] <= tenure[1])
]

# ----- Search Bar -----

# Create a search bar
search_query = st.text_input("**Search any keyword:**")

# Filter the DataFrame based on the search query
if search_query:
    # Convert all columns to string and check if the search query is in any of them
    filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
else:
    filtered_data = data

# Display the filtered DataFrame
st.dataframe(filtered_data)