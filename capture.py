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

def CW_capture(proj_name, scope, target):

    ktp = cw.ktp.Basic()
    trace_array = []
    textin_array = []

    # Let's create a key/text pair
    # key, text = ktp.next()
    # secret_key = key
    # The key is sent to the target and will be kept fixed from now on
    # target.simpleserial_write('k', key)

    proj = cw.create_project(proj_name, overwrite=True)

    for i in trange(globals.num_traces):
        key, text = ktp.next()
        trace = cw.capture_trace(scope, target, text, key)
        if not trace:
            continue
        proj.traces.append(trace)

    proj.export(globals.proj_export_absolute_path+'/'+proj_name)
    proj.save()


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
            proj_name = "AES_SBOX_"+str(globals.num_traces)+"traces"
            leak_model = cwa.leakage_models.sbox_output

        elif (sbox_num == ThesisProject.FREYRE_SBOX_1):
            proj_name = "Freyre_SBOX_1_"+str(globals.num_traces)+"traces"
            leak_model = cwa.leakage_models.sbox_freyre_1

        elif (sbox_num == ThesisProject.FREYRE_SBOX_2):
            proj_name = "Freyre_SBOX_2_"+str(globals.num_traces)+"traces"
            leak_model = cwa.leakage_models.sbox_freyre_2

        elif (sbox_num == ThesisProject.FREYRE_SBOX_3):
            proj_name = "Freyre_SBOX_3_"+str(globals.num_traces)+"traces"
            leak_model = cwa.leakage_models.sbox_freyre_3

        else:
            pass

        # Print Globals configuration
        print(f"🟢 Starting testing SBOX #{sbox_num.value} | Project: {proj_name}🟢\n")
        globals.print_globals_config()

        # Compile and Program
        CW_init.compile_target(sbox_num.value)
        CW_init.program_target(scope, prog)

        # Capture traces
        capture_time = -1
        if (globals.enable_capture is True):
            capture_begin_time = time.time()
            CW_capture(proj_name, scope, target)
            CW_init.disconnect(scope, target)
            capture_end_time = time.time()
            capture_time = capture_end_time - capture_begin_time
        else:
            current_project = cw.open_project(proj_name)

        # Analyze Traces
        attack = cwa.cpa(current_project, leak_model)
        results = attack.run()
        stat_data = results.find_maximums()
        df = pd.DataFrame(stat_data).transpose()

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
