import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
import matplotlib.pyplot as plt
import seaborn as sns

# read csv from a git hub repo and assign variable values
final_df = pd.read_csv("output.csv")

## fill na with delhi
final_df["State"] = final_df["State"].fillna("Delhi")
final_df["Days"] = final_df['Days'].fillna("2")
final_df = final_df.rename(columns={'Days': 'Days Posted Back'})

## Replace the strings
index1 = final_df['Platform'].value_counts().index
elements = [' LinkedIn', ' Www.foundit.in']

for x in index1:
    if x not in elements:
        final_df['Platform'] = final_df['Platform'].replace(x, 'Company Website(s)')

final_df['Platform'] = final_df['Platform'].replace(' Www.foundit.in', 'foundit')
##########################################################################################
st.set_page_config(
    page_title='Business Analyst Job Analytics Dashboard',
    layout='wide'
)

# dashboard title
st.title("Business Analyst Jobs Analytics Basic Dashboard")
st.markdown("###### This below results displayed based on live data fetched from Google Jobs API and captured data from (16/11/2022) to (18/12/2022)")
st.markdown("###### Tech Stack used: Google Jobs API, Python and libraries, AWS RDS and SQL Server for storing data, Git and Github for version control, Streamlit and Render for Web app and for deployments")
st.markdown("##### About mywork")
st.markdown("###### As I am still in early stages of learning, I preferred trying to fetch real time data instead of kaggle and trying to learn by doing.")
st.markdown("###### I am planning to add more features like analyzing salaries, years of exp by using NLP. But need to start learning NLP.")

# # top-level filters
job_filter = st.selectbox("Select the Job Title", pd.unique(final_df['Title']))
#
# # creating a single-element container.
placeholder = st.empty()
#
# dataframe filter
final_df1 = final_df[final_df['Title'] == job_filter]

index = final_df1['Platform'].value_counts().index
plat_val = final_df1['Platform'].value_counts().values

# creating KPIs
Number_of_Jobs = final_df1.groupby(['State', 'Platform', 'Days Posted Back']).size().sum()

with placeholder.container():
    # create one column
    kpi1 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    st.metric(label="Total Number of Jobs ⏳", value=int(Number_of_Jobs))
    # kpi2.metric(label="Married Count 💍", value=int(count_married), delta=- 10 + count_married)
    # kpi3.metric(label="A/C Balance ＄", value=f"$ {round(balance, 2)} ", delta=- round(balance / count_married) * 100)

    # create two columns for charts

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Number of new jobs posted in respective states")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(x="State", data=final_df1)
        st.pyplot(fig)

    with fig_col2:
        st.markdown("### Platform Based")
        fig2 = plt.figure(figsize=(4, 3))
        plt.pie(plat_val, labels=index, autopct='%1.2f%%')
        st.write(fig2)

    st.markdown("### Detailed Data View")
    # Check if the resulting dataset is empty
    if final_df.empty:
        st.write("No results found.")
    else:
        # Display the filtered dataset
        st.dataframe(final_df1)
    # time.sleep(1)
    # Create a form to collect user feedback

    st.markdown("### Feedback form")
    feedback_form = st.form(key='feedback_form')
    name = st.text_input('Name')
    email = st.text_input('Email')
    feedback = st.text_area('Feedback')

    # Create a submit button
    if st.button('Submit'):
        # Display the collected feedback in the app
        st.sidebar.success(f'Thanks for your feedback, {name}!')
        st.sidebar.write('---')
        st.sidebar.write(f'Name: {name}')
        st.sidebar.write(f'Email: {email}')
        st.sidebar.write(f'Feedback: {feedback}')
    # placeholder.empty()
