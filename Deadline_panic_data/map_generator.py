import random
import os
import json
import copy

map             = []
map_framed      = {}
finish_frame    = []


class frame:
    def __init__(self, position, lv=0):
        self.lv             = lv
        self.seed           = seed + (position[0]**2)*3 + (position[1]**3)*2 + (lv**4)*4
        self.position       = [position[0], position[1]]    #[x, y]
        self.zone           = None
        self.type           = None
        self.disposition    = {}
        self.mobs           = {}
        self.case_vide      = []
        self.id             = {}
    def generate_frame(self):
        random.seed(self.seed)
        self.zone           = random.choice(list(preset_placement["preset_placement"]))
        self.type           = random.choice(list(preset_placement["preset_placement"][self.zone]))
        self.disposition    = copy.deepcopy(preset_placement["preset_placement"][self.zone][self.type])
        self.id             = copy.deepcopy(preset_placement["preset_placement"][self.zone][self.type])
        for y in range(len(self.disposition)):
            for x in range(len(self.disposition[y])):
                valeur = self.disposition[y][x]
                if valeur == 0:self.case_vide.append(f"{x}, {y}")
                elif valeur == 1:
                    obj = random.choice(preset_placement["preset"][self.zone])
                    self.disposition[y][x] = obj
                    self.id[y][x] = random.randint(11111, 99999)
                else: continue
    def generate_mobs(self):
        random.seed(self.seed)
        i = random.randint(int(0.17*((self.lv-1)**2)+2), int(0.15*((self.lv-1)**2)+5))
        quota = {mob: 0 for mob in preset_placement["mobs"]}
        while i > 0:
            random.shuffle(self.case_vide)
            mob = random.choice(preset_placement["preset_mobs"][self.zone])
            if quota[mob] != preset_placement["mobs"][mob]["max_per_frame"]:
                quota[mob] +=1
                case_utiliser = random.choice(self.case_vide)
                self.mobs[random.randint(11111, 99999)] = [mob, case_utiliser]
                self.case_vide.remove(case_utiliser)
                i -= 1
            else: continue  
    def afficher(self):
        print(self.seed, self.position, self.zone, self.type)
        print(self.disposition)
    def get_disposition(self):
        return self.disposition
    def get_seed(self):
        return self.seed
    def get_zone(self):
        return self.zone
    def get_mob(self):
        return self.mobs
    def get_id(self):
        return self.id
    
def set_doss():
    global preset_placement, data, seed
    dossier = os.path.dirname(__file__)
    chemin_preset = os.path.join(dossier, "preset_placement.json")
    chemin_save = os.path.join(dossier, "Save\\instance.json")
    with open(chemin_preset, "r", encoding="utf-8") as jason: preset_placement = json.load(jason)
    with open(chemin_save, "r", encoding="utf-8") as jason: data = json.load(jason)
    seed = data["seed"]

def generer_map(lv):
    global map, map_framed, finish_frame
    set_doss()
    row_num         = 11 #toujour impair
    col_num         = 11 #toujour impair
    map             = []
    map_framed      = {}
    finish_frame    = []
    nb_frames       = int((0.5*(lv**2))+20)
    for i in range(row_num):
        col = []
        for j in range(col_num):
            col.append(0)
        map.append(col)
    #map[row][col]
    map[int((row_num-1)/2)][int((col_num-1)/2)] = 1
    position = [int((row_num-1)/2), int((col_num-1)/2)]
    map_framed[f"{position}"] = frame(position, lv)
    map_framed[f"{position}"].generate_frame()
    frames_placed = 1
    directions = None
    oposite_directions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    random.seed(seed+lv)
    while frames_placed < nb_frames:
        if directions:
            list_directions = ['N', 'S', 'E', 'W']
            list_directions.remove(oposite_directions[directions])
            directions = random.choice(list_directions)
        elif not directions:
            directions = random.choice(['N', 'S', 'E', 'W'])
        if directions == 'N':
            position[0] -= 1
            if position[0] < 0:
                position[0] += row_num
            if map[position[0]][position[1]] == 1:
                continue
            map[position[0]][position[1]] = 1
            frames_placed += 1
        elif directions == 'S':
            position[0] += 1
            if position[0] > row_num - 1:
                position[0] -= row_num
            if map[position[0]][position[1]] == 1:
                continue
            map[position[0]][position[1]] = 1
            frames_placed += 1
        elif directions == 'E':
            position[1] += 1
            if position[1] > col_num - 1:
                position[1] -= col_num
            if map[position[0]][position[1]] == 1:
                continue
            map[position[0]][position[1]] = 1
            frames_placed += 1
        elif directions == 'W':
            position[1] -= 1
            if position[1] < 0:
                position[1] += col_num
            if map[position[0]][position[1]] == 1:
                continue
            map[position[0]][position[1]] = 1
            frames_placed += 1
        else:
            break
        if map[position[0]][position[1]] == 1:
            map_framed[f"{position}"] = frame(position, lv)
            map_framed[f"{position}"].generate_frame()
            map_framed[f"{position}"].generate_mobs()
            finish_frame = position
        else: continue
    return map, map_framed, finish_frame

def afficher_map(map):
    VERT  = "\033[92m"
    ROUGE = "\033[91m"
    JAUNE = "\033[33m"
    RESET = "\033[0m"
    nb_uns      = 0
    nb_zero     = 0
    Y = 0
    for ligne in map:
        ligne_affichee = ""
        X = 0
        for case in ligne:
            if finish_frame == [Y, X]:
                nb_uns  += 1
                ligne_affichee += JAUNE  + "1 " + RESET
            else:
                if case == 1:
                    nb_uns  += 1
                    ligne_affichee += VERT  + "1 " + RESET
                else:
                    nb_zero += 1
                    ligne_affichee += ROUGE + "0 " + RESET
            X += 1
        Y += 1
        print(ligne_affichee)

if __name__ == "__main__":
    for i in range(9):
        generer_map(i+1)
        afficher_map(map)
        print(finish_frame)
        print(f"level {i+1}")