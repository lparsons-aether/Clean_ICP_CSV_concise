import pandas as pd
import numpy as np
import os

from write_clean_csv import write_clean_csv
from reorganize_headers import reorganize_clean_headers

# Make the directories for the outputs. You can change these but good to keep them the same

clean_icp_dir = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/IX cycling clean concise icp reports"
if not os.path.exists(clean_icp_dir):
    os.mkdir(clean_icp_dir)

reorganized_clean_icp_dir = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/IX cycling reorganized " \
                            "clean concise icp reports"
if not os.path.exists(reorganized_clean_icp_dir):
    os.mkdir(reorganized_clean_icp_dir)

def loop_through_folder(directory_str):
    """loops through a folder and returns a list of file paths as strings for all items in the folder"""
    directory = os.fsencode(directory_str)
    master_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename == ".DS_Store":
            pass
        elif ".csv" in filename:
            file_path = directory_str + "/" + filename
            master_list.append(file_path)
        else:
            pass

    return sorted(master_list)


list_icp_concise_path = loop_through_folder("/Users/leoparsons/Desktop/Aether_Biomachines/"
                                          "Experiments/ICP-OES/IX cycling concise icp reports")

print("generating concise reports...")
for path in list_icp_concise_path:
    output_dir = clean_icp_dir
    clean_icp_filepath = write_clean_csv(filepath_in=path, filepath_out=output_dir)

list_icp_clean_concise_path = loop_through_folder(clean_icp_dir)

print("generating clean concice reports...")
for path in list_icp_clean_concise_path:
    output_dir = reorganized_clean_icp_dir
    reorganized_clean_icp_filepath = reorganize_clean_headers(filepath_in=path, filepath_out=output_dir)

def combine_df(path_list: list):
    """takes a list of paths to csv files you want to concat"""
    # Turn csv into pandas dfs
    df_list = []
    for path in path_list:
        df = pd.read_csv(path)
        df_list.append(df)
    concat_df = pd.concat(df_list, ignore_index=True)

    return concat_df


# This will be the running ICP DB file which you can upload stuff to
ICP_DB_filename = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/ICP DB.csv"
combine_df(loop_through_folder(reorganized_clean_icp_dir)).set_index("sample_name").to_csv(ICP_DB_filename)
print(f"ICP DB.csv created: {ICP_DB_filename}")
