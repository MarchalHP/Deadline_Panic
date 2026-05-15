import random
from preset_placement import preset, preset_placement, type_list
seed = 1234567890
class frame:
    def __init__(self, position=[0, 0]):
        self.position = position
        random.seed(seed+(self.position[0]*self.position[1]))
        self.type = random.choice(type_list)
        self.placement = []
        self.inventair = {}
    def generate_placement(self):
        if self.type in preset_placement:
            random.seed(seed+(self.position[0]*self.position[1]))
            self.placement = random.choice(preset_placement[self.type])
            self.inventair = {}
            x = y = 0
            for i in self.placement:
                x += 1
                y = 0
                for j in i:
                    y += 1
                    if j == 0:
                        continue
                    elif j == 1:
                        self.inventair[f'{x}, {y}'] = random.choice(preset[self.type])
                    else:
                        return "ERROR"
        else:
            return "type inexistant"
    def get_type(self):
        return self.type
    def get_placement(self):
        return self.placement
    def get_inventair(self):
        return self.inventair