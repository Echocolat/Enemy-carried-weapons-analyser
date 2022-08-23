import oead
import pathlib
from collections import Counter
import json
import os

with open('map_file_list.json','r') as file_list:
    MAP_LIST = json.loads(file_list.read())
    # Gets all map files' name and put them in a list

def get_data_on_one_map(file):

    ### Returns a list of dicts, that contain every weapon found within enemies' hands (with their enemy, and localisation)###

    data_file = oead.byml.from_binary(oead.yaz0.decompress(pathlib.Path(file).read_bytes()))      # Deserializes the map
    enemy_and_weapon = []                                                                         # Initializes the list

    for object in data_file['Objs']:                                                              # Iterates through every object on the map unit
        if object['UnitConfigName'][:6] == 'Enemy_' and '!Parameters' in object:                  # If the object is an enemy with parameters,
            for parameter in object['!Parameters']:                                               # we check its weapon parameters, which are
                if 'EquipItem' in parameter and 'Weapon_' in object['!Parameters'][parameter]:    # in 'EquipItemX'. 
                    enemy_and_weapon.append({
                        'Weapon': object['!Parameters'][parameter],
                        'Enemy': object['UnitConfigName'],
                        'Localisation': file[27:-7]
                        })

    return enemy_and_weapon

def get_data_on_all_map():

    ### Iterates through all map files and adds all 'enemy_and_weapon' lists together ###

    enemy_weapon = []                                                                    # Initializes the list

    for map_file in MAP_LIST:                                                            # Iterates throughg the map file list

        if os.path.exists('aoc\\0010\\' + map_file):                                     # Checks if the file exists in the modded path
            enemy_weapon = enemy_weapon + get_data_on_one_map('aoc\\0010\\'+map_file)    # Calling the function with the path of the modded map file

    return sorted(enemy_weapon, key=lambda d: d['Weapon'])                               # Sorting it for visibility purposes

def get_enemies_per_weapons(list_of_dicts):

    ### Transforms the list of dicts ('weapon':weapon,'enemy':enemy) in a dict of a list of enemies carrying the same weapon ###

    enemies_per_weapon = {}                                                     # Initializes the dict

    for dicts in list_of_dicts:                                                 # Iterates through the list of dicts

        if not dicts['Weapon'] in enemies_per_weapon:                           # If the key of the weapon doesn't exist yet, we create a list
            enemies_per_weapon[dicts['Weapon']] = [dicts['Enemy']]              # the enemy who carries the weapon

        else:
            enemies_per_weapon[dicts['Weapon']].append(dicts['Enemy'])          # Else we add the enemy to the list of the already existing weapon key

    return enemies_per_weapon

def get_num_enemies_carrying_same_weapon(dict_of_lists):

    ### Transforms the dict of lists of enemies per weapon into a counter of same enemies who carry the same weapon (sorted) ###

    num_enemies_carrying_same_weapon = {}                               # Initializes the dict

    for key in dict_of_lists:                                           # Iterates through the weapons

        num_enemies_counter = dict(Counter(dict_of_lists[key]))         # Gets the counter
        num_enemies_carrying_same_weapon[key] = dict(                   # Sort it (from biggest to smallest)
            sorted(
                num_enemies_counter.items(), 
                key=lambda item: item[1], 
                reverse=True
                )
            )

    return num_enemies_carrying_same_weapon

def main():

    enemy_weapon = get_data_on_all_map()
    enemies_per_weapons = get_enemies_per_weapons(enemy_weapon)
    num_enemies_carrying_same_weapon = get_num_enemies_carrying_same_weapon(enemies_per_weapons)

    with open('enemies_weapons_local.json','w') as output:
        output.write(json.dumps(enemy_weapon,indent=2))

    with open('enemies_per_weapon.json','w') as output_f:
        output_f.write(json.dumps(enemies_per_weapons,indent=2))

    with open('num_enemies_carrying_same_weapon.json','w') as output_ff:
        output_ff.write(json.dumps(num_enemies_carrying_same_weapon,indent=2))

if __name__ == '__main__':
    main()