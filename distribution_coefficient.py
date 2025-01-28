import pandas as pd
import numpy as np
df = pd.read_csv(
    '/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Pretty_IX_Cycling_data_12.20.2024.csv'
)

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

pretty_results = []

cols_to_sub_mean_raffinate = [c for c in df.columns if 'Raffinate (ppm) mean' in c or 'Raffinate (mmol) mean' in c]
col_raffinate_error = [c for c in df.columns if 'Raffinate (ppm) std' in c or 'Raffinate (mmol) std' in c]

cols_to_sub_mean_eluate = [c for c in df.columns if 'Eluate (ppm) mean' in c or 'Eluate (mmol) mean' in c]
cols_to_sub_mean_eluate_error = [c for c in df.columns if 'Eluate (ppm) std' in c or 'Eluate (mmol) std' in c]

blanks = df[df['Adsorbent Code'] == 'Blank']
samples = df[df['Adsorbent Code'] != 'Blank']


def get_index_of_col(df, column_name):
    return list(df.columns).index(column_name) + 1  # plus 1 to deal with Index being first value in tuple


def get_Kd(b: pd.DataFrame, r: pd.DataFrame, m: pd.Series, v: pd.Series, columns_to_operate: list, d=1.5):
    """b: blank, r: raffinate, m: 'Adsorbent mass (mg)', v: 'Brine volume (ml)', d: density of adsorbent,
    columns_to_operate: list of column names you want to do operations on returns dataframe with partition coefficients
    for each ion"""
    r_copy = r.copy()
    r[columns_to_operate] = (b[columns_to_operate]-r[columns_to_operate])  # mmol adsorbed
    adsorbent_volume_mL = np.asarray(m)/1000/np.asarray(d)  # volume of adsorbent
    r[columns_to_operate] = r[columns_to_operate].apply(lambda x: np.asarray(x) / adsorbent_volume_mL)  # concentration ads
    r_copy[columns_to_operate] = r_copy[columns_to_operate].apply(lambda x: np.asarray(x) / np.asarray(v))  # concentration raffinate
    r[columns_to_operate] = r_copy[columns_to_operate].div(r[columns_to_operate])
    return r

def get_Kd_error(b: pd.DataFrame, r: pd.DataFrame, columns_to_operate: list, error_to_operate: list):
    r_copy = r.copy()
    measurements = r[columns_to_operate].copy()
    measurements.columns = error_to_operate  # columns need to have the same names for the .div() method
    r[columns_to_operate] = (b[columns_to_operate] - r[columns_to_operate])
    r[error_to_operate] = ((b[error_to_operate].mul(b[error_to_operate])) + (r[error_to_operate].mul(r[error_to_operate])))**0.5
    r[error_to_operate] = (r[error_to_operate].div(measurements))**2
    r_copy[error_to_operate] = (r_copy[error_to_operate]/measurements)**2
    return r

def subtract_eluate_background(b: pd.DataFrame, e: pd.DataFrame, columns_to_operate: list):
    """b: blank, e: eluate, columns_to_operate: list of column names you want to do operations on returns dataframe
    with eluate blank subtracted for each ion"""
    e_copy = e.copy()
    e_copy[columns_to_operate] = e[columns_to_operate].sub(b[columns_to_operate])
    return e_copy


def get_eluate_subtraction_error(b: pd.DataFrame, e: pd.DataFrame, columns_to_operate: list):
    e_copy = e.copy()
    e_copy[columns_to_operate] = ((e_copy[columns_to_operate].mul(e_copy[columns_to_operate])) +
                                  (b[columns_to_operate].mul(b[columns_to_operate])))**0.5
    return e_copy

Kd_df_list = []
Kd_df_error_list = []
eluate_list = []
eluate_error_list = []
for dedup_row in blanks.itertuples():
    blank_index = dedup_row[0]
    add_me = {}
    for filter_col in filter_columns:
        add_me[filter_col] = dedup_row[get_index_of_col(df, filter_col)]
    measurements = df[
        (df['Experiment ID'] == add_me['Experiment ID']) &
        (df['Adsorbent Code'] != "Blank") &
        (df['IX Cycle'] == add_me['IX Cycle']) &
        (df['Brine ID'] == add_me['Brine ID']) &
        # (df['Adsorbent Mass (mg)'] == add_me['Adsorbent Mass (mg)']) &
        (df['Brine volume (ml)'] == add_me['Brine volume (ml)']) &
        (df['Eluant1 M'] == add_me['Eluant1 M']) &
        (df['Elution1 Volume (ml)'] == add_me['Elution1 Volume (ml)']) &
        (df['# Washes'] == add_me['# Washes']) &
        (df['Eluant Time (min)'] == add_me['Eluant Time (min)']) &
        (df['Time Raffinate (min)'] == add_me['Time Raffinate (min)'])
        ]

    if not measurements.empty:  # avoids issues with concat on an empty df

        # setting up data frame of blank values to do operations #
        subset_me_len_index = len(list(measurements.index))
        concat_list = []
        for x in range(subset_me_len_index):
            concat_list.append(blanks.loc[blank_index].to_frame().transpose())
        # setting up data frame of blank values to do operations #

        blanks_for_operation = pd.concat(concat_list).reset_index().drop(['index'], axis=1)
        measurements_copy = measurements.copy().reset_index().drop(['index'], axis=1)

        Kd_df = get_Kd(blanks_for_operation.copy(), measurements_copy, measurements['Adsorbent Mass (mg)'].copy(),
                       measurements['Brine volume (ml)'].copy(), cols_to_sub_mean_raffinate)
        Kd_rename_columns = [c for c in df.columns if 'Raffinate (ppm) mean' in c]
        Kd_df_add = Kd_df[filter_columns + Kd_rename_columns].copy()
        for item in Kd_rename_columns:
            new_item = item[:2].strip()
            Kd_rename_columns[Kd_rename_columns.index(item)] = new_item + " Partition Coefficient"
        Kd_df_add.columns = filter_columns + Kd_rename_columns
        Kd_df_list.append(Kd_df_add)

        Kd_df_error = get_Kd_error(blanks_for_operation.copy(), measurements_copy, cols_to_sub_mean_raffinate,
                                   col_raffinate_error)
        Kd_rename_error_columns = [c for c in df.columns if 'Raffinate (mmol) std' in c]
        Kd_df_error_add = Kd_df_error[filter_columns + Kd_rename_error_columns].copy()
        for item in Kd_rename_error_columns:
            new_item = item[:2].strip()
            Kd_rename_error_columns[Kd_rename_error_columns.index(item)] = new_item + ' Partition error'
        Kd_df_error_add.columns = filter_columns + Kd_rename_error_columns
        Kd_df_error_list.append(Kd_df_error_add)

        eluate_background_subtract = subtract_eluate_background(blanks_for_operation.copy(), measurements_copy,
                                                                cols_to_sub_mean_eluate)
        cols_to_sub_mean_eluate_2 = cols_to_sub_mean_eluate.copy()
        eluate_rename_columns_add = eluate_background_subtract[filter_columns + cols_to_sub_mean_eluate_2].copy()
        for item in cols_to_sub_mean_eluate_2:
            if '(ppm)' in item:
                new_item = item[:2].strip()
                cols_to_sub_mean_eluate_2[cols_to_sub_mean_eluate_2.index(item)] = new_item + ' Eluate (ppm) Blank Subtracted'
            if '(mmol)' in item:
                new_item = item[:2].strip()
                cols_to_sub_mean_eluate_2[cols_to_sub_mean_eluate_2.index(item)] = new_item + ' Eluate (mmol) Blank Subtracted'
        eluate_rename_columns_add.columns = filter_columns + cols_to_sub_mean_eluate_2
        eluate_list.append(eluate_rename_columns_add)

        eluate_background_subtract_error = get_eluate_subtraction_error(blanks_for_operation.copy(), measurements_copy,
                                                                cols_to_sub_mean_eluate_error)
        cols_to_sub_mean_eluate_error_2 = cols_to_sub_mean_eluate_error.copy()
        eluate_error_rename_columns_add = eluate_background_subtract_error[filter_columns + cols_to_sub_mean_eluate_error_2].copy()
        for item in cols_to_sub_mean_eluate_error_2:
            if '(ppm)' in item:
                new_item = item[:2].strip()
                cols_to_sub_mean_eluate_error_2[
                    cols_to_sub_mean_eluate_error_2.index(item)] = new_item + ' Eluate (ppm) Blank Subtracted std'
            if '(mmol)' in item:
                new_item = item[:2].strip()
                cols_to_sub_mean_eluate_error_2[
                    cols_to_sub_mean_eluate_error_2.index(item)] = new_item + ' Eluate (mmol) Blank Subtracted std'
        eluate_error_rename_columns_add.columns = filter_columns + cols_to_sub_mean_eluate_error_2
        eluate_error_list.append(eluate_error_rename_columns_add)


pretty_df_Kd = pd.concat(Kd_df_list).reset_index().drop(['index'], axis=1)
pretty_df_Kd_error = pd.concat(Kd_df_error_list).reset_index().drop(['index'], axis=1)
pretty_df_eluate_background = pd.concat(eluate_list).reset_index().drop(['index'], axis=1)
pretty_df_eluate_error = pd.concat(eluate_error_list).reset_index().drop(['index'], axis=1)

pretty_df = pretty_df_Kd.merge(pretty_df_Kd_error, on=filter_columns)
pretty_df = pretty_df.merge(pretty_df_eluate_background, on=filter_columns)
pretty_df = pretty_df.merge(pretty_df_eluate_error, on=filter_columns)

partition_coefficients = [c for c in pretty_df if 'Partition Coefficient' in c]
partition_coefficients.pop(partition_coefficients.index('Nd Partition Coefficient'))
pretty_df['Nd selectivity'] = pretty_df['Nd Partition Coefficient'].div(pretty_df[partition_coefficients].sum(axis=1))

output_path = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Kd_IX_Cycling_data_12.20.2024.csv"
pretty_df.to_csv(output_path)
print(f"partition coefficient csv file written to: {output_path}")


