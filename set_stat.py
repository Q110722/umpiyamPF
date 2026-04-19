import numpy as np
import math
import os
from collections import defaultdict

def set_directory(directory):
    Total_STAT_ARRAY = np.zeros((38, 1))
    Total_IGNORE = []
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            filepath = os.path.join(directory, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = f.read().splitlines()
            STAT_ARRAY, IGNORE = import_stat(data)
            Total_STAT_ARRAY += STAT_ARRAY 
            Total_IGNORE.append(IGNORE)
            
    return Total_STAT_ARRAY, Total_IGNORE

def import_stat(data):
    stats = defaultdict(float)
    IGNORE = []
    for line in data:
        line = line.strip()
        if line in ('MAIN', 'UPT', 'LPT', '') or line.startswith('%%') or '=' not in line:
            continue         
        k, v = line.split('=', 1)
        val = float(v) if '.' in v else int(v)

        if k == 'IGNORE':
            IGNORE.append(int(val))
        elif k == 'ALL':
            stats['DEX'] += val
            stats['STR'] += val
        elif k == 'ALL%':
            stats['DEX%'] += val
            stats['STR%'] += val
        elif k == 'WEAPON_ATTACK':
            stats['WEAPON_ATTACK'] += val
            stats['ATTACK'] += val
        else:
            stats[k] += val

    keys = [
        'STR', 'STR%', 'DEX', 'DEX%', 'LVS', 'LVD', 'ATTACK', 'ATTACK%',
        'DAMAGE', 'BOSS_DAMAGE', 'CRI_RATE', 'CRI_DAMAGE', 'COOL',
        'SYM_DEX', 'SYM_STR', 'LUMI_ATTACK', 'WEAPON_ATTACK', 'level',
        'haebang', 'Buff_duration', 'Restraint_level', 'Mer', 'Cardinal_ratio',
        'Server_lag', 'RT_ratio', 'Ability_additional_damage', 'Ability_passive',
        'Ability_prob', 'Fatal_strike', 'Boss_slayer', 'Just_one', 'Nobless_damage',
        'Nobless_boss_damage', 'Nobless_critical_damage', 'Nobless_ignore_guard',
        'Defense_smash', 'Continuous_level', 'Soul_con'
    ]
    STAT_ARRAY = np.vstack([stats[key] for key in keys])

    return STAT_ARRAY, IGNORE
    
def cal_stat(Total_STAT_ARRAY, Total_IGNORE):
    T = Total_STAT_ARRAY
    FINAL_ATTACK = 57.70 if T[18] == 1 else 43.36  
    level = T[17]
    base_stat = 5 * level + 18
    lv_ratio = level // 9 
    NET_ATTACK = math.floor(T[6,0] * (1 + T[7,0]/100) + T[15,0])
    NET_IGNORE = 0
    for sublist in Total_IGNORE:
        for item in sublist:
            NET_IGNORE += (100 - NET_IGNORE) * item / 100
    NET_IGNORE = round(NET_IGNORE, 2)
    a = math.floor(base_stat * 1.16) + T[2,0] + T[5,0] * lv_ratio
    NET_DEX = math.floor(a * (1 + T[3,0]/100) + T[13,0])
    NET_DEX2 = math.floor((base_stat + T[2,0] + T[5,0] * lv_ratio) * (1 + T[3,0]/100) + T[13,0]) 
    NET_STR = math.floor((4 + T[0,0] + T[4,0] * lv_ratio) * (1 + T[1,0]/100) + T[14,0])
    SGONG_MAX = math.floor(round((NET_DEX * 4 + NET_STR) * 0.01 * NET_ATTACK * 1.3) * (1 + T[8,0]/100) * (1 + FINAL_ATTACK/100))
    NET_STAT = [NET_ATTACK, NET_IGNORE, NET_DEX, NET_STR, NET_DEX2, SGONG_MAX, FINAL_ATTACK]
    
    return NET_STAT, a

def print_stat(print_property, Total_STAT_ARRAY, NET_STAT, a):
    T = Total_STAT_ARRAY
    N = NET_STAT
    if print_property == 1:
        print(
            f"STR = {round(T[0,0])}\n"
            f"STR% = {round(T[1,0])}\n"
            f"DEX = {int(a)}\n"
            f"DEX% = {round(T[3,0])}\n"
            f"TOTAL DEX w/ MY= {N[2]}\n"
            f"ATT = {round(T[6,0])}\n"
            f"ATT% = {round(T[7,0])}\n"
            f"NET ATT = {N[0]}\n"
            f"FINAL ATTACK = {N[6]}\n"
            f"DAMAGE = {round(T[8,0])}\n"
            f"BOSS DAMAGE = {round(T[9,0])}\n"
            f"IGNORE GUARD = {N[1]}\n"
            f"CRITICAL RATE = {round(T[10,0])}\n"
            f"CRITICAL DAMAGE = {round(T[11,0])}\n"
            f"COOLTIME REDUCE = {round(T[12,0])}\n"
            f"REUSE = {T[27,0] + 7.5}\n"  # 아티팩트 반영
            f"ABS DEX = {round(T[13,0])}\n"
            f"ABS STR = {round(T[14,0])}"
        )  
    elif print_property == 2:
        print(
            f"STR = {N[3]}\n"
            f"DEX(메용X) = {N[4]}\n"
            f"DEX(메용O) = {N[2]}\n"
            f"공격력 = {N[0]}\n"
            f"뒷스공 = {N[5]//10000}만 {N[5]%10000}"
        )




