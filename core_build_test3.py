from set_stat import*
from calculate_log_assault_fix4 import cal_log_assault_fix4
from calculate_log2 import cal_log2

print_property = 0
plot_graph = 0
ring = 1
VI_level = [0,0,0,0,1,0,0,0,0]
directory = 'umpiyam_24'
max_value = 30
deal_time = 720
delay = 3500

gap = 5

VI_Erda = [[4,4,4,4,5,3,3,3,3],
           [1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1],
           [2,2,2,2,2,1,1,1,1],
           [2,2,2,2,2,1,1,1,1],
           [2,2,2,2,2,1,1,1,1],
           [3,3,3,3,3,2,2,2,2],
           [3,3,3,3,3,2,2,2,2],
           [8,8,8,8,10,5,5,5,5],
           [3,3,3,3,3,2,2,2,2],
           [3,3,3,3,3,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [3,3,3,3,4,2,2,2,2],
           [4,4,4,4,5,3,3,3,3],
           [12,12,12,12,15,8,8,8,8],
           [4,4,4,4,5,3,3,3,3],
           [4,4,4,4,5,3,3,3,3],
           [4,4,4,4,5,3,3,3,3],
           [4,4,4,4,5,3,3,3,3],
           [4,4,4,4,5,3,3,3,3],
           [5,5,5,5,6,3,3,3,3],
           [5,5,5,5,6,3,3,3,3],
           [5,5,5,5,6,3,3,3,3],
           [6,6,6,6,7,4,4,4,4],
           [15,15,15,15,20,10,10,10,10]]

VI_Erda2 = [[75,75,75,75,0,50,50,50,50],
           [23,23,23,23,30,15,15,15,15],
           [27,27,27,27,35,18,18,18,18],
           [30,30,30,30,40,20,20,20,20],
           [34,34,34,34,45,23,23,23,23],
           [38,38,38,38,50,25,25,25,25],
           [42,42,42,42,55,28,28,28,28],
           [45,45,45,45,60,30,30,30,30],
           [49,49,49,49,65,33,33,33,33],
           [150,150,150,150,200,100,100,100,100],
           [60,60,60,60,80,40,40,40,40],
           [68,68,68,68,90,45,45,45,45],
           [75,75,75,75,100,50,50,50,50],
           [83,83,83,83,110,55,55,55,55],
           [90,90,90,90,120,60,60,60,60],
           [98,98,98,98,130,65,65,65,65],
           [105,105,105,105,140,70,70,70,70],
           [113,113,113,113,150,75,75,75,75],
           [120,120,120,120,160,80,80,80,80],
           [263,263,263,263,350,175,175,175,175],
           [128,128,128,128,170,85,85,85,85],
           [135,135,135,135,180,90,90,90,90],
           [143,143,143,143,190,95,95,95,95],
           [150,150,150,150,200,100,100,100,100],
           [158,158,158,158,210,105,105,105,105],
           [165,165,165,165,220,110,110,110,110],
           [173,173,173,173,230,115,115,115,115],
           [180,180,180,180,240,120,120,120,120],
           [188,188,188,188,250,125,125,125,125],
           [375,375,375,375,500,250,250,250,250]]

# 1: 코스트 고려 최적화, 2: 강화 횟수만 고려 최적화, 3: 랜덤 강화
test = 1

# 에르다 소모 고려 최적화
if test == 1:
    f = open("에르다 소모 고려 최적화5.txt", "w")
    Total_STAT_ARRAY, Total_IGNORE = set_directory(directory)
    NET_STAT, a = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
    print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a)
    
    for j in range(5000):
        max_i = 0
        max_sum = 0
        max_sum_eff = 0
        max_cost = 0
        
        sum_ref, Cardinal_Ratio, Deal_Int_C, Deal_Int_CC, CRein_time_end, time_int = cal_log2(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)
        print(VI_level)
        f.write(str(VI_level) + '\n')
        
        for i in range(9):         
            if VI_level[i] < max_value:
                forecast = gap
                lev_diff = max_value - VI_level[i]
                if lev_diff < forecast:
                    forecast = lev_diff
                VI_level[i] += forecast
                
                sum, Cardinal_Ratio, Deal_Int_C, Deal_Int_CC, CRein_time_end, time_int = cal_log2(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time, delay)
                
                sum_eff = sum - sum_ref
                Cost = 0
                for k in range (forecast):
                    Cost += VI_Erda2[VI_level[i]-forecast+k][i]
                sum_eff = sum_eff/Cost
                
                VI_level[i] -= forecast
                if sum_eff > max_sum_eff:
                    max_sum_eff = sum_eff
                    max_sum = sum
                    max_i = i
                    max_cost = Cost             
                
        if VI_level[max_i] < max_value:
            max_cost = VI_Erda2[VI_level[max_i]][i]            
            VI_level[max_i] += 1
               
        #print(max_i)
        if max_i == 0:
            print('Evolve_Tempest')
        if max_i == 1:
            print('Unbound')
        if max_i == 2:
            print('Obsidian')
        if max_i == 3:
            print('Ultimate')
        if max_i == 4:
            print('Forsaken')
        if max_i == 5:
            print('Blast_VI')
        if max_i == 6:
            print('Discharge_VI')
        if max_i == 7:
            print('Resonance_VI')
        if max_i == 8:
            print('Materialize')
                        
        print('Cost: ' + str(max_cost))
        f.write(str(max_sum) + '\n')
        f.write(str(max_cost) + '\n')
        f.write(str(max_i) + '\n\n')
                   
        if VI_level == [30,30,30,30,30,30,30,30,30]:
            break
        
    f.close()
    
    
# 강화 횟수만 고려 최적화
if test == 2:
    f = open("강화 횟수만 고려 최적화.txt", "w")
    for j in range(1000):
        max_i = 0
        max_sum = 0
        max_cost = 0
        
        print(VI_level)
        f.write(str(VI_level) + '\n')
        
        for i in range(6):
            if VI_level[i] < max_value:
                VI_level[i] += 1
                
                Total_STAT_ARRAY, Total_IGNORE = set_directory(directory)
                NET_STAT = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
                print_stat(print_property, Total_STAT_ARRAY, NET_STAT)
                sum, Cardinal_Ratio, Deal_Int_C, Deal_Int_CC, CRein_time_end, time_int = cal_DPM_6th_final(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level)
                
                Cost = VI_Erda[VI_level[i]-1][i]
                
                VI_level[i] -= 1
                if sum > max_sum:
                    max_sum = sum
                    max_i = i
                    max_cost = Cost
                   
        if VI_level[max_i] < max_value:
            VI_level[max_i] += 1
         
        print(max_i)
        f.write(str(max_sum) + '\n')
        f.write(str(max_cost) + '\n')
        f.write(str(max_i) + '\n\n')
            
        
        if VI_level == [30,30,30,30,30,30]:
            break
        
    f.close()

    
# 무지성 랜덤 강화 (전반적으로 균등하게 레벨업)
if test == 3:
    f = open("랜덤 강화.txt", "w")
    for j in range(1000):
        max_i = 0
        max_sum = 0
        max_cost = 0
        

        
        a = int(np.random.random(1)*10000)
        b = a%6
        
        if VI_level[b] < max_value:
            print(VI_level)
            f.write(str(VI_level) + '\n')
        
        if VI_level == [30,30,30,30,30,30]:
            break
           
        if VI_level[b] < max_value:
            VI_level[b] += 1
                
            Total_STAT_ARRAY, Total_IGNORE = set_directory(directory)
            NET_STAT = cal_stat(Total_STAT_ARRAY, Total_IGNORE)
            print_stat(print_property, Total_STAT_ARRAY, NET_STAT)
            sum, Cardinal_Ratio, Deal_Int_C, Deal_Int_CC, CRein_time_end, time_int = cal_DPM_6th_final(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level)
                
            Cost = VI_Erda[VI_level[b]-1][b]
               
            VI_level[b] -= 1
            if sum > max_sum:
                max_sum = sum
                max_i = b
                max_cost = Cost
        else:
            continue
                   
        if VI_level[max_i] < max_value:
            VI_level[max_i] += 1
         
        print(max_i)
        f.write(str(max_sum) + '\n')
        f.write(str(max_cost) + '\n')
        f.write(str(max_i) + '\n\n')
               
    f.close()
    
    
    
    
    
    
    
    
    