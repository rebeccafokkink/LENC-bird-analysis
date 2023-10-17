# Import some libraries
import pandas as pd

# Import the data frame
main_df = pd.read_excel('UPDATED_clean_database.xlsx')

# Rename important headers and bird species

main_df = main_df.rename(columns={'Unnamed: 1': 'survey type', 'Unnamed: 2': 'transect number', 'Coloum 6': 'build up'})
main_df['survey type'] = main_df['survey type'].str.lower() #make everything in the column lowercase

for col_idx in range(17, 96):
    main_df.columns.values[col_idx] = main_df.iloc[6, col_idx]

# Select entries for bird observations
bird_df = main_df[main_df['survey type'] == 'bird'].copy() #filter for bird observations

# 'Coloum 13' to 'Coloum 91' are bird species
# Specify the range of columns analyzed
# Row 9 and onwards have the actual observations per bird species
start_column_idx = 17
end_column_idx = 95
start_row_idx = 8

# Select the columns and rows in the specified range
bird_species_df = bird_df.iloc[start_row_idx:, start_column_idx:end_column_idx + 1]  # Adding 1 to include the last column

# Concatenate the 'build up' column with bird_species_df
selected_data = pd.concat([bird_df['build up'], bird_species_df], axis=1)

# Group by 'build up' and sum the count of observed species
count_per_species = selected_data.groupby('build up').sum()

# Create a new column 'species count' and initialize it with zeros in count_per_species
count_per_species['species count'] = 0

# Iterate through the rows and count different species for each build-up category
for index, row in count_per_species.iterrows():
    species_count = sum([1 if pd.notna(value) and str(value).isdigit() and int(value) > 0 else 0 for value in row])
    count_per_species.at[index, 'species count'] = species_count

# Create a new column 'total birds' and initialize it with zeros in count_per_species
count_per_species['total birds'] = 0

# Iterate through the rows and sum all integer values for each species
for index, row in count_per_species.iterrows():
    total = sum([int(value) if pd.notna(value) and str(value).isdigit() else 0 for value in row])
    count_per_species.at[index, 'total birds'] = total

# Save the updated DataFrame to 'output.csv'
count_per_species.to_csv('output.csv', index=True)