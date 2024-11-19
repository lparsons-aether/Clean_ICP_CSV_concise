import csv
from itertools import groupby
import pandas as pd


def clean_line(line):
    return line.replace('"', "").strip()


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def read_local_icp_file(icp_file):
    results = {}
    with open(icp_file) as f:
        reader = csv.reader(f)
        line = next(reader)
        line = line[:-1]
        while not (line[0] == '' and all_equal(line)):
            # currently looking at the run method data
            if 'Session Summary' not in line[0]:
                raise Exception("Missing Session Summary")
            line = next(reader)
            results['session_summary'] = {}
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = line[0].split(":")[0]
                if len(line[0].split(":")) > 1:
                    value = line[0].split(":")[1]
                else:
                    value = ""
                results['session_summary'][key] = value
                line = next(reader)
            line = next(reader)

            if 'Method Summary' not in line[0]:
                raise Exception("Missing Method Summary")
            results['method_summary'] = {}
            line = next(reader)
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = line[0].split(":")[0]
                if len(line[0].split(":")) > 1:
                    value = line[0].split(":")[1]
                else:
                    value = ""
                results['method_summary'][key] = value
                line = next(reader)
            line = next(reader)

            if 'Instrument ID' not in line:
                raise Exception("Missing Instrument ID")
            results['instrument_id'] = {}
            line = next(reader)
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = line[0].split(":")[0]
                if len(line[0].split(":")) > 1:
                    value = line[0].split(":")[1]
                else:
                    value = ""
                results['instrument_id'][key] = value
                line = next(reader)
            line = next(reader)  # "Results corrected by IS"
            if "Results corrected by IS" in line[0]:
                results['is_correction'] = True
            else:
                results['is_correction'] = False
                # raise NotImplementedError("Not ready to handle no is correction")
            line = next(reader)  # blank line before measurements

            results['measurement_list'] = []
            line = next(reader)

            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                measurement = {}
                # line = clean_line(line)
                line_split = line
                name = line_split.pop(0)
                measurement['name'] = name
                if name == "Method Instrument and Sampling Parameters":
                    line.insert(0, name)
                    break
                for str in line_split:
                    if '[' in str and ']' in str:
                        unit = str[str.find('[') + 1: str.find(']')]  # split out unit
                        str = str[:str.find('[') + 1] + str[str.find(']') + 1:]  # remove unit from key
                    key = '_'.join(str.lower().split(':')[0].split(' '))
                    value = ''
                    if len(str.lower().split(':')) > 1:
                        value = str.lower().split(':')[1].strip(",").strip()
                    measurement[key] = value
                line = next(reader)
                column_list = line
                # hard code here for first column
                column_list[0] = 'ion_wavelength_unit_replicate'
                measurement['value_list'] = []
                line = next(reader)

                while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                    measurement_value = {}
                    val_list = line
                    val_list = val_list + ([''] * (len(column_list) - len(val_list)))
                    for index, key in enumerate(column_list):
                        measurement_value[key] = val_list[index]
                    measurement['value_list'].append(measurement_value)
                    line = next(reader)
                results['measurement_list'].append(measurement)
                line = next(reader)

            # line = next(reader)  # move to method instrument and sampling parameters

            if 'Method Instrument and Sampling Parameters' not in line[0]:
                raise Exception("Method Instrument and Sampling Parameters not in file")
            line = next(reader)
            results['method_parameters'] = {}
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                val_list = line
                for line_val in val_list:
                    if '[' in line_val and ']' in line_val:
                        unit = line_val[line_val.find('[') + 1: line_val.find(']')]  # split out unit
                        line_val = line_val[:line_val.find('[')] + line_val[
                                                                   line_val.find(']') + 1:]  # remove unit from key
                        line_val = line_val.strip()
                        key = '_'.join(line_val.lower().split(':')[0].split(' '))
                        results['method_parameters'][key + '_unit'] = unit.strip()
                    key = '_'.join(line_val.lower().split(':')[0].split(' '))
                    value = ''
                    if len(line[0].lower().split(':')) > 1:
                        value = ':'.join(line_val.lower().split(':')[1:]).strip()
                results['method_parameters'][key] = value.strip()
                line = next(reader)
            line = next(reader)

            if 'Method Elements' not in line[0]:
                raise Exception("Method Elements not in file")
            line = next(reader)
            results['method_elements'] = {}
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = '_'.join(line[0].lower().split('-')[0].split(' '))
                value_list = line[0].lower().split('-')[1].split(',')
                results['method_elements'][key] = []
                for value in value_list:
                    if value == '':
                        continue
                    results['method_elements'][key].append(float(value))
                line = next(reader)
            line = next(reader)

            if 'Method Standards' not in line[0]:
                raise Exception("Method Standards not in file")
            results['method_standards'] = {}
            line = next(reader)
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = line[0]
                value_list = line.pop(0)
                results['method_standards'][key] = value_list
                line = next(reader)
            line = next(reader)
            # Added this bit here so you can cycle through the method standards to populate the concentraiton and ion
            # columns in reorganize_headers_logic.py
            method_standards = list(results['method_standards'].keys())
            clean_method_standards = []
            for item in method_standards:
                text_split = item.split(" ")
                text_join = text_split[0] + " " + text_split[2]
                clean_method_standards.append(text_join)

            if "Internal Standards" not in line[0]:
                raise Exception("Internal Standards not in file")
            results['method_internal_standards'] = {}
            line = next(reader)
            while not (len(line) == 0 or (line[0] == '' and all_equal(line))):
                key = line[0].split(" -")[0]
                value_list = key + line[0].split(",")[1]
                results['method_internal_standards'][key] = value_list
                line = next(reader)

            return results
