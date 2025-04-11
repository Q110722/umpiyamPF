import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from calculate_DPM_6th4_log_rev_34 import cal_DPM_6th4_log_rev_34

from calculate_log import cal_log
from calculate_log2 import cal_log2
from calculate_log_assault_fix2 import cal_log_assault_fix2
from calculate_log_assault_fix3 import cal_log_assault_fix3
from calculate_log_assault_fix4 import cal_log_assault_fix4


# This code reads item-related ASCII files and updates the specification, DPM

# print (1=Detail, 2=Brief, 0=None)
print_property = 0
# compare? (1=Yes, 0= No)
compare_property = 0
# plot graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color)
plot_graph = 0

directory1 = 'test'
directory2 = 'test'
deal_time = 720
delay = 1100

VI_level1 = [30,30,30,30,30,   30,30,30,30]
VI_level2 = [30,30,30,30,30,   30,30,30,30]

VI_level = VI_level1
ring = 2

reuse_list = [0, 5, 6.5, 7.5, 15.5, 17, 17.5, 24, 26, 27.5]
#reuse_list = [26, 27.5]
cool_list = [0,1,2,3,4,5,6,7]

with open('data.txt','w') as file:
    
    for i in range (len(reuse_list)):
        reuse = reuse_list[i]
        for j in range (len(cool_list)):
            cool = cool_list[j]
            
            Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
            Total_STAT_ARRAY[12] = cool
            NET_STAT, a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
            print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
            if cool < 7:
                sum1, Cardinal_Ratio1, Deal_Int_C1, Deal_Int_CC1, CRein_time_end1, time_int1 = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay, reuse)
            if cool == 7:
                sum1, Cardinal_Ratio1, Deal_Int_C1, Deal_Int_CC1, CRein_time_end1, time_int1 = cal_log2(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay, reuse)
            print('재사용:'+str(reuse))
            print('쿨감:'+str(cool))
            print(sum1)
            
            file.write(str(reuse)+'\n')
            file.write(str(cool)+'\n')
            file.write(str(sum1)+'\n\n')

            


        



