import numpy as np
import math
import matplotlib.pyplot as plt

def cal_log(plot_graph, Total_STAT_ARRAY, NET_STAT, ring, VI_level, deal_time_ref, delay):
    
    Buff_Duration = 1.46
    Cardinal_Ratio = 1
    Boss_Guard = 380
    deal_time = deal_time_ref
    
    #VI_level:  0 = Tempest
    #           1 = Unbound
    #           2 = Obsidian
    #           3 = Ultimate
    #           4 = Forsaken
    #           5 = Blast_VI
    #           6 = Discharge_VI
    #           7 = 3rd (Transition, Resonance, Astra)
    #           8 = 4th (Raven, Assault, Materialize)
    
    # 강화코어 최종뎀 보정
    VI_level_factor = [0,0,0,0]
    for i in range (4): # 0~3
        if VI_level[i] == 30:
            VI_level_factor[i] = 1.6
        elif VI_level[i] != 0:
            VI_level_factor[i] = 1 + (10 + 15*(VI_level[i]//10) + (VI_level[i]%10))/100
        else:
            VI_level_factor[i] = 1
            
            
    Damage = int(Total_STAT_ARRAY[8])
    Boss_Damage = int(Total_STAT_ARRAY[9])
    Ignore_Guard = NET_STAT[1]
    Critical_Prob = int(Total_STAT_ARRAY[10])
    Critical_Damage = int(Total_STAT_ARRAY[11])
    DEX_with_MY = NET_STAT[2]
    DEX_without_MY = NET_STAT[4]
    STR = NET_STAT[3]
    
    Attack_Ratio = int(Total_STAT_ARRAY[7])
    Attack = int(NET_STAT[0])
    Attack_abs = int(Total_STAT_ARRAY[6,0])
    Attack_lumi = int(Total_STAT_ARRAY[15,0])
    Weapon_attack = int(Total_STAT_ARRAY[16,0])
    
    Cool = int(Total_STAT_ARRAY[12,0])
    Weapon_DEX = round(NET_STAT[2] + Weapon_attack*4*(1+Total_STAT_ARRAY[3,0]/100))
    #print(Weapon_DEX)
    
    FINAL_ATTACK = (1 + NET_STAT[6]/100)
    
    Restraint_level = int(Total_STAT_ARRAY[20])
    Mer = int(Total_STAT_ARRAY[21])
    Server_Lag = int(Total_STAT_ARRAY[23])
    RT_ratio = int(Total_STAT_ARRAY[24])

    # 영메
    Attack_Ratio += 4
    
    # 스탯창 반영 안되는 어빌리티
    Ability_Additional_Damage = int(Total_STAT_ARRAY[25]) # 8, 10
    Ability_Passive = int(Total_STAT_ARRAY[26]) # 1
    # 재사용 
    Ability_Prob = float(Total_STAT_ARRAY[27]) # 10, 20
    #아티팩트
    Ability_Prob += 0
    
    def calculate_damage_increase(prob):
        return ((prob / (1 - prob/100)) * 100)/100
    
    Ability_Prob = calculate_damage_increase(Ability_Prob)
    #print(Ability_Prob)

    # Special Core
    Fatal_Strike = int(Total_STAT_ARRAY[28])
    Boss_Slayer = int(Total_STAT_ARRAY[29])
    Just_One = int(Total_STAT_ARRAY[30])
    Defense_Smash = int(Total_STAT_ARRAY[35])
    

    # Nobless Skill points
    Nobless_Damage = int(Total_STAT_ARRAY[31])
    Nobless_Boss_Damage = int(Total_STAT_ARRAY[32])
    Nobless_Critical_Damage = int(Total_STAT_ARRAY[33])
    Nobless_Ignore_Guard = int(Total_STAT_ARRAY[34])

    # Dope
    Boss_Damage += 20
    #Ignore_Guard = Ignore_Guard + (100-Ignore_Guard)*0.2
    Critical_Damage += 5

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
    

    #------------------------------------------------
    # No Edit on Following Lines

    HyperSkill = [SharpEyes_Persist,SharpEyes_IgnoreGuard,SharpEyes_Critical_Prob,Cardinal_Force_Reinforce,Cardinal_Force_Additional_Enhance,Cardinal_Force_Bonus_Attack,Ancient_Force_BossKiller,Ancient_Force_Ignore_Guard,Ancient_Force_Enchant_Enhance]

    MY2_DEX = DEX_without_MY + 5*(DEX_with_MY - DEX_without_MY)
       
    # Add Nobless Skill
    Damage += Nobless_Damage
    Boss_Damage += Nobless_Boss_Damage
    Critical_Damage += Nobless_Critical_Damage
    Ignore_Guard = Ignore_Guard + (100 - Ignore_Guard)*Nobless_Ignore_Guard/100

    # Link Skill List (Not shown in stat) # 모법, 카데나, 아크
    Boss_Damage += 11 + 9 + 12
    Ignore_Guard = Ignore_Guard + (100 - Ignore_Guard)*0.09

    # 4th Curse Transition
    Critical_Damage -= 1
    

    if Mer == 200:
        Cool_R = 0.95
    if Mer == 250:
        Cool_R = 0.94
        
    Real_Attack = Attack_abs
    # 소울 공20
    Real_Attack += 20
    Attack_lumi *= 100
    Boss_Damage += Ability_Additional_Damage
    # 와헌 유니온 대원 효과
    Damage += 5
    Attack_Ratio += Ability_Passive
    Real_Attack += 2*Ability_Passive
    # 길축, 몬파레드, 유힘, MVP, 우르스, 붕뿌, 275의자
    Real_Attack += 30 + 30 + 30 + 30 + 30 + 30 + 50
    
    # 6차 극딜 빌드
    Condition_ARRAY1 = np.zeros(17)
    Condition_ARRAY1[7] = 0         # Barrier (80)   
    Condition_ARRAY1[14] = 80       # Evolve (80)
    Condition_ARRAY1[0] = 160       # Epic (130)
    Condition_ARRAY1[1] = 290       # MY2 (130)
    Condition_ARRAY1[2] = 420       # CRein (30)
    Condition_ARRAY1[3] = 450       # 엔버 (100)
    Condition_ARRAY1[4] = 550       # Seed Ring (100)
    Condition_ARRAY1[5] = 650       # Evolve_tempest (430)    
    Condition_ARRAY1[16] = 1080     # Forsaken (6730)
    Condition_ARRAY1[8] = 7810      # Ultimate (100)
    Condition_ARRAY1[13] = 7910     # Relic_evolution (350)
    Condition_ARRAY1[6] = 8260      # Unbound (530)
    Condition_ARRAY1[9] = 8790      # Bind (730)
    Condition_ARRAY1[10] = 9520 + 10000
    
    Condition_ARRAY1[11] = 650      # Boss, Defense
    Condition_ARRAY1[12] = 650     # Fatal Strike
    
    # 5차 극딜 빌드
    Condition_ARRAY2 = np.zeros(17)
    Condition_ARRAY2[7] = 0         # Barrier (80)   
    Condition_ARRAY2[14] = 80       # Evolve (80)
    Condition_ARRAY2[0] = 160       # Epic (130)
    Condition_ARRAY2[1] = 290       # MY2 (130)
    Condition_ARRAY2[2] = 420       # CRein (30)
    Condition_ARRAY2[3] = 450       # 엔버 (100)
    Condition_ARRAY2[4] = 550       # Seed Ring (100)
    Condition_ARRAY2[5] = 650       # Evolve_tempest (430)    
    Condition_ARRAY2[9] = 1080     # Bind (730)
    Condition_ARRAY2[8] = 1810      # Ultimate (100)
    Condition_ARRAY2[13] = 1910     # Relic_evolution (350)  
    Condition_ARRAY2[6] = 2260     # Unbound (530)
    Condition_ARRAY2[10] = 2790 + 10000
    
    Condition_ARRAY2[11] = 650     # Boss, Defense
    Condition_ARRAY2[12] = 650     # Fatal Strike
    # Condition_ARRAY[0] = Epic_time
    #                   1= MY2_time
    #                   2= CRein_time
    #                   3= Angelic_time
    #                   4= SeedRing_time
    #                   5= Evolve_tempest_time
    #                   6= Unbound_time
    #                   7= Obsidian_time
    #                   8= Ultimate_time
    #                   9= Free_Deal_time
    #                   10= Non_Free_Deal_time
    #                   11= Boss_Slayer_time
    #                   12= Fatal_Strike_time
    #                   13= Relic_Evolution_time
    #                   14= Evolve_time2 (#이볼브)
    #                   15= Bind_time (제거)
    #                   16= Forsaken_time

    def calculate_deal(RT_ratio, Server_Lag, HyperSkill, Damage, Boss_Damage, Ignore_Guard, Critical_Prob, Critical_Damage, DEX_with_MY, MY2_DEX, Weapon_DEX, Attack_Ratio, Real_Attack, Buff_Duration, Restraint_level,deal_time):
        Total_Deal_Time_Interval = []
        Total_Time = []
        Deal_Ratio = []
        Cumulative_Deal = []
        Deal_Cardinal_Blast = []
        Deal_Cardinal_Discharge = []
        Deal_Cardinal_Transition = []
        Deal_Additional_Blast = []
        Deal_Additional_Discharge = []
        Deal_Resonance = []
        Deal_Triple_Impact = []
        Deal_Raven = []
        Deal_Guided_Arrow = []
        Deal_Ultimate_Blast = []
        Deal_Evolve_Tempest = []
        Deal_Obsidian_Barrier = []
        Deal_Relic_Unbound = []
        Deal_Evolve = []
        Deal_Forsaken = []
        Deal_Additional_Blast_Curse_Arrow = []
        Deal_Forsaken_Arrow = []
        Deal_Ancient_Fury = []
        Deal_Material = []
        Deal_test_graph = []
        Deal_Resonance2 = []
        
        Evolve_Tempest_times_used = 0
        Evolve_Tempest_attacks = 0
        Relic_Unbound_times_used = 0
        Relic_Unbound_attacks = 0
        Obsidian_Barrier_times_used = 0
        Obsidian_Barrier_attacks = 0
        Ultimate_Blast_times_used = 0
        Ultimate_Blast_attacks = 0
        Forsaken_Relic_times_used = 0
        Forsaken_Relic_attacks = 0
        Resonance_times_used = 0
        Resonance_attacks = 0
        Cardinal_Blast_times_used = 0
        Cardinal_Blast_attacks = 0
        Cardinal_Discharge_times_used = 0
        Cardinal_Discharge_attacks = 0
        Forsaken_Arrow_times_used = 0
        Forsaken_Arrow_attacks = 0
        Ancient_Fury_times_used = 0
        Ancient_Fury_attacks = 0
        Additional_Discharge_times_used = 0
        Additional_Discharge_attacks = 0
        Additional_Blast_times_used = 0
        Additional_Blast_attacks = 0
        Additional_Blast_Curse_Arrow_times_used = 0
        Additional_Blast_Curse_Arrow_attacks = 0
        Raven_times_used = 0
        Raven_attacks = 0
        Evolve_times_used = 0
        Evolve_attacks = 0
        Guided_Arrow_times_used = 0
        Guided_Arrow_attacks = 0
        Material_times_used = 0
        Material_attacks = 0
        Resonance_times_used2 = 0
        Resonance_attacks2 = 0
        
        
        # 특정 변수 정의
        SharpEyes_Duration = 0
        Cardinal_Damage = 0
        Additional_Ratio = 40
        Additional_Ratio_VI = 41+((VI_level[5]-1)//3)
        Cardinal_Attack = 5
        Ancient_Enchant_Ignore_Guard = 0
        Enchant_Damage = 0
        Ancient_Enchant_Boss_Damage = 51 + Ability_Passive
        Restraint_level2 = Restraint_level
        Resonance_Num = 1 + Ability_Prob/100
        
        # 하이퍼 스킬 패시브
        if HyperSkill[0] == 1:
            SharpEyes_Duration += 30
        if HyperSkill[1] == 1:
            Ignore_Guard = Ignore_Guard + (100-Ignore_Guard)*0.05
        if HyperSkill[2] == 1:
            Critical_Prob += 5
        if HyperSkill[3] == 1:
            Cardinal_Damage = 20
        if HyperSkill[4] == 1:
            Additional_Ratio = 50
            Additional_Ratio_VI = 51+((VI_level[5]-1)//3)
        if HyperSkill[5] == 1:
            Cardinal_Attack = 6
        if HyperSkill[6] == 1:
            Ancient_Enchant_Boss_Damage = 71 + Ability_Passive
        if HyperSkill[7] == 1:
            Ancient_Enchant_Ignore_Guard = 20
        if HyperSkill[8] == 1:
            Enchant_Damage += 20
        
        # 변수 초기값 지정
        Cardinal_Blast_Delay = 0
        Cardinal_Discharge_Delay = 0
        Cardinal_Transition_Delay = 0
        Triple_Impact_Delay = 0
        Resonance_Delay = 0
        Raven_Delay = 0
        Guided_Arrow_Delay = 0
        Ultimate_Blast_Delay = 0
        Evolve_Tempest_Delay = 0
        Obsidian_Barrier_Delay = 0
        Relic_Unbound_Delay = 0
        Evolve_Delay = 0
        Curse_Arrow_Delay = 0
        Ancient_Fury_Delay = 0
        Cardinal_between_Delay = 0
        
        Active = 1
        Active_Delay = 0
        Resonance_stack = 1
        Discharge_Used = 0
        Additional_Blast_Curse_Arrow = 0
        Forsaken_Arrow = 0
        Ancient_Fury = 0
        Res_stack = 0
        Material_stack = 0
        
        
        # 딜 계산 수행 루프 (10 ms 단위)
        iteration_time = 10 # ms
        for t in range(0*1000,deal_time*1000,iteration_time):
            
            Damage2 = Damage
            Boss_Damage2 = Boss_Damage
            Critical_Prob2 = Critical_Prob
            Critical_Damage2 = Critical_Damage
            DEX2 = DEX_with_MY
            Attack_Ratio2 = Attack_Ratio
            Ignore_Guard2 = Ignore_Guard
            VMatrix_Ignore_Guard = Ignore_Guard + (100-Ignore_Guard)*0.2
            
            
            # 5차 극딜 때 기존 빌드대로 넣도록 조정
            if (t//(120*1000))%3 != 0:
                Condition_ARRAY = Condition_ARRAY2
            else:
                Condition_ARRAY = Condition_ARRAY1
            
            # 포세이큰 렐릭 -> 에인션트, 인챈트 스킬 최종뎀 증가 반영
            if Condition_ARRAY[16] <= t%(360*1000) <= Condition_ARRAY[16] + (30+Server_Lag)*1000:
                Ancient_Enchant_Final_Damage = 1.1*(1.05+(VI_level[4]//3)/100)
            else:
                Ancient_Enchant_Final_Damage = 1.1
              
            # 렐릭 에볼루션 활성화 지정
            if Condition_ARRAY[13] <= t%(120*1000) <= Condition_ARRAY[13] + (30 + Server_Lag)*1000:
                Active_Relic_Evolution = 1
            else:
                Active_Relic_Evolution = 0 

            # 에픽 어드벤처
            if Condition_ARRAY[0] <= t%(120*1000) <= Condition_ARRAY[0] + (60 + Server_Lag)*1000:
                Damage2 += 10

            # 엔버 링크2
            if Condition_ARRAY[3] <= t%(60*1000) < Condition_ARRAY[3] + (10*Buff_Duration + Server_Lag)*1000:
                Damage2 += 45
            
            # 크리인
            if Condition_ARRAY[2] <= t%(120*1000) < Condition_ARRAY[2] + (30+Server_Lag)*1000:
                Critical_Damage2 = Critical_Damage2 + Critical_Prob2/2
                #첫번째 크리인 종료 시간만 따로 저장
                if Condition_ARRAY[2] <= t < Condition_ARRAY[2] + (30+Server_Lag)*1000:                 
                    CRein_time_end = t
            
            # 카인링크
            if Condition_ARRAY[4] <= t%(40*1000) < Condition_ARRAY[4] + (20+Server_Lag)*1000:
                Damage2 += 17
                
            # 모도링크
            if Condition_ARRAY[4] <= t%(20*1000) < Condition_ARRAY[4] + (10+Server_Lag)*1000:
                Damage2 += 18
            
                
#-----------시드링 설정 구간--------------------------------------------------------------------------------------------------------------------
            test_graph = 0
                        
            # 리레+웨펖 반복, 메용2 상시 사용
            if ring == 1:
                if Condition_ARRAY[1] <= t%(120*1000) <= Condition_ARRAY[1] + (60 + Server_Lag)*1000:
                    Damage2 += 20
                    DEX2 = MY2_DEX
                    #test_graph = 10000000000000000000000000
                    if Condition_ARRAY[4] <= t%(240*1000) < Condition_ARRAY[4] + 15*1000:
                        Attack_Ratio2 += Restraint_level2
                        #test_graph = 10000000000000000000000000
                    if Condition_ARRAY[4] + 120*1000 <= t%(240*1000) < Condition_ARRAY[4] + (135 + Server_Lag)*1000:
                        DEX2 = Weapon_DEX + (MY2_DEX - DEX_with_MY)
                        #test_graph = 10000000000000000000000000
            
            # 컨티링만 사용, 메용2 상시 사용
            if ring == 2:
                # Continuous
                if Condition_ARRAY[1] <= t%(120*1000) <= Condition_ARRAY[1] + (60 + Server_Lag)*1000:
                    Damage2 += 20
                    DEX2 = MY2_DEX
                    #test_graph = 10000000000000000000000000
                if Condition_ARRAY[4] <= (t-delay)%(12*1000) < Condition_ARRAY[4] + 8*1000:
                    Damage2 += 140
                    Attack_Ratio2 += 10
                    #test_graph = 10000000000000000000000000
                
                 
            # 시드링 사용X, 메용2만 사용 
            if ring == 0:
                if Condition_ARRAY[1] <= t%(120*1000) <= Condition_ARRAY[1] + (60 + Server_Lag)*1000:
                    Damage2 += 20
                    DEX2 = MY2_DEX   
#-------------------------------------------------------------------------------------------------------------------------------

                
            # Skill Usable (Active?)
            if Active_Delay <= 0:
                Active = 1
                Active_Delay -= iteration_time
            else:
                Active = 0
                Active_Delay -= iteration_time
            
            if Boss_Slayer == 1:
                if Condition_ARRAY[11] <= t%(120*1000) < Condition_ARRAY[11] + (10 + Server_Lag)*1000:
                    Boss_Damage2 += 50
            if Fatal_Strike == 1:
                if Condition_ARRAY[12] <= t%(30*1000) < Condition_ARRAY[12] + (2+Server_Lag)*1000:
                    Boss_Damage2 += 100
            if Defense_Smash == 1:
                if Condition_ARRAY[11] <= t%(120*1000) < Condition_ARRAY[11] + (10 + Server_Lag)*1000:
                    Ignore_Guard2 = 100
                    VMatrix_Ignore_Guard = 100
                
       
            # 포세이큰 강화효과 추가
            Forsaken_ignore = Ignore_Guard2
            Forsaken_Boss = Boss_Damage2
            
            if 10 <= VI_level[4] < 30:
                Forsaken_ignore = Forsaken_ignore + (100-Forsaken_ignore)*0.2
            if 20 <= VI_level[4]:
                Forsaken_Boss += 20
            if 30 <= VI_level[4]:
                Forsaken_Boss += 30
                Forsaken_ignore = Forsaken_ignore + (100-Forsaken_ignore)*0.5


            # 극딜 스킬 스택(최대 타수) 설정
            if t%(120*1000) == 0:
                Evolve_Tempest_Stack = 84
                Relic_Unbound_Stack = 4
                # 옵시디언 배리어 타수 증가 반영
                Obsidian_Barrier_Stack = int((12 + int(math.ceil(VI_level[2]/4)))/0.480)
                Ultimate_Blast_Stack = 1
            
            
            # Evolve Tempest
            if Condition_ARRAY[5] <= t%(120*1000) <= Condition_ARRAY[5] + 15*1000:
                if Evolve_Tempest_Delay <= 0 and Evolve_Tempest_Stack > 0:
                    Evolve_Tempest = VI_level_factor[0]*(1000*6)*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(Ignore_Guard2+(100-Ignore_Guard2)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                    Evolve_Tempest_Delay = 120 - iteration_time
                    Evolve_Tempest_Stack -= 1
                    Evolve_Tempest_times_used += 1
                    Evolve_Tempest_attacks += 6
                elif Evolve_Tempest_Delay > 0 and Evolve_Tempest_Stack > 0:
                    Evolve_Tempest = 0
                    Evolve_Tempest_Delay -= iteration_time
                else:
                    Evolve_Tempest = 0
            else:
                Evolve_Tempest = 0        
                Evolve_Tempest_Delay = 0
            
            # Relic Unbound  
            if Condition_ARRAY[6] + 0.5*1000 <= t%(120*1000) <= Condition_ARRAY[6] + 0.5*1000 + 20*1000:
                if Relic_Unbound_Delay <= 0 and Relic_Unbound_Stack > 0:
                    Relic_Unbound = VI_level_factor[1]*6*(1375*8)*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage+Enchant_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(Ignore_Guard2+(100-Ignore_Guard2)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                    Relic_Unbound_Delay = 2000 - iteration_time
                    Relic_Unbound_Stack -= 1
                    Relic_Unbound_times_used += 6
                    Relic_Unbound_attacks += 48
                elif Relic_Unbound_Delay > 0 and Relic_Unbound_Stack > 0:
                    Relic_Unbound = 0
                    Relic_Unbound_Delay -= iteration_time
                else:
                    Relic_Unbound = 0
            else:
                Relic_Unbound = 0
                Relic_Unbound_Delay = 0
                    
            # Obsidian Barrier
            if Condition_ARRAY[7] <= t%(120*1000) <= Condition_ARRAY[7] + 25*1000:
                if Obsidian_Barrier_Delay <= 0 and Obsidian_Barrier_Stack > 0:
                    Obsidian_Barrier = VI_level_factor[2]*(1040*5)*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage+Enchant_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(Ignore_Guard2+(100-Ignore_Guard2)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                    #print('Obs')
                    #print((Ignore_Guard2+(100-Ignore_Guard2)*Ancient_Enchant_Ignore_Guard/100)/100)
                    Obsidian_Barrier_Delay = 460 - iteration_time
                    Obsidian_Barrier_Stack -= 1
                    Obsidian_Barrier_times_used += 1
                    Obsidian_Barrier_attacks += 5
                elif Obsidian_Barrier_Delay > 0 and Obsidian_Barrier_Stack > 0:
                    Obsidian_Barrier = 0
                    Obsidian_Barrier_Delay -= iteration_time
                else:
                    Obsidian_Barrier = 0
            else:
                Obsidian_Barrier = 0
                Obsidian_Barrier_Delay = 0
                
            # Ultimate Blast: 1320
            if Condition_ARRAY[8] + 1.8*1000 <= t%(120*1000) <= Condition_ARRAY[8] + 15*1000 + 1.8*1000:
                if Ultimate_Blast_Stack > 0:
                    Ultimate_Blast = VI_level_factor[3]*6*(1000*15*2)*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*100*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                    #print('Ult')
                    #print(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)
                    Ultimate_Blast_Stack -= 1
                    Ultimate_Blast_times_used += 6
                    Ultimate_Blast_attacks += 90
                else:
                    Ultimate_Blast = 0
            else:
                Ultimate_Blast = 0
                
            # Forsaken Relic
            if t%(360*1000) == Condition_ARRAY[16]:
                #Ancient_Fury = (1200+40*VI_level[4])*8*3*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(Ignore_Guard2+(100-Ignore_Guard2)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                Ancient_Fury_Delay = 0
            elif t%(360*1000) == Condition_ARRAY[16] + 1500: 
                Forsaken_Relic = (775+26*VI_level[4])*9*22*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
            elif t%(360*1000) == Condition_ARRAY[16] + 4100:
                Forsaken_Relic = (775+26*VI_level[4])*9*2*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
            elif t%(360*1000) == Condition_ARRAY[16] + 4300:
                Forsaken_Relic = (765+26*VI_level[4])*14*1*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
            elif t%(360*1000) == Condition_ARRAY[16] + 5300:
                Forsaken_Relic = (765+26*VI_level[4])*14*4*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
            elif t%(360*1000) == Condition_ARRAY[16] + 5700:
                Forsaken_Relic = (765+26*VI_level[4])*14*6*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
            elif t%(360*1000) == Condition_ARRAY[16] + 6300:
                Forsaken_Relic = (765+26*VI_level[4])*14*19*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                Forsaken_Relic_times_used += 54
                Forsaken_Relic_attacks += 636
                
            else:
                Forsaken_Relic = 0
                Ancient_Fury = 0
                Ancient_Fury_Delay -= iteration_time
                
            # 렐릭 마테리얼라이즈 스택 설정 (레조넌스는 따로 설정)
            if Condition_ARRAY[5] == t%(120*1000): #이볼템
                Material_stack += 6
            if Condition_ARRAY[6] == t%(120*1000): #언바
                Material_stack += 5
            if Condition_ARRAY[7] == t%(120*1000): #배리어
                Material_stack += 6
            if Condition_ARRAY[8] == t%(120*1000): #얼블
                Material_stack += 20
                
            if Material_stack > 0 and VI_level[8] > 0:
                Material = Material_stack*8*(405+4*VI_level[8])*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Ignore_Guard2/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                Material_times_used += Material_stack
                Material_attacks += 8*Material_stack
                Material_stack2 = Material_stack
                Material_stack = 0
            else:
                Material = 0
            
            
            Active_Additional_Discharge = 0
            Active_Additional_Blast = 0    
            # Deal Cycle when No-buff and burst
            if Condition_ARRAY[9] <= t%(120*1000) < 120*1000:
                # Cardinal_Ratio setting
                if Condition_ARRAY[10] <= t%(120*1000) < 120*1000:
                    Cardinal_Ratio2 = Cardinal_Ratio
                else:
                    Cardinal_Ratio2 = 1
                
                
                # Resonance VI
                if Resonance_Delay <= 0 and Discharge_Used == 1 and VI_level[7] > 0:
                    if Res_stack < 4:
                        Resonance = Resonance_Num*(Cardinal_Ratio2+np.sqrt(Cardinal_Ratio2))/2*((920+29*VI_level[7])*6*2.2*(1.1**5))*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(VMatrix_Ignore_Guard+(100-VMatrix_Ignore_Guard)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                        Res_stack += 1
                        Resonance_attacks += 6*Resonance_Num
                        Resonance_times_used += Resonance_Num
                        Resonance2 = 0
                        
                    elif Res_stack == 4:
                        Resonance2 = Resonance_Num*(Cardinal_Ratio2+np.sqrt(Cardinal_Ratio2))/2*((591+34*VI_level[7])*10*2.2*(1.1**5))*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(VMatrix_Ignore_Guard+(100-VMatrix_Ignore_Guard)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                        Res_stack = 0
                        Resonance_attacks2 += 10*Resonance_Num
                        Resonance_times_used2 += Resonance_Num
                        Resonance = 0
                        
                    Resonance_Delay = (15*Cool_R-Cool)*1000 - iteration_time
                    Resonance_stack -= 1
                    Material_stack += 2*Resonance_Num
                    Cardinal_between_Delay = 480
                
                elif VI_level[7] > 0:
                    Resonance = 0
                    Resonance2 = 0
                    Resonance_Delay -= iteration_time   
                
                # Resonance
                if Resonance_Delay <= 0 and Discharge_Used == 1 and VI_level[7] == 0:
                    Resonance = Resonance_Num*(Cardinal_Ratio2+np.sqrt(Cardinal_Ratio2))/2*(895*6*2.2*(1.1**5))*(100+Damage2+Boss_Damage2+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(VMatrix_Ignore_Guard+(100-VMatrix_Ignore_Guard)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK
                    Resonance_Delay = (15*Cool_R-Cool)*1000 - iteration_time
                    Resonance_stack -= 1
                    Resonance_times_used += Resonance_Num
                    Resonance_attacks += 6*Resonance_Num
                    Material_stack += 2*Resonance_Num
                    Cardinal_between_Delay = 480
                
                elif VI_level[7] == 0:
                    Resonance = 0
                    Resonance_Delay -= iteration_time   
                    
                # Cardinal Blast VI
                if Cardinal_Blast_Delay <= 0 and Active == 1 and VI_level[5] > 0:
                    Cardinal_Blast = Cardinal_Ratio2*((660+11*VI_level[5])*2.2*Cardinal_Attack)*(100+Damage2+Boss_Damage2+Cardinal_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Cardinal_Blast_Delay = 460 - iteration_time
                    Cardinal_Blast_times_used += 1
                    Cardinal_Blast_attacks += 6
                    Active_Additional_Discharge = 1
                    Cardinal_between_Delay = 240 - iteration_time
                    if Discharge_Used == 1:
                        Resonance_Delay -= 1*1000
                        Triple_Impact_Delay -= 1*1000
                        Ancient_Fury_Delay -= 1*1000
                    Discharge_Used = 0

                elif VI_level[5] > 0:
                    Cardinal_Blast = 0
                    Cardinal_Blast_Delay -= iteration_time
                    Cardinal_between_Delay -= iteration_time
                    
                # Cardinal Blast 
                if Cardinal_Blast_Delay <= 0 and Active == 1 and VI_level[5] == 0:
                    Cardinal_Blast = Cardinal_Ratio2*((615+5*Ability_Passive)*2.2*Cardinal_Attack)*(100+Damage2+Boss_Damage2+Cardinal_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Cardinal_Blast_Delay = 460 - iteration_time
                    Cardinal_Blast_times_used += 1
                    Cardinal_Blast_attacks += 6
                    Active_Additional_Discharge = 1
                    Cardinal_between_Delay = 240 - iteration_time
                    if Discharge_Used == 1:
                        Resonance_Delay -= 1*1000
                        Triple_Impact_Delay -= 1*1000
                        Ancient_Fury_Delay -= 1*1000
                    Discharge_Used = 0

                elif VI_level[5] == 0:
                    Cardinal_Blast = 0
                    Cardinal_Blast_Delay -= iteration_time
                    Cardinal_between_Delay -= iteration_time 
               
            
               # Cardinal Discharge VI
                if Cardinal_Discharge_Delay <= 0 and Active == 1 and Cardinal_between_Delay <= 0 and VI_level[6] > 0:
                    # x2 attack if there exists a boss
                    Cardinal_Discharge = Cardinal_Ratio2*2*((325+5*VI_level[6])*2.2*Cardinal_Attack)*(100+Damage2+Boss_Damage2+Cardinal_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Cardinal_Discharge_Delay = 460 - iteration_time
                    Cardinal_Discharge_times_used += 2
                    Cardinal_Discharge_attacks += 12
                    Active_Additional_Blast = 1
                    Resonance_Delay -= 1*1000
                    Triple_Impact_Delay -= 1*1000
                    Ancient_Fury_Delay -= 1*1000
                    Discharge_Used = 1
                elif VI_level[6] > 0:
                    Cardinal_Discharge = 0
                    Cardinal_Discharge_Delay -= iteration_time
                    
               # Cardinal Discharge
                if Cardinal_Discharge_Delay <= 0 and Active == 1 and Cardinal_between_Delay <= 0 and VI_level[6] == 0:
                    # x2 attack if there exists a boss
                    Cardinal_Discharge = Cardinal_Ratio2*2*((305+5*Ability_Passive)*2.2*Cardinal_Attack)*(100+Damage2+Boss_Damage2+Cardinal_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Cardinal_Discharge_Delay = 460 - iteration_time
                    Cardinal_Discharge_times_used += 2
                    Cardinal_Discharge_attacks += 12
                    Active_Additional_Blast = 1
                    Resonance_Delay -= 1*1000
                    Triple_Impact_Delay -= 1*1000
                    Ancient_Fury_Delay -= 1*1000
                    Discharge_Used = 1
                elif VI_level[6] == 0:
                    Cardinal_Discharge = 0
                    Cardinal_Discharge_Delay -= iteration_time
                    
                # 포세이큰 렐릭 해방 추가 마법 화살
                if Condition_ARRAY[16] <= t%(360*1000) <= Condition_ARRAY[16] + (30+Server_Lag)*1000:
                    if Active_Additional_Blast == 1 or Active_Additional_Discharge == 1:
                        Forsaken_Arrow = Cardinal_Ratio2*((810+27*VI_level[4])*5)*(100+Damage2+Forsaken_Boss)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Forsaken_ignore/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                        Forsaken_Arrow_times_used += 1
                        Forsaken_Arrow_attacks += 5
                    else:
                        Forsaken_Arrow = 0
                        
                # Ancient Fury
                if Condition_ARRAY[16] <= t%(360*1000) <= Condition_ARRAY[16] + (30+Server_Lag)*1000:
                    if Ancient_Fury_Delay <= 0:
                        Ancient_Fury = Cardinal_Ratio2*(650+21*VI_level[4])*15*3*(100+Damage2+Forsaken_Boss+Ancient_Enchant_Boss_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-(Forsaken_ignore+(100-Forsaken_ignore)*Ancient_Enchant_Ignore_Guard/100)/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*Ancient_Enchant_Final_Damage*FINAL_ATTACK                 
                        
                        if Cool == 0:
                            Ancient_Fury_Delay = 10000 - iteration_time
                        elif Cool == 1:
                            Ancient_Fury_Delay = 9500* - iteration_time
                        elif Cool == 2:
                            Ancient_Fury_Delay = 9000 - iteration_time
                        elif Cool == 3:
                            Ancient_Fury_Delay = 8550 - iteration_time
                        elif Cool == 4:
                            Ancient_Fury_Delay = 8100 - iteration_time
                        elif Cool == 5:
                           Ancient_Fury_Delay = 7695 - iteration_time     
                        elif Cool == 6:
                            Ancient_Fury_Delay = 7290 - iteration_time
                        elif Cool == 7:
                            Ancient_Fury_Delay = 6926 - iteration_time
                            
                        Ancient_Fury_times_used += 3
                        Ancient_Fury_attacks += 45
                    else:
                        Ancient_Fury = 0
                        #Ancient_Fury_Delay -= iteration_time
                
                
                # Additional Discharge VI (No Delay)
                if Active_Additional_Discharge == 1 and Active == 1 and VI_level[6] > 0:
                    if Active_Relic_Evolution == 1:
                        Arrow_Num_Discharge = 5
                    else:
                        Arrow_Num_Discharge = 4           
                    Additional_Discharge = Cardinal_Ratio2*(55/100)*(((185+3*VI_level[6])*3)+((185+3*VI_level[6])*0.7*3)*(Arrow_Num_Discharge-1))*2.2*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Additional_Discharge_times_used += (55/100)*Arrow_Num_Discharge
                    Additional_Discharge_attacks += (55/100)*Arrow_Num_Discharge*3
                    Active_Additional_Discharge = 0                    
                elif VI_level[6] > 0:
                    Additional_Discharge = 0
                    
                # Additional Discharge (No Delay)
                if Active_Additional_Discharge == 1 and Active == 1 and VI_level[6] == 0:
                    if Active_Relic_Evolution == 1:
                        Arrow_Num_Discharge = 4
                    else:
                        Arrow_Num_Discharge = 3                    
                    Additional_Discharge = Cardinal_Ratio2*(Additional_Ratio/100)*((166+Ability_Passive)*3*2.2*Arrow_Num_Discharge)*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Additional_Discharge_times_used += (Additional_Ratio/100)*Arrow_Num_Discharge
                    Additional_Discharge_attacks += (Additional_Ratio/100)*Arrow_Num_Discharge*3
                    Active_Additional_Discharge = 0
                elif VI_level[6] == 0:
                    Additional_Discharge = 0
                    
                # Additional Blast VI (No Delay)
                if Active_Additional_Blast == 1 and Active == 1 and VI_level[5] > 0:
                    if Active_Relic_Evolution == 1:
                        Arrow_Num_Blast = (2+(VI_level[5]//20))+1
                    else:
                        Arrow_Num_Blast = (2+(VI_level[5]//20))            
                    Additional_Blast = Cardinal_Ratio2*(Additional_Ratio_VI/100)*(((240+3*VI_level[5])*3)+((240+3*VI_level[5])*0.7*3)*(Arrow_Num_Blast-1))*2.2*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Additional_Blast_times_used += (Additional_Ratio_VI/100)*Arrow_Num_Blast
                    Additional_Blast_attacks += (Additional_Ratio_VI/100)*Arrow_Num_Blast*3
                    Active_Additional_Blast = 0
                elif VI_level[5] > 0:
                    Additional_Blast = 0
                    
                # Additional Blast (No Delay)
                if Active_Additional_Blast == 1 and Active == 1 and VI_level[5] == 0:
                    if Active_Relic_Evolution == 1:
                        Arrow_Num_Blast = 3
                    else:
                        Arrow_Num_Blast = 2            
                    Additional_Blast = Cardinal_Ratio2*(Additional_Ratio/100)*((221+Ability_Passive)*3*2.2*Arrow_Num_Blast)*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Additional_Blast_times_used += (Additional_Ratio/100)*Arrow_Num_Blast
                    Additional_Blast_attacks += (Additional_Ratio/100)*Arrow_Num_Blast*3
                    Active_Additional_Blast = 0
                elif VI_level[5] == 0:
                    Additional_Blast = 0
                    
                # Additional Blast Curse Arrow (쿨감 적용 O)
                if VI_level[5] > 0:
                    Curse_Cool = 20-Cool
                    if Curse_Arrow_Delay <= 0:
                        Additional_Blast_Curse_Arrow = ((6+(VI_level[5]//3))*(120+2*VI_level[5])*4)*2.2*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                        Additional_Blast_Curse_Arrow_times_used += 6+(VI_level[5]//3)
                        Additional_Blast_Curse_Arrow_attacks += (6+(VI_level[5]//3))*4
                        Curse_Arrow_Delay = Curse_Cool*1000 - iteration_time
                    elif Curse_Arrow_Delay > 0:
                        Additional_Blast_Curse_Arrow = 0
                        Curse_Arrow_Delay -= iteration_time
                    else:
                        Additional_Blast_Curse_Arrow = 0

                    
                # Cardinal Transition (Delay_Example = 300 ms)
                if Cardinal_Transition_Delay <= 0 and Active == 1:
                    Cardinal_Transition = 0*(547*2.2*Cardinal_Attack)*(100+Damage2+Boss_Damage2+Cardinal_Damage)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Cardinal_Transition_Delay = 300 - iteration_time
                else:
                    Cardinal_Transition = 0
                    Cardinal_Transition_Delay -= iteration_time
                
                
            else:
                Cardinal_Blast = 0
                Cardinal_Discharge = 0
                Cardinal_Transition = 0
                Additional_Discharge = 0
                Additional_Blast = 0
                Resonance = 0
                Resonance2 = 0
                Triple_Impact = 0

                
            
            # Raven VI
            if Condition_ARRAY[14] + (40 + Server_Lag)*1000 <= t%(120*1000) < Condition_ARRAY[14] + 120*1000 and VI_level[8] > 0:
                if Raven_Delay <= 0:
                    Raven = 2.80*(435+5*VI_level[8])*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Raven_times_used += 1
                    Raven_attacks += 1
                    Raven_Delay = 3000 - iteration_time
                else:
                    Raven = 0
                    Raven_Delay -= iteration_time
            elif VI_level[8] > 0:
                Raven = 0
                Raven_Delay = 0
                
            # Raven
            if Condition_ARRAY[14] + (40 + Server_Lag)*1000 <= t%(120*1000) < Condition_ARRAY[14] + 120*1000 and VI_level[8] == 0:
                if Raven_Delay <= 0:
                    Raven = 2.80*(390)*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-VMatrix_Ignore_Guard/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Raven_times_used += 1
                    Raven_attacks += 1
                    Raven_Delay = 1700 - iteration_time
                    #Raven_Delay = 1700 - iteration_time
                else:
                    Raven = 0
                    Raven_Delay -= iteration_time
            elif VI_level[8] == 0:
                Raven = 0
                Raven_Delay = 0
                
            # Evolve
            if Condition_ARRAY[5] + 10*1000 <= t%(120*1000) < Condition_ARRAY[14] + (40 + Server_Lag)*1000:
                if Evolve_Delay <= 0 and Condition_ARRAY[5] + 10*1000 <= t%(120*1000):
                    Evolve = (900*7)*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Ignore_Guard2/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                    Evolve_times_used += 1
                    Evolve_attacks += 7
                    Evolve_Delay = 3650 - iteration_time
                else:
                    Evolve = 0    
                    Evolve_Delay -= iteration_time
            else:
                Evolve = 0    
                Evolve_Delay = 0
                
            # Guided Arrow (Delay Example = 100 ms)
            if Guided_Arrow_Delay <= 0:
                Guided_Arrow = (880)*(100+Damage2+Boss_Damage2)*(135+Critical_Damage2)*(100-Boss_Guard*(1-Ignore_Guard2/100))*((100+Attack_Ratio2)*Real_Attack+Attack_lumi)*(DEX2+STR/4)*FINAL_ATTACK
                Guided_Arrow_times_used += 1
                Guided_Arrow_attacks += 1
                Guided_Arrow_Delay = 310 - iteration_time
            else:
                Guided_Arrow = 0
                Guided_Arrow_Delay -= iteration_time
            
         
            # 시드링 스위칭 동안 액티브 딜량 zero
            if ring != 2:
                if  80*1000 < t%(120*1000) < (80+6)*1000:
                    if Cardinal_Blast != 0:
                        Cardinal_Blast = 0
                        Cardinal_Blast_times_used -= 1
                        Cardinal_Blast_attacks -= 6
                    if Cardinal_Discharge != 0:
                        Cardinal_Discharge = 0
                        Cardinal_Discharge_times_used -= 2
                        Cardinal_Discharge_attacks -= 12
                    if Additional_Discharge != 0:
                        Additional_Discharge = 0
                        Additional_Discharge_times_used -= Arrow_Num_Discharge
                        Additional_Discharge_attacks -= Arrow_Num_Discharge*3
                    if Additional_Blast != 0:
                        Additional_Blast = 0
                        Additional_Blast_times_used -= Arrow_Num_Blast
                        Additional_Blast_attacks -= Arrow_Num_Blast*3
                    if Resonance != 0:
                        Resonance = 0
                        Resonance_times_used -= 1
                        Resonance_attacks -= 6
                    if Resonance2 != 0:
                        Resonance2 = 0
                        Resonance_times_used2 -= 1
                        Resonance_attacks2 -= 10
                    if Material != 0:
                        Material = 0
                        Material_times_used -= Material_stack2
                        Material_attacks -= 8*Material_stack2
                    

            # 시간, 스킬 별 딜량 데이터 저장
            Total_Time.append(t)
            Deal_Cardinal_Blast.append(Cardinal_Blast)
            Deal_Cardinal_Discharge.append(Cardinal_Discharge)
            Deal_Cardinal_Transition.append(Cardinal_Transition)
            Deal_Additional_Blast.append(Additional_Blast)
            Deal_Additional_Discharge.append(Additional_Discharge)
            Deal_Resonance.append(Resonance)
            Deal_Triple_Impact.append(Triple_Impact)
            Deal_Raven.append(Raven)
            Deal_Guided_Arrow.append(Guided_Arrow)
            Deal_Ultimate_Blast.append(Ultimate_Blast)
            Deal_Evolve_Tempest.append(Evolve_Tempest)
            Deal_Obsidian_Barrier.append(Obsidian_Barrier)
            Deal_Relic_Unbound.append(Relic_Unbound)
            Deal_Evolve.append(Evolve)
            Deal_Forsaken.append(Forsaken_Relic)
            Deal_Additional_Blast_Curse_Arrow.append(Additional_Blast_Curse_Arrow)
            Deal_Forsaken_Arrow.append(Forsaken_Arrow)
            Deal_Ancient_Fury.append(Ancient_Fury)
            Deal_Material.append(Material)
            Deal_test_graph.append(test_graph)
            Deal_Resonance2.append(Resonance2)
        
        Skill_log_times = []
        Skill_log_times.append(Evolve_Tempest_times_used)
        Skill_log_times.append(Relic_Unbound_times_used)
        Skill_log_times.append(Obsidian_Barrier_times_used)
        Skill_log_times.append(Ultimate_Blast_times_used)
        Skill_log_times.append(Forsaken_Relic_times_used)
        Skill_log_times.append(Resonance_times_used)
        Skill_log_times.append(Cardinal_Blast_times_used)
        Skill_log_times.append(Cardinal_Discharge_times_used)
        Skill_log_times.append(Forsaken_Arrow_times_used)
        Skill_log_times.append(Ancient_Fury_times_used)
        Skill_log_times.append(Additional_Discharge_times_used)
        Skill_log_times.append(Additional_Blast_times_used)
        Skill_log_times.append(Additional_Blast_Curse_Arrow_times_used)
        Skill_log_times.append(Raven_times_used)
        Skill_log_times.append(Evolve_times_used)
        Skill_log_times.append(Guided_Arrow_times_used)
        Skill_log_times.append(Material_times_used)
        Skill_log_times.append(Resonance_times_used2)
        
        Skill_log_attacks = []
        Skill_log_attacks.append(Evolve_Tempest_attacks)
        Skill_log_attacks.append(Relic_Unbound_attacks)
        Skill_log_attacks.append(Obsidian_Barrier_attacks)
        Skill_log_attacks.append(Ultimate_Blast_attacks)
        Skill_log_attacks.append(Forsaken_Relic_attacks)
        Skill_log_attacks.append(Resonance_attacks)
        Skill_log_attacks.append(Cardinal_Blast_attacks)
        Skill_log_attacks.append(Cardinal_Discharge_attacks)
        Skill_log_attacks.append(Forsaken_Arrow_attacks)
        Skill_log_attacks.append(Ancient_Fury_attacks)
        Skill_log_attacks.append(Additional_Discharge_attacks)
        Skill_log_attacks.append(Additional_Blast_attacks)
        Skill_log_attacks.append(Additional_Blast_Curse_Arrow_attacks)
        Skill_log_attacks.append(Raven_attacks)
        Skill_log_attacks.append(Evolve_attacks)
        Skill_log_attacks.append(Guided_Arrow_attacks)
        Skill_log_attacks.append(Material_attacks)
        Skill_log_attacks.append(Resonance_attacks2)
                        
        # 2D array로 통합
        Deal = np.vstack((Deal_Cardinal_Blast, Deal_Cardinal_Discharge, Deal_Cardinal_Transition, Deal_Additional_Blast, Deal_Additional_Discharge, Deal_Resonance, Deal_Triple_Impact, Deal_Raven, Deal_Guided_Arrow, Deal_Ultimate_Blast, Deal_Evolve_Tempest, Deal_Obsidian_Barrier, Deal_Relic_Unbound, Deal_Evolve, Deal_Forsaken, Deal_Additional_Blast_Curse_Arrow,Deal_Forsaken_Arrow,Deal_Ancient_Fury, Deal_Material, Deal_Resonance2, Deal_test_graph))
        
        # 최종 딜량 보정 (4*무기상수*직업보정상수*랩차보정*속성보정*포스보정*숙련도보정%10^12)
        for i in range(len(Deal)):
            for j in range(len(Deal[i])):
                #Deal[i][j] *= 4 * (1.3 * 1 * 1.2 * (50 + 5/2)/100 * 1.5 * (1 + 0.86)/2) / (10**12)
                Deal[i][j] *= 4 * (1.3 * 1 * 1.2 * (50 + 5/2)/100 * 1.25 * (1 + 0.86)/2) / (10**12)
        
        # 시간, 딜량, 크리인 시간 데이터 return
        return Total_Time, Deal, CRein_time_end, Skill_log_times, Skill_log_attacks
    
    # 딜 계산 함수 실행
    time, Deal, CRein_time_end, Skill_log_times, Skill_log_attacks = calculate_deal(RT_ratio, Server_Lag, HyperSkill, Damage, Boss_Damage, Ignore_Guard, Critical_Prob, Critical_Damage, DEX_with_MY, MY2_DEX, Weapon_DEX, Attack_Ratio, Real_Attack, Buff_Duration, Restraint_level, deal_time)
    
    
    # 스킬 별 누적 딜 (Deal_Cumulative) 계산
    Deal_Cumulative = np.zeros(len(Deal))
    for j in range(0,len(np.transpose(Deal)),1):
        for i in range(0,len(Deal), 1):
            Deal_Cumulative[i] += Deal[i,j]
            continue
    
    # 최종 누적 딜 (sum) 계산
    sum = 0
    for i in Deal_Cumulative:
        sum += i

    
    with open('log.txt','w') as file:
        file.write('패스파인더 스킬 점유율\n')
        file.write(f"총 딜량: {(sum/10**12):.4f}\n\n")
        
        file.write('이볼브 템페스트\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[10]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[10]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[0]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[0]}\n\n")
        
        file.write('렐릭 언바운드\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[12]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[12]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[1]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[1]}\n\n")
        
        file.write('옵시디언 배리어\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[11]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[11]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[2]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[2]}\n\n")
        
        file.write('얼티밋 블래스트\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[9]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[9]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[3]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[3]}\n\n")
        
        file.write('포세이큰 렐릭\n')
        file.write(f"데미지 점유율: {(Deal_Cumulative[14]+Deal_Cumulative[16]+Deal_Cumulative[17])/sum*100:.3f}%\n")
        file.write(f"데미지: {(Deal_Cumulative[14]+Deal_Cumulative[16]+Deal_Cumulative[17]):.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[4]+Skill_log_times[8]+Skill_log_times[9]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[4]+Skill_log_attacks[8]+Skill_log_attacks[9]}\n\n")
        
        file.write('엣지 오브 레조넌스\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[5]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[5]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[5]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[5]}\n\n")
        
        file.write('에인션트 임팩트\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[19]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[19]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[17]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[17]}\n\n")
        
        file.write('카디널 블래스트\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[0]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[0]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[6]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[6]}\n\n")
        
        file.write('카디널 디스차지\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[1]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[1]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[7]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[7]}\n\n")
        
        file.write('에디셔널 디스차지\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[4]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[4]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[10]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[10]}\n\n")
        
        file.write('에디셔널 블래스트\n')
        file.write(f"데미지 점유율: {(Deal_Cumulative[3]+Deal_Cumulative[15])/sum*100:.3f}%\n")
        file.write(f"데미지: {(Deal_Cumulative[3]+Deal_Cumulative[15]):.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[11]+Skill_log_times[12]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[11]+Skill_log_attacks[12]}\n\n")
        
        file.write('레이븐\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[7]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[7]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[13]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[13]}\n\n")
        
        file.write('이볼브\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[13]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[13]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[14]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[14]}\n\n")
        
        file.write('가이디드 애로우\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[8]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[8]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[15]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[15]}\n\n")
        
        file.write('렐릭 마테리얼라이즈\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[18]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[18]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[16]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[16]}\n\n")
        
        file.write('참고------------------\n\n')
        
        file.write('에디셔널 블래스트 (기본화살)\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[3]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[3]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[11]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[11]}\n\n")
        
        file.write('에디셔널 블래스트 (저주화살)\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[15]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[15]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[12]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[12]}\n\n")
        
        file.write('포세이큰 렐릭 (컷신)\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[14]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[14]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[4]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[4]}\n\n")
        
        file.write('포세이큰 렐릭 (마법화살)\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[16]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[16]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[8]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[8]}\n\n")
        
        file.write('포세이큰 렐릭 (고대의 분노)\n')
        file.write(f"데미지 점유율: {Deal_Cumulative[17]/sum*100:.3f}%\n")
        file.write(f"데미지: {Deal_Cumulative[17]:.3f}\n")
        file.write(f"사용횟수: {Skill_log_times[9]}\n")
        file.write(f"공격횟수: {Skill_log_attacks[9]}\n\n")
        

    minute = '{:.1f}'.format(deal_time/60)   
    jo = int(sum//10**12)
    jo_remainder = int(sum%10**12)
    euk = int(jo_remainder//10**8)
    euk_remainder = int(jo_remainder%10**8)
    man = int(euk_remainder//10**4)
    
    # 누적 딜 출력
    print(str(minute) + '분 딜량 = ' + str(jo) + '조 ' + str(euk) + '억 ' + str(man) + '만 ')
    #print(str(minute) + '분 딜량 = ' + str(sum))
    #print('{0:.1f}분 딜량 = {1:.4f}"'.format(deal_time/60, sum))
    
    
    Deal_Int = np.zeros([len(Deal),deal_time])
    Deal_Int_C = np.zeros(deal_time)
    Deal_Int_CC = np.zeros(deal_time)
    
    for i in range(0,len(Deal),1):
        for j in range(0,deal_time,1):
            for k in range(0,100,1):
                Deal_Int[i,j] += Deal[i,j*100+k]
                
    time_int = np.zeros(deal_time)
    for i in range(0,deal_time,1):            
        time_int[i] = i+1
        
    for j in range(0,deal_time,1):  
        for i in range(0,len(Deal),1):
            Deal_Int_C[j] += Deal_Int[i,j]
    
    Deal_Int_CC[0] = Deal_Int_C[0]
    for j in range(1,deal_time,1):
        Deal_Int_CC[j] = Deal_Int_CC[j-1] + Deal_Int_C[j]



# Plot graph ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    plt.style.use('dark_background')
    if plot_graph == 2:

        fig, axs = plt.subplots(2,1,figsize=(10,8),gridspec_kw={'height_ratios': [1,1]},dpi=500)
        
        axs[0].set_title('Integrated (1s) Data')
        axs[1].set_xlabel('Time [s]')
        axs[0].set_ylabel('Non-Cumulative Deal [AU]')
        axs[1].set_ylabel('Cumulative Deal [AU]')
                  
        axs[0].bar(time_int,Deal_Int[0,:],width=0.6, color = 'magenta',bottom = 0)           
        axs[0].bar(time_int,Deal_Int[1,:],width=0.6, color = 'cyan', bottom = Deal_Int[0,:])
        axs[0].bar(time_int,Deal_Int[3,:],width=0.6, color = 'violet', bottom = Deal_Int[0,:]+Deal_Int[1,:])
        axs[0].bar(time_int,Deal_Int[4,:],width=0.6, color = 'darkturquoise', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:])
        axs[0].bar(time_int,Deal_Int[5,:],width=0.6, color = 'purple', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:])
        axs[0].bar(time_int,Deal_Int[6,:],width=0.6, color = 'deepskyblue', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:])
        axs[0].bar(time_int,Deal_Int[7,:],width=0.6, color = 'navy', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:])
        axs[0].bar(time_int,Deal_Int[8,:],width=0.6, color = 'yellowgreen', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:])
        axs[0].bar(time_int,Deal_Int[9,:],width=0.6, color = 'red', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:])
        axs[0].bar(time_int,Deal_Int[10,:],width=0.6, color = 'plum', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:])
        axs[0].bar(time_int,Deal_Int[11,:],width=0.6, color = 'orchid', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:])
        axs[0].bar(time_int,Deal_Int[12,:],width=0.6, color = 'deeppink', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:])
        axs[0].bar(time_int,Deal_Int[13,:],width=0.6, color = 'thistle', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:])
        axs[0].bar(time_int,Deal_Int[14,:],width=0.6, color = 'yellow', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:])
        axs[0].bar(time_int,Deal_Int[15,:],width=0.6, color = 'red', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:])
        axs[0].bar(time_int,Deal_Int[16,:],width=0.6, color = 'blue', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:]+Deal_Int[15,:])
        axs[0].bar(time_int,Deal_Int[17,:],width=0.6, color = 'green', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:]+Deal_Int[15,:]+Deal_Int[16,:])
        axs[0].bar(time_int,Deal_Int[18,:],width=0.6, color = 'white', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:]+Deal_Int[15,:]+Deal_Int[16,:]+Deal_Int[17,:])
        axs[0].bar(time_int,Deal_Int[19,:],width=0.6, color = 'pink', bottom = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:]+Deal_Int[15,:]+Deal_Int[16,:]+Deal_Int[17,:]+Deal_Int[18,:])

        # Test_graph
        axs[0].bar(time_int,Deal_Int[20,:],width=0.6, color = 'black')


        axs[1].bar(time_int,Deal_Int_CC, width=1, color = 'lightskyblue')
        x = np.linspace(0,deal_time,100)
        y = Deal_Int_CC[deal_time-1]/deal_time*x
        axs[1].plot(x,y, 'k--')
        
        if deal_time >= 120:
            value = (Deal_Int_CC[int(np.floor(CRein_time_end/1000))]/Deal_Int_CC[119])*100
            line = axs[1].axhline(y = Deal_Int_CC[int(np.floor(CRein_time_end/1000))], color='green', linestyle = 'dashed', label='{:.2f}%' .format(value))
            plt.legend(bbox_to_anchor = (0.8,0.2))
            value2 = ((Deal_Int_CC[18]-Deal_Int_CC[2])/Deal_Int_CC[119])*100
            line = axs[1].axhline(y = Deal_Int_CC[18], color='red', linestyle = 'dashed', label='{:.2f}%' .format(value2))
            plt.legend(bbox_to_anchor = (0.8,0.2))
        
        axs[1].text(0,Deal_Int_CC[deal_time-1]*0.95,'Total Deal:')
        axs[1].text(deal_time/8.5,Deal_Int_CC[deal_time-1]*0.95,'{:.6}' .format(Deal_Int_CC[deal_time-1]))
        
        if Cardinal_Ratio != 1:
            axs[1].text(20,Deal_Int_CC[deal_time-1]*0.7,'NON-IDEAL !!!', size= 25, color ='red')
        
        max_value = max(Deal_Int_C)    
        if Fatal_Strike == 1:
            axs[0].text(30, max_value*0.8, 'Fatal Strike', size = 20, color = 'blue')
        if Boss_Slayer == 1:
            axs[0].text(30, max_value*0.8, 'Boss Slayer', size = 20, color = 'blue')
        if Defense_Smash == 1:
            axs[0].text(30, max_value*0.8, 'Defense Smash', size = 20, color = 'blue')
        
        # Plot Information 
        axs[0].text(deal_time*230/240, max_value*0.9, int((Buff_Duration-1)*100))
        axs[0].text(deal_time*230/240, max_value*0.85, Mer)
        axs[0].text(deal_time*230/240, max_value*0.8, Cool)
        axs[0].text(deal_time*230/240, max_value*0.75, Cardinal_Ratio, color = 'red')
        axs[0].text(deal_time*230/240, max_value*0.7, Server_Lag)
        axs[0].text(deal_time*230/240, max_value*0.65, RT_ratio)
        
        axs[0].text(deal_time*185/240, max_value*0.9, 'Buff Duration')
        axs[0].text(deal_time*185/240, max_value*0.85, 'Mercedes Lv.')
        axs[0].text(deal_time*185/240, max_value*0.8, 'Cooltime Reduce')
        axs[0].text(deal_time*185/240, max_value*0.75, 'Proficiency', color = 'red')
        axs[0].text(deal_time*185/240, max_value*0.7, 'Server Lag')
        axs[0].text(deal_time*185/240, max_value*0.65, 'R/T Ratio')

        
    if plot_graph == 3:
            fig, axs = plt.subplots(2,1,figsize=(10,8),gridspec_kw={'height_ratios': [1,1]},dpi=500)
            plt.style.use('dark_background')
            
            axs[0].set_title('Integrated (1s) Data w/o color')
            axs[1].set_xlabel('Time [s]')
            axs[0].set_ylabel('Non-Cumulative Deal [AU]')
            axs[1].set_ylabel('Cumulative Deal [AU]')          
            
            axs[0].bar(time_int,Deal_Int_C, width=1.2, color = 'lightskyblue')   
            
            
            axs[1].bar(time_int,Deal_Int_CC, width=1, color = 'lightskyblue')
            x = np.linspace(0,deal_time,100)
            y = Deal_Int_CC[deal_time-1]/deal_time*x
            axs[1].plot(x,y, 'k--')
            
            if deal_time >= 120:
                value = (Deal_Int_CC[int(np.floor(CRein_time_end/1000))]/Deal_Int_CC[119])*100
                line = axs[1].axhline(y = Deal_Int_CC[int(np.floor(CRein_time_end/1000))], color='green', linestyle = 'dashed', label='{:.2f}%' .format(value))
                plt.legend(bbox_to_anchor = (0.8,0.2))
                value2 = ((Deal_Int_CC[18]-Deal_Int_CC[2])/Deal_Int_CC[119])*100
                line = axs[1].axhline(y = Deal_Int_CC[18], color='red', linestyle = 'dashed', label='{:.2f}%' .format(value2))
                plt.legend(bbox_to_anchor = (0.8,0.2))
            
            axs[1].text(0,Deal_Int_CC[deal_time-1]*0.95,'Total Deal:')
            axs[1].text(deal_time/8.5,Deal_Int_CC[deal_time-1]*0.95,'{:.6}' .format(Deal_Int_CC[deal_time-1]))
            
            if Cardinal_Ratio != 1:
                axs[1].text(20,Deal_Int_CC[deal_time-1]*0.7,'NON-IDEAL !!!', size= 25, color ='red')
            
            max_value = max(Deal_Int_C)    
            if Fatal_Strike == 1:
                axs[0].text(30, max_value*0.8, 'Fatal Strike', size = 20, color = 'blue')
            if Boss_Slayer == 1:
                axs[0].text(30, max_value*0.8, 'Boss Slayer', size = 20, color = 'blue')
            if Defense_Smash == 1:
                axs[0].text(30, max_value*0.8, 'Defense Smash', size = 20, color = 'blue')
            
            # Plot Information 
            axs[0].text(deal_time*230/240, max_value*0.9, int((Buff_Duration-1)*100))
            axs[0].text(deal_time*230/240, max_value*0.85, Mer)
            axs[0].text(deal_time*230/240, max_value*0.8, Cool)
            axs[0].text(deal_time*230/240, max_value*0.75, Cardinal_Ratio, color = 'red')
            axs[0].text(deal_time*230/240, max_value*0.7, Server_Lag)
            axs[0].text(deal_time*230/240, max_value*0.65, RT_ratio)
            
            axs[0].text(deal_time*185/240, max_value*0.9, 'Buff Duration')
            axs[0].text(deal_time*185/240, max_value*0.85, 'Mercedes Lv.')
            axs[0].text(deal_time*185/240, max_value*0.8, 'Cooltime Reduce')
            axs[0].text(deal_time*185/240, max_value*0.75, 'Proficiency', color = 'red')
            axs[0].text(deal_time*185/240, max_value*0.7, 'Server Lag')
            axs[0].text(deal_time*185/240, max_value*0.65, 'R/T Ratio')
        
        
    Deviation = 0
    if Deviation == 1:
            # Deal Deviation
            Deal_Int_Test = Deal_Int[0,:]+Deal_Int[1,:]+Deal_Int[3,:]+Deal_Int[4,:]+Deal_Int[5,:]+Deal_Int[6,:]+Deal_Int[7,:]+Deal_Int[8,:]+Deal_Int[9,:]+Deal_Int[10,:]+Deal_Int[11,:]+Deal_Int[12,:]+Deal_Int[13,:]+Deal_Int[14,:]+Deal_Int[15,:]+Deal_Int[16,:]+Deal_Int[17,:]+Deal_Int[18,:]
            Deal_Int_Test_C = np.zeros(int(deal_time/5))
            for i in range (0,int(deal_time/5)):
                for j in range (0,5):
                    Deal_Int_Test_C[i] += Deal_Int_Test[i*5+j]
      
            Deal_Int_Test_C_Sum = 0
            for k in range (0,int(deal_time/5)):
                Deal_Int_Test_C_Sum += Deal_Int_Test_C[k]
            Average_Deal = Deal_Int_Test_C_Sum/(deal_time/5)
            #print(Deal_Int_Test_C_Sum)
            Deviation_Deal = np.zeros(int(deal_time/5))
            Deviation_Deal_C = 0
            for i in range(0,int(deal_time/5)):
                Deviation_Deal[i] = abs(Deal_Int_Test_C[i] - Average_Deal)/Average_Deal
                Deviation_Deal_C += Deviation_Deal[i]
            #print(Deviation_Deal_C/48)
            
            plt.figure(figsize=(8,4), dpi=500)
            plt.title('5s Data')
            plt.xlabel('Time [s]')
            plt.ylabel('Non-Cumulative Deal [AU]')
            time = np.linspace(0,deal_time,num=int(deal_time/5))
            plt.bar(time,Deal_Int_Test_C,width=4, color = 'skyblue',bottom = 0)
            plt.axhline(y = Average_Deal, color = 'k', linestyle = 'dashed')
            plt.text(150,1.7e24,'{:.4f}' .format(Deviation_Deal_C/(deal_time/5)))

        
    return sum, Cardinal_Ratio, Deal_Int_C, Deal_Int_CC, CRein_time_end, time_int

















