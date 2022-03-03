import pandas as pd
from pathlib import Path


print(Path(__file__).parents[0] / 'data/store_based.csv')

store_example_file = Path(__file__).parents[0] / 'data/store_based.csv'

df = pd.read_csv(store_example_file)
print(df.head())
