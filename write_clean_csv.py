import numpy as np
import pandas as pd
import statistics
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.transforms

from csv_organizer_concise import read_local_icp_file
import csv

# Make sure to add a space between the two parts of the csv

# original_csv = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/IX cycling concise icp reports/LP004087 N1 Cycles 1-3_concise.csv" # <-- type your file path here
# if you want to run this code individually type path above and call function at end of script

### This code will output the csv with the averages included: ###


def write_clean_csv(filepath_in: str, filepath_out: str = None):
    """will write a clean csv file from the concise icp report file. Pass in the filepath for the icp report file
    csv as the first argument (filepath_in) and the desired directory to save the clean csv function as the second
    argument (filepath_out). If no filepath_out is provided the function will save the clean icp csv file in the
    directory containing the icp report file."""
    # with change to csv_organizer_concise, we need to change the indexing for the function call
    results_library = read_local_icp_file(filepath_in)
    measurements = results_library['measurement_list']
    if filepath_out is not None:
        filepath_out = filepath_out + "/" + filepath_in.split("/")[-1].split(".")[0] + "_clean.csv"
    if filepath_out is None:
        filepath_out = f"{filepath_in.split('.')[0]}_clean.csv"
    with open(filepath_out, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = list(measurements[2]['value_list'][0].keys())
        header_names = 'sample_name'
        final_conc_header = [header_names]
        std_dev_header = [header_names]
        isr_header = ["ISR [%]"]
        time_header = ["Time"]
        LOD_header = []
        overall_correction_factor_header = ["Overall Correction Factor"]

        for item in header:
            if "Final Conc." in item:
                final_conc_header.append(item)
            if "Final RSD" in item:
                # this is really the name for the RSD but you want to change it
                std_dev_header.append(item.split(":")[0] + ": standard_deviation")
            if "LOD" in item:
                LOD_header.append(item)

        csv_writer.writerow(final_conc_header + std_dev_header[1:] + isr_header + time_header + LOD_header +
                            overall_correction_factor_header)

        intensity_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for k in library:
                if "Final Conc." in k:
                    value = library[k]
                    if "," in library[k]:
                        value = library[k].replace(",", "")
                    if library[k] == "Saturated":
                        value = "0"
                    list_a.append(value)
            intensity_library[name] = list_a[1:]

        LOD_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for k in library:
                if "LOD" in k:
                    value = library[k]
                    if "," in library[k]:
                        value = library[k].replace(",", "")
                    if library[k] == "Saturated":
                        value = "0"
                    list_a.append(value)
            LOD_library[name] = list_a[1:]

        rsd_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for k in library:
                if "Final RSD" in k:
                    value = library[k]
                    if library[k] == "n/a":
                        value = "0"
                    list_a.append(value)
            rsd_library[name] = list_a[1:]

        isr_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for key in library:
                if ": ISR [%]" in key and library[key] != "n/a":
                    isr_value = library[key]
                    list_a.append(isr_value)
                    break
            isr_library[name] = list_a[1:]

        time_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for k in library:
                if "Time" in k:
                    value = library[k]
                    if library[k] == "n/a":
                        value = "0"
                    list_a.append(value)
            time_library[name] = list_a[1:]

        overall_correction_library = {}
        for library in measurements[2]["value_list"]:
            name = library["ion_wavelength_unit_replicate"]
            list_a = []
            list_a.append(name)
            for k in library:
                if "Overall Correction Factor" in k:
                    value = library[k]
                    if library[k] == "n/a":
                        value = "0"
                    list_a.append(value)
            overall_correction_library[name] = list_a[1:]

        # csv_writer.writerow("")

        std_dev_lib = {}
        for k in intensity_library:
            std_dev_list = []
            for item in intensity_library[k]:
                try:
                    float(item)
                except ValueError:
                    item = np.nan
                    std_dev_list.append(item)
                else:
                    index_item = rsd_library[k][intensity_library[k].index(item)]
                    if "," in index_item:
                        index_item = index_item.replace(",", "")
                    if index_item == "":
                        index_item = 0
                    std_dev = round((float(item) * float(index_item) / 100), 4)
                    std_dev_list.append(std_dev)
            std_dev_lib[k] = std_dev_list

        for key in std_dev_lib:
            line_a = intensity_library[key]
            line_a.insert(0, key)
            line_b = std_dev_lib[key]
            line_c = isr_library[key]
            line_d = time_library[key]
            line_e = LOD_library[key]
            line_f = overall_correction_library[key]
            csv_writer.writerow(line_a + line_b + line_c + line_d + line_e + line_f)

        return filepath_out


# write_clean_csv(filepath_in=original_csv, filepath_out="/Users/leoparsons/Downloads")
