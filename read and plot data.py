import numpy as np
import matplotlib.pyplot as plt

VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = []

plt.figure(dpi=500)
k = 2

with open('배리어 패치 후//umpiyam_random1_0.65.txt', 'r') as file:
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

if k == 1:     
    plt.plot(Deal, color='green', label='Random_1')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='green', label='Random_1')
   
    
VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = [] 
    
with open('배리어 패치 후//umpiyam_random2_0.65.txt', 'r') as file:
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

if k == 1:     
    plt.plot(Deal, color='grey', label='Random_2')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='grey', label='Random_2')
    
    
VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = [] 
    
with open('배리어 패치 후//umpiyam_random3_0.65.txt', 'r') as file:
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


if k == 1:     
    plt.plot(Deal, color='blue', label='Random_2')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='blue', label='Random_2')
    
VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = [] 
    
with open('배리어 패치 후//umpiyam_rein_0.65.txt', 'r') as file:
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

if k == 1:     
    plt.plot(Deal, color='red', label='Rein')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='red', label='Rein')

VI_level_array = []
Deal = []
Erda_cost = []
reinforce_array = [] 
    
with open('배리어 패치 후//umpiyam_erda_0.65.txt', 'r') as file:
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

if k == 1:     
    plt.plot(Deal, color='black', label='Erda')    
if k == 2:
    plt.plot(Erda_cost_C, Deal, color='black', label='Erda')



if k == 1:     
    plt.xlabel('Reinforce Number')
    
if k == 2:
    plt.xlabel('Erda_cost_Cumulative')

plt.ylabel('Deal')
plt.legend()
plt.show()






