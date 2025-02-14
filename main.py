import os
import pandas as pd

# Definir la ruta de la carpeta
folder_path = 'Datos/Consolidado 2/Archivos'

# Obtener una lista de todos los archivos CSV en la carpeta
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Inicializar un DataFrame vacío para almacenar todos los datos transpuestos
all_transposed_data = pd.DataFrame()

# Leer y procesar cada archivo CSV
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    print(f'Procesando archivo: {csv_file}')

    try:
        # Leer el archivo CSV con el delimitador adecuado
        with open(file_path, 'r', encoding='latin1') as file:
            lines = file.readlines()

        data = pd.read_csv(file_path, encoding='latin1', delimiter=',', on_bad_lines='skip')

        print(data)

        # Encontrar el índice de la fila "Country Name"
        start_index = 0
        for i, line in enumerate(lines):
            if line.startswith('\"Country Name\"'):
                start_index = i
                break

        print(start_index)

        years = data.columns[4:]

        # Crear una lista para almacenar las filas transpuestas
        transposed_data = []

        print(data.head())

        # Iterar sobre cada fila del DataFrame original
        for index, row in data.iterrows():
            country_name = row['Country Name']
            country_code = row['Country Code']
            indicator_name = row['Indicator Name']
            indicator_code = row['Indicator Code']

            # Iterar sobre las columnas de años
            for year in years[:-2]:  # Excluir 'Unnamed: 68' y 'Most_Recent_Value'
                value = row[year]
                if not pd.isna(value):
                    transposed_data.append([country_name, country_code, indicator_name, indicator_code, year, value])

        # Crear un nuevo DataFrame con los datos transpuestos
        transposed_df = pd.DataFrame(transposed_data, columns=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Year', 'Value'])

        # Concatenar los datos transpuestos al DataFrame principal
        all_transposed_data = pd.concat([all_transposed_data, transposed_df], ignore_index=True)

        print(transposed_df.head())
        print(data.head())
    except pd.errors.ParserError as e:
        print(f'Error al procesar el archivo {csv_file}: {e}')

# Mostrar el DataFrame combinado
print(all_transposed_data.head())