from chipwhisperer.common.api.ProjectFormat import Project
import globals
import CW_init
import sboxes

import random
import time

import chipwhisperer as cw
import chipwhisperer.analyzer as cwa
import matplotlib.pyplot as plt
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

    ktp = cw.ktp.Basic()

    # Let's create a key/text pair
    # key, text = ktp.next()
    # secret_key = key
    # The key is sent to the target and will be kept fixed from now on
    # target.simpleserial_write('k', key)

    current_project = cw.create_project(f"{proj_absolute_path}{proj_name}", overwrite=True)

    for i in trange(globals.num_traces):
        key, text = ktp.next()
        trace = cw.capture_trace(scope, target, text, key)
        if not trace:
            continue
        current_project.traces.append(trace)

    if (globals.enable_autosave is True):
        current_project.export(f"{proj_zip_absolute_path}{proj_name}")
        current_project.save()
    else:
        pass

    return current_project


# Definition of the formatter, .format() accepts a callable argument, called with the value of a individual cell
# "stat" is a single cell: each cell is a triple (key_guess, corr_position, corr)
def format_stat(stat):
    # Let's avoid once again the effects of the PGE row
    if type(stat) is int:
        return str(stat)
    else:
        return str("{:02X}<br>{:.3f}".format(stat[0], stat[2]))


# .apply() applies a function column-wise, row-wise or table-wise
# Given a row, we apply the red color to all those cells that contain the correct key guess
def color_corr_key(row):
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


def stats_callback():

    global callback_trace_current_num
    global key

    # Let's retrieve the attack results obtained up to now
    results = attack.results

    # Let's set the known key
    results.set_known_key(key)

    # Retrieves a list with 16 elements, one for each subkey.
    # Each subkey contains a list with all the 256 possible guesses
    # Each guess consists of a tuple containing the guess value, the correlation value and its X position
    stat_data = results.find_maximums()
    
    # Create a Pandas DataFrame (tabular data) with the retrieved data
    df = pd.DataFrame(stat_data).transpose()

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

    # Save Files
    with open(f"{dataframe_absolute_path}/dataframe_traces[{callback_trace_current_num} of {globals.num_traces}].html", 'w') as f:
        f.write(df_styled.render())
    df.head(globals.num_df_head).to_latex(f"{latex_absolute_path}/table_traces[{callback_trace_current_num} of {globals.num_traces}]");
    df.head(globals.num_df_head).to_csv(f"{csv_absolute_path}/csv_traces[{callback_trace_current_num} of {globals.num_traces}]");

    callback_trace_current_num += globals.num_callback_traces


def print_time_results(script_time, capture_time) -> None:
    print(f"\n")
    print(f"🔵 [INFO] Printing the execution times")

    print(f"TOT Script Time (hh:mm:ss.ms): {script_time}\n")
    
    print(f"--> TOT Time required by capture: {capture_time:.4f} secs")
    print(f"\t--> Time required by each trace captured: {capture_time/globals.num_traces:.4f} secs\n")
    print(f"\n")



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

    (scope, target, prog) = CW_init.cw_init()

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

        else:
            pass

        # Paths
        proj_absolute_path =        f"/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/projects/traces_{globals.num_traces}/{proj_name}/"
        proj_zip_absolute_path =    f"/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/projects/traces_{globals.num_traces}/{proj_name}/zips/"
        dataframe_absolute_path =   f"/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/projects/traces_{globals.num_traces}/{proj_name}/dataframes/"
        csv_absolute_path =         f"/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/projects/traces_{globals.num_traces}/{proj_name}/csv/"
        latex_absolute_path =       f"/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/projects/traces_{globals.num_traces}/{proj_name}/latex/"
        p = Path(f"{proj_absolute_path}")
        p.mkdir(parents=True, exist_ok=True)
        p = Path(f"{proj_zip_absolute_path}")
        p.mkdir(parents=True, exist_ok=True)
        p = Path(f"{dataframe_absolute_path}")
        p.mkdir(parents=True, exist_ok=True)
        p = Path(f"{csv_absolute_path}")
        p.mkdir(parents=True, exist_ok=True)
        p = Path(f"{latex_absolute_path}")
        p.mkdir(parents=True, exist_ok=True)


        # Print Globals configuration
        print(f"🟢 Starting testing SBOX #{sbox_num.value} | Project: {proj_name}🟢\n")
        globals.print_globals_config()

        # Capture traces
        capture_time = -1
        if (globals.enable_capture is True):
            # Compile and Program
            CW_init.compile_target(sbox_num.value)
            CW_init.program_target(scope, prog)

            capture_start_time = time.time()
            current_project = CW_capture(proj_name, scope, target)
            capture_end_time = time.time()
            capture_time = capture_end_time - capture_start_time
        else:
            current_project = cw.open_project(f"{proj_absolute_path}{proj_name}")

        if (globals.enable_analysis is True):
            # Retrieve the reference secret key
            key = current_project.keys[0]

            # Analyze Traces
            attack = cwa.cpa(current_project, leak_model)

            attack_start_time = time.time()
            callback_trace_current_num = globals.num_callback_traces
            results = attack.run(stats_callback, globals.num_callback_traces)
            attack_end_time = time.time()
            attack_time = attack_end_time - attack_start_time
        else:
            pass


    # end for
    CW_init.disconnect(scope, target)
    script_end_time = datetime.now()
    ### END
    print_time_results(script_end_time-script_begin_time, capture_time)





    # results_per_leak_bit = [[] for _ in range(globals.num_bits)]
    # for leak_bit_pos in range(globals.num_bits):
        
    #     print(f"\n")
    #     print(f"\t --> leak_position:\t{leak_bit_pos}")

    #     # Store your key_guess here, compare to known_key
    #     found_key = [0 for _ in range(globals.num_bytes)]
    #     keys_scores = [[] for _ in range(globals.num_keys)]

    #     cnt_found_list = []

    #     print(f"\n")
    #     print(f"🟢 Starting {len(ScoreModes)} different DPA attacks 🟢\n")
    #     for _, mode in enumerate(ScoreModes):
    #         if (mode == ScoreModes.GLOBAL_SAD):
    #             begin_time = time.time()
    #             cnt_found_list.append(DPA_subBytes_leakage_model(keys_scores, found_key, mode=mode, leak_position=leak_bit_pos))
    #             end_time = time.time()
    #             dpa_GLOBAL_SAD_times.append(end_time - begin_time)
    #         if (mode == ScoreModes.LOCAL_SAD):
    #             begin_time = time.time()
    #             cnt_found_list.append(DPA_subBytes_leakage_model(keys_scores, found_key, mode=mode, leak_position=leak_bit_pos))
    #             end_time = time.time()
    #             dpa_LOCAL_SAD_times.append(end_time - begin_time)
    #         if (mode == ScoreModes.GLOBAL_MAX):
    #             begin_time = time.time()
    #             cnt_found_list.append(DPA_subBytes_leakage_model(keys_scores, found_key, mode=mode, leak_position=leak_bit_pos))
    #             end_time = time.time()
    #             dpa_GLOBAL_MAX_times.append(end_time - begin_time)
    #         if (mode == ScoreModes.LOCAL_MAX):
    #             begin_time = time.time()
    #             cnt_found_list.append(DPA_subBytes_leakage_model(keys_scores, found_key, mode=mode, leak_position=leak_bit_pos))
    #             end_time = time.time()
    #             dpa_LOCAL_MAX_times.append(end_time - begin_time)

            
    #     print(f"\n")
    #     print(f"🟢 DPA AttacksSummary 🟢\n")
    #     for i, cnt_item in enumerate(cnt_found_list, start=1):
    #         if (i == (globals.ScoreModes.GLOBAL_SAD)):
    #             print(f"\tw/ ScoreModes.GLOBAL_SAD:\tfound {cnt_item}/16 keys!")
    #         if (i == (globals.ScoreModes.LOCAL_SAD)):
    #             print(f"\tw/ ScoreModes.LOCAL_SAD:\tfound {cnt_item}/16 keys!")
    #         if (i == (globals.ScoreModes.GLOBAL_MAX)):
    #             print(f"\tw/ ScoreModes.GLOBAL_MAX:\tfound {cnt_item}/16 keys!")
    #         if (i == (globals.ScoreModes.LOCAL_MAX)):
    #             print(f"\tw/ ScoreModes.LOCAL_MAX:\tfound {cnt_item}/16 keys!")

    #     results_per_leak_bit[leak_bit_pos] = cnt_found_list

    # script_end_time = datetime.now()
    # # results_per_leak_bit = [[random.randint(0,16) for _ in range(4)] for _ in range(16)]
    # plot_script_summary(results_per_leak_bit)
    # print_time_results(script_end_time-script_begin_time, capture_time, dpa_GLOBAL_SAD_times, dpa_GLOBAL_MAX_times, dpa_LOCAL_SAD_times, dpa_LOCAL_MAX_times)
