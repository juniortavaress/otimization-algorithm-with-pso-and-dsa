import os 
import json
import inspect
import pandas as pd
import numpy as np
from get_results_from_odb_file.layout_excel_file import *

# Calculates statistics (min, max, mean, std) for forces in the specified range.
def calculate_statistics(df, start_percent, end_percent):
    """
    Args:
        df (pd.DataFrame): DataFrame with experiment results.
        start_percent (float): Start percentage of the data range.
        end_percent (float): End percentage of the data range.

    Returns:
        dict: Dictionary with calculated statistics for cutting and normal forces.
    """
    length = len(df)
    start_index, end_index = int(length * start_percent), int(length * end_percent) - 1

    stats = {
        "Cutting Normal Force FcN [N]": df["Normal Force [N]"].iloc[start_index:end_index + 1].agg(['min', 'max', 'mean', 'std']),
        "Cutting Force Fc [N]": df["Cutting Force [N]"].iloc[start_index:end_index + 1].agg(['min', 'max', 'mean', 'std']),}
    return stats


# Combines the data of RF1 and RF2 into a single DataFrame.
def combine_data(data, workpiece_width_experiment, workpiece_width_simulation):
    """
    Args:
        data (dict): Dictionary containing the force data (RF1, RF2).
        filename (str): The JSON file name to be used as sheet name.

    Returns:
        pd.DataFrame: Combined dataframe of the forces.
    """
    rf1_df = pd.DataFrame(data["RF1"], columns=["Time [s]", "Force [N]"])
    rf2_df = pd.DataFrame(data["RF2"], columns=["Time [s]", "Force [N]"])
    rf_list = {"rf1": rf1_df, "rf2": rf2_df}

    for name, rf in rf_list.items():
        rf["Time [ms]"] = (rf["Time [s]"]*1000).round(2)
        new_column_name = "Cutting Force [N]" if name == "rf1" else "Normal Force [N]"
        rf[new_column_name] = (rf["Force [N]"] * workpiece_width_experiment / workpiece_width_simulation * (-1)).round(2)
        rf.drop(columns=["Time [s]", "Force [N]"], inplace=True)

    combined_df = pd.merge(rf1_df, rf2_df, on="Time [ms]", how="outer")
    return combined_df


# Function to process a JSON file and save data into an Excel sheet
def json_to_combined_excel(json_file, writer, stats_list, start_percent, end_percent, workpiece_width_experiment, workpiece_width_simulation, temperature_threshold):
    """
    Args:
        json_file (str): Path to the JSON file.
        writer (pandas.ExcelWriter): Excel writer object to save the data.
        stats_list (list): List to store calculated statistics.
        start_percent (float): Start percentage of the data range for statistics.
        end_percent (float): End percentage of the data range for statistics.
        workpiece_width_experiment (float): Width of the workpiece used in the experiment.
        workpiece_width_simulation (float): Width of the simulated workpiece.
        temperature_threshold (float): Temperature threshold for additional calculations.
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        combined_df_with_results = combine_data(data, workpiece_width_experiment, workpiece_width_simulation)
        sheet_name = os.path.basename(json_file)[0:29]
        # print('-', sheet_name)
    
        combined_df_with_results.to_excel(writer, sheet_name=sheet_name, index=False)

        # Calculate statistics
        stats = calculate_statistics(combined_df_with_results, start_percent, end_percent)

        # Flatten stats dictionary for easy insertion into the stats list
        stats_flat = {
            "Filename": sheet_name,
            "Normal Force [N].min": round(stats["Cutting Normal Force FcN [N]"]["min"], 2),
            "Normal Force [N].max": round(stats["Cutting Normal Force FcN [N]"]["max"], 2),
            "Normal Force [N].mean": round(stats["Cutting Normal Force FcN [N]"]["mean"], 2),
            "Normal Force [N].std": round(stats["Cutting Normal Force FcN [N]"]["std"], 2),
            "Cutting Force [N].min": round(stats["Cutting Force Fc [N]"]["min"], 2),
            "Cutting Force [N].max": round(stats["Cutting Force Fc [N]"]["max"], 2),
            "Cutting Force [N].mean": round(stats["Cutting Force Fc [N]"]["mean"], 2),
            "Cutting Force [N].std": round(stats["Cutting Force Fc [N]"]["std"], 2),
            # "Maximum Temperature at Last Frame [°C]": round(stats["Maximum Temperature at Last Frame [°C]"], 2),
            # f"Penetration Depth for Last Frame < {temperature_threshold}°C [µm]": round(stats[f"Penetration Depth for Last Frame < {temperature_threshold}°C [µm]"], 2),
            # "Temperature at Maximum Temperature at 1st Node [°C]": round(stats["Temperature at Maximum Temperature at 1st Node [°C]"], 2),
            # f"Penetration Depth for Frame with Tmax [µm]": round(stats[f"Penetration Depth for Frame with Tmax [µm]"], 2)
            "Maximum Temperature at Last Frame [°C]": round(97.66, 2),
            f"Penetration Depth for Last Frame < {temperature_threshold}°C [µm]": round(000.000, 2),
            "Temperature at Maximum Temperature at 1st Node [°C]": round(000.000, 2),
            f"Penetration Depth for Frame with Tmax [µm]": round(000.000, 2)}

        stats_list.append(stats_flat)
        add_graps_to_excel(writer, sheet_name, combined_df_with_results) # Add charts
        
    except Exception as e:
        print(f"Error processing file {json_file}: {e}")


# Process all JSON files in a folder and save combined data and statistics to an Excel file.
def process_json_to_excel(folder_path, output_file, start_percent, end_percent, workpiece_width_experiment, workpiece_width_simulation, temperature_threshold):
    """
    Args:
        folder_path (str): Path to the folder containing JSON files.
        output_file (str): Path to the output Excel file.
        start_percent (float): Start percentage of the data range.
        end_percent (float): End percentage of the data range.
        workpiece_width_experiment (float): Width of the workpiece used in the experiment.
        workpiece_width_simulation (float): Width of the simulated workpiece.
        temperature_threshold (float): Temperature threshold for calculations.
    """
    stats_list = []

    try:
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            stats_df = pd.DataFrame(stats_list)
            stats_df.to_excel(writer, sheet_name="Evaluation Statistics", index=False, startrow=2, header=False)
            stats_sheet = writer.sheets["Evaluation Statistics"]

            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    json_to_combined_excel(json_file_path, writer, stats_list, start_percent, end_percent, workpiece_width_experiment, workpiece_width_simulation, temperature_threshold)
            
            stats_df = pd.DataFrame(stats_list)
            stats_df.to_excel(writer, sheet_name="Evaluation Statistics", index=False, startrow=2, header=False)

            format_statistics_sheet_xlsxwriter(stats_sheet, writer.book, temperature_threshold, start_percent, end_percent)

    except Exception as e:
        print(f"Error writing Excel file: {e}")


# Main function
def main():
    """
    Main function to process JSON files and generate an Excel file with results.
    """
    main_dir = (os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
    result_dir = os.path.join(main_dir, "results-json-excel")
    json_dir = os.path.join(result_dir, "json-files") 
    excel_folder = os.path.join(result_dir, "excel-file")
    excel_output_file = os.path.join(excel_folder, "Results.xlsx")

    if not os.path.exists(excel_folder):
        os.makedirs(excel_folder)

    # Constants
    WORKPIECE_WIDTH_EXPERIMENT = 4
    WORKPIECE_WIDTH_SIMULATION = 0.02
    START_PERCENT = 0.25
    END_PERCENT = 1.00
    TEMPERATURE_THRESHOLD = 60

    process_json_to_excel(json_dir, excel_output_file, START_PERCENT, END_PERCENT, WORKPIECE_WIDTH_EXPERIMENT, WORKPIECE_WIDTH_SIMULATION, TEMPERATURE_THRESHOLD)


if __name__ == "__main__":
    main()
