# FYP: Integrating Machine Learning Analytics with Interactive Visualization for Telecom Churn Prediction
# NAME: LAI LI SYUEN TP060921
# APD3F2402CS(DA)
# ASIA PACIFIC UNIVERSITY
# References: https://www.youtube.com/@CodingIsFun


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
# import matplotlib.pyplot as plt # pip install matplotlib
# import seaborn as sns # pip install seaborn

st.set_page_config(page_title = "Teleco Churn Prediction",
                   page_icon=":bar_chart:",
                   layout="wide"
)

@st.cache_data
def get_dataset():
    data = pd.read_csv("CustomerChurn.csv")
    return data

data = get_dataset()

# Streamlit app header
st.title(":bar_chart: Telecom Churn Dataset Analysis")
st.markdown("##")

# AVG Monthly & Total Charges
# Convert 'Total Charges' to numeric, coercing errors
data['Total Charges'] = pd.to_numeric(data['Total Charges'], errors='coerce')
average_monthly_charges = round(data["Monthly Charges"].mean(),2)
average_total_charges = round(data["Total Charges"].mean(),2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Average Monthly Charges:")
    st.subheader(f"US $ {average_monthly_charges:,}")
with right_column:
    st.subheader("Average Total Charges:")
    st.subheader(f"US $ {average_total_charges:,}")

st.markdown("---")

# ----- SIDEBAR -----
st.sidebar.success("Select a page above.")

# Tenure by Churn
fig_tenure_churn = px.box(
    data,
    x="Churn",
    y="Tenure",
    title="<b> Box Plot of Tenure by Churn <b>",
    color="Churn",
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig_tenure_churn)

# Types of Payment Method
# Count the occurrences of each payment method
payment_counts = data['Payment Method'].value_counts().reset_index()
payment_counts.columns = ['Payment Method', 'Count']
# Calculate the percentage of each payment method
total_count = payment_counts['Count'].sum()
payment_counts['Percentage'] = (payment_counts['Count'] / total_count) * 100

# Plotting
fig_payment_method_churn = px.bar(
    payment_counts,
    y='Payment Method',
    x='Count',
    title="<b> Distribution of Payment Methods <b>",
    color='Count',
    color_continuous_scale=px.colors.sequential.Blues,  # Different shades of blue
    template="plotly_white"
)

# Add percentage text on top of bars
for i, row in payment_counts.iterrows():
    fig_payment_method_churn.add_annotation(
        y=row['Payment Method'],
        x=row['Count'],
        text=f"{row['Percentage']:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black"),
        yshift=5  # Adjust the position of the text
    )

# Display the plot in Streamlit
st.plotly_chart(fig_payment_method_churn)

# Count the occurrences of each contract type
contract_counts = data['Contract'].value_counts().reset_index()
contract_counts.columns = ['Contract', 'Count']

# Plotting the pie chart
fig_contract = px.pie(
    contract_counts,
    values='Count',
    names='Contract',
    title="<b> Contract Distribution <b>",
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig_contract)

# Grouping data by 'Internet Service' and 'Churn' to get the counts
internet_churn_counts = data.groupby(['Internet Service', 'Churn']).size().unstack(fill_value=0)

# Resetting the index for plotting
internet_churn_counts = internet_churn_counts.reset_index()

# Melting the DataFrame for Plotly
melted_counts = internet_churn_counts.melt(id_vars='Internet Service', var_name='Churn', value_name='Count')

# Plotting the stacked bar chart using Plotly
fig_internet_churn = px.bar(
    melted_counts,
    x='Internet Service',
    y='Count',
    color='Churn',
    title='Relationship between Internet Service and Customer Churn',
    labels={'Count': 'Number of Customers'},
    color_discrete_sequence=['blue', 'red'],
    text='Count'  # Adding text labels directly from the melted DataFrame
)

# Update layout for better readability
fig_internet_churn.update_layout(
    xaxis_title='Internet Service',
    yaxis_title='Number of Customers',
    barmode='stack'
)

# Display the plot in Streamlit
st.plotly_chart(fig_internet_churn)

# Embed Power BI dashboard
power_bi_embed_url = "https://app.powerbi.com/view?r=eyJrIjoiODcwZWM3MjAtZTQzMy00ZjMzLThiZDAtYzJkMDQxZjVjNmZiIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9"  # Replace with your Power BI embed URL

# Create an iframe to embed the Power BI report
st.markdown(
    f"""
    <iframe 
        src="{power_bi_embed_url}" 
        width="100%" 
        height="600" 
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
    """,
    unsafe_allow_html=True
)
