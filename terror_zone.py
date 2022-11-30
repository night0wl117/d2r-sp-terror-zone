import configparser
import pandas as pd
import numpy as np
import time
import json
import shutil
from datetime import datetime
from random import randrange
from pathlib import Path

LEVELS_TXT_FILE = 'global\excel\levels.txt'
LEVELS_TXT_TEMPLATE_FILE = 'levels.txt'
SUPERUNIQUES_TXT_FILE = 'global\excel\superuniques.txt'
SUPERUNIQUES_TXT_TEMPLATE_FILE = 'superuniques.txt'
MONSTATS_TXT_FILE = 'global\excel\monstats.txt'
MONSTATS_TXT_TEMPLATE_FILE = 'monstats.txt'
LEVELS_JSON_FILE = 'local\lng\strings\levels.json'
LEVELS_JSON_FILE_TEMPLATE = 'levels.json'

def main():
    config = read_config_file('config.ini')
    d2_mod_data_folder = config['SETTINGS']['d2r_mod_data_folder_path']

    tzone_df = read_terror_zone_file()
    initial_start = True
    keep_current_zone = input(
        f'''
Do you want to keep current zone(s): {get_current_zone_area_name()} ?
(Y/N): ''')

    lvls = []
    while True:
        character_lvl = get_character_level()
        lvls.append(character_lvl)
        lvls = lvls[-2:]
        if len(lvls) > 1:
            if lvls[0] != lvls[1]:
                print('Character level changed in config.ini. Updating files accordingly...')

                config_zone_id = get_current_zone_id()
                update_levels_txt_file(Path(d2_mod_data_folder, LEVELS_TXT_FILE), config_zone_id)
                update_monstats_file(Path(d2_mod_data_folder, MONSTATS_TXT_FILE), config_zone_id, tzone_df, character_lvl)
                update_superunique_file(Path(d2_mod_data_folder, SUPERUNIQUES_TXT_FILE), config_zone_id, tzone_df)
                update_level_json_file(tzone_df, config_zone_id, Path(d2_mod_data_folder, LEVELS_JSON_FILE), LEVELS_JSON_FILE_TEMPLATE)

                print('Files updated. Restart D2R for the changes to take effect.')

        # if len(lvls) > 1:
        #     print(f'prev: {lvls[-2]}')
        now = datetime.now()

        if not initial_start:
            time.sleep(10)

        if now.minute == 59 or initial_start:
            if keep_current_zone.lower() == 'y':

                print('Updating files just to be sure...')
                config_zone_id = get_current_zone_id()
                update_levels_txt_file(Path(d2_mod_data_folder, LEVELS_TXT_FILE), config_zone_id)
                update_monstats_file(Path(d2_mod_data_folder, MONSTATS_TXT_FILE), config_zone_id, tzone_df, character_lvl)
                update_superunique_file(Path(d2_mod_data_folder, SUPERUNIQUES_TXT_FILE), config_zone_id, tzone_df)
                update_level_json_file(tzone_df, config_zone_id, Path(d2_mod_data_folder, LEVELS_JSON_FILE), LEVELS_JSON_FILE_TEMPLATE)
                print('Files updated. You can now start D2R. If the game is running you have to restart D2R.')

                initial_start = False
                keep_current_zone = 'N'
            else:
                # Setting the files to original state before updating them
                set_files_to_original_state()

                zone_id = get_random_zone_id(tzone_df)
                area_names = get_area_name(tzone_df, zone_id)

                print(f'Character level: {character_lvl}')
                print(f'Terrorized Zone (level: {min(character_lvl + 2, 96)}): {area_names}')

                # Updating files with new terror zone(s)
                update_zones_in_config_file(zone_id)
                update_level_json_file(tzone_df, zone_id, Path(d2_mod_data_folder, LEVELS_JSON_FILE), LEVELS_JSON_FILE_TEMPLATE)
                update_levels_txt_file(Path(d2_mod_data_folder, LEVELS_TXT_FILE), zone_id)
                update_monstats_file(Path(d2_mod_data_folder, MONSTATS_TXT_FILE), zone_id, tzone_df, character_lvl)
                update_superunique_file(Path(d2_mod_data_folder, SUPERUNIQUES_TXT_FILE), zone_id, tzone_df)

                print('Please restart D2R.')
                
                if not initial_start:
                    time.sleep(120)
                initial_start = False


def set_files_to_original_state():

    config = read_config_file('config.ini')
    d2_mod_data_folder = config['SETTINGS']['d2r_mod_data_folder_path']
    
    shutil.copy2(LEVELS_TXT_TEMPLATE_FILE, Path(d2_mod_data_folder, LEVELS_TXT_FILE))
    shutil.copy2(SUPERUNIQUES_TXT_TEMPLATE_FILE, Path(d2_mod_data_folder, SUPERUNIQUES_TXT_FILE))
    shutil.copy2(MONSTATS_TXT_TEMPLATE_FILE, Path(d2_mod_data_folder, MONSTATS_TXT_FILE))
    shutil.copy2(LEVELS_JSON_FILE_TEMPLATE, Path(d2_mod_data_folder, LEVELS_JSON_FILE))

def update_levels_txt_file(file, zone_id):
    main_file_df = pd.read_csv(file, delimiter='\t')
    character_lvl = get_character_level()
    mon_lvl = min(main_file_df[main_file_df['Id'].isin(zone_id)]['MonLvlEx(H)'].astype(int).values)
    main_file_df['MonLvlEx(H)'] = np.where(main_file_df['Id'].isin(zone_id), max(mon_lvl, min(character_lvl + 2, 96)), main_file_df['MonLvlEx(H)'])
    # Set monster density to 2200
    main_file_df['MonDen(H)'] = np.where(main_file_df['Id'].isin(zone_id), 2200, main_file_df['MonDen(H)'])
    # add potential 2 extra boss packs
    main_file_df['MonUMin(H)'] = np.where(main_file_df['Id'].isin(zone_id), main_file_df['MonUMin(H)'] + 2, main_file_df['MonUMin(H)'])
    main_file_df['MonUMax(H)'] = np.where(main_file_df['Id'].isin(zone_id), main_file_df['MonUMax(H)'] + 2, main_file_df['MonUMax(H)'])

    # format file
    m = main_file_df.select_dtypes(np.number)
    main_file_df[m.columns] = m.round().astype('Int64')

    # save file
    main_file_df.to_csv(file, header=True, index=False, sep='\t', mode='w')

def update_superunique_file(file, zone_id, terror_zone_df):
    main_file_df = pd.read_csv(file, delimiter='\t')
    # Get superuniques if any
    superunique_ids = get_superunique_hcidx(terror_zone_df, zone_id)
    # Check if superuniques have multiple TC level
    # eg.: Countess (H) Desecrated A, Countess (H) Desecrated B, Countess (H) Desecrated C....
    has_multiple_tc_lvl = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]['HasMultipleTcLevel'].notnull().any()

    # if it has multiple tc level, we choose one depending on our character level
    # eg. Countess:
    # Countess (H) Desecrated A -> lvl 82
    # Countess (H) Desecrated B -> lvl 84
    # Countess (H) Desecrated C -> lvl 87
    # Countess (H) Desecrated D -> lvl 90
    # Countess (H) Desecrated E -> lvl 93
    # Countess (H) Desecrated F -> lvl 96
    # eg.: if we are level 90, that means uniques/bosses are 90 + 5 (95), so we choose Countess (H) Desecrated E (lvl 93)
    if has_multiple_tc_lvl:
        correct_tc_for_multiple_lvl_tc = get_correct_TC_for_multiple_lvl_TC(terror_zone_df, zone_id)
        main_file_df['TC(H)'] = np.where(main_file_df['hcIdx'].isin(superunique_ids), correct_tc_for_multiple_lvl_tc, main_file_df['TC(H)'])
    # else we just upgrade its level if has only one TC
    else:
        main_file_df['TC(H)'] = np.where(main_file_df['hcIdx'].isin(superunique_ids), main_file_df['TC(H) Desecrated'], main_file_df['TC(H)'])

    # format file
    m = main_file_df.select_dtypes(np.number)
    main_file_df[m.columns] = m.round().astype('Int64')

    # save file
    main_file_df.to_csv(file, header=True, index=False, sep='\t', mode='w')

def update_monstats_file(file, zone_id, terror_zone_df, character_lvl):
    boss_id = get_boss_monster_hcIdx_for_tz(terror_zone_df, zone_id)
    # if tz does not have boss, return: no changes needed
    if boss_id.size == 0:
        return

    # Check if boss has multiple TC level
    has_multiple_tc_lvl = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]['BossTC'].notnull().any()
    main_file_df = pd.read_csv(file, delimiter='\t')
    boss_lvl = main_file_df[main_file_df['*hcIdx'].isin(boss_id)]['Level(H)'].astype(int).values[0]

    # We upgrade tc if has only one TC level
    if not has_multiple_tc_lvl:
        main_file_df['TreasureClass(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), main_file_df['TreasureClassDesecrated(H)'], main_file_df['TreasureClass(H)'])
        main_file_df['TreasureClassChamp(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), main_file_df['TreasureClassDesecratedChamp(H)'], main_file_df['TreasureClassChamp(H)'])
        main_file_df['TreasureClassUnique(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), main_file_df['TreasureClassDesecratedUnique(H)'], main_file_df['TreasureClassUnique(H)'])
        main_file_df['Level(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), max(boss_lvl, min(character_lvl + 5, 99)) , main_file_df['Level(H)'])

        # if boss is Andariel, update Quest Treasure Class too (since she is always bugged so the game uses that column)
        if boss_id[0] == 156:
            main_file_df['TreasureClassQuest(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), main_file_df['TreasureClassDesecrated(H)'], main_file_df['TreasureClassQuest(H)'])
    # else we choose one depending on our character level
    else:
        correct_tc_for_boss = get_correct_TC_for_boss(terror_zone_df, zone_id)
        main_file_df['TreasureClass(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), correct_tc_for_boss, main_file_df['TreasureClass(H)'])
        main_file_df['TreasureClassChamp(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), correct_tc_for_boss, main_file_df['TreasureClassChamp(H)'])
        main_file_df['TreasureClassUnique(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), correct_tc_for_boss, main_file_df['TreasureClassUnique(H)'])
        main_file_df['Level(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), max(boss_lvl, min(character_lvl + 5, 99)) , main_file_df['Level(H)'])

        # if boss is Andariel, update Quest Treasure Class too (since she is always bugged)
        if boss_id[0] == 156:
            main_file_df['TreasureClassQuest(H)'] = np.where(main_file_df['*hcIdx'].isin(boss_id), correct_tc_for_boss, main_file_df['TreasureClassQuest(H)'])

    # format file
    m = main_file_df.select_dtypes(np.number)
    main_file_df[m.columns] = m.round().astype('Int64')

    # save file
    main_file_df.to_csv(file, header=True, index=False, sep='\t', mode='w')

def update_level_json_file(terror_zone_df, zone_id, json_file, json_file_template):
    """Adds 'Terrorized' text with a line break to the current TZ areas"""
    level_ids = get_terrorized_json_level_ids(terror_zone_df, zone_id)
    
    with open(json_file_template, encoding='utf-8-sig') as file:
        data = json.load(file)

    for level in data:
        if level['id'] in level_ids:
            level['enUS'] = 'Terrorized\n' + level['enUS']

    with open(json_file, encoding='utf-8', mode='w') as file:
        file.write(json.dumps(data, ensure_ascii=False))

def get_area_name(dataframe: pd.DataFrame, id):
    random_area = dataframe[dataframe['Id'].isin(id)]
    area = random_area['*StringName'].values
    return ", ".join(sorted(set(area.tolist())))

def read_terror_zone_file():
    df = pd.read_csv('levels_terrorized.txt', delimiter='\t')
    return df

def get_random_zone_id(terror_zone_df: pd.DataFrame):
    max_group_value = terror_zone_df['Groups'].max()
    random_group_id = randrange(1, max_group_value + 1)
    random_row = terror_zone_df[terror_zone_df['Groups'] == random_group_id]
    return random_row['Id'].astype('Int64').values.tolist()

def read_config_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def get_character_level():
    config = read_config_file('config.ini')
    character_lvl = int(config['CHARACTER'].get('Level'))
    return character_lvl

def get_current_zone_area_name():
    config = read_config_file('zones.ini')
    current_zone = config['CURRENTZONE'].get('Area')
    return current_zone

def get_current_zone_id():
    config = read_config_file('zones.ini')
    current_id = config['CURRENTZONE'].get('id')
    current_id = json.loads(current_id)
    return current_id

def update_zones_in_config_file(zone_id):
    area_names = get_area_name(read_terror_zone_file(), zone_id)
    config = read_config_file('zones.ini')
    config.set('CURRENTZONE', 'id', str(zone_id))
    config.set('CURRENTZONE', 'Area', str(area_names))
    with open('zones.ini', 'w') as config_file:
        config.write(config_file)

def get_superunique_hcidx(terror_zone_df: pd.DataFrame, zone_id) -> list:
    rows = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]
    only_superunique_rows = rows[rows['SuperUniqueHcIdx'].notnull()]
    a = only_superunique_rows['SuperUniqueHcIdx'].str.split(', ')
    if not a.empty:
        return list(map(int, a.tolist()[0]))
    else:
        return []

def get_boss_monster_hcIdx_for_tz(terror_zone_df, zone_id) -> list:
    """Returns current TZ boss"""
    df = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]
    boss_hcidx = df[df['monstatsBossHcIdx'].notnull()]['monstatsBossHcIdx'].astype(int).values
    return boss_hcidx

def get_terrorized_json_level_ids(terror_zone_df:pd.DataFrame, zone_id):
    """Returns the IDs of the current TZ areas"""
    df = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]
    level_ids = df['levelsJsonId'].astype(int).tolist()
    return level_ids

def get_correct_TC_for_multiple_lvl_TC(terror_zone_df, zone_id):
    """Returns the correct Treasure Class if a superunique has multiple tc levels"""
    df = pd.read_csv('treasureclassex.txt', delimiter='\t')
    rows = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]
    only_superunique_rows = rows[rows['SuperUniqueHcIdx'].notnull()]
    tc = only_superunique_rows['SuperUniqueTC'].values[0]

    character_lvl = get_character_level() + 5
    TC_rows = df[df['Treasure Class'].str.contains(tc, regex=False)]

    TC_levels = TC_rows['level'].astype(int).tolist()
    TC_levels.sort()

    # if character level (+5) is less than the boss' min TC level we choose the boss' min TC level
    if character_lvl < min(TC_levels):
        max_lvl = min(TC_levels)

    for lvl in TC_levels:
        while lvl < character_lvl:
            max_lvl = lvl
            break

    return TC_rows[TC_rows['level'] == max_lvl]['Treasure Class'].astype(str).values[0]

def get_correct_TC_for_boss(terror_zone_df, zone_id):
    """Returns the correct Treasure Class if boss has multiple tc levels"""
    df = pd.read_csv('treasureclassex.txt', delimiter='\t')
    rows = terror_zone_df[terror_zone_df['Id'].isin(zone_id)]
    only_boss_rows = rows[rows['monstatsBossHcIdx'].notnull()]
    tc = only_boss_rows['BossTC'].values[0]
    character_lvl = get_character_level() + 5
    TC_rows = df[df['Treasure Class'].str.contains(tc, regex=False)]
    TC_levels = TC_rows[TC_rows['level'].notna()]['level'].astype(int).tolist()
    TC_levels.sort()
    
    # if character level (+5) is less than the boss' min TC level we choose the boos' min TC level
    if character_lvl < min(TC_levels):
        max_lvl = min(TC_levels)
    
    for lvl in TC_levels:
        while lvl < character_lvl:
            max_lvl = lvl
            break

    return TC_rows[TC_rows['level'] == max_lvl]['Treasure Class'].astype(str).values[0]

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        user_input = input("""
Do you want to set files to their original state? (Y/N): """)
        if user_input.lower() == 'y':
            set_files_to_original_state()

        
