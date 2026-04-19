import numpy as np
import matplotlib.pyplot as plt
import math

    #VI_level:  0 = Tempest
    #           1 = Unbound
    #           2 = Obsidian
    #           3 = Ultimate
    #           4 = Forsaken
    #           5 = Blast_VI
    #           6 = Discharge_VI
    #           7 = 3rd (Transition, Resonance, Astra)
    #           8 = 4th (Raven, Assault, Materialize)
    #           9 = Penetration
    #           10 = Hecate
    #           11 = Evolve_VI
    
def calc_vi_factor(lvl):
    if lvl == 30: return 1.6
    if lvl == 0: return 1.0
    return 1 + (10 + 15*(lvl//10) + (lvl%10)) / 100

def get_forsaken_bonus(forsaken_level):
    return [(0, 0.0), (0, 0.2), (20, 0.2), (50, 0.5)][min(3, forsaken_level // 10)]

def T(stats, time, time_test=0):
    R, C = stats["Cool_R"], stats["Cool"]
    raw_t = max(0, 360 * R - C) * (time / 360) * 1000 if time >= 60 else max(0, time * R - C) * 1000
    return int(round(raw_t / 10) * 10)

def seed_ring(stats):
    r_lvl = stats["Restraint_level"]
    c_lvl = stats["Continuous_level"]
    r_att, r_time = {1: (17, 9), 2: (34, 11), 3: (51, 13), 4: (68, 15), 5: (68, 20), 6: (85, 20)}.get(r_lvl, (0, 0))
    
    return {
        "Restraint_att": r_att,
        "Restraint_time": r_time,
        "Continuous_att": (2 * c_lvl + 2) if c_lvl > 0 else 0,
        "Continuous_dmg": 9 * c_lvl,
        "Soul_con": {2: 45, 3: 60}.get(stats["Soul_con"], 0)
    }

def parse_character_stats(Total_STAT_ARRAY, NET_STAT):
    T, N = Total_STAT_ARRAY, NET_STAT
    mer = int(T[21])
    w_atk = int(T[16,0])
    passive = int(T[26])
    prob = float(T[27]) + 7.5
    ig = N[1]
    ig += (100 - ig) * int(T[34]) / 100 # 노블방무
    ig += (100 - ig) * 0.09 # 모법 링크

    return {
        'Buff_Duration': 1 + int(T[19]) / 100,
        'Damage': int(T[8]) + int(T[31]) + 5, # 기본 + 노블 + 와헌유니온
        'Boss_Damage': int(T[9]) + int(T[32]) + int(T[25]) + 20 + 32, # 기본+노블+어빌+도핑+링크(11+9+12)
        'Ignore_Guard': ig,
        'Critical_Prob': int(T[10]),
        'Critical_Damage': int(T[11]) + int(T[33]) + 5 - 1, # 기본+노블+도핑-4차저주
        'DEX_with_MY': N[2],
        'DEX_without_MY': N[4],
        'STR': N[3],
        'Attack_Ratio': int(T[7]) + 4 + passive, # 기본 + 영메 + 어빌패시브
        'Attack': int(N[0]),
        'Attack_abs': int(T[6,0]),
        'Attack_lumi': int(T[15,0]) * 100,
        'Weapon_attack': w_atk,
        'Cool': int(T[12,0]),
        'Weapon_DEX': round(N[2] + w_atk * 4 * (1 + T[3,0] / 100)),
        'FINAL_ATTACK': 1 + N[6] / 100,
        'Restraint_level': int(T[20]),
        'Continuous_level': int(T[36]),
        'Soul_con': int(T[37]),
        'Mer': mer,
        'Server_Lag': int(T[23]),
        'RT_ratio': int(T[24]),
        'Ability_Additional_Damage': int(T[25]),
        'Ability_Passive': passive,
        'Ability_Prob': prob / (1 - prob / 100),
        'Fatal_Strike': int(T[28]),
        'Boss_Slayer': int(T[29]),
        'Just_One': int(T[30]),
        'Defense_Smash': int(T[35]),
        
        # 하이퍼스킬
        'HyperSkill': [0, 0, 0, 1, 1, 1, 1, 1, 0],
        'MY2_DEX': N[4] + 5 * (N[2] - N[4]),
        'Cool_R': 0.94 if mer == 250 else (0.95 if mer == 200 else 1.0),
        # 소울20 + 어빌패시브1랩 + 230(길축/몬파 등 버프 합산)
        'Real_Attack': int(T[6,0]) + 20 + 2 * passive + 230 
    }

def burst_time():
    delays = {
        # 시퀀스 등록 스킬
        'Sequence_Start': 60,
        'Sequence_End': 60,
        'Barrier': 90,
        'Epic': 90,
        'MY2': 90,
        'CRein': 90,
        'Angelic': 90,
        'SeedRing': 90,
        'Evolve': 90,
        # 그 외 (검토 필요)
        'Evolve_tempest': 420,
        'Forsaken': 6720,
        'Ultimate': 1800,
        'Relic_evolution': 300,
        'Unbound': 540,
        'Bind': 120,
        # 5차 극딜 게이지 쌓는 시간
        'Gauge':5000
    }

    # 6차 극딜
    sequence1 = [
        'Sequence_Start', 
        'Epic', 'MY2', 'CRein', 'Evolve', 'Angelic', 'SeedRing', 'Barrier',
        'Sequence_End',
        'Evolve_tempest', 'Forsaken', 'Ultimate', 'Relic_evolution', 'Unbound', 'Bind'
    ]
    # 5차 극딜
    sequence2 = [
        'Sequence_Start', 
        'Epic', 'MY2', 'CRein', 'Evolve', 'Angelic', 'SeedRing', 'Barrier',
        'Sequence_End',
        'Evolve_tempest', 'Bind', 'Ultimate', 'Relic_evolution', 'Unbound'
    ]

    idx = {
        'Epic': 0, 'MY2': 1, 'CRein': 2, 'Angelic': 3, 'SeedRing': 4,
        'Evolve_tempest': 5, 'Unbound': 6, 'Barrier': 7, 'Ultimate': 8,
        'Bind': 9, 'Non_Free_Deal': 10, 'Boss_Slayer': 11, 'Fatal_Strike': 12,
        'Relic_evolution': 13, 'Evolve': 14, 'Forsaken': 16
    }
    
    def build_array(sequence):
        arr = np.zeros(17)
        current_time = 0
        for i, skill in enumerate(sequence):
            if skill in idx:
                arr[idx[skill]] = current_time
            current_delay = delays[skill]
            if skill == 'Ultimate' and i + 1 < len(sequence) and sequence[i+1] == 'Relic_evolution':
                current_delay -= 1700
            current_time += current_delay
        arr[idx['Non_Free_Deal']] = current_time + 10000 # 이제는 필요 없는 코드
        arr[idx['Boss_Slayer']] = arr[idx['Evolve_tempest']] 
        arr[idx['Fatal_Strike']] = arr[idx['Evolve_tempest']]
        return arr

    Condition_ARRAY1 = build_array(sequence1)
    Condition_ARRAY2 = build_array(sequence2)

    return Condition_ARRAY1, Condition_ARRAY2

def apply_hyper_skills(stats, VI_level):
    SharpEyes_Duration = 30 if stats['HyperSkill'][0] == 1 else 0
    if stats['HyperSkill'][1] == 1:
        stats["Ignore_Guard"] = stats["Ignore_Guard"] + (100 - stats["Ignore_Guard"]) * 0.05
    if stats['HyperSkill'][2] == 1:
        stats['Critical_Prob'] += 5 
    Cardinal_Damage = 20 if stats['HyperSkill'][3] == 1 else 0
    if stats['HyperSkill'][4] == 1:
        Additional_Ratio = 50
        Additional_Ratio_VI = 51 + ((VI_level[5] - 1) // 3)
    else:
        Additional_Ratio = 40
        Additional_Ratio_VI = 41 + ((VI_level[5] - 1) // 3) 
    Cardinal_Attack = 6 if stats['HyperSkill'][5] == 1 else 5
    if stats['HyperSkill'][6] == 1:
        Ancient_Enchant_Boss_Damage = 71 + stats["Ability_Passive"]
    else:
        Ancient_Enchant_Boss_Damage = 51 + stats["Ability_Passive"] 
    Ancient_Enchant_Ignore_Guard = 20 if stats['HyperSkill'][7] == 1 else 0
    Enchant_Damage = 20 if stats['HyperSkill'][8] == 1 else 0
    
    return (stats, SharpEyes_Duration, Cardinal_Damage, Additional_Ratio, 
            Additional_Ratio_VI, Cardinal_Attack, Ancient_Enchant_Boss_Damage, 
            Ancient_Enchant_Ignore_Guard, Enchant_Damage)

# legacy
def get_base_stacks(cool_time):
    stack_mapping = {
        0: (6, 6),
        1: (6, 5),
        2: (6, 5),
        3: (5, 5),
        4: (5, 4),
        5: (5, 4),
        6: (4, 4),
        7: (4, 4)
    }
    return stack_mapping.get(cool_time, (6, 6))

def calc_D(pct, base_ign, Boss_Guard, stats, Damage2, Boss_Damage2, Critical_Damage2, DEX2, Attack_Ratio2, add_boss=0, add_ign=0, f_dmg=1.0):
    tot_ign = base_ign + (100 - base_ign) * add_ign / 100
    guard_pen = Boss_Guard * (1 - tot_ign / 100)
    if guard_pen < 0: guard_pen = 0       
    tot_atk = (100 + Attack_Ratio2) * stats['Real_Attack'] + stats['Attack_lumi']
    tot_stat = DEX2 + stats['STR'] / 4
    return pct * (100 + Damage2 + Boss_Damage2 + add_boss) * (135 + Critical_Damage2) * (100 - guard_pen) * tot_atk * tot_stat * f_dmg * stats['FINAL_ATTACK']

def calc_Ascent_D(pct, bonus_boss, bonus_ign, stats, Boss_Guard):
    # 모자/반지 스탯 제외
    tot_atk = (100 + stats["Attack_Ratio"]) * stats['Real_Attack'] + stats['Attack_lumi']
    tot_stat = stats["DEX_with_MY"] + stats['STR'] / 4 - 1000
    dmg_sum = 100 + stats["Damage"] + stats["Boss_Damage"] + bonus_boss
    crit_dmg = 135 + stats["Critical_Damage"]
    remain_guard = (1 - stats["Ignore_Guard"] / 100) * (1 - bonus_ign / 100)
    guard_pen = Boss_Guard * remain_guard
    if guard_pen < 0: guard_pen = 0
    f_atk = 1.25
    return pct * dmg_sum * crit_dmg * (100 - guard_pen) * tot_atk * tot_stat * f_atk

# 업데이트 예정
#def calc_Ascent_D(pct, bonus_boss, bonus_ign, T, N, Boss_Guard):
#    pure_atk = math.floor(T[6,0] * (1 + T[7,0]/100) + T[15,0])
#    tot_atk = (100 + T[7,0]) * pure_atk + T[15,0] * 100 
#    dmg_sum = 100 + T[8,0] + T[9,0] + bonus_boss
#    crit_dmg = 135 + T[11,0]
#    tot_stat = N[2] + N[3] / 4 - 1000
#    pure_ignore = N[1]
#    remain_guard = (1 - pure_ignore / 100) * (1 - bonus_ign / 100)
#    guard_pen = Boss_Guard * remain_guard
#    if guard_pen < 0: guard_pen = 0
#    f_atk = 1.25
#    return pct * dmg_sum * crit_dmg * (100 - guard_pen) * tot_atk * tot_stat * f_atk

def log_array():
    skill_names = [
            "Cardinal_Blast", "Cardinal_Discharge", "Cardinal_Transition", 
            "Additional_Blast", "Additional_Discharge", "Resonance", 
            "Triple_Impact", "Raven", "Guided_Arrow", "Ultimate_Blast", 
            "Evolve_Tempest", "Obsidian_Barrier", "Relic_Unbound", "Evolve", 
            "Forsaken_Relic", "Additional_Blast_Curse_Arrow", "Forsaken_Arrow", 
            "Ancient_Fury", "Material", "test_graph", "Resonance2", "Assault", 
            "Hecate", "Styx", "Phlegethon", "Penetration", "CoS", "SiM", "Evolve_Orbit"
        ]
    state = {name: {"times_used": 0, "attacks": 0, "delay": 0, "damage": []} for name in skill_names}
    return state

def write_skill_log(total_sum, Deal_Cumulative, deal_order, state, filename='log.txt'):
    final_deal = {name: Deal_Cumulative[i] for i, name in enumerate(deal_order)}
    log_targets = [
        ('이볼브 템페스트', ['Evolve_Tempest']),
        ('렐릭 언바운드', ['Relic_Unbound']),
        ('옵시디언 배리어', ['Obsidian_Barrier']),
        ('얼티밋 블래스트', ['Ultimate_Blast']),
        ('포세이큰 렐릭', ['Forsaken_Relic', 'Forsaken_Arrow', 'Ancient_Fury']),
        ('엣지 오브 레조넌스', ['Resonance']),
        ('에인션트 임팩트', ['Resonance2']),
        ('콤보 어썰트', ['Assault']),
        ('카디널 블래스트', ['Cardinal_Blast']),
        ('카디널 디스차지', ['Cardinal_Discharge']),
        ('에디셔널 디스차지', ['Additional_Discharge']),
        ('에디셔널 블래스트', ['Additional_Blast', 'Additional_Blast_Curse_Arrow']),
        ('레이븐', ['Raven']),
        ('이볼브', ['Evolve', 'Evolve_Orbit']),
        ('가이디드 애로우', ['Guided_Arrow']),
        ('렐릭 마테리얼라이즈', ['Material']),
        ('솔 헤카테', ['Hecate']),
        ('스틱스', ['Styx']),
        ('플레게톤', ['Phlegethon']),
        ('어센트', ["Penetration"]),
        ('크오솔', ["CoS"]),
        ('스인미', ["SiM"]),
    ]

    ref_targets = [
        ('에디셔널 블래스트 (기본화살)', ['Additional_Blast']),
        ('에디셔널 블래스트 (저주화살)', ['Additional_Blast_Curse_Arrow']),
        ('포세이큰 렐릭 (컷신)', ['Forsaken_Relic']),
        ('포세이큰 렐릭 (마법화살)', ['Forsaken_Arrow']),
        ('포세이큰 렐릭 (고대의 분노)', ['Ancient_Fury']),
        ('이볼브: 칠흑의 궤적', ['Evolve_Orbit'])
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('패스파인더 스킬 점유율\n')
        file.write(f"총 딜량: {(total_sum / 10**12):.9f}\n\n")
        def write_log(targets):
            for kor_name, keys in targets:
                skill_deal = sum(final_deal[k] for k in keys)
                skill_times = sum(state[k]["times_used"] for k in keys)
                skill_attacks = sum(state[k]["attacks"] for k in keys)
                file.write(f'{kor_name}\n')
                file.write(f"{skill_deal / total_sum * 100:.2f}%\n")
                file.write(f"{skill_deal:.0f}\n")
                file.write(f"{int(skill_times)}\n")
                file.write(f"{int(skill_attacks)}\n\n")
        write_log(log_targets)
        file.write('참고------------------\n\n')
        write_log(ref_targets)

def write_timeline_log(timeline_log, filename='timeline.txt'):
    col_map = {
        "Cardinal_Blast": "블래",
        "Cardinal_Discharge": "디차",
        "Assault": "어썰트",
        "Resonance": "레조",
        "Evolve_Tempest": "템페스트",
        "Ultimate_Blast": "얼블",
        "Relic_Unbound": "언바",
        "Obsidian_Barrier": "배리어",
        "Forsaken_Relic": "포세이큰",
        "Penetration": "어센트",
    }
    
    headers = ["Time(m:s:ms)", "블래", "디차", "어썰트", "레조", "템페스트", "얼블", "언바", "배리어", "포세이큰", "어센트"]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\t'.join(headers) + '\n')
        for t, active_skills in timeline_log:
            mins = t // 60000
            secs = (t % 60000) // 1000
            ms = t % 1000
            time_str = f"{mins:02d}:{secs:02d}:{ms:03d}"
            
            row = [time_str]
            active_kor = {col_map[sk] for sk in active_skills if sk in col_map}
            for header in headers[1:]:
                if header in active_kor:
                    row.append('1')
                else:
                    row.append('')  
            f.write('\t'.join(row) + '\n')


def draw_graph(plot_graph, deal_time, time_int, Deal_Int, Deal_Int_C, Deal_Int_CC, 
                    CRein_time_end, Cardinal_Ratio, stats, Deviation=0):
    # plot_graph == 0 None
    #               1 Raw
    #               2 1s Resolution
    #               3 1s Resolution w/o color (왜 만들었지..?)
    #               4 데미지 상승량 평가
    #               5 빌드 별 편차 계산 
    
    Mer = stats['Mer']
    Cool = stats['Cool']
    Server_Lag = stats['Server_Lag']
    RT_ratio = stats['RT_ratio']
    Buff_Duration = stats['Buff_Duration']
    plt.style.use('dark_background')
    
    if plot_graph in [2, 3]:
        fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 1]}, dpi=500)
        axs[0].set_title('Integrated (1s) Data' if plot_graph == 2 else 'Integrated (1s) Data w/o color')
        axs[1].set_xlabel('Time [s]')
        axs[0].set_ylabel('Non-Cumulative Damage [AU]')
        axs[1].set_ylabel('Cumulative Damage [AU]')
        
        if plot_graph == 2:
            indices = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
            skill_labels = [
                "Cardinal_Blast", "Cardinal_Discharge", "Additional_Blast", "Additional_Discharge", "Resonance", 
                "Triple_Impact", "Raven", "Guided_Arrow", "Ultimate_Blast", 
                "Evolve_Tempest", "Obsidian_Barrier", "Relic_Unbound", "Evolve", "Forsaken_Relic",
                "Additional_Blast_Curse_Arrow", "Forsaken_Arrow", 
                "Ancient_Fury", "Material", "Resonance2", "Assault", "Hecate", "Styx", "Phlegethon", "Penetration",
                "CoS", "SiM", "Orbit"
            ]
            colors = [
                'magenta',        # 0: Cardinal_Blast 
                'cyan',           # 1: Cardinal_Discharge 
                'violet',         # 3: Additional_Blast 
                'darkturquoise',  # 4: Additional_Discharge 
                'purple',         # 5: Resonance 
                'deepskyblue',    # 6: Triple_Impact 
                'navy',           # 7: Raven 
                'yellowgreen',    # 8: Guided_Arrow 
                'red',            # 9: Ultimate_Blast 
                'plum',           # 10: Evolve_Tempest 
                'orchid',         # 11: Obsidian_Barrier 
                'deeppink',       # 12: Relic_Unbound 
                'thistle',        # 13: Evolve 
                'yellow',         # 14: Forsaken_Relic 
                'red',            # 15: Additional_Blast_Curse_Arrow 
                'blue',           # 16: Forsaken_Arrow 
                'green',          # 17: Ancient_Fury 
                'white',          # 18: Material 
                'pink',           # 19: Resonance2 
                'lime',           # 20: Assault 
                'indigo',         # 21: Hecate
                'gold',           # 22: Styx
                'crimson',        # 23: Phlegethon
                'silver',          # 24: Penetration
                'orange',         # 25: CoS
                'saddlebrown',     # 26: SiM
                'lightskyblue'    # 27: Orbit
            ]
            
            current_bottom = np.zeros(deal_time)
    
            for idx, color, label in zip(indices, colors, skill_labels):
                axs[0].bar(time_int, Deal_Int[idx, :], width=0.6, color=color, bottom=current_bottom, label=label)
                current_bottom += Deal_Int[idx, :]
                
            axs[0].bar(time_int, Deal_Int[-1, :], width=0.6, color='white') # Test graph
            axs[0].legend(loc='upper right', fontsize='xx-small', ncol=4, framealpha=0.3)
        
        elif plot_graph == 3:
            axs[0].bar(time_int, Deal_Int_C, width=1.2, color='lightskyblue')

        axs[1].bar(time_int, Deal_Int_CC, width=1, color='lightskyblue')
        x = np.linspace(0, deal_time, 100)
        y = (Deal_Int_CC[-1] / deal_time) * x
        axs[1].plot(x, y, 'k--')
        
        if deal_time >= 120:
            idx_crein = int(np.floor(CRein_time_end / 1000))
            value = (Deal_Int_CC[idx_crein] / Deal_Int_CC[119]) * 100
            axs[1].axhline(y=Deal_Int_CC[idx_crein], color='green', linestyle='dashed', label=f'{value:.2f}%')
            
            value2 = ((Deal_Int_CC[18] - Deal_Int_CC[2]) / Deal_Int_CC[119]) * 100
            axs[1].axhline(y=Deal_Int_CC[18], color='red', linestyle='dashed', label=f'{value2:.2f}%')
            axs[1].legend(bbox_to_anchor=(0.8, 0.2))
        
        axs[1].text(0, Deal_Int_CC[-1] * 0.95, 'Total Damage:')
        axs[1].text(deal_time / 8.5, Deal_Int_CC[-1] * 0.95, f'{Deal_Int_CC[-1]:.6e}')
        
        if Cardinal_Ratio != 1:
            axs[1].text(20, Deal_Int_CC[-1] * 0.7, 'NON-IDEAL !!!', size=25, color='red')
            
        max_value = np.max(Deal_Int_C)
        
        if stats["Fatal_Strike"] == 1: axs[0].text(30, max_value * 0.8, 'Fatal Strike', size=20, color='blue')
        if stats["Boss_Slayer"] == 1: axs[0].text(30, max_value * 0.8, 'Boss Slayer', size=20, color='blue')
        if stats["Defense_Smash"] == 1: axs[0].text(30, max_value * 0.8, 'Defense Smash', size=20, color='blue')
        
        info_texts = [
            (0.90, f"{int((Buff_Duration-1)*100)}", 'Buff Duration', 'white'),
            (0.85, f"{Mer}", 'Mercedes Lv.', 'white'),
            (0.80, f"{Cool}", 'Cooltime Reduce', 'white'),
            (0.75, f"{Cardinal_Ratio}", 'Proficiency', 'red'),
            (0.70, f"{Server_Lag}", 'Server Lag', 'white'),
            (0.65, f"{RT_ratio}", 'R/T Ratio', 'white')
        ]
        
        #for y_pos, val, label, col in info_texts:
            #axs[0].text(deal_time * 230/240, max_value * y_pos, val, color=col)
            #axs[0].text(deal_time * 185/240, max_value * y_pos, label, color=col)
    if plot_graph == 0:
        return
    
    Deviation = 0
    if Deviation == 1:
        Deal_Int_Test_C = Deal_Int_C.reshape(-1, 5).sum(axis=1)
        Average_Deal = np.mean(Deal_Int_Test_C)
        Deviation_Deal_C = np.sum(np.abs(Deal_Int_Test_C - Average_Deal) / Average_Deal)
        
        plt.figure(figsize=(8, 4), dpi=500)
        plt.title('5s Data')
        plt.xlabel('Time [s]')
        plt.ylabel('Non-Cumulative Damage [AU]')
        
        time_5s = np.linspace(0, deal_time, num=int(deal_time/5))
        plt.bar(time_5s, Deal_Int_Test_C, width=4, color='skyblue', bottom=0)
        plt.axhline(y=Average_Deal, color='k', linestyle='dashed')
        
        plt.text(150, 1.7e24, f'{Deviation_Deal_C / (deal_time/5):.4f}')
    
    plt.tight_layout()    
    plt.show()
    plt.close('all')

def compare_graph(plot_graph, time_int1, Deal_Int_C1, Deal_Int_C2, Deal_Int_CC1, Deal_Int_CC2, total_sum1, total_sum2, Cardinal_Ratio1):
    import matplotlib.pyplot as plt
    import numpy as np

    if plot_graph == 4:
        plt.style.use('dark_background')
        fig, axs = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [1, 1]}, dpi=500)
          
        axs[0].set_title('Integrated (1s) Data w/o color')
        axs[1].set_xlabel('Time [s]')
        axs[0].set_ylabel('Non-Cumulative Damage [AU]')
        axs[1].set_ylabel('Cumulative Damage [AU]')
                
        axs[0].bar(time_int1, Deal_Int_C2, width=1.2, color='royalblue') 
        axs[0].bar(time_int1, Deal_Int_C1, width=1.2, color='lightskyblue')   
        axs[1].bar(time_int1, Deal_Int_CC2, width=1, color='royalblue')
        axs[1].bar(time_int1, Deal_Int_CC1, width=1, color='lightskyblue')
                
        increase_ratio = (total_sum2 / total_sum1 - 1) * 100
        axs[1].text(15, total_sum2 * 0.95, f'Increased Damage = {increase_ratio:.4f} %', size=15, color='white')
                
        if Cardinal_Ratio1 != 1:
            axs[1].text(20, Deal_Int_CC2[-1] * 0.7, 'NON-IDEAL !!!', size=25, color='red') 
        
        plt.show()

    elif plot_graph == 5:
        with np.errstate(divide='ignore', invalid='ignore'):
            Deal_Int_CC3 = np.where(Deal_Int_CC1 != 0, (Deal_Int_CC1 - Deal_Int_CC2) / Deal_Int_CC1, 0)
        
        plt.style.use('dark_background')
        plt.figure(figsize=(6, 4), dpi=500)
        
        plt.fill_between(time_int1, Deal_Int_CC3, 0, where=(Deal_Int_CC3 >= 0), interpolate=True, color='yellow', alpha=0.6)
        plt.fill_between(time_int1, Deal_Int_CC3, 0, where=(Deal_Int_CC3 < 0), interpolate=True, color='deeppink', alpha=0.6)
        
        plt.axhline(y=0, linestyle='--', color='white')  
        plt.xlabel('Time [s]')
        plt.ylabel('Damage Difference Ratio') 
        plt.show()



