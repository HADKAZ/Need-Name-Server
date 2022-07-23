import json, time

class Carte:
    def __init__(self, map_file : str) -> None:
        with open(map_file, "r") as map:
            self.map = json.load(map)
        self.map_file = map_file
        self.color = [i for i in range(10)]

    def formating(self, data : dict) -> int:
        """Met les données au format de la carte"""
        if data["color"] in self.colors: 
            return data["color"]
        else:
            return 1

    def set_pixel(self, position : tuple, data : str) -> None:
        """Modifie la couleur d'un pixel"""
        self.map[position[0]][position[1]] == self.formating(data)
        self.sauvegarde()

    def set_pixels(self, position1 : tuple, position2 : tuple, data : dict) -> None:
        """Met à jours tout les pixels entre position1 et position2"""
        data = self.formating(data)
        for x in range(position1[0], position2[0]):
            for y in range(position1[1], position2[1]):
                self.map[x][y] = data

    def sauvegarde(self) -> None:
        """Sauvegarde la carte dans le fichier"""
        with open(self.map_file, "w") as map:
            json.dump(self.map, map)

