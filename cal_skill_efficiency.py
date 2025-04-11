import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from calculate_log_assault import cal_log_assault
from calculate_log_assault_fix4 import cal_log_assault_fix4

# print (1=Detail, 2=Brief, 0=None)
print_property = 2
# compare? (1=Yes, 0= No)
compare_property = 0
# plot DPM graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color)
plot_graph = 0

directory1 = 'umpiyam_24'

deal_time = 720
delay = 3500

VI_level_init = [0,0,0,0,1,0,0,0,0]
ring = 1

#VI_level:  0 = Tempest
#           1 = Unbound
#           2 = Obsidian
#           3 = Ultimate
#           4 = Forsaken
#           5 = Blast_VI
#           6 = Discharge_VI
#           7 = Resonance_VI
#           8 = Raven VI, Material

skill_index = 8

def skill_increase(VI_level_init, skill_index, list):
    VI_level = VI_level_init
    for skill_level in range(0,30):
        
        Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
        NET_STAT, a = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
        original_dpm, _, _, _, _, _ = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)   
        VI_level[skill_index] += 1
        dpm_with_target_increase, _, _, _, _, _ = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)   
        eff = (dpm_with_target_increase/original_dpm-1)*100
        print(eff)
        list.append(eff)
        
    return list

list = []
list = skill_increase(VI_level_init, skill_index, list)

print(list)


        
        
        