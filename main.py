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
print_property = 2
# compare? (1=Yes, 0= No)
compare_property = 0
# plot graph (0= None, 1=Raw, 2=1s Resolution, 3=1s Resolution w/o color)
plot_graph = 0

directory1 = 'test'
directory2 = 'test'
deal_time = 720
delay = 3500

VI_level1 = [30,30,30,30,30,   30,30,30,30]
VI_level2 = [0,0,0,0,1,   0,0,0,1]

VI_level = VI_level1
ring = 1
if compare_property == 1:
    print('전 ----------------')
Total_STAT_ARRAY, Total_IGNORE = set_directory(directory1)
#print(Total_STAT_ARRAY)
NET_STAT, a  = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
sum1, Cardinal_Ratio1, Deal_Int_C1, Deal_Int_CC1, CRein_time_end1, time_int1 = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)

VI_level = VI_level2
ring = 1
if compare_property == 1:
    print('후 ----------------')
    Total_STAT_ARRAY, Total_IGNORE = set_directory(directory2)               
    NET_STAT, a = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
    print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
    sum2, Cardinal_Ratio2, Deal_Int_C2, Deal_Int_CC2, CRein_time_end2, time_int2 = cal_log_assault_fix4(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)
    print('최종뎀 상승량 =',round((sum2/sum1-1)*100,4),'% (보스 숙련도',Cardinal_Ratio1,')')
    
# plot_graph = 3    
if plot_graph == 3:
    plt.style.use('dark_background')
    fig, axs = plt.subplots(2,1,figsize=(8,8),gridspec_kw={'height_ratios': [1,1]},dpi=500)
      
    axs[0].set_title('Integrated (1s) Data w/o color')
    axs[1].set_xlabel('Time [s]')
    axs[0].set_ylabel('Non-Cumulative Deal [AU]')
    axs[1].set_ylabel('Cumulative Deal [AU]')
            
    axs[0].bar(time_int1,Deal_Int_C2, width=1.2, color = 'royalblue') 
    axs[0].bar(time_int1,Deal_Int_C1, width=1.2, color = 'lightskyblue')   
    axs[1].bar(time_int1,Deal_Int_CC2, width=1, color = 'royalblue')
    axs[1].bar(time_int1,Deal_Int_CC1, width=1, color = 'lightskyblue')
            
    axs[1].text(15, sum2*0.95, 'Increased Deal = %.4f %%'%round((sum2/sum1-1)*100,4), size= 15, color ='white')
            
    if Cardinal_Ratio1 != 1:
        axs[1].text(20,Deal_Int_CC2[239]*0.7,'NON-IDEAL !!!', size= 25, color ='red')
            
        max_value = max(Deal_Int_C2)    
        if int(Total_STAT_ARRAY[28]) == 1:
            axs[0].text(30, max_value*0.8, 'Fatal Strike', size = 20, color = 'blue')
        if int(Total_STAT_ARRAY[29]) == 1:
            axs[0].text(30, max_value*0.8, 'Boss Slayer', size = 20, color = 'blue')
        if int(Total_STAT_ARRAY[35]) == 1:
            axs[0].text(30, max_value*0.8, 'Defense Smash', size = 20, color = 'blue')
            
            
# plot_graph = 4 일 때 시간에 따른 딜량 차이 그래프 비교
if plot_graph == 4:
    Deal_Int_CC3 = np.zeros(len(Deal_Int_CC1))
    for i in range(len(Deal_Int_CC1)):
        Deal_Int_CC3[i] = (Deal_Int_CC1[i] - Deal_Int_CC2[i])/1e12
    
    plt.style.use('dark_background')
    plt.figure(figsize=(6, 4), dpi=500)
    plt.fill_between(time_int1, Deal_Int_CC3, 0, where=(Deal_Int_CC3 >= 0), interpolate=True, color='yellow', alpha=0.6)
    plt.fill_between(time_int1, Deal_Int_CC3, 0, where=(Deal_Int_CC3 < 0), interpolate=True, color='deeppink', alpha=0.6)
    
    #for i in range(len(Deal_Int_CC3)):
    for i in range(0):
        if Deal_Int_CC3[i] >= 0:
            plt.plot(time_int1[i], Deal_Int_CC3[i], marker='o', linestyle='-', color='y', markersize=2)
        else:
            plt.plot(time_int1[i], Deal_Int_CC3[i], marker='o', linestyle='-', color='deeppink', markersize=2)
    
    plt.axhline(y=0, linestyle='--', color='white')  
    plt.xlabel('Time [s]')
    plt.ylabel('Damage difference [AU]')
    plt.show()

        




