import pandas as pd

df = pd.read_csv("/Users/leoparsons/Downloads/IX Cycling Data - Cycling DB (4).csv")


filter_columns = [
    'Experiment ID',
    'Adsorbent Code',
    'IX Cycle',
    'Brine ID',
    'Adsorbent Mass (mg)',
    'Brine volume (ml)',
    'Eluant1 M',
    'Elution1 Volume (ml)',
    '# Washes',
    'Eluant Time (min)',
    'Time Raffinate (min)',
    'Support',
    'Active material'
]

cols_to_avg = [c for c in df.columns if 'Eluate (ppm)' in c or 'Raffinate (ppm)' in c or 'Raffinate (mmol)' in c or
               'Eluate (mmol)' in c]

deduped_by_filter_col = df.drop_duplicates(subset=filter_columns)

def get_index_of_col(df, column_name):
    return list(df.columns).index(column_name) + 1  # plus 1 to deal with Index being first value in tuple

pretty_results = []

for dedup_row in deduped_by_filter_col.itertuples():
    add_me = {}

    for filter_col in filter_columns:
        add_me[filter_col] = dedup_row[get_index_of_col(df, filter_col)]
    avg_me = df[
        (df['Experiment ID'] == add_me['Experiment ID']) &
        (df['Adsorbent Code'] == add_me['Adsorbent Code']) &
        (df['IX Cycle'] == add_me['IX Cycle']) &
        (df['Brine ID'] == add_me['Brine ID']) &
        (df['Adsorbent Mass (mg)'] == add_me['Adsorbent Mass (mg)']) &
        (df['Brine volume (ml)'] == add_me['Brine volume (ml)']) &
        (df['Eluant1 M'] == add_me['Eluant1 M']) &
        (df['Elution1 Volume (ml)'] == add_me['Elution1 Volume (ml)']) &
        (df['# Washes'] == add_me['# Washes']) &
        (df['Eluant Time (min)'] == add_me['Eluant Time (min)']) &
        (df['Time Raffinate (min)'] == add_me['Time Raffinate (min)']) &
        (df['Support'] == add_me['Support']) &
        (df['Active material'] == add_me['Active material'])
        ]

    for value_tuple in avg_me[cols_to_avg].mean().items():
        add_me[value_tuple[0] + ' mean'] = value_tuple[1]
    for value_tuple in avg_me[cols_to_avg].std().items():
        add_me[value_tuple[0] + ' std'] = value_tuple[1]

    pretty_results.append(add_me)

pretty_df = pd.DataFrame(pretty_results)
pretty_df.head()
output_path = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Pretty_IX_Cycling_data_12.20.2024.csv"
pretty_df.to_csv(output_path)
print(f"average csv file written to: {output_path}")