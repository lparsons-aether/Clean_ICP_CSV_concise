import pandas as pd
import numpy as np

# clean_csv = "/Users/leoparsons/Downloads/LP004083 Cycle 1_concise_clean.csv"


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
        "Li 460.289: Final Conc. [ppm]",
        "Na 589.592: Final Conc. [ppm]",
        "K 766.490: Final Conc. [ppm]",
        "Mg 285.213: Final Conc. [ppm]",
        "Ca 396.847: Final Conc. [ppm]",
        "Sr 460.722: Final Conc. [ppm]",
        "Mn 403.076: Final Conc. [ppm]"
    ]

    N2_headers_master = [
        "Y 377.433: Final Conc. [ppm]",
        "Ce 446.021: Final Conc. [ppm]",
        "Pr 532.276: Final Conc. [ppm]",
        "Nd 404.080: Final Conc. [ppm]",
        "Gd 342.247: Final Conc. [ppm]",
        "Tb 370.286: Final Conc. [ppm]",
        "Dy 340.780: Final Conc. [ppm]",
        "Sm 442.434: Final Conc. [ppm]",
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
        # Added backup lines here
        "Li 460.289: Final Conc. [ppm]",
        "Na 589.592: Final Conc. [ppm]",
        "K 766.490: Final Conc. [ppm]",
        "Mg 285.213: Final Conc. [ppm]",
        "Ca 396.847: Final Conc. [ppm]",
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

    return IX_df.to_csv(filepath_out)


# reorganize_clean_headers(filepath_in=clean_csv, filepath_out="/Users/leoparsons/Downloads/test")
