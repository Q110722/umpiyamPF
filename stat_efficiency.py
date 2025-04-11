import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from calculate_log_assault_fix4 import cal_log_assault_fix4


# print (1=Detail, 2=Brief, 0=None)
print_property = 2
# compare? (1=Yes, 0= No)
compare_property = 0
# plot graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color)
plot_graph = 0

directory1 = 'umpiyam_24'
directory2 = 'umpiyam_24'
# 딜 타임 초 단위
deal_time = 720
delay = 1100

VI_level = [30,30,30,30,30,30,30,  30,30]
ring = 2

base_stat_index = 10  # ATTACK
target_stat_index = 11  # DEX

def stat_increase_linear_interp(base_stat_index, target_stat_index):
    base_increase = 1
    Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
    Total_STAT_ARRAY[base_stat_index] += base_increase
    NET_STAT,a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
    
    print_property = 1
    print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
    
    original_dpm, _, _, _, _, _ = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)   
    Total_STAT_ARRAY[base_stat_index] -= base_increase
    
    prev_efficiency_diff = None
    prev_dex_increase = None
    
    for target_increase in range(0, 100):
        Total_STAT_ARRAY[target_stat_index] += target_increase
        NET_STAT, a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
        dpm_with_target_increase, _, _, _, _, _ = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)
        
        efficiency_diff = dpm_with_target_increase - original_dpm
        print(efficiency_diff)
        
        if efficiency_diff < 0:        
            prev_efficiency_diff = efficiency_diff
            prev_dex_increase = target_increase
        
        if efficiency_diff * prev_efficiency_diff <= 0:
            break
        
        Total_STAT_ARRAY[target_stat_index] -= target_increase
           
    matching_increase = np.interp(0, [prev_efficiency_diff, efficiency_diff], [prev_dex_increase, target_increase])
    print(f"base stat {base_increase:.2f} = target stat {matching_increase:.2f}")
    
    return matching_increase

matching_increase = stat_increase_linear_interp(base_stat_index, target_stat_index)
