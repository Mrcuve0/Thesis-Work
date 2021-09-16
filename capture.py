import multiprocessing
import os

from typing import List
from chipwhisperer.common.api.ProjectFormat import Project
from numpy.core.fromnumeric import clip
import globals
import CW_init
import sboxes

import random
import time

import chipwhisperer as cw
import chipwhisperer.analyzer as cwa

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')   # Lifesaver command to avoid X non-requested usage (see https://stackoverflow.com/a/34583288)

import numpy as np
import pandas as pd

from datetime import datetime
from tqdm import trange
from tqdm.cli import main
from pathlib import Path
from globals import ThesisProject


#   _____  ______ ______   
#  |  __ \|  ____|  ____|  
#  | |  | | |__  | |__ ___ 
#  | |  | |  __| |  __/ __|
#  | |__| | |____| |  \__ \
#  |_____/|______|_|  |___/
#                          
#                          

# class AES128_sbox_freyre_1(cwa.AESLeakageHelper):
#     name = 'HW: AES Freyre1 SBox Output, First Round (Enc)'
#     def leakage(self, pt, ct, key, bnum):
#         return self.sbox_freyre_1((pt[bnum] ^ key[bnum]))
    
# class AES128_sbox_freyre_2(cwa.AESLeakageHelper):
#     name = 'HW: AES Freyre2 SBox Output, First Round (Enc)'
#     def leakage(self, pt, ct, key, bnum):
#         return self.sbox_freyre_2((pt[bnum] ^ key[bnum]))
    
# class AES128_sbox_freyre_3(cwa.AESLeakageHelper):
#     name = 'HW: AES Freyre3 SBox Output, First Round (Enc)'
#     def leakage(self, pt, ct, key, bnum):
#         return self.sbox_freyre_3((pt[bnum] ^ key[bnum]))

def CW_capture(proj_name, scope, target) -> Project:
    """
    Creates a project, captures for a specified number of traces, saves them in the project
    """
    ktp = cw.ktp.Basic()

    current_project = cw.create_project(f"{proj_absolute_path}{proj_name}", overwrite=True)

    for i in trange(globals.num_traces):
        key, text = ktp.next()
        trace = cw.capture_trace(scope, target, text, key)
        if not trace:
            continue
        current_project.traces.append(trace)

    if (globals.enable_autosave is True):
        current_project.export(f"{proj_absolute_path}/{zips_folder_name}{proj_name}")
        current_project.save()
    else:
        pass

    return current_project


# Definition of the formatter, .format() accepts a callable argument, called with the value of a individual cell
# "stat" is a single cell: each cell is a triple (key_guess, corr_position, corr)
def format_stat(stat) -> str:
    """
    Formats row by row the content of the cells: the bytes are expressed in hex, the correlation position is discarded
    """
    # Let's avoid once again the effects of the PGE row
    if type(stat) is int:
        return str(stat)
    else:
        return str("{:02X}<br>{:.3f}".format(stat[0], stat[2]))


# .apply() applies a function column-wise, row-wise or table-wise
def color_corr_key(row) -> list:
    """
    Given a row, we apply the red color to all those cells that contain the correct key guess
    """
    global key
    ret = [""] * 16
    # Let's avoid the effects of the PGE row
    if (row.name != 'PGE='):
        for i,bnum in enumerate(row):
            if bnum[0] == key[i]:
                ret[i] = "color: red"
            else:
                ret[i] = ""
    return ret


def stats_callback() -> None:
    """
    Callback function, called each num_callback_traces to plot intermediate results
    """
    global key
    global attack
    global callback_trace_current_num

    # print(f"[PID: {os.getpid()}]\t[stats_callback]")

    # Let's retrieve the attack results obtained up to now
    results = attack.results
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | attack.results done!")

    # Let's set the known key
    results.set_known_key(key)

    # Retrieves a list with 16 elements, one for each subkey.
    # Each subkey contains a list with all the 256 possible guesses
    # Each guess consists of a tuple containing the guess value, the correlation value and its X position
    stat_data = results.find_maximums()
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | results.find_maximums() done!")
    
    # Create a Pandas DataFrame (tabular data) with the retrieved data
    df = pd.DataFrame(stat_data).transpose()
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | df=pd.DataFrame().transpose() done!")

    #Add PGE row
    df_pge = pd.DataFrame(results.pge).transpose().rename(index={0:"PGE="}, columns=int)
    df = pd.concat([df_pge, df], ignore_index=False)

    # Display the dataFrame using a certain layout, define the color used to represent the real key bytes
    df_styled = df.head(globals.num_df_head).style.format(format_stat).apply(color_corr_key, axis=1).set_caption(f"Finished traces {callback_trace_current_num} to {globals.num_traces}")
    df_styled = df_styled.set_table_styles([
        {'selector': 'tbody tr:nth-child(even)',
            'props': [("background-color", '#fff')]},
        {'selector': 'tbody tr:nth-child(odd)',
            'props': [("background-color", '#eee')]},
        {'selector': 'td',
            'props': [("padding", '.8em')]},
        {'selector': 'th',
            'props': [("font-size", 'globals.num_df_head0%'), ("text-align", "center")]},
        {'selector': 'thead',
            'props': [("border-bottom", "1px solid black"), ("vertical-align", "bottom")]},
        {'selector': ' ',
            'props': [("margin", '0'),("font-family",'"Helvetica", "Arial", sans-serif'), ("border-collapse", "collapse"), ("border","none"), ("text-align", "right")]}
    ])
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | .format(format_stat).apply(color_corr_key) done!")

    # Save Files
    with open(f"{current_proj_absolute_path}/{dataframes_folder_name}/dataframe_traces[{callback_trace_current_num} of {globals.num_traces}].html", 'w') as f:
        f.write(df_styled.render())
    df.head(globals.num_df_head).to_latex(f"{current_proj_absolute_path}/{latex_folder_name}/table_traces[{callback_trace_current_num} of {globals.num_traces}].tex");
    df.head(globals.num_df_head).to_csv(f"{current_proj_absolute_path}/{csv_folder_name}/csv_traces[{callback_trace_current_num} of {globals.num_traces}].csv");

    # print(f"[PID: {os.getpid()}]\t[stats_callback] | Save Files done!")
    callback_trace_current_num += globals.num_callback_traces
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | callback_trace_current_num increment done!")
    # print(f"[PID: {os.getpid()}]\t[stats_callback] | callback_trace_current_num: {callback_trace_current_num}")


def plot_pge(plot_data) -> None:
    """
    Plots the PGE trends for all the 16 correct key guesses
    """
    global key

    # clip_min_y = 0
    # clip_max_y = 300

    pges = [plot_data.pge_vs_trace(i) for i,_ in enumerate(key)]

    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[14,10])
    plt.grid(b=True, which='major', axis='both', alpha=0.2)
    
    for i, bnum in enumerate(key):
        plt.plot(pges[i][0], pges[i][1], linewidth=3, label=f"Byte #{i}")
        # plt.plot(pges[i][0], pges[i][1], linewidth=3, label=f"Byte #{i} | Key: 0x{bnum:02X}")

    plt.plot(pges[i][0], [globals.pge_threshold for _ in range(len(pges[i][0]))], linewidth=3, linestyle="dashed",  color="red", label=f"max(PGE) < {globals.pge_threshold}")
    # plt.plot(pges[i][0], [globals.pge_threshold for _ in range(len(pges[i][0]))], linewidth=3, color="red", label=f"max(PGE) < {globals.pge_threshold}")
        
    plt.legend(title=f"Known Key", fontsize=12, loc="upper right")
    plt.title(f"{proj_name} - PGE", fontsize=18)

    ax1.set_xticks(globals.x_axis)
    # ax1.set_yticks(list(range(clip_min_y, clip_max_y+1, 10)))
    ax1.set_ylabel('Partial Guessing Entropy (PGE)', fontsize=16)
    ax1.set_xlabel('Traces', fontsize=16)

    # plt.show()
    plt.savefig(f"{current_proj_absolute_path}/{plots_folder_name}/PGE.png")
    plt.close(fig)


def plot_correlation(plot_data) -> None:
    """
    Plots the various correlations of both the correct key guesses and the wrong ones
    """
    global key

    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[18,12])
    plt.grid(b=True, which='major', axis='both', alpha=0.2)

    # Plot the wrong key_guesses
    decimator = 0
    for i, bnum in enumerate(key):
        corrs = plot_data.corr_vs_trace(i)
        for j in range(0, 256):
            decimator += 1
            if (j != bnum):
                if (decimator % 10 == 0):
                    plt.plot(corrs[0], corrs[1][j], color="#73757a")
                    
    # Now plot the corect key_guesses on top of the wrong ones
    for i, bnum in enumerate(key):
        corrs = plot_data.corr_vs_trace(i)
        for j in range(0, 256):
            if (j == bnum):
                plt.plot(corrs[0], corrs[1][j], linewidth=3, label=f"Byte #{i}")

    plt.legend(title=f"Known Key", fontsize=12, loc="lower left")
    plt.title(f"{proj_name} - Correlations", fontsize=18)

    ax1.set_xticks(globals.x_axis)
    ax1.set_ylabel('Correlation', fontsize=16)
    ax1.set_xlabel('Traces', fontsize=16)
    
    # plt.show()
    plt.savefig(f"{current_proj_absolute_path}/{plots_folder_name}/correlations.png")
    plt.close(fig)


def plot_avg_pge(iterations_data, key) -> None:
    """
    Plots the average PGE trends for all the 16 correct key guesses
    """

    clip_min_y = 0

    if globals.num_traces == 50:
        clip_max_y = 50
        y_step = 4
    elif globals.num_traces == 100:
        clip_max_y = 25
        y_step = 2
    elif globals.num_traces == 200:
        clip_max_y = 12
        y_step = 1
    else:
        clip_max_y = 6
        y_step = 1

    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[14,10])
    plt.grid(b=True, which='major', axis='both', alpha=0.2)

    x_axis = iterations_data[0].pge_vs_trace(0)[0]

    key_pge_traces_summary = [[], []]
    for i, bnum in enumerate(key):
        pges_traces = []
        for sbox_iteration, plot_data in enumerate(iterations_data):
            pges = plot_data.pge_vs_trace(i)
            # Isolate the PGE trace for the given key in the given iteration
            pges_traces.append(pges[1])
        # Compute the mean and std_dev for the given key considered ALL possible iterations
        key_pge_traces_summary[0] = np.mean(pges_traces, 0).astype(int)
        key_pge_traces_summary[1] = np.std(pges_traces, 0)
        # plt.plot(x_axis, key_pge_traces_summary[0], clip_min_y, clip_max_y, linewidth=3, label=f"Byte #{i} | Key: 0x{bnum:02X}")
        # plt.plot(x_axis, key_pge_traces_summary[0], clip_min_y, clip_max_y, linewidth=3, label=f"Byte #{i}")
        plt.plot(x_axis, key_pge_traces_summary[0], linewidth=3, label=f"Byte #{i}")

        max_clipped = np.add(key_pge_traces_summary[0], key_pge_traces_summary[1])
        max_clipped = np.clip(max_clipped, clip_min_y, clip_max_y)
        min_clipped = np.subtract(key_pge_traces_summary[0], key_pge_traces_summary[1])
        min_clipped = np.clip(min_clipped, clip_min_y, clip_max_y)
        ax1.fill_between(x_axis, max_clipped, min_clipped, alpha=0.1)

    # plt.plot(x_axis, [globals.pge_threshold for _ in range(len(x_axis))], linewidth=3, color="red", label=f"max(PGE) < {globals.pge_threshold}")
    plt.plot(x_axis, [globals.pge_threshold for _ in range(len(x_axis))], linewidth=3, linestyle="dashed", color="red", label=f"max(PGE) < {globals.pge_threshold}")
    
    plt.legend(title=f"Known Key", fontsize=12, loc="upper right")
    plt.title(f"{proj_name} - Average PGE (on {globals.test_iterations} iterations)", fontsize=18)
    ax1.set_xticks(globals.x_axis)
    ax1.set_yticks(list(range(clip_min_y, clip_max_y+1, y_step)))
    ax1.set_ylabel(f"Average Partial Guessing Entropy (PGE)", fontsize=16)
    ax1.set_ylim([clip_min_y, clip_max_y])
    ax1.set_xlabel('Traces', fontsize=16)

    # plt.show()
    plt.savefig(f"{proj_absolute_path}/{plots_folder_name}/avg_PGE.png")
    plt.close(fig)


# def plot_avg_correlation(iterations_data, key) -> None:
#     """
#     Plots the average correlations of both the correct key guesses and the wrong ones
#     """

#     fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[18,12])
#     plt.grid(b=True, which='major', axis='both', alpha=0.2)

#     # Collect all the wrong key_guesses trace (w/ decimation)
#     decimator = 0

#     x_axis = iterations_data[0].corr_vs_trace(0)[0]

#     # for sbox_i, sbox_data in enumerate(sboxes_data):
#     for i, bnum in enumerate(key):
#         for j in range(0, 256):
#             decimator += 1
#             if (j != bnum and decimator % 10 == 0):
#                 nonkey_corr_traces_summary = [[],[]]
#                 corrs_traces = []
#                 for sbox_iteration, plot_data in enumerate(iterations_data):
#                     corrs = plot_data.corr_vs_trace(i)
#                     # Isolate the correlation trace for the given WRONG subkey candidate in the given iteration
#                     corrs_traces.append(corrs[1][j])
#                 # Compute the mean and std_dev for the given WRONG subkey candidate considered ALL possible iterations
#                 nonkey_corr_traces_summary[0] = np.mean(corrs_traces, 0)
#                 nonkey_corr_traces_summary[1] = np.std(corrs_traces, 0)
#                 # nonkeys_summaries[i].append(nonkey_corr_traces_summary)
#                 plt.plot(x_axis, nonkey_corr_traces_summary[0], color="#73757a")

#     # Now plot the corect key_guesses on top of the wrong ones
#     for i, bnum in enumerate(key):
#         for j in range(0, 256):
#             if (j == bnum):
#                 key_corr_traces_summary = [[],[]]
#                 corrs_traces = []
#                 for sbox_iteration, plot_data in enumerate(iterations_data):
#                     corrs = plot_data.corr_vs_trace(i)
#                     # Isolate the correlation trace for the given CORRECT subkey candidate in the given iteration
#                     corrs_traces.append(corrs[1][j])
#                 # Compute the mean and std_dev for the given CORRECT subkey candidate considered ALL possible iterations
#                 key_corr_traces_summary[0] = np.mean(corrs_traces, 0)
#                 key_corr_traces_summary[1] = np.std(corrs_traces, 0)
#                 # plt.plot(x_axis, key_corr_traces_summary[0], linewidth=3, label=f"Byte #{i} | Key: 0x{bnum:02X}")
#                 plt.plot(x_axis, key_corr_traces_summary[0], linewidth=3, label=f"Byte #{i}")
#                 ax1.fill_between(x_axis, key_corr_traces_summary[0] + key_corr_traces_summary[1], key_corr_traces_summary[0] - key_corr_traces_summary[1], alpha=0.1)


#     plt.legend(title=f"Known Key", fontsize=12, loc="lower left")
#     plt.title(f"{proj_name} - Average Correlations (on {globals.test_iterations} iterations)", fontsize=18)

#     ax1.set_xticks(globals.x_axis)
#     ax1.set_ylabel('Average Correlation', fontsize=16)
#     ax1.set_xlabel('Traces', fontsize=16)
    
#     # plt.show()
#     plt.savefig(f"{proj_absolute_path}/{plots_folder_name}/avg_correlations.png")
#     plt.close(fig)


def plot_avg_correlation(iterations_data, key) -> None:
    """
    Plots the average correlations of both the correct key guesses and the wrong ones so to visually compute the MTD (Minimum Traces to Disclosure) metric
    """

    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[18,12])
    fig_mtd, ax1_mtd = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=[18,12])

    plt.grid(b=True, which='major', axis='both', alpha=0.2)

    # Collect all the wrong key_guesses trace (w/ decimation)
    decimator = 0

    x_axis = iterations_data[0].corr_vs_trace(0)[0]

    # for sbox_i, sbox_data in enumerate(sboxes_data):
    for i, bnum in enumerate(key):
        for j in range(0, 256):
            decimator += 1

            if (j != bnum):
                corrs_traces = []
                nonkey_corr_traces_summary = [[],[]] 
                for sbox_iteration, plot_data in enumerate(iterations_data):
                    corrs = plot_data.corr_vs_trace(i)
                    # Isolate the correlation trace for the given WRONG subkey candidate in the given iteration
                    corrs_traces.append(corrs[1][j])
                # Compute the mean and std_dev for the given WRONG subkey candidate considered ALL possible iterations
                nonkey_corr_traces_summary[0] = np.mean(corrs_traces, 0)
                nonkey_corr_traces_summary[1] = np.std(corrs_traces, 0)
                
                if (decimator % 10 == 0):
                    ax1.plot(x_axis, nonkey_corr_traces_summary[0], color="#73757a")
                line_wrong, = ax1_mtd.plot(x_axis, nonkey_corr_traces_summary[0], color="#00e5f0", label=f"Incorrect Keys")




            # if (j != bnum and decimator % 10 == 0):
            #     corrs_traces = []
            #     nonkey_corr_traces_summary = [[],[]] 
            #     for sbox_iteration, plot_data in enumerate(iterations_data):
            #         corrs = plot_data.corr_vs_trace(i)
            #         # Isolate the correlation trace for the given WRONG subkey candidate in the given iteration
            #         corrs_traces.append(corrs[1][j])
            #     # Compute the mean and std_dev for the given WRONG subkey candidate considered ALL possible iterations
            #     nonkey_corr_traces_summary[0] = np.mean(corrs_traces, 0)
            #     nonkey_corr_traces_summary[1] = np.std(corrs_traces, 0)

            #     # nonkeys_summaries[i].append(nonkey_corr_traces_summary)
            #     ax1.plot(x_axis, nonkey_corr_traces_summary[0], color="#73757a")

            # if (j != bnum):
            #     corrs_traces = []
            #     nonkey_corr_traces_summary = [[],[]] 
            #     for sbox_iteration, plot_data in enumerate(iterations_data):
            #         corrs = plot_data.corr_vs_trace(i)
            #         # Isolate the correlation trace for the given WRONG subkey candidate in the given iteration
            #         corrs_traces.append(corrs[1][j])
            #     # Compute the mean and std_dev for the given WRONG subkey candidate considered ALL possible iterations
            #     nonkey_corr_traces_summary[0] = np.mean(corrs_traces, 0)

            #     line_wrong, = ax1_mtd.plot(x_axis, nonkey_corr_traces_summary[0], color="#00e5f0", label=f"Incorrect Keys")


    # Now plot the corect key_guesses on top of the wrong ones
    key_corr_traces_mtd = []
    for i, bnum in enumerate(key):
        for j in range(0, 256):
            if (j == bnum):
                corrs_traces = []
                key_mtd = []
                key_corr_traces_summary = [[],[]]
                for sbox_iteration, plot_data in enumerate(iterations_data):
                    corrs = plot_data.corr_vs_trace(i)
                    # Isolate the correlation trace for the given CORRECT subkey candidate in the given iteration
                    corrs_traces.append(corrs[1][j])
                # Compute the mean and std_dev for the given CORRECT subkey candidate considered ALL possible iterations
                key_corr_traces_summary[0] = np.mean(corrs_traces, 0)
                key_corr_traces_summary[1] = np.std(corrs_traces, 0)
                key_corr_traces_mtd.append(key_corr_traces_summary[0])
                # plt.plot(x_axis, key_corr_traces_summary[0], linewidth=3, label=f"Byte #{i} | Key: 0x{bnum:02X}")
                ax1.plot(x_axis, key_corr_traces_summary[0], linewidth=3, label=f"Byte #{i}")
                ax1.fill_between(x_axis, key_corr_traces_summary[0] + key_corr_traces_summary[1], key_corr_traces_summary[0] - key_corr_traces_summary[1], alpha=0.1)
                
    key_mtd = np.mean(key_corr_traces_mtd, 0)
    # print(f"key_corr_traces_mtd: {key_corr_traces_mtd}")
    # print(f"key_corr_traces_mtd[0]: {key_corr_traces_mtd[0]}")
    # print(f"key_mtd: {key_mtd}")

    line_key, = ax1_mtd.plot(x_axis, key_mtd, color="#ff0000", linewidth=3, label=f"Correct Key")

    ax1.legend(title=f"Known Key", fontsize=12, loc="lower left")
    ax1.set_title(f"{proj_name} - Average Correlations (on {globals.test_iterations} iterations)", fontsize=18)
    ax1.set_xticks(globals.x_axis)
    ax1.set_ylabel('Average Correlation', fontsize=16)
    ax1.set_xlabel('Traces', fontsize=16)

    # ax1_mtd.legend(by_label.values(), by_label.keys(), title=f"MTD", fontsize=12, loc="lower left")
    ax1_mtd.legend([line_key, line_wrong], [f"Correct Key",f"Incorrect Keys"], title=f"MTD", fontsize=12, loc="lower left")
    ax1_mtd.set_title(f"{proj_name} - Minimum Traces to Disclosure (on {globals.test_iterations} iterations)", fontsize=18)
    ax1_mtd.set_xticks(globals.x_axis)
    ax1_mtd.set_ylabel('Average Correlation', fontsize=16)
    ax1_mtd.set_xlabel('Traces', fontsize=16)
    
    # plt.show()
    fig.savefig(f"{proj_absolute_path}/{plots_folder_name}/avg_correlations.png")
    plt.close(fig)

    fig_mtd.savefig(f"{proj_absolute_path}/{plots_folder_name}/mtd.png")
    plt.close(fig_mtd)


def print_time_results(script_time, capture_time) -> None:
    """
    Prints the time required for capturing the given number of traces and to analyze them.
    """
    print(f"\n")
    print(f"🔵 [INFO] Printing the execution times")

    print(f"TOT Script Time (hh:mm:ss.ms): {script_time}\n")
    
    print(f"--> TOT Time required by capture: {capture_time:.4f} secs")
    print(f"\t--> Time required by each trace captured: {capture_time/globals.num_traces:.4f} secs\n")
    print(f"\n")


def multiprocess_cpa(proj_data) -> list:
    """
    Function executed by each process. A CPA attack on the given project is performed, the related data and plots are created.
    """
    global key
    global attack
    global callback_trace_current_num
    global current_proj_absolute_path

    # Set path for stats_callback() function, which cannot accept parameters
    current_proj_absolute_path = proj_data[0]

    print(f"[PID: {os.getpid()}]\t[multiprocess_cpa]\t[path = {proj_data[0]}]\t[proj = {proj_data[1]}]")

    # Each process should open its corresponding project
    current_project = cw.open_project(f"{proj_data[0]}{proj_data[1]}")

    # Compute the Signal-to-Noise ratio
    # cwa.calculate_snr(current_project.traces, leak_model)

    # Retrieve the reference secret key
    key = current_project.keys[0]
    # print(f"[PID: {os.getpid()}]\t[multiprocess_dpa] | key is {key}")
    
    # Analyze Traces
    attack = cwa.cpa(current_project, leak_model)
    # print(f"[PID: {os.getpid()}]\t[multiprocess_cpa] | cwa.cpa() done!")

    # Correlation Power Analysis
    callback_trace_current_num = globals.num_callback_traces
    results = attack.run(stats_callback, globals.num_callback_traces)
    # print(f"[PID: {os.getpid()}]\t[multiprocess_cpa] | attack.run() done!")

    plot_data = cwa.analyzer_plots(results)
    plot_pge(plot_data)
    # print(f"[PID: {os.getpid()}]\t[multiprocess_cpa] | plot_pge() done!")
    plot_correlation(plot_data)
    # print(f"[PID: {os.getpid()}]\t[multiprocess_cpa] | plot_correlation() done!")
    # print(f"[PID: {os.getpid()}]\t[multiprocess_cpa] | plot_data: {plot_data}")

    return plot_data, key

#   __  __          _____ _   _ 
#  |  \/  |   /\   |_   _| \ | |
#  | \  / |  /  \    | | |  \| |
#  | |\/| | / /\ \   | | | . ` |
#  | |  | |/ ____ \ _| |_| |\  |
#  |_|  |_/_/    \_\_____|_| \_|
#                               
#                               

if __name__ == "__main__":
    script_begin_time = datetime.now()

    globals.enable_capture  = False
    globals.enable_autosave = False
    globals.enable_analysis = True

    globals.multiproc = True

    if (globals.enable_analysis is False):
        globals.multiproc = False
    else:
        pass

    key = None
    attack = None
    callback_trace_current_num = None
    current_proj_absolute_path = None

    # Num of traces to capture
    traces = [
        # 50, 
        100, 
        200,
        300, 
        500, 
        # 1000, 
        # 5000,
        # 10_000
        ]

    for globals.num_traces in traces:
        globals.num_callback_traces = globals.num_traces//10
        globals.x_axis = list(range(0, globals.num_callback_traces + globals.num_traces, globals.num_callback_traces))

        # In this test, iterate so to test all available SBoxes
        for sbox_num in ThesisProject:
            if (sbox_num == ThesisProject.AES_SBOX):
                proj_name = "AES_SBOX"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_output

            elif (sbox_num == ThesisProject.FREYRE_SBOX_1):
                proj_name = "Freyre_SBOX_1"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_freyre_1

            elif (sbox_num == ThesisProject.FREYRE_SBOX_2):
                proj_name = "Freyre_SBOX_2"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_freyre_2

            elif (sbox_num == ThesisProject.FREYRE_SBOX_3):
                proj_name = "Freyre_SBOX_3"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_freyre_3

            elif (sbox_num == ThesisProject.HUSSAIN_SBOX_6):
                proj_name = "Hussain_SBOX_6"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_hussain_6

            elif (sbox_num == ThesisProject.OZKAYNAK_SBOX_1):
                proj_name = "Ozkaynak_SBOX_1"
                # +str(globals.num_traces)
                leak_model = cwa.leakage_models.sbox_ozkaynak_1
            else:
                pass

            # Stores all the data computed in all the iterations for the current SBox
            # if globals.multiproc is False:
            iterations_data = []
    
            proj_absolute_paths = []
            proj_names = []

            for i in range(0+globals.iterations_offset, globals.test_iterations+globals.iterations_offset):
                # Connect and Init ChipWhisperer if capture is required
                if (globals.enable_capture is True):
                    (scope, target, prog) = CW_init.cw_init()
                else:
                    pass

                # Define Paths and create related folders if don't exist
                proj_absolute_path = f"{Path.cwd()}/projects_additional/traces_{globals.num_traces}_{i}/{proj_name}/"
                zips_folder_name = "zips"
                dataframes_folder_name = "dataframes"
                csv_folder_name = "csv"
                latex_folder_name = "latex"
                plots_folder_name = "plots"

                for folder in ["", zips_folder_name, dataframes_folder_name, csv_folder_name, latex_folder_name, plots_folder_name]:
                    p = Path(f"{proj_absolute_path}/{folder}")
                    p.mkdir(parents=True, exist_ok=True)



                # Print Globals configuration
                print(f"\n🟢Project: {proj_name} | Iteration #{i} | Testing SBOX #{sbox_num.value}🟢\n")
                globals.print_globals_config()

                # Capture traces if necessary or load previous project
                capture_time = -1
                if (globals.enable_capture is True):
                    # Compile and Program Target
                    CW_init.compile_target(sbox_num.value)
                    CW_init.program_target(scope, prog)
                    # Launch Trace Capture
                    capture_start_time = time.time()
                    current_project = CW_capture(proj_name, scope, target)
                    capture_end_time = time.time()
                    capture_time = capture_end_time - capture_start_time
                    CW_init.disconnect(scope, target)

                # Do a CPA attack if requested
                if (globals.enable_analysis is True):
                    if (globals.enable_capture is True):
                        # The project is already open, no need to do anything
                        pass
                    else:
                        # Need to open a project
                        if globals.multiproc is True:
                            proj_absolute_paths.append(proj_absolute_path)
                            proj_names.append(proj_name)
                        else:
                            # No multiprocessing available
                            # Setting path vars for stats_callback() function
                            current_proj_absolute_path = proj_absolute_path
                            current_project = cw.open_project(f"{proj_absolute_path}{proj_name}")
                            # Retrieve the reference secret key
                            key = current_project.keys[0]
                            # Analyze Traces
                            attack = cwa.cpa(current_project, leak_model)
                            # Correlation Power Analysis
                            attack_start_time = time.time()
                            callback_trace_current_num = globals.num_callback_traces
                            results = attack.run(stats_callback, globals.num_callback_traces)
                            attack_end_time = time.time()
                            attack_time = attack_end_time - attack_start_time

                            plot_data = cwa.analyzer_plots(results)
                            plot_pge(plot_data)
                            plot_correlation(plot_data)

                            # Given this SBox, store the data computed for this i-th iteration
                            iterations_data.append(plot_data)
                else:
                    pass

            # END "for" on all iterations for this specific SBox

            # If Multiprocessing is enabled, the N iterations required are computed on N different cores so to speedup the analysis
            if (globals.multiproc is True):
                iterations_data = []
                key = []
                with multiprocessing.Pool() as pool:
                    for data, k in pool.map(multiprocess_cpa, zip(proj_absolute_paths, proj_names)):
                        key.append(k)
                        iterations_data.append(data)
                key = key[0]

            if (globals.enable_analysis is True):
                # Print the average correlation traces (for MTD computation)
                plot_avg_correlation(iterations_data, key)
                # Print the average PGE traces
                plot_avg_pge(iterations_data, key)
            else:
                pass

        # END "for" on all SBoxes to be tested
    # END "for" on all set of traces

    # Compute the overall time necessary to complete the script
    script_end_time = datetime.now()
    ### END
    print_time_results(script_end_time-script_begin_time, capture_time)