import pandas as pd
import numpy as np
df = pd.read_csv(
    '/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Pretty_IX_Cycling_data_12.20.2024.csv')

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
cols_to_sub_mean_eluate = [c for c in df.columns if 'Eluate (ppm) mean' in c or 'Eluate (mmol) mean' in c]

blanks = df[df['Adsorbent Code'] == "Blank"]
samples = df[df['Adsorbent Code'] != 'Blank']

def get_index_of_col(df, column_name):
    return list(df.columns).index(column_name) + 1  # plus 1 to deal with Index being first value in tuple


def calculate_Kd(raff, brine, adsorbent_mass, brine_volume, adsorbent_density=1.5):
    # Density of Si is 1.5 ml/g
    Kd = (brine - raff)/(adsorbent_mass/1000/adsorbent_density)/(raff/brine_volume)
    return Kd
adsorbent_density = 1.5

add_me_2 = []
for dedup_row in blanks.itertuples():
    blank_index = dedup_row[0]
    add_me = {}
    for filter_col in filter_columns:
        add_me[filter_col] = dedup_row[get_index_of_col(df, filter_col)]
    subset_me = df[
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

    # can you write this to pass in parts of the data frame to the function, "Kd"? #
    if not subset_me.empty:  # avoids issues with concat on an empty df
        subset_me_len_index = len(list(subset_me.index))
        concat_list = []
        for x in range(subset_me_len_index):
            concat_list.append(blanks.loc[blank_index].to_frame().transpose())

        blanks_for_operation = pd.concat(concat_list).reset_index().drop(['index'], axis=1)
        subset_me_sub = subset_me.copy().reset_index().drop(['index'], axis=1)

        Kd_df = subset_me_sub.copy()
        Kd_df_2 = Kd_df.copy()
        # print(np.asarray(Kd_df['Adsorbent Mass (mg)']))

        try:
            subset_me_sub[cols_to_sub_mean_raffinate] = blanks_for_operation[cols_to_sub_mean_raffinate] - \
                                                  subset_me_sub[cols_to_sub_mean_raffinate]
            subset_me_sub[cols_to_sub_mean_raffinate] = subset_me_sub[cols_to_sub_mean_raffinate].apply(lambda x:
                                                            np.asarray(x) / (np.asarray(Kd_df['Adsorbent Mass (mg)'])
                                                                        *1000*adsorbent_density))
            Kd_df_2[cols_to_sub_mean_raffinate] = Kd_df[cols_to_sub_mean_raffinate].apply(lambda x:
                                                            np.asarray(x) / (np.asarray(Kd_df['Brine volume (ml)'])))
            subset_me_sub[cols_to_sub_mean_raffinate] = subset_me_sub[cols_to_sub_mean_raffinate] / Kd_df_2[cols_to_sub_mean_raffinate] #this gives you the partition coefficent

            cols_to_sub_mean_raffinate_2 = [c for c in df.columns if 'Raffinate (ppm) mean' in c]
            Kd_df_add = subset_me_sub[filter_columns + cols_to_sub_mean_raffinate_2].copy()

            for item in cols_to_sub_mean_raffinate_2:
                new_item = item[:2].strip()
                cols_to_sub_mean_raffinate_2[cols_to_sub_mean_raffinate_2.index(item)] = new_item + " Parition Coefficient"
            Kd_df_add.columns = filter_columns + cols_to_sub_mean_raffinate_2
            add_me_2.append(Kd_df_add)
        except KeyError:
            print(subset_me_sub)
            pass
        # can you write this to pass in parts of the data frame to the function, "Kd"? #


    # print(subset_me_sub)

    # for row in subset_me.itertuples():
    #
    #     for filter_col in filter_columns:
    #         add_me_2[filter_col] = row[get_index_of_col(df, filter_col)]


            # for value in subset_me[cols_to_sub_mean].items():
            #     length_value = len(value)
            #     column_name = value[0]
            #     column_values = value[1]
            #     blank_row = dedup_row[get_index_of_col(df, column_name)]
            #     if len(column_values) > 0:
            #         for x in range(len(column_values)):
            #             adsorbent_mass = list(subset_me['Adsorbent Mass (mg)'])[x]
            #             brine_volume = list(subset_me['Brine volume (ml)'])[x]
            #             for measurement in column_values:
            #                 if 'Raffinate' in column_name:
            #                     difference = blank_row - measurement
            #                     # print(f'blank: {blank_row}\n sample value: {measurement} \n difference: {difference}')
            #                     if measurement != 0:
            #                         Kd = calculate_Kd(measurement, blank_row, adsorbent_mass, brine_volume)
            #                         # print(Kd)

            #                         add_me_2[column_name + ' Kd'] = Kd
            #                 if 'Eluate' in column_name:
            #                     difference = measurement - blank_row
            #                     add_me_2[column_name + ' blank subtracted'] = difference

    # pretty_results.append(add_me_2)

# pretty_df = pd.DataFrame(pretty_results).set_index('Experiment ID')
# pretty_df.head()
pretty_df = pd.concat(add_me_2).reset_index().drop(['index'], axis=1)

output_path = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Kd_IX_Cycling_data_12.20.2024.csv"
pretty_df.to_csv(output_path)
print(f"average csv file written to: {output_path}")