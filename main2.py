import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from cal_function import *

from calculate_log_new_rev12 import cal_log_new_rev12

# print (1=Detail, 2=Brief, 0=None)
print_property = 0
# compare? (1=Yes, 0= No)
compare_property = 0
# plot graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color, 4=dmg inc, 5=build comp)
plot_graph = 0

directory1 = 'ingeng'
directory2 = 'ingeng'
deal_time = 650
#           템 언 배 얼 포      블 디 레 콤 페 헤 이
VI_level1 = [30,30,30,30,30,   30,30,30,30,30,30,30]
#VI_level1 = [21,11,21,12,18,   30,28,30,30,10,9]
VI_level2 = [10,4,13,6,19,   30,27,29,30, 15, 1, 1]

VI_level = VI_level1
ring = 1
if compare_property == 1:
    print('전 ----------------')
Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
NET_STAT, a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
stats = parse_character_stats(Total_STAT_ARRAY, NET_STAT)
print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
sum1, Cardinal_Ratio1, Deal_Int_C1, Deal_Int_CC1, CRein_time_end1, time_int1 = cal_log_new_rev12(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time)

VI_level = VI_level1
ring = 1
if compare_property == 1:
    print('후 ----------------')
    Total_STAT_ARRAY, Total_IGNORE = set_directory(directory2)               
    NET_STAT, a = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
    stats = parse_character_stats(Total_STAT_ARRAY, NET_STAT)
    print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
    sum2, Cardinal_Ratio2, Deal_Int_C2, Deal_Int_CC2, CRein_time_end2, time_int2 = cal_log_new_rev12(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time)
    print('최종뎀 상승량 =',round((sum2/sum1-1)*100,4),'% (보스 숙련도',Cardinal_Ratio1,')')

if plot_graph >=3:    
    compare_graph(plot_graph, time_int1, Deal_Int_C1, Deal_Int_C2, Deal_Int_CC1, Deal_Int_CC2, sum1, sum2, Cardinal_Ratio1)
            
            


        




