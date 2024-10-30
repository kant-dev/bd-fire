import pandas as pd

def load_and_prepare_data():
    csv_files = [
        'data/queimadas_19_20.csv', 
        'data/queimadas_20_21.csv', 
        'data/queimadas_21_22.csv', 
        'data/queimadas_22_23.csv', 
        'data/queimadas_23_24.csv', 
    ]
    data = pd.concat([pd.read_csv(file) for file in csv_files])
    
    data.fillna(0, inplace=True)
    
    data['DataHora'] = pd.to_datetime(data['DataHora'])
    data['Mes'] = data['DataHora'].dt.month
    data['Ano'] = data['DataHora'].dt.year

    return data
