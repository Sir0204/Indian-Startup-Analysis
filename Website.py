#### COMPANY POV
#1. Name
#2. Founders
#3.Industry
#4. Subindustry
#5. Location
#6. Funding Rounds-- stage,Investor,Date
#7. Similar Company

### INVESTOR POV
#1.NAme
#2. Recent investments
#3. Biggest Investments
#4. Generally invest in -- sector , stage , city
#5. YoY investment graphh
#6. Similar investors

#### GENERAL Analysis
#1. MoM chart - total + count
#2. Sector Analysis + max + Avg + total funded startups
#3. Type of funding
#4. City wise funding
#5. Top startups - year wise and overall


####### ---------- START ----------- ############

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='Indian Startup Analysis')   # use for config the page
df = pd.read_csv('Startup_clean_data.csv')


# convert date into datetime object
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
#st.dataframe(df)
  ## data clean for investors
#df['Investors Name'] = df['Investors Name'].fillna('not disclosed')  -- ab hta diya kyoki data cleaned kar liye hamne

def overall_analysis():

    st.title('Overall Analysis')

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    total = round(df['amount '].sum())

    with col1:
        st.metric('Total Funding', str(total) + ' CR')

    max_funding = df.groupby(
        'Startup Name'
    )['amount '].sum().max()

    with col2:
        st.metric('Max Funding', str(round(max_funding)) + ' CR')

    avg_funding = df.groupby(
        'Startup Name'
    )['amount '].sum().mean()

    with col3:
        st.metric('Average Funding', str(round(avg_funding)) + ' CR')

    total_startup = df['Startup Name'].nunique()

    with col4:
        st.metric('Total Funded Startup', total_startup)


    #  MoM Analysis

    st.subheader('MoM Analysis')

    select_option = st.selectbox(
        'Select Type',
        ['Total', 'Count']
    )

    if select_option == 'Total':

        temp_df = df.groupby(
            ['year', 'month']
        )['amount '].sum().reset_index()

    else:

        temp_df = df.groupby(
            ['year', 'month']
        )['amount '].count().reset_index()

    temp_df['x_axis'] = (
        temp_df['month'].astype(str)
        + '-'
        + temp_df['year'].astype(str)
    )

    fig, ax = plt.subplots()

    ax.plot(
        temp_df['x_axis'],
        temp_df['amount '],
        marker='o'
    )

    ax.set_xlabel('Month')
    ax.set_ylabel('Funding' if select_option == 'Total'
                  else 'Number of Deals')

    plt.xticks(rotation=90)

    st.pyplot(fig)
    #  Sector Analysis
    st.subheader('Sector Analysis')

    sector = df.groupby(
        'Vertical'
    )['amount '].agg(
        ['sum', 'mean', 'count']
    ).sort_values(
        'sum',
        ascending=False
    )

    sector.columns = [
        'Total Funding',
        'Average Funding',
        'Funding Count'
    ]

    st.dataframe(
        sector.head(10),
        use_container_width=True
    )


    #  Funding Type

    st.subheader('Type of Funding')

    funding_type = df.groupby(
        'round'
    )['amount '].sum().sort_values(
        ascending=False
    )

    st.bar_chart(funding_type)


    # City Wise Funding

    st.subheader('City Wise Funding')

    city = df.groupby(
        'City'
    )['amount '].sum().sort_values(
        ascending=False
    ).head(10)

    st.bar_chart(city)


    #  Top Startups

    st.subheader('Top Startups Overall')

    top_startups = df.groupby(
        'Startup Name'
    )['amount '].sum().sort_values(
        ascending=False
    ).head(10)

    st.dataframe(
        top_startups.reset_index(),
        use_container_width=True
    )


    # - Year Wise Top Startups -

    st.subheader('Top Startups - Year Wise')

    selected_year = st.selectbox(
        'Select Year',
        sorted(df['year'].dropna().unique())
    )

    year_data = df[
        df['year'] == selected_year
    ]

    top_year = year_data.groupby(
        'Startup Name'
    )['amount '].sum().sort_values(
        ascending=False
    ).head(10)

    st.dataframe(
        top_year.reset_index(),
        use_container_width=True
    )


def load_investor_details(investor):
    st.title(investor)


    # load the recent investments of investor

    last5_df = df[df['Investors Name'].str.contains(investor)].head()[['Date','Startup Name','Vertical','City','round','amount ']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2,col3 = st.columns(3)
    with col1:
        # biggest investments
        big_invest = df[df['Investors Name'].str.contains(investor)].groupby('Startup Name')[
            'amount '].sum().sort_values(ascending=False)
        st.subheader('Biggest Investments')
        st.dataframe(big_invest)
        st.subheader('visual of biggest investments')
        fig, ax = plt.subplots()
        ax.bar(big_invest.index, big_invest.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['Investors Name'].str.contains(investor)].groupby('Vertical')['amount '].sum()
        st.subheader('Sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index)
        st.pyplot(fig1)
    with col3:
        city_series = df[df['Investors Name'].str.contains(investor)].groupby('City')['amount '].sum()
        st.subheader('City investments')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index)
        st.pyplot(fig3)


    year_series = df[df['Investors Name'].str.contains(investor)].groupby('year')['amount '].sum()
    st.subheader('YoY Investments')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)

####  STARTUP #####

def startup_analysis(startup):

    temp = df[df['Startup Name'] == startup]

    st.title(startup)

    # Company details
    st.subheader("Company Details")

    col1, col2, col3, col4 = st.columns(4)

    col1.write("Industry")
    col1.write(temp['Vertical'].iloc[0])

    col2.write("SubIndustry")
    col2.write(temp['SubVertical'].iloc[0])

    col3.write("City")
    col3.write(temp['City'].iloc[0])

    col4.write("Founders")
    col4.write("Not available")

    # Funding
    st.subheader("Funding Details")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Funding",
        round(temp['amount '].sum(), 2),
        "CR"
    )

    col2.metric(
        "Funding Rounds",
        len(temp)
    )

    col3.metric(
        "Investors",
        temp['Investors Name'].nunique()
    )

    # Funding rounds
    st.subheader("Funding Rounds")

    st.dataframe(
        temp[['Date', 'round', 'amount ', 'Investors Name']],
        use_container_width=True
    )

    # Similar companies
    st.subheader("Similar Companies")

    similar = df[
        (df['Vertical'] == temp['Vertical'].iloc[0]) &
        (df['SubVertical'] == temp['SubVertical'].iloc[0]) &
        (df['Startup Name'] != startup)
    ]

    similar = similar.groupby('Startup Name')['amount '].sum()
    similar = similar.sort_values(ascending=False).head(10)

    st.dataframe(similar.reset_index())

    # Funding graph
    st.subheader("Funding Trend")

    graph = temp.sort_values('Date')

    fig, ax = plt.subplots()

    ax.plot(
        graph['Date'],
        graph['amount '],
        marker='o'
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox(
    "Select One",
    [
        "Overall Analysis",
        "Startup",
        "Investor"
    ]
)

if option == "Overall Analysis":
    overall_analysis()
elif option == "Startup":
    selected_startup = st.sidebar.selectbox(
        "Select Startup",
        sorted(df['Startup Name'].unique())
    )

    if st.sidebar.button("Find Startup"):

        startup_analysis(selected_startup)

else:
    selected_investor = st.sidebar.selectbox(
        "Select Investor",
        sorted(
            set(
                df['Investors Name']
                .dropna()
                .str.split(',')
                .sum()
            )
        )
    )

    if st.sidebar.button("Find Investor"):

        load_investor_details(selected_investor)

