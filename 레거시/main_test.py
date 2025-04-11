import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from calculate_DPM_6th4 import cal_DPM_6th4
from calculate_DPM_6th4_log import cal_DPM_6th4_log
from calculate_DPM_6th4_new import cal_DPM_6th4_new


# This code reads item-related ASCII files and updates the specification, DPM

# print (1=Detail, 2=Brief, 0=None)
print_property = 1
# compare? (1=Yes, 0= No)
compare_property = 0
# plot graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color)
plot_graph = 0

directory1 = 'umpiyam_24'
directory2 = 'umpiyam_24'
deal_time = 720
delay = 3500

VI_level1 = [20,6,9,10,30,30,28,  0,0]

VI_level2 = [30,30,30,30,30,30,30,  0,0]

VI_level = VI_level2
ring = 1
if compare_property == 1:
    print('전 ----------------')
Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
#print(Total_STAT_ARRAY)
NET_STAT, a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
#sum1, Cardinal_Ratio1, Deal_Int_C1, Deal_Int_CC1, CRein_time_end1, time_int1 = cal_DPM_6th4_new(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)
cal_DPM_6th4_new(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)

