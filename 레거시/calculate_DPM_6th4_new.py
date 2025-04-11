import numpy as np
import math
import matplotlib.pyplot as plt

def cal_DPM_6th4_new(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time_ref, delay):

    Buff_duration = 1.46
    Cardinal_Ratio = 1
    Boss_Guard = 380
    deal_time = deal_time_ref
    
    # VI_level: 0 = Tempest
    #           1 = Unbound
    #           2 = Obsidian
    #           3 = Ultimate
    #           4 = Forsaken
    #           5 = Blast_VI
    #           6 = Discharge_VI
    
    # 강화코어 최종뎀 보정
    VI_level_factor = [0,0,0,0]
    for i in range (4): # 0~3
        if VI_level[i] == 30:
            VI_level_factor[i] = 1.6
        elif VI_level[i] != 0:
            VI_level_factor[i] = 1 + (10 + 15*(VI_level[i]//10) + (VI_level[i]%10))/100
        else:
            VI_level_factor[i] = 1
    
    class Stat:
        def __init__(self, total_stat_array, net_stat):
            self.damage = int(total_stat_array[8])                 # 0 Damage
            self.boss_damage = int(total_stat_array[9])            # 1 Boss_Damage
            self.ignore_guard = net_stat[1]                        # 2 Ignore_Guard
            self.critical_prob = int(total_stat_array[10])         # 3 Critical_Prob
            self.critical_damage = int(total_stat_array[11])       # 4 Critical_Damage
            self.dex_with_my = net_stat[2]                         # 5 DEX_with_MY
            self.dex_without_my = net_stat[4]                      # 6 DEX_without_MY
            self.str = net_stat[3]                                 # 7 STR
            self.attack_ratio = int(total_stat_array[7])           # 8 Attack_Ratio (공퍼)
            self.attack = int(net_stat[0])                         # 9 Attack (최종 공격력)
            self.attack_abs = int(total_stat_array[6][0])          # 10 Attack_abs, Real_Attack (깡공)
            self.attack_lumi = int(total_stat_array[15][0])        # 11 Attack_lumi
            self.weapon_attack = int(total_stat_array[16][0])      # 12 Weapon_attack (무기 공격력)
            self.cool = int(total_stat_array[12][0])               # 13 Cool
            self.weapon_dex = round(net_stat[2] + int(total_stat_array[16][0]) * 4 * (1 + total_stat_array[3][0] / 100))  # 14 Weapon_DEX
            self.final_attack = (1 + net_stat[6] / 100)            # 15 Final_attack
            self.restraint_level = int(total_stat_array[20])       # 16 Restraint_level
            self.mer_lv = int(total_stat_array[21])                # 17 Mer Lv
            self.server_lag = int(total_stat_array[23])            # 18 Server_Lag
            self.rt_ratio = int(total_stat_array[24])              # 19 RT_ratio
            self.my2_dex = net_stat[4] + 5 * (net_stat[2] - net_stat[4])  # 20 MY2_DEX
            self.cool_r = 1                                        # 21 Cool_R    

        def __str__(self):
            return f"""Stat(
        damage={self.damage}, 
        boss_damage={self.boss_damage}, 
        ignore_guard={self.ignore_guard}, 
        critical_prob={self.critical_prob}, 
        critical_damage={self.critical_damage},
        dex_with_my={self.dex_with_my},
        dex_without_my={self.dex_without_my},
        str={self.str},
        attack_ratio={self.attack_ratio},
        attack={self.attack},
        attack_abs={self.attack_abs},
        attack_lumi={self.attack_lumi},
        weapon_attack={self.weapon_attack},
        cool={self.cool},
        weapon_dex={self.weapon_dex},
        final_attack={self.final_attack},
        restraint_level={self.restraint_level},
        mer_lv={self.mer_lv},
        server_lag={self.server_lag},
        rt_ratio={self.rt_ratio},
        my2_dex={self.my2_dex},
        cool_r={self.cool_r}
        )"""    
    
    stat = Stat(Total_STAT_ARRAY,NET_STAT)
    #print(stat)
    
    class Condition:
        def __init__(self, total_stat_array):
            self.ability_damage = int(total_stat_array[25])  # 0 어빌리티 상추뎀
            self.ability_passive = int(total_stat_array[26])          # 1 어빌리티 패시브
            self.ability_reuse = int(total_stat_array[27])         # 2 어빌리티 재사용
            self.fatal_strike = int(total_stat_array[28])             # 3 Fatal_Strike
            self.boss_slayer = int(total_stat_array[29])              # 4 Boss_Slayer
            self.just_one = int(total_stat_array[30])                 # 5 Just_One
            self.defense_smash = int(total_stat_array[35])            # 6 Defense_Smash
            self.nobless_damage = int(total_stat_array[31])           # 7 Nobless_Damage
            self.nobless_boss_damage = int(total_stat_array[32])      # 8 Nobless_Boss_Damage
            self.nobless_critical_damage = int(total_stat_array[33])  # 9 Nobless_Critical_Damage
            self.nobless_ignore_guard = int(total_stat_array[34])     # 10 Nobless_Ignore_Guard
    
        def __str__(self):
            return f"""Condition(
        ability_damage={self.ability_damage},
        ability_passive={self.ability_passive},
        ability_reuse={self.ability_reuse},
        fatal_strike={self.fatal_strike},
        boss_slayer={self.boss_slayer},
        just_one={self.just_one},
        defense_smash={self.defense_smash},
        nobless_damage={self.nobless_damage},
        nobless_boss_damage={self.nobless_boss_damage},
        nobless_critical_damage={self.nobless_critical_damage},
        nobless_ignore_guard={self.nobless_ignore_guard}
        )"""
    
    condition = Condition(Total_STAT_ARRAY)
    #print(condition)
    
    # 영메
    stat.attack_ratio += 4
    # 아티팩트
    condition.ability_reuse += 6.75
    # Dope
    stat.boss_damage += 20
    stat.ignore_guard += (100-stat.ignore_guard)*0.2
    stat.critical_damage += 5
    # Add Nobless Skill
    stat.damage += condition.nobless_damage
    stat.boss_damage += condition.nobless_boss_damage
    stat.critical_damage += condition.nobless_critical_damage
    stat.ignore_guard += (100-stat.ignore_guard)*condition.nobless_ignore_guard/100
    # Link Skill List (Not shown in stat) # 모법, 카데나, 아크
    stat.boss_damage += 11 + 9 + 12
    stat.ignore_guard += (100-stat.ignore_guard)*0.09
    # 4th Curse Transition
    stat.critical_damage += 10
    
    if stat.mer_lv >= 200:
        stat.cool_r = 0.95
    if stat.mer_lv >= 250:
        stat.cool_r = 0.94
        
    # 소울 공20, 어빌 패시브 공, 길축, 몬파레드, 유힘, MVP, 우르스, 붕뿌, 275의자    
    stat.attack_abs += 20 + 2*condition.ability_passive + 30 + 30 + 30 + 30 + 30 + 30 + 50
    stat.boss_damage += condition.ability_damage
    # 와헌 유니온 대원 효과
    stat.damage += 5
    stat.attack_ratio += condition.ability_passive
    
    #print(stat)
    #print(condition)
    
    # HyperSkill Passive
    SharpEyes_Persist = 0
    SharpEyes_IgnoreGuard = 0
    SharpEyes_Critical_Prob = 0
    Cardinal_Force_Reinforce = 1
    Cardinal_Force_Additional_Enhance = 1
    Cardinal_Force_Bonus_Attack = 1
    Ancient_Force_BossKiller = 1
    Ancient_Force_Ignore_Guard = 1
    Ancient_Force_Enchant_Enhance = 0
    
    HyperSkill = [SharpEyes_Persist,SharpEyes_IgnoreGuard,SharpEyes_Critical_Prob,Cardinal_Force_Reinforce,Cardinal_Force_Additional_Enhance,Cardinal_Force_Bonus_Attack,Ancient_Force_BossKiller,Ancient_Force_Ignore_Guard,Ancient_Force_Enchant_Enhance]

    # 6차 극딜 빌드
    cycle_6th = ['evolve',
                 'epic',
                 'MY2',
                 'crein',
                 'angelic',
                 'seedring',
                 'obsidian',
                 'tempest',
                 'forsaken',
                 'ultimate',
                 'relic_evolution',
                 'unbound',
                 ]
    
    class Delay:
        def __init__(self):
            self.evolve = 0
            self.epic = 540
            self.MY2 = 1140
            self.crein = 540
            self.angelic = 900
            self.seedring = 320
            self.obsidian = 80
            self.tempest = 200
            self.forsaken = 6540
            self.ultimate = 120
            self.relic_evolution = 350
            self.unbound = 600
            self.bind = 500

    delay = Delay()
    
    def calculate_skill_activation_times(cycle, delay):
        activation_times = []
        current_time = 0
        
        for skill in cycle:
            skill_delay = getattr(delay, skill)
            activation_times.append((skill, current_time))
            current_time += skill_delay
        
        return activation_times

    activation_times = calculate_skill_activation_times(cycle_6th, delay)
    
    for skill, time in activation_times:
        print(f"Skill: {skill}, Activation Time: {time}ms")


    
    # 5차 극딜 빌드
    
    cycle_5th = []
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





















