import random
from enum import IntEnum
from random import sample

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

cw_target_fw_absolute_path = "/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/ChipWhisperer_Projects/chipwhisperer/hardware/victims/firmware/simpleserial-aes/"
cw_target_fw_hex = f"simpleserial-aes-{cw_platform}.hex"
cw_scope_adc_samples = 5000

#            ______  _____ 
#      /\   |  ____|/ ____|
#     /  \  | |__  | (___  
#    / /\ \ |  __|  \___ \ 
#   / ____ \| |____ ____) |
#  /_/    \_\______|_____/ 
#                          
#                          

# known_key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

# def aes_internal(key, input_byte) -> int:
#     """
#     Theoretical model representing the AddRoundKey and SubBytes AES operations
#     """
#     return sbox[key ^ input_byte]


#   _____  _____   ____       _ ______ _____ _______ 
#  |  __ \|  __ \ / __ \     | |  ____/ ____|__   __|
#  | |__) | |__) | |  | |    | | |__ | |       | |   
#  |  ___/|  _  /| |  | |_   | |  __|| |       | |   
#  | |    | | \ \| |__| | |__| | |___| |____   | |   
#  |_|    |_|  \_\\____/ \____/|______\_____|  |_|   
#                                                    
#                                                    

num_bits = 8
num_keys = pow(2, num_bits)
num_bytes = 16
num_traces = 100

class ThesisProject(IntEnum):
    AES_SBOX = 0
    FREYRE_SBOX_1 = 1
    FREYRE_SBOX_2 = 2
    FREYRE_SBOX_3 = 3


sbox_selected = ThesisProject.FREYRE_SBOX_3

if (sbox_selected == ThesisProject.AES_SBOX):
    proj_name = "AES_SBOX_"+str(num_traces)+"traces"
elif (sbox_selected == ThesisProject.FREYRE_SBOX_1):
    proj_name = "Freyre_SBOX_1_"+str(num_traces)+"traces"
elif (sbox_selected == ThesisProject.FREYRE_SBOX_2):
    proj_name = "Freyre_SBOX_2_"+str(num_traces)+"traces"
elif (sbox_selected == ThesisProject.FREYRE_SBOX_3):
    proj_name = "Freyre_SBOX_3_"+str(num_traces)+"traces"
else:
    pass

proj_export_absolute_path = "/home/sem/Syncthing/Politecnico di Torino/01 - Magistrale/Tesi/00-Notes/Thesis-Work/zip-projects/"



# sample_GLOBAL_range_min = 0
# sample_GLOBAL_range_max = cw_scope_adc_samples
# sample_LOCAL_range_min = 1290
# sample_LOCAL_range_stride = 60
# sample_LOCAL_range_max = sample_LOCAL_range_min + sample_LOCAL_range_stride


def print_globals_config():
    """
    Print a summary of the global script configuration (you an adjust the parameters by modifying
    the `globals.py` script)
    """
    print(f"\n")
    print(f" --- Globals Config ---")
    print(f"\t --> num_bits:\t{num_bits}")
    print(f"\t --> num_bytes:\t{num_bytes}")
    print(f"\t --> num_keys:\t{num_keys}")
    print(f"\t --> num_traces:\t{num_traces}")
    print(f"\t --> Sbox:\t{sbox_selected}")
    print(f"\t --> Ongoing Project:\t{proj_name}")
    # print(f"\t --> leak_position:\t{leak_position}")
    # print(f"\t --> sample_GLOBAL_range_min:\t{sample_GLOBAL_range_min}")
    # print(f"\t --> sample_GLOBAL_range_max:\t{sample_GLOBAL_range_max}")
    # print(f"\t --> sample_LOCAL_range_min:\t{sample_LOCAL_range_min}")
    # print(f"\t --> sample_LOCAL_range_stride:\t{sample_LOCAL_range_stride}")
    # print(f"\t --> sample_LOCAL_range_max:\t{sample_LOCAL_range_max}")
    print(f"\n")





