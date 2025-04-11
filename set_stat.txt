import numpy as np
import math
import os

# Accumulate stats in each array elements

def set_directory(directory):
    Total_STAT_ARRAY = np.zeros((36,1))
    Total_IGNORE = []
    initial_directory = os.getcwd()

    os.chdir(directory)
    for file in os.listdir():
        if file.endswith('.txt'):
            f = open(file, 'r')
            data = f.read().splitlines()
            STAT_ARRAY, IGNORE = import_stat(data)
            f.close()
            for i in range (0,len(Total_STAT_ARRAY)):
                Total_STAT_ARRAY[i,0] += STAT_ARRAY[i,0]
            Total_IGNORE.append(IGNORE)
    os.chdir(initial_directory)  
    
    return Total_STAT_ARRAY, Total_IGNORE

def import_stat(data):
    DEX = 0             #2
    DEX_percent = 0     #3
    STR = 0             #0
    STR_percent = 0     #1
    ATTACK = 0          #6
    ATTACK_percent = 0  #7
    BOSS_DAMAGE = 0     #9
    DAMAGE = 0          #8
    IGNORE = []         #
    CRI_RATE = 0        #10
    CRI_DAMAGE = 0      #11
    LVS = 0             #4
    LVD = 0             #5
    COOL = 0            #12
    SYM_DEX = 0         #13
    SYM_STR = 0         #14
    LUMI_ATTACK = 0     #15
    WEAPON_ATTACK = 0   #16
    level = 0           #17
    haebang = 0         #18
    buff_duration = 0   #19
    restraint = 0       #20
    mer = 0             #21
    cardinal_ratio = 0  #22
    sever_lag = 0       #23
    RT_ratio = 0        #24
    abil_add_damage = 0 #25
    abil_passive = 0    #26
    abil_prob = 0       #27
    fatal_strike = 0    #28
    boss_slayer = 0     #29
    just_one = 0        #30
    nobless_damage = 0  #31
    nobless_boss = 0    #32
    nobless_critical = 0#33
    nobless_ignore = 0  #34
    defense_smash = 0   #35

    index = []
    for i in range (0,len(data)):
        if data[i] == 'MAIN' or  data[i] == 'UPT' or data[i] == 'LPT' or data[i] == '\n' or data[i].startswith('%%'):
            index.append(i)
    for i in range (0,len(index)):
        del data[index[i]-i]
        
    for i in range (0, len(data)):
        if data[i].startswith('DEX='):
            DEX += int(data[i].replace('DEX=', ''))            
        if data[i].startswith('DEX%='):
            DEX_percent += int(data[i].replace('DEX%=', ''))           
        if data[i].startswith('STR='):
            STR += int(data[i].replace('STR=', ''))               
        if data[i].startswith('STR%='):
            STR_percent += int(data[i].replace('STR%=', ''))           
        if data[i].startswith('ATTACK='):
            ATTACK += int(data[i].replace('ATTACK=', ''))           
        if data[i].startswith('ATTACK%='):
            ATTACK_percent += int(data[i].replace('ATTACK%=', ''))       
        if data[i].startswith('ALL='):
            DEX += int(data[i].replace('ALL=', ''))
            STR += int(data[i].replace('ALL=', ''))           
        if data[i].startswith('ALL%='):
            DEX_percent += int(data[i].replace('ALL%=', ''))
            STR_percent += int(data[i].replace('ALL%=', ''))          
        if data[i].startswith('BOSS_DAMAGE='):
            BOSS_DAMAGE += int(data[i].replace('BOSS_DAMAGE=', ''))     
        if data[i].startswith('DAMAGE='):
            DAMAGE += int(data[i].replace('DAMAGE=', ''))         
        if data[i].startswith('CRI_RATE='):
            CRI_RATE += int(data[i].replace('CRI_RATE=', ''))          
        if data[i].startswith('CRI_DAMAGE='):
           CRI_DAMAGE += int(data[i].replace('CRI_DAMAGE=', ''))       
        if data[i].startswith('LVS='):
            LVS += int(data[i].replace('LVS=', ''))           
        if data[i].startswith('LVD='):
            LVD += int(data[i].replace('LVD=', ''))      
        if data[i].startswith('IGNORE='):
            IGNORE.append(int(data[i].replace('IGNORE=', '')))     
        if data[i].startswith('COOL='):
            COOL += int(data[i].replace('COOL=', ''))      
        if data[i].startswith('SYM_DEX='):
            SYM_DEX += int(data[i].replace('SYM_DEX=', ''))   
        if data[i].startswith('SYM_STR='):
            SYM_STR += int(data[i].replace('SYM_STR=', ''))        
        if data[i].startswith('LUMI_ATTACK='):
            LUMI_ATTACK += int(data[i].replace('LUMI_ATTACK=', ''))         
        if data[i].startswith('WEAPON_ATTACK='):
            WEAPON_ATTACK += int(data[i].replace('WEAPON_ATTACK=', ''))
            ATTACK += int(data[i].replace('WEAPON_ATTACK=', ''))         
        if data[i].startswith('level='):
            level += int(data[i].replace('level=', ''))           
        if data[i].startswith('haebang='):
            haebang += int(data[i].replace('haebang=', ''))          
        if data[i].startswith('Buff_duration='):
            buff_duration += float(data[i].replace('Buff_duration=', ''))
        if data[i].startswith('Restraint_level='):
            restraint += int(data[i].replace('Restraint_level=', ''))
        if data[i].startswith('Mer='):
            mer += int(data[i].replace('Mer=', ''))
        if data[i].startswith('Cardinal_ratio='):
            cardinal_ratio += float(data[i].replace('Cardinal_ratio=', ''))
        if data[i].startswith('Server_lag='):
            sever_lag += int(data[i].replace('Server_lag=', ''))
        if data[i].startswith('RT_ratio='):
            RT_ratio += int(data[i].replace('RT_ratio=', ''))
        if data[i].startswith('Ability_additional_damage='):
            abil_add_damage += int(data[i].replace('Ability_additional_damage=', ''))
        if data[i].startswith('Ability_passive='):
            abil_passive += int(data[i].replace('Ability_passive=', ''))
        if data[i].startswith('Ability_prob='):
            abil_prob += int(data[i].replace('Ability_prob=', ''))
        if data[i].startswith('Fatal_strike='):
            fatal_strike += int(data[i].replace('Fatal_strike=', ''))
        if data[i].startswith('Boss_slayer='):
            boss_slayer += int(data[i].replace('Boss_slayer=', ''))
        if data[i].startswith('Just_one='):
            just_one += int(data[i].replace('Just_one=', ''))
        if data[i].startswith('Nobless_damage='):
            nobless_damage += int(data[i].replace('Nobless_damage=', ''))
        if data[i].startswith('Nobless_boss_damage='):
            nobless_boss += int(data[i].replace('Nobless_boss_damage=', ''))
        if data[i].startswith('Nobless_critical_damage='):
            nobless_critical += int(data[i].replace('Nobless_critical_damage=', ''))
        if data[i].startswith('Nobless_ignore_guard='):
            nobless_ignore += int(data[i].replace('Nobless_ignore_guard=', ''))
        if data[i].startswith('Defense_smash='):
            defense_smash += int(data[i].replace('Defense_smash=', ''))
        
    STAT_ARRAY = np.vstack((STR, STR_percent, DEX, DEX_percent, LVS, LVD, ATTACK, ATTACK_percent, DAMAGE, BOSS_DAMAGE, CRI_RATE, CRI_DAMAGE, COOL, SYM_DEX, SYM_STR, LUMI_ATTACK, WEAPON_ATTACK, level, haebang, buff_duration,restraint,mer,cardinal_ratio,sever_lag,RT_ratio,abil_add_damage,abil_passive,abil_prob,fatal_strike,boss_slayer,just_one,nobless_damage,nobless_boss,nobless_critical,nobless_ignore,defense_smash))

    return STAT_ARRAY, IGNORE
    
def cal_stat(Total_STAT_ARRAY, Total_IGNORE):
    # Calculate NET ATTACK, floor
    NET_STAT = []
    if Total_STAT_ARRAY[18] == 1:
        FINAL_ATTACK = 45.2
    else:
        FINAL_ATTACK = 32
        
    lvd_lv = 9
    level=Total_STAT_ARRAY[17]
    base_stat = 5*level+18
    lv_ratio = np.floor(level/lvd_lv)
    #print(lv_ratio)
    
    NET_ATTACK = math.floor(Total_STAT_ARRAY[6,0]*(1+Total_STAT_ARRAY[7,0]/100)+Total_STAT_ARRAY[15,0])
    FLAT_IGNORE = [item for sublist in Total_IGNORE for item in sublist]
    #print(FLAT_IGNORE), round
    NET_IGNORE = 0
    for i in range (0,len(FLAT_IGNORE)):
        NET_IGNORE += (100-NET_IGNORE)*FLAT_IGNORE[i]/100
    NET_IGNORE = round(NET_IGNORE,2)

    # Calculate NET_DEX, floor
    NET_DEX = math.floor((math.floor(base_stat*1.16) + Total_STAT_ARRAY[2,0]+Total_STAT_ARRAY[5,0]*lv_ratio)*(1+Total_STAT_ARRAY[3,0]/100)+Total_STAT_ARRAY[13,0])
    NET_STR = math.floor((4+Total_STAT_ARRAY[0,0]+Total_STAT_ARRAY[4,0]*lv_ratio)*(1+Total_STAT_ARRAY[1,0]/100)+Total_STAT_ARRAY[14,0])
    NET_DEX2 = math.floor((math.floor(base_stat*1.00) + Total_STAT_ARRAY[2,0]+Total_STAT_ARRAY[5,0]*lv_ratio)*(1+Total_STAT_ARRAY[3,0]/100)+Total_STAT_ARRAY[13,0])

    a = (math.floor(base_stat*1.16) + Total_STAT_ARRAY[2,0]+Total_STAT_ARRAY[5,0]*lv_ratio)
    # Calculate SGong
    #SGONG_MAX = round((NET_DEX*4 + NET_STR)*0.01*(NET_ATTACK)*1.3*(1+Total_STAT_ARRAY[8,0]/100)*(1+FINAL_ATTACK/100))
    SGONG_MAX = math.floor(round((NET_DEX*4 + NET_STR)*0.01*(NET_ATTACK)*1.3)*(1+Total_STAT_ARRAY[8,0]/100)*(1+FINAL_ATTACK/100))
    #SGONG_MIN = round(0.86*(NET_DEX*4 + NET_STR)*0.01*(NET_ATTACK)*1.3*(1+Total_STAT_ARRAY[8,0]/100)*(1+FINAL_ATTACK/100))

    NET_STAT.append(NET_ATTACK)
    NET_STAT.append(NET_IGNORE)
    NET_STAT.append(NET_DEX)
    NET_STAT.append(NET_STR)
    NET_STAT.append(NET_DEX2)
    NET_STAT.append(SGONG_MAX)
    NET_STAT.append(FINAL_ATTACK)
    
    return NET_STAT, a 


def print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a):
    
    
    if print_property == 1:
        print('STR =', round(Total_STAT_ARRAY[0,0]))
        print('STR% =', round(Total_STAT_ARRAY[1,0]))
        print('TOTAL STR =', NET_STAT[3])
        print('DEX =', a)
        
        print('DEX% =', round(Total_STAT_ARRAY[3,0]))
        print('TOTAL DEX w/o MY =', NET_STAT[4])
        print('TOTAL DEX w/ MY=', NET_STAT[2])
        print('WEAPON DEX =', round(NET_STAT[2] + Total_STAT_ARRAY[16,0]*4*(1+Total_STAT_ARRAY[3,0]/100)))
        print('LVS =', round(Total_STAT_ARRAY[4,0]))
        print('LVD =', round(Total_STAT_ARRAY[5,0]))
        print('ATT =', round(Total_STAT_ARRAY[6,0]))
        print('WEAPON ATTACK =',round(Total_STAT_ARRAY[16,0]))
        print('ATT% =', round(Total_STAT_ARRAY[7,0]))
        print('NET ATT =',NET_STAT[0])
        print('FINAL ATTACK =', NET_STAT[6])
        print('DAMAGE =', round(Total_STAT_ARRAY[8,0]))
        print('BOSS DAMAGE =', round(Total_STAT_ARRAY[9,0]))
        print('IGNORE GUARD =', NET_STAT[1])
        print('CRITICAL RATE =', round(Total_STAT_ARRAY[10,0]))
        print('CRITICAL DAMAGE =', round(Total_STAT_ARRAY[11,0]))
        print('COOLTIME REDUCE =', round(Total_STAT_ARRAY[12,0]))
        print('ABS DEX =', round(Total_STAT_ARRAY[13,0]))
        print('ABS STR =',round(Total_STAT_ARRAY[14,0]))
        print('SGONG =', NET_STAT[5]//10000,'\b만',NET_STAT[5]%10000)
        
    if print_property == 2:
        print('STR =', NET_STAT[3])
        print('DEX(메용X) =', NET_STAT[4])
        print('DEX(메용O) =', NET_STAT[2])
        print('공격력 =',NET_STAT[0])
        print('뒷스공 =', NET_STAT[5]//10000,'\b만',NET_STAT[5]%10000)




