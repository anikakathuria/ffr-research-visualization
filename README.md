You can access this tool at (https://ffr-research-visualization.streamlit.app), which will display Columbia's data. Currently it allows you to filter by
years, funders, and recipients, and will display the following graphs:
- Funding by Selected Funders for Selected Recipients Over Time
- Total Funding Over Time
- Top Funders in Selected Range for Selected Recipients
- Top Recipients in Selected Range
- Studies Funded by Selected Funders

## How to apply the tool to other data

To create this tool for your school's data, you just need to have a csv file called "all_quantitative_research.csv" that contains the columns 
"Company Name," "Funder,"Donation Amount," "Year," and "Source". For our data, we have the columns "Columbia school?" and "Which Specific Columbia Program?" but you can
replace those terms with the name of your recipient column/columns, or delete everything to do with receipients if you don't want that at all. 
*Also, the difference between Company Name and Funder is how we aggregated companies that have multiple different foundations that might have donated;
e.g.: "Royal Dutch Shell Foundation" or "Shell Usa Company Foundation" would be listed under Funder but we manually put "Shell" as the Company Name and 
did that for all our data (which you can also take a look at in this repo). The funder selector tool will operate on the company names, not the original funder names. 

We also wanted to include the studies we found from WOS (https://github.com/anikakathuria/WOS_scraping), all that data is in "studies.csv". This tool will
match funder names and search those studies and display a table with studies who have a funder with the selected company names. If you don't want this, you can delete
the importing of this csv and the very last graph at the end!

## How to deploy the tool for public use

Streamlit makes this super easy!! I was able to just create an account and make an app using their website -- the app is connected to this repository
and hosted on their free community cloud. I had to write some dependencies in requirements.txt but Streamlit will take care of downloading those if you articulate them, 
and if you don't add anything these will work.  

