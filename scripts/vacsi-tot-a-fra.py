import json
import pandas as pd
import requests

## FRANCE
def download_fra_data():
  url = "https://www.data.gouv.fr/fr/datasets/r/dc103057-d933-4e4b-bdbf-36d312af9ca9"
  data = requests.get(url)

  with open('data/input/vacsi-tot-a-fra.csv', 'wb') as f:
          f.write(data.content)
          
def prepare_data(df):
  df_clage_vacsi = pd.read_csv('data/input/clage_spf.csv', sep=';')
  df = df.merge(df_clage_vacsi, left_on="clage_vacsi", right_on="code_spf").groupby(["jour", "categorie-large"]).sum().reset_index()
  return df

def import_fra_data():
  df = pd.read_csv('data/input/vacsi-tot-a-fra.csv', sep=';')
  return prepare_data(df)

def csv_to_json_fra(df):
  jour_max = df.jour.max()
  df = df[(df.clage_vacsi != 0) & (df.jour == jour_max)]
  df = df.sort_values(by="categorie-large")

  dict_json = {"age": [str(age) + " ans" for age in df["categorie-large"].tolist()], 
              "n_dose1": df.n_tot_dose1.tolist(), 
              "n_dose2": df.n_tot_dose2.tolist(),
              "n_dose1_pop": list(df.n_tot_dose1.values/df.population.values*100),
              "n_dose2_pop": list(df.n_tot_dose2.values/df.population.values*100)}

  with open("data/output/vacsi-tot-a-fra_lastday.json", "w") as outfile:
    outfile.write(json.dumps(dict_json))


download_fra_data()
df = import_fra_data()
csv_to_json_fra(df)