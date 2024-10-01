import numpy as np
import pandas as pd
import statistics
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.transforms

from csv_organizer_concise import read_local_icp_file
import csv

# Make sure to add a space between the two parts of the csv

original_csv = "/Users/leoparsons/Downloads/LP004083 Cycle 1_concise" # <-- type your file path here

results_library = read_local_icp_file(f"{original_csv}.csv")

print(results_library.keys())
print(results_library['method_internal_standards'])
measurements = results_library['measurement_list']

### This code will output the csv with the averages included: ###

with open(f"{original_csv}_clean.csv", 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    header = list(measurements[2]['value_list'][0].keys())
    header_names = 'sample_name'
    final_conc_header = [header_names]
    std_dev_header = [header_names]
    isr_header = ["ISR [%]"]
    time_header = ["Time"]
    LOD_header = []

    for item in header:
        if "Final Conc." in item:
            if "Y" not in item:
                final_conc_header.append(item)
        if "Final RSD" in item:
            # this is really the name for the RSD but you want to change it
            if "Y" not in item:
                std_dev_header.append(item.split(":")[0] + ": standard_deviation")
        if "LOD" in item:
            if "Y" not in item:
                LOD_header.append(item)

    csv_writer.writerow(final_conc_header + std_dev_header[1:] + isr_header + time_header + LOD_header)

    intensity_library = {}
    for library in measurements[2]["value_list"]:
        name = library["ion_wavelength_unit_replicate"]
        list_a = []
        list_a.append(name)
        for k in library:
            if "Y" not in k:
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
            if "Y" not in k:
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
            if "Y" not in k:
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

        for k in library:
            if "Li 460.289: ISR [%] Y 377.433" in k or "Ce 413.380: ISR [%] Y 377.433" in k:
                value = library[k]
                if library[k] == "n/a":
                    value = "0"
                list_a.append(value)
            if "Li 460.289: ISR [%] Y 377.433" not in list(library.keys()):
                if "K 766.490: ISR [%] Y 377.433" in k:
                    value = library[k]
                    if library[k] == "n/a":
                        value = "0"
                    list_a.append(value)

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

    # csv_writer.writerow("")

    std_dev_lib = {}
    for k in intensity_library:
        if "Y" not in k:
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
        csv_writer.writerow(line_a + line_b + line_c + line_d + line_e)

