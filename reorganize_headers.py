import pandas as pd
import numpy as np

# clean_csv = "/Users/leoparsons/Desktop/Aether_Biomachines/Experiments/ICP-OES/IX cycling clean concise icp reports/LP004067-cycle1_concise_wavelength_clean.csv"


def reorganize_clean_headers(filepath_in: str, filepath_out: str = None):
    """reorganizes the clean icp csv file. Pass in the filepath for the clean icp report file
       csv as the first argument (filepath_in) and the desired directory to save the reorganized
       clean csv function as the second argument (filepath_out). If no filepath_out is provided the function will save
       the reorganized clean icp csv file in the directory containing the clean icp report file."""
    if filepath_out is not None:
        filepath_out = filepath_out + "/" + filepath_in.split("/")[-1].split(".")[0] + "_reorganized.csv"
    if filepath_out is None:
        filepath_out = filepath_in.split(".")[0] + "_reorganized.csv"
    df = pd.read_csv(filepath_in)
    df_headers = list(df)

    # This generates an uniqe list of ions to the data file
    ion_headers = []
    for header in df_headers:
        header_split = header.split(":")
        if len(header_split) > 1 and "(" not in header_split[0]:
            ion_headers.append(header_split[0].rstrip())
        elif len(header_split) > 1 and "(" in header_split[0]:
            header_split_2 = header_split[0].split("(")[0]
            ion_headers.append(header_split_2.rstrip())
    method_standards = sorted(list(set(ion_headers)))

    new_df_headers = df_headers.copy()
    rename_dic = {}
    for header in new_df_headers:
        if "(" in header:
            header_items = header.split(" ")
            header_items.pop(2)
            header_items.pop(2)
            header_items[1] = header_items[1] + ":"
            new_header = " ".join(header_items)
            df_headers[df_headers.index(header)] = new_header
            rename_dic[header] = new_header

    if bool(rename_dic):
        df.rename(columns=rename_dic, inplace=True)


    N1_headers_master = [
        "Li Final Conc. [ppm]", "Li wavelength (nm)",
        "Na Final Conc. [ppm]", "Na wavelength (nm)",
        "K Final Conc. [ppm]",  "K wavelength (nm)",
        "Mg Final Conc. [ppm]", "Mg wavelength (nm)",
        "Ca Final Conc. [ppm]", "Ca wavelength (nm)",
        "Sr Final Conc. [ppm]", "Sr wavelength (nm)",
        "Mn Final Conc. [ppm]", "Mn wavelength (nm)"
    ]
    N2_headers_master = [
        "Y Final Conc. [ppm]", "Y wavelength (nm)",
        "Ce Final Conc. [ppm]", "Ce wavelength (nm)",
        "Pr Final Conc. [ppm]", "Pr wavelength (nm)",
        "Nd Final Conc. [ppm]", "Nd wavelength (nm)",
        "Gd Final Conc. [ppm]", "Gd wavelength (nm)",
        "Tb Final Conc. [ppm]", "Tb wavelength (nm)",
        "Dy Final Conc. [ppm]", "Dy wavelength (nm)",
        "Sm Final Conc. [ppm]", "Sm wavelength (nm)",
        "ISR [%]",
        "Time",
        "Overall Correction Factor",
        "Li 460.289: LOD [ppb]",
        "Na 589.592: LOD [ppb]",
        "K 766.490: LOD [ppb]",
        "Mg 285.213: LOD [ppb]",
        "Ca 396.847: LOD [ppb]",
        "Sr 460.722: LOD [ppb]",
        "Mn 403.076: LOD [ppb]",
        "Y 377.433: LOD [ppb]",
        "Ce 446.021: LOD [ppb]",
        "Pr 532.276: LOD [ppb]",
        "Nd 404.080: LOD [ppb]",
        "Gd 342.247: LOD [ppb]",
        "Tb 370.286: LOD [ppb]",
        "Dy 340.780: LOD [ppb]",
        "Sm 442.434: LOD [ppb]",
    ]

    N1_headers = N1_headers_master.copy()

    N2_headers = N2_headers_master.copy()

    missing_headers = []
    N1_missing_headers = []
    N2_missing_headers = []

    for header in N1_headers + N2_headers:
        if header not in df_headers:
            missing_headers.append(header)
    for header in missing_headers:
        if header in N1_headers:
            N1_headers.pop(N1_headers.index(header))
            N1_missing_headers.append(header)
        if header in N2_headers:
            N2_headers.pop(N2_headers.index(header))
            N2_missing_headers.append(header)

    N1_df = df[N1_headers].copy()
    N1_df[N1_missing_headers] = np.nan
    N2_df = df[N2_headers].copy()
    N2_df[N2_missing_headers] = np.nan

    first_columns_df = N1_df[N1_headers_master].merge(N2_df[N2_headers_master], left_index=True, right_index=True)

    for header in df_headers:
        if header in N2_headers or header in N1_headers:
            df.drop(labels=header, axis=1, inplace=True)

    reorganized_df = first_columns_df.merge(df, left_index=True, right_index=True)
    reorganized_df_headers = list(reorganized_df)
    reorganized_df_headers.pop(reorganized_df_headers.index("sample_name"))
    reorganized_df_headers.insert(0, "sample_name")

    #add code here to add a column at the start before the Li siganl to have a reference to the parent brine sample code

    IX_df = reorganized_df[reorganized_df_headers].set_index("sample_name")

    # This code will fill in the first columns of the df as outlined in N1_headers_master and N2_headers_master with the
    # data from the first lines list first then will go through the rest of the method standards to fill in any nan
    # with other available lines. If no line has a signal above the LOD for a sample_name then the cell is left nan.
    first_lines = ["Li 460.289",
        "Na 589.592",
        "K 766.490",
        "Mg 285.213",
        "Ca 396.847",
        "Sr 460.722",
        "Mn 403.076",
        "Y 377.433",
        "Ce 446.021",
        "Pr 532.276",
        "Nd 404.080",
        "Gd 342.247",
        "Tb 370.286",
        "Dy 340.780",
        "Sm 442.434",]

    final_conc = ": Final Conc. [ppm]"
    lod = ": LOD [ppb]"
    for line in first_lines:
        if line in method_standards:
            IX_df_conc_series = line.split(" ")[0] + " Final Conc. [ppm]"
            IX_df_wavelength_series = line.split(" ")[0] + " wavelength (nm)"
            final_conc_test = IX_df[f"{line}{final_conc}"]
            lod_test = IX_df[f"{line}{lod}"]
            above_lod = final_conc_test - (3.3*lod_test) / 1000
            above_lod.clip(0, inplace=True)
            for sample_name in list(above_lod.index):
                if np.isnan(IX_df.loc[sample_name, IX_df_conc_series]):
                    if above_lod.loc[sample_name] > 0:
                        IX_df.loc[sample_name, IX_df_conc_series] = final_conc_test.loc[sample_name]
                        IX_df.loc[sample_name, IX_df_wavelength_series] = line

    for method_standard in method_standards:
        IX_df_conc_series = method_standard.split(" ")[0] + " Final Conc. [ppm]"
        IX_df_wavelength_series = method_standard.split(" ")[0] + " wavelength (nm)"
        final_conc_test = IX_df[f"{method_standard}{final_conc}"]
        lod_test = IX_df[f"{method_standard}{lod}"]
        above_lod = final_conc_test - lod_test/1000
        above_lod.clip(0, inplace=True)
        for sample_name in list(above_lod.index):
            if np.isnan(IX_df.loc[sample_name, IX_df_conc_series]):
                if above_lod.loc[sample_name] > 0:
                    IX_df.loc[sample_name, IX_df_conc_series] = final_conc_test.loc[sample_name]
                    IX_df.loc[sample_name, IX_df_wavelength_series] = method_standard

    return IX_df.to_csv(filepath_out)


# reorganize_clean_headers(filepath_in=clean_csv, filepath_out="/Users/leoparsons/Downloads/")
