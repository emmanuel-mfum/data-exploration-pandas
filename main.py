import pandas as pd

# Main dataframe to collect the data
table_data = pd.read_html('https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors')

df = table_data[0].copy()  # makes a deep copy of the data frame (data and indices)
# Set the columns of our data frame
df.columns = ['Rank', 'Major', 'Degree Type', 'Early Career Pay', 'Mid-Career Pay', '% High Meaning']


# Add the other pages of the table form the website

for n in range(2, 35):
    table_data = pd.read_html(f'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{n}')
    page_df = table_data[0].copy()
    page_df.columns = ['Rank', 'Major', 'Degree Type', 'Early Career Pay', 'Mid-Career Pay', '% High Meaning']
    #  This will append each data frame (rows) to our first data frame , ignore index parameter will make the indices
    # of our rows to go from 0, 1 ..n-1 if set to True
    df = df.append(page_df, ignore_index=True)

# Selects the necessary columns
df = df[['Major', 'Early Career Pay', 'Mid-Career Pay']]

# Clean our data
# df.replace(to_replace="Major:", value="", regex=True, inplace=True)
# df.replace(to_replace="Mid-Career Pay:", value="", regex=True, inplace=True)

# The function used here is Dataframe.replace(). We pass a dictionary as the first argument.
# The keys in the dictionary represent the value to be replaced, while the values of the dictionary
# represents the new values
# Regex is set to true as we want to interpret the values we are replacing as regular expressions (String)
# Inplace is set to true as we want to let the data remain in place (returning nothing) instead of having to store
# a copy of the dataframe  in a new variable

df.replace({"Major:": "", "^Early Career Pay:\$": "", "^Mid-Career Pay:\$": "", ",": ""}, regex=True, inplace=True)

# Converting the salaries into number type
df[['Early Career Pay', 'Mid-Career Pay']] = df[['Early Career Pay', 'Mid-Career Pay']].apply(pd.to_numeric)

# After the previous steps, we can explore and manipulate the data as we want

pd.set_option('display.max_columns', None)  # in order to view all the columns

print(df.sort_values('Early Career Pay', ascending=False).head())
print(df.sort_values('Mid-Career Pay', ascending=False).head())
