import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sequence = ["_high", "_low", ""]
sequence_iter = iter(sequence)

list = [1.5, 1.4, 1.3, 1.2, 1.1, "tomato"]

# for item_seq in sequence:
#     for item_list in list:
#         print(f"this is the {item_list}, this is the {sequence}")
#
#     print(f"this is the next thing in the sequence, {next(sequence_iter)}, {item_seq}")

while sequence_iter:
    try:
        print(next(sequence_iter))
    except StopIteration:
        break

# file_path  = "/Users/leoparsons/Desktop/Coding_Projects/Python_Projecs/NMR_Processing/LP3-049/LP3-049-5d"
# dictionary_name = ""
# print(len(file_path))
# for character in file_path[::-1]:
#     if character != "/":
#         dictionary_name = dictionary_name + character
#     elif character == "/":
#         dictionary_name = dictionary_name[::-1]
#         break
# print(dictionary_name)

integration_dic = {'LP3-070-rxn-384hours': {'ppm': [0.97, 1.02, 1.03, 1.42, 1.51, 1.52, 1.96, 2.52, 2.53, 2.69, 2.78, 3.01, 3.75, 4.08, 5.08, 6.02, 6.1], 'std_integration': [7.172676, 1.4823799, 1.2713674, 6.593769, 1.4801061, 1.2813773, 1.5142697, 2.4096856, 2.0837634, 0.9009275, 1.6524807, 1.138016, 9.53212, 4.0527353, 1.0188302, 1.0, 2.6170642], 'raw_integration': [88477100.0, 18285600.0, 15682697.0, 81336110.0, 18257552.0, 15806173.0, 18678970.0, 29724192.0, 25703844.0, 11113210.0, 20383844.0, 14037768.0, 117581550.0, 49991704.0, 12567575.0, 12335299.0, 32282270.0]}, 'LP3-070-rxn-48hours': {'ppm': [0.97, 1.42, 1.96, 1.97, 2.52, 2.53, 2.78, 3.0, 3.01, 3.75, 4.05, 4.08, 5.08, 6.02, 6.1, 7.85, 7.87], 'std_integration': [7.1835995, 6.6420865, 1.354683, 1.3379618, 2.3968527, 2.2505186, 1.6816715, 1.1721501, 1.1760784, 8.619358, 1.9476902, 4.052471, 1.0238464, 1.0, 2.2763438, 1.0826771, 1.0348183], 'raw_integration': [102613860.0, 94878630.0, 19350918.0, 19112064.0, 34237750.0, 32147448.0, 24021772.0, 16743534.0, 16799648.0, 123122900.0, 27821708.0, 57887370.0, 14625094.0, 14284462.0, 32516348.0, 15465460.0, 14781822.0]}, 'LP3-070-rxn-72hours': {'ppm': [0.94, 0.97, 1.42, 1.43, 1.96, 2.52, 2.53, 2.78, 3.01, 3.75, 4.05, 4.08, 5.08, 6.02, 6.1, 7.72, 7.85, 9.14], 'std_integration': [2.4931996, 7.1183763, 6.5598, 6.1917725, 1.2190781, 2.3741636, 2.2427733, 1.6276722, 1.1189488, 8.501192, 1.3557761, 3.8340833, 0.9588781, 1.0, 2.1788847, 1.0693938, 1.0284693, 0.5927219], 'raw_integration': [35809784.0, 102241120.0, 94218296.0, 88932320.0, 17509598.0, 34100070.0, 32212914.0, 23378228.0, 16071442.0, 122102480.0, 19472988.0, 55068870.0, 13772350.0, 14362983.0, 31295284.0, 15359684.0, 14771888.0, 8513254.0]}, 'LP3-070-rxn-24hours': {'ppm': [0.97, 1.42, 1.96, 1.97, 2.52, 2.53, 2.78, 3.01, 3.75, 4.05, 4.08, 5.08, 6.02, 6.1, 7.72, 7.85, 9.14], 'std_integration': [7.271134, 6.714359, 1.2769402, 1.2811521, 2.4136589, 2.376053, 1.6891063, 1.1889389, 8.627752, 1.4508593, 4.0797267, 1.0291171, 1.0, 2.2588563, 1.134586, 1.0769283, 0.6351795], 'raw_integration': [105531110.0, 97450240.0, 18533138.0, 18594268.0, 35031140.0, 34485340.0, 24515196.0, 17255912.0, 125220680.0, 21057348.0, 59211960.0, 14936306.0, 14513708.0, 32784382.0, 16467049.0, 15630222.0, 9218810.0]}, 'LP3-070-rxn-312hours': {'ppm': [0.98, 1.03, 1.43, 1.5, 1.52, 1.96, 1.97, 2.52, 2.53, 2.78, 3.01, 3.75, 4.08, 5.08, 6.02, 6.1], 'std_integration': [7.016187, 1.2559408, 6.538309, 1.208707, 1.2231779, 1.4575027, 1.4834354, 2.2282548, 2.3867934, 1.7095205, 1.1584674, 9.433677, 4.0837264, 1.0017805, 1.0, 2.4924955], 'raw_integration': [90537660.0, 16206801.0, 84371070.0, 15597290.0, 15784024.0, 18807778.0, 19142416.0, 28753650.0, 30799448.0, 22059844.0, 14948993.0, 121733220.0, 52696864.0, 12927088.0, 12904112.0, 32163442.0]}, 'LP3-070-rxn-15min': {'ppm': [0.96, 1.41, 1.96, 2.52, 2.53, 2.78, 3.01, 3.75, 4.08, 6.02, 6.1, 7.71, 7.72, 7.85, 7.86, 7.87], 'std_integration': [6.768471, 6.4789424, 1.5069112, 2.3240778, 2.232124, 1.5723035, 1.1716325, 15.097453, 7.5968575, 1.0, 3.8302114, 2.101219, 2.057207, 1.9889528, 2.1097703, 2.022114], 'raw_integration': [80143920.0, 76715680.0, 17842992.0, 27518876.0, 26430072.0, 18617288.0, 13873034.0, 178765500.0, 89952660.0, 11840772.0, 45352660.0, 24880054.0, 24358920.0, 23550736.0, 24981308.0, 23943390.0]}}

# def refernce_dic_to_intd_std(int_std_ppm):
#     """Input the ppm shift for the internal standard to the 1/100 ppm. Only works if the internal standard does not have neighboring peaks within .01 ppm"""
#     referenced_int_dic = {}
#     for k in integration_dic.keys():
#         referenced_dic = {}
#         ppm_list = integration_dic[k].keys()
#         for i in ppm_list:
#             rounded_value = round(i, 2)
#             if rounded_value == int_std_ppm:
#                 ref_int = integration_dic[k][i]
#             else:
#                 pass
#         for i in ppm_list:
#             referenced_int = integration_dic[k][i]/ref_int
#             referenced_dic[i] = referenced_int
#         referenced_int_dic[k] = referenced_dic
#     return referenced_int_dic

# referenced_int_dic = {}
# for k in integration_dic.keys():
#     referenced_dic = {}
#     ppm_list = integration_dic[k].keys()
#     for i in ppm_list:
#         rounded_value = round(i, 2)
#         if rounded_value == int_std_ppm:
#             ref_int = integration_dic[k][i]
#         else:
#             pass
#     for i in ppm_list:
#         referenced_int = integration_dic[k][i]/ref_int
#         referenced_dic[i] = referenced_int
#     referenced_int_dic[k] = referenced_dic

# columns=np.arange(0, len(integration_dic[k].keys()))


def generate_integration_df(integration_dic_input):
    integration_dic = integration_dic_input
    df = pd.DataFrame()
    for k in integration_dic.keys():
        data = pd.DataFrame(integration_dic[k])
        data["sample_name"] = k
        data["number_H"] = np.nan
        df = df._append(data, ignore_index=True)
    return df

integration_df = generate_integration_df(integration_dic)
integration_df["concentraiton_int_std"] = 10
integration_df["corrected_int"] = integration_df["std_integration"] * integration_df["number_H"]
integration_df["concentration"] = np.nan

for x in pd.unique(integration_df["sample_name"]):
    # print(integration_df[integration_df["sample_name"] == x])
    rows = integration_df[integration_df["sample_name"] == x]
    print(rows)
    rows_2 = rows[integration_df["ppm"] == 3.75]
    row_2_int = rows_2["std_integration"]
    print(rows_2)
    print(row_2_int)


signals = [(0.97, 3),(1.02, 6), (1.03, 6), (7.87, 1)]

def set_integration_H(integration_df, signals):
    """Sets the 'number_H' column of the integration df based on the signals list where each tuple contains the
    (ppm, number_H)"""
    unique_names = integration_df["sample_name"].unique()
    for i, j in signals:
        for name in unique_names:
            # integration_df[integration_df["ppm"] == i]["number_H"] = j
            rows = integration_df[integration_df["ppm"] == i]
            rows_2 = rows[integration_df["sample_name"] == name]
            rows_2_idx = rows_2.index
            # print(name)
            # print(rows)
            integration_df.loc[rows_2_idx, "number_H"] = j
    return integration_df.dropna(ignore_index=True)

print(set_integration_H(integration_df, signals))


            # y = integration_df.loc[[integration_df[integration_df["ppm"] == i] & integration_df[integration_df["name"] == name]],integration_df["number_H"]]
            # print(y)
            # print(integration_df[integration_df["ppm"] == i])










