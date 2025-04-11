import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = []

plt.figure(dpi=500)
k = 2

with open('솔 에르다 소모 고려 최적화.txt', 'r') as file:
    lines = file.readlines()

for i in range(0, len(lines), 5):
    vi_level = [int(float(num)) if num.isdigit() else float(num) for num in lines[i].strip()[1:-1].split(', ') if num]
    if vi_level:
        VI_level_array.append(vi_level)

        deal = float(lines[i+1])
        Deal.append(deal)

        reinforce = int(lines[i+3].strip()) if lines[i+3].strip() else 0
        reinforce_array.append(reinforce)

        erda_cost = int(lines[i+2])
        Erda_cost.append(erda_cost)

Erda_cost_C = np.cumsum(Erda_cost)

new_Erda_cost_C = np.linspace(Erda_cost_C.min(),Erda_cost_C.max(),Erda_cost_C.max()-Erda_cost_C.min()+1)
interpolator = interp1d(Erda_cost_C, Deal, kind = 'cubic')
new_Deal = interpolator(new_Erda_cost_C)
derivative_Deal= np.gradient(new_Deal, new_Erda_cost_C)
print(new_Erda_cost_C)

Deal_increase_percentage = [(new_Deal[i+1] - new_Deal[i]) / new_Deal[i] * 100 for i in range(len(new_Deal)-1)]



if k == 1:     
    plt.plot(Deal, color='green', label='Random_1')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='green', label='Erda_P')
    #plt.plot(new_Erda_cost_C[:-1], Deal_increase_percentage, color='green')
    plt.axhline(y=7.0e25, color='r', linestyle='--', label='5 Lv.')
    plt.axhline(y=7.7e25, color='r', linestyle='--', label='5 Lv.')
    plt.axvline(x=500, color='b', linestyle='--', alpha=0.8)
    plt.axvline(x=2000, color='b', linestyle='--', alpha=0.8)
    #plt.axhline(y=3.0967/719, color='skyblue', linestyle='--', label='6 Lv.')
    #plt.axhline(y=3.2871/1250, color='y', linestyle='--', label='7 Lv.')
    #plt.axhline(y=3.6191/3126, color='r', linestyle='--', label='8 Lv.')  # y=5 라인 추가 
    #plt.axhline(y=3.9654/13620, color='b', linestyle='--', label='9 Lv.')
    #plt.axhline(y=4.4523/145925, color='magenta', linestyle='--', label='10 Lv.')
    
    #plt.legend()
    
if k == 1:     
    plt.xlabel('Reinforce Number')
    
if k == 2:
    plt.xlabel('Erda Cumulative')
 

#plt.yticks([])
#plt.ylim(0,0.01)
plt.ylabel('Deal Increase Efficiency (%)')
#plt.ylabel('Deal')
#plt.legend()
plt.show()
