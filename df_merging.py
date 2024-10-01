import pandas as pd
import os

config_1 = {
    "directory": "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Plots/S_AA_runs/icp_runs_metadata",
    "output_path": "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/Plots/S_AA_runs/icp_runs_metadata",
    "sample_name": "A_AA_runs_metadata_combined.csv"
}

def combine_df(path_list: list):
    """takes a list of paths to csv files you want to concat"""
    # Turn csv into pandas dfs
    df_list = []
    for path in path_list:
        df = pd.read_csv(path)
        df_list.append(df)
    concat_df = pd.concat(df_list, ignore_index=True)

    return concat_df


def loop_through_folder(directory_str):
    """loops through a folder and returns a list of file paths as strings for all items in the folder"""
    directory = os.fsencode(directory_str)
    master_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename == ".DS_Store":
            pass
        else:
            file_path = directory_str + "/" + filename
            master_list.append(file_path)

    return master_list

master_list = loop_through_folder(config_1["directory"])

combined_df = combine_df(master_list)

path = config_1["output_path"] + "/" + config_1["sample_name"]

combined_df.to_csv(path, sep=",")

