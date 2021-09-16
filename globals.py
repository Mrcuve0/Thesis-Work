import random
from enum import IntEnum
from random import sample

#    _____ ____  _   _ ______ _____ _____ 
#   / ____/ __ \| \ | |  ____|_   _/ ____|
#  | |   | |  | |  \| | |__    | || |  __ 
#  | |   | |  | | . ` |  __|   | || | |_ |
#  | |___| |__| | |\  | |     _| || |__| |
#   \_____\____/|_| \_|_|    |_____\_____|
#                                         
#                                         

# Dummy default vars, set them inside capture.py script
enable_capture  = False
enable_autosave = False
enable_analysis = False

#    _______          __
#   / ____\ \        / /
#  | |     \ \  /\  / / 
#  | |      \ \/  \/ /  
#  | |____   \  /\  /   
#   \_____|   \/  \/    
#                       
#                       

cw_platform = "CWLITEXMEGA"
cw_cryptotarget = "AVRCRYPTOLIB"
cw_scope_adc_samples = 5000

cw_target_fw_absolute_path = "/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/ChipWhisperer_Projects/chipwhisperer/hardware/victims/firmware/simpleserial-aes/"
cw_target_fw_hex = f"simpleserial-aes-{cw_platform}.hex"

#   _____  _____   ____       _ ______ _____ _______ 
#  |  __ \|  __ \ / __ \     | |  ____/ ____|__   __|
#  | |__) | |__) | |  | |    | | |__ | |       | |   
#  |  ___/|  _  /| |  | |_   | |  __|| |       | |   
#  | |    | | \ \| |__| | |__| | |___| |____   | |   
#  |_|    |_|  \_\\____/ \____/|______\_____|  |_|   
#                                                    
#                                                    

multiproc = True

test_iterations = 20
iterations_offset = 0

num_traces = 50
num_callback_traces = num_traces//10
num_df_head = 10
pge_threshold = 4
num_bits = 8
num_keys = pow(2, num_bits)
num_bytes = 16

x_axis = list(range(0, num_callback_traces+num_traces, num_callback_traces))

class ThesisProject(IntEnum):
    AES_SBOX = 0
    FREYRE_SBOX_1 = 1
    FREYRE_SBOX_2 = 2
    FREYRE_SBOX_3 = 3
    HUSSAIN_SBOX_6 = 4
    OZKAYNAK_SBOX_1 = 5

def print_globals_config():
    """
    Print a summary of the global script configuration (you an adjust the parameters by modifying
    the `globals.py` script)
    """
    print(f"\n")
    print(f" --- Globals Config ---")
    print(f"\t --> enable_capture:\t{enable_capture}")
    print(f"\t --> enable_autosave:\t{enable_autosave}")
    print(f"\t --> enable_analysis:\t{enable_analysis}")
    print(f"\t --> multiproc:\t{multiproc}")
    print(f"\t --> num_bits:\t{num_bits}")
    print(f"\t --> num_bytes:\t{num_bytes}")
    print(f"\t --> num_keys:\t{num_keys}")
    print(f"\t --> num_traces:{num_traces}")
    print(f"\t --> num_callback_traces:{num_callback_traces}")
    print(f"\t --> num_df_head:\t{num_df_head}")
    print(f"\t --> pge_threshold:\t{pge_threshold}")
    print(f" --- Globals Config ---")
    print(f"\n")






