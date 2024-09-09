import streamlit as st
import pandas as pd
import plotly.express as px

# Load the monetary funding data CSV file
funding_data = pd.read_csv('all_quantitative_research.csv')

# Load the studies CSV file
studies_data = pd.read_csv('studies.csv')

# Store the original funder names and company names
funding_data['Original Funder'] = funding_data['Funder']
funding_data['Company Name'] = funding_data['Company Name']
studies_data['Original Funder'] = studies_data['Funder']

# Clean 'Donation Amount' by removing commas and converting to numeric
funding_data['Donation Amount'] = pd.to_numeric(funding_data['Donation Amount'].str.replace(',', ''), errors='coerce')

# Convert 'Year' to a datetime object and extract the year as a 4-digit number
funding_data['Year'] = pd.to_datetime(funding_data['Year'], format='%Y', errors='coerce').dt.year
studies_data['Year'] = pd.to_datetime(studies_data['Year'], format='%Y', errors='coerce').dt.year

# Replace NA values with blank
funding_data = funding_data.fillna('')
studies_data = studies_data.fillna('')

# Concatenate 'Columbia school?' and 'Which Specific Columbia Program?' for display
funding_data['School and Program'] = funding_data['Columbia school?']
funding_data['School and Program'] = funding_data.apply(
    lambda row: f"{row['Columbia school?']}, {row['Which Specific Columbia Program?']}"
    if row['Which Specific Columbia Program?'] else row['Columbia school?'],
    axis=1
)

# Normalize company names for matching, but use the original case for display
funding_data['Normalized Company Name'] = funding_data['Company Name'].str.lower().str.strip()
studies_data['Company Name'] = studies_data['Funder'].str.lower().str.strip()

# Streamlit app title
st.title('Fossil Fuel Funding of Columbia Climate Research Data Visualization')

# Sidebar filters
st.sidebar.subheader('Filter by Year Range')
year_min = funding_data['Year'].min()
year_max = funding_data['Year'].max()
selected_years = st.sidebar.slider(
    'Select Year Range',
    min_value=int(year_min),
    max_value=int(year_max),
    value=(int(year_min), int(year_max))
)

# Select specific companies to view using "Company Name"
st.sidebar.subheader('Filter by Funder')
company_names = list(funding_data['Company Name'].unique())
company_names.insert(0, "All")  # Add "All" option

selected_company_names = st.sidebar.multiselect('Select Funders', company_names, ["All"])

# If "All" is selected, select all companies
if "All" in selected_company_names:
    selected_company_names = company_names[1:]  # Exclude "All"

# Filter funding data based on selected years and company names
filtered_funding_data = funding_data[
    (funding_data['Year'] >= selected_years[0]) &
    (funding_data['Year'] <= selected_years[1]) &
    (funding_data['Company Name'].isin(selected_company_names))
]

# Sidebar filter for Columbia school and program
st.sidebar.subheader('Filter by Recipient')
school_program_options = list(funding_data['School and Program'].unique())
school_program_options.insert(0, "All")  # Add "All" option

selected_school_programs = st.sidebar.multiselect('Select School/Program', school_program_options, ["All"])

# If "All" is selected, select all school/program options
if "All" in selected_school_programs:
    selected_school_programs = school_program_options[1:]  # Exclude "All"

# Adjust filter logic to include schools with and without specific programs
filtered_funding_data = filtered_funding_data[
    filtered_funding_data['School and Program'].apply(lambda x: any(school_program in x for school_program in selected_school_programs))
]

# Calculate total funding for the filtered data
total_funding = filtered_funding_data['Donation Amount'].sum()

# Display dynamically updated data preview with additional details
st.write("Data Preview (Filtered):")
filtered_funding_data_display = filtered_funding_data[['Company Name', 'Original Funder', 'Donation Amount', 'Year', 'School and Program', 'Source', 'Notes']].round(2)
filtered_funding_data_display['Year'] = filtered_funding_data_display['Year'].astype(str)  # Convert 'Year' to string to avoid commas
filtered_funding_data_display.index = range(1, len(filtered_funding_data_display) + 1)  # Start numbering at 1
st.dataframe(filtered_funding_data_display)

# Visualize funding by selected companies over time (by "Company Name" now)
st.subheader('Funding by Selected Funders for Selected Recipients Over Time')
funder_chart = px.bar(
    filtered_funding_data,
    x='Year',
    y='Donation Amount',
    color='Company Name',  # Changed to group by company name
    title=f'Funding by Selected Funders for Selected Recipients Over Time ({selected_years[0]} - {selected_years[1]}) - Total: ${total_funding:,.2f}',
    labels={'Year': 'Year', 'Donation Amount': 'Donation Amount', 'Company Name': 'Company'},
    template='plotly_white'
)
funder_chart.update_layout(
    font=dict(
        family="Helvetica, Arial, sans-serif",
        size=14,
        color="Black"
    ),
    xaxis_title='Year',
    yaxis_title='Donation Amount'
)
st.plotly_chart(funder_chart, use_container_width=True)

# Visualize total funding over time
st.subheader('Total Funding Over Time')
funding_over_time = filtered_funding_data.groupby('Year')['Donation Amount'].sum().reset_index()

# Check if there are enough data points for a line chart
if len(funding_over_time) > 1:
    fig = px.line(
        funding_over_time,
        x='Year',
        y='Donation Amount',
        title=f'Total Funding Over Time ({selected_years[0]} - {selected_years[1]}) - Total: ${total_funding:,.2f}',
        labels={'Year': 'Year', 'Donation Amount': 'Donation Amount'},
        template='plotly_white'
    )
else:
    fig = px.scatter(
        funding_over_time,
        x='Year',
        y='Donation Amount',
        title=f'Total Funding Over Time ({selected_years[0]} - {selected_years[1]}) - Total: ${total_funding:,.2f}',
        labels={'Year': 'Year', 'Donation Amount': 'Donation Amount'},
        template='plotly_white'
    )

fig.update_layout(
    font=dict(
        family="Helvetica, Arial, sans-serif",
        size=14,
        color="Black"
    ),
    xaxis_title='Year',
    yaxis_title='Donation Amount'
)
st.plotly_chart(fig, use_container_width=True)

# Display top companies and calculate total for those companies
st.subheader('Top Funders in Selected Range for Selected Recipients')
top_companies = filtered_funding_data.groupby('Company Name')['Donation Amount'].sum().nlargest(10).reset_index()
top_n = len(top_companies)  # Number of companies displayed
top_companies_total = top_companies['Donation Amount'].sum()
top_companies_chart = px.bar(
    top_companies,
    x='Donation Amount',
    y='Company Name',
    title=f'Top {top_n} Funders in Selected Range for Selected Recipients - Total: ${top_companies_total:,.2f}',
    orientation='h',
    labels={'Donation Amount': 'Donation Amount', 'Company Name': 'Funder'},
    template='plotly_white'
)
top_companies_chart.update_layout(
    font=dict(
        family="Helvetica, Arial, sans-serif",
        size=14,
        color="Black"
    ),
    xaxis_title='Donation Amount',
    yaxis_title='Funder'
)
st.plotly_chart(top_companies_chart, use_container_width=True)

# Calculate top recipients based on the sum of 'Donation Amount'
top_recipients = filtered_funding_data.groupby('School and Program')['Donation Amount'].sum().nlargest(10).reset_index()
top_recipient_n = len(top_recipients)
top_recipients_total = top_recipients['Donation Amount'].sum()

# Create a bar chart to visualize the top recipients
st.subheader('Top Recipients in Selected Range')
top_recipients_chart = px.bar(
    top_recipients,
    x='Donation Amount',
    y='School and Program',
    title=f'Top {top_recipient_n} Recipients in Selected Range<br>Total: ${top_recipients_total:,.2f}',
    orientation='h',
    labels={'Donation Amount': 'Donation Amount', 'School and Program': 'Recipient'},
    template='plotly_white'
)

# Adjust the layout to handle long titles
top_recipients_chart.update_layout(
    font=dict(
        family="Helvetica, Arial, sans-serif",
        size=14,
        color="Black"
    ),
    xaxis_title='Donation Amount',
    yaxis_title='Recipient',
    title_x=0.5,  # Center the title
    margin=dict(t=100),  # Increase top margin to accommodate long titles
)

# Display the chart
st.plotly_chart(top_recipients_chart, use_container_width=True)

# Display the number of studies funded by selected company names in a table
matching_studies = studies_data[studies_data['Company Name'].apply(lambda x: any(company_name.lower() in x for company_name in selected_company_names))]
matching_studies_display = matching_studies[['Original Funder', 'Year', 'Specific Study DOI', 'Article Title', 'Source Title']].reset_index(drop=True)
matching_studies_display.index = range(1, len(matching_studies_display) + 1)  # Start numbering at 1

# Show the table with the total number of studies in the title
st.subheader(f'Studies Funded by Selected Funders (Total: {len(matching_studies_display)})')
st.dataframe(matching_studies_display)

st.markdown(
    """
    **Note**: While 141 studies were found associated with the monetary funders, 
    there are actually 784 studies associated with all companies on GOGEL (Global Oil and Gas Exit List) and GCEL (Global Coal Exit List).
    To view them and all our raw data, visit this link: 
    [View the data on Google Sheets](https://docs.google.com/spreadsheets/d/1YUyaAc7bS6f8nIWgQSFUVByV_8mlqsSap2XAQfRfReQ/edit?gid=1536854#gid=1536854)
    """
)
