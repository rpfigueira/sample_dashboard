
import requests
import pandas as pd

# Get list o municipalities from wikidata
# Define the SPARQL query
query = """
SELECT ?municipality ?municipalityLabel ?district ?districtLabel WHERE {
  ?municipality wdt:P31 wd:Q13217644;  # instance of municipality of Portugal
                wdt:P131 ?district.   # located in the administrative entity (district)
  ?district wdt:P31 wd:Q3032141

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?districtLabel ?municipalityLabel
"""

# URL for the Wikidata SPARQL endpoint
url = "https://query.wikidata.org/sparql"

# Send the request to Wikidata
response = requests.get(url, params={'format': 'json', 'query': query}, headers={'User-Agent': 'Mozilla/5.0'})

# Parse the JSON response
data = response.json()

# Extract the results
results = data['results']['bindings']

# Transform into a DataFrame
df = pd.DataFrame([{
    'district': item['districtLabel']['value'],
    'municipality': item['municipalityLabel']['value'],
    'municipality_id': item['municipality']['value'].split('/')[-1]
} for item in results])

# Display the first rows
print(df.head())

# Import file with data about construction
df_construction = pd.read_csv("data/978.csv")

print(df_construction.head())

# Merge the dataframes
# Assuming you want to keep all municipalities from df and add matching construction data
df_merged = pd.merge(df, df_construction, left_on='municipality', right_on='02. Nome Região (Portugal)', how='left')


df_merged = df_merged.drop(columns={'02. Nome Região (Portugal)', '06. Filtro 3',
                                    '07. Escala', '08. Símbolo'})

# rename columns
df_merged = df_merged.rename(columns={'01. Ano':'year', 
                                       '02. Nome Região (Portugal)':'municipality',
                                       '03. Âmbito Geográfico':'region_type',
                                       '04. Filtro 1':'construction_type',
                                       '05. Filtro 2':'dwelling_type',
                                       '09. Valor':'value_construction_type'})

# Display the first few rows of the merged dataframe
print("Merged DataFrame head:")
print(df_merged.head())
print("\nMerged DataFrame info:")
print(df_merged.info())

# merge dwelling archetypes
# Import file with data about dwelling types
df_dwelling = pd.read_csv("data/980_dwelling.csv")

# drop columns
df_dwelling = df_dwelling.drop(columns={'03. Âmbito Geográfico', '05. Filtro 2',
                                    '06. Filtro 3', '07. Escala', '08. Símbolo'})

# rename columns
df_dwelling = df_dwelling.rename(columns={'01. Ano':'year', 
                                       '02. Nome Região (Portugal)':'municipality',
                                       '03. Âmbito Geográfico':'region_type',
                                       '04. Filtro 1':'type',
                                       '09. Valor':'value_dwelling_type'})

# Display the first few rows of the merged dataframe
print("Merged DataFrame head:")
print(df_dwelling.head())
print("\nMerged DataFrame info:")
print(df_dwelling.info())

# Merge the dataframes
# Assuming you want to keep all municipalities from df and add matching construction data
df_merged = pd.merge(df_merged, df_dwelling, on=['municipality', 'year'], 
                     how='left')



# save as csv
df_merged.to_csv("data/portugal_municipalities.csv", index=False)