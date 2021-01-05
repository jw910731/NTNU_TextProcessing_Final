import pandas as pd

def csvwrite(DICT):
    pd.DataFrame(DICT).to_csv('output.csv', header=True,encoding='utf-8')