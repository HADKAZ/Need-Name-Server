import json, random, time

class Authentification:
    def __init__(self, user_file : str) -> None:
        with open(user_file) as users:
            self.users = json.load(users)
        self.user_file = user_file
        
    def check_id(self, id : int) -> bool:
        """Renvoie si un identifiant est présent dans la base"""
        return id in self.users

    def load_user(self, id : int) -> dict:
        """Renvoie les données d'un utilisateur"""
        if self.check_id(id):
            return self.users[id]

    def new_modification(self, id : int) -> None:
        """Met à jours le temps de la dernière modification"""
        if self.check_id(id):
            self.users[id]["last_modification"] = time.time()

    def new_ip(self, id : int, ip : str) -> None:
        """Met à jours la dernière adresse ip utilisée par l'utilisateur"""
        if self.check_id(id):
            self.users[id]["last_ip"] = ip

    def add_user(self, data : dict) -> int:
        """Ajoute un utilisateur dans la base, renvoie son identifiant"""
        usr = {
            "name" : data["payload"]["name"], 
            "last_ip" : data["ip"], 
            "last_modification" : time.time()
            }

        id = self.generate_id(8)
        self.users[id] = usr
        self.sauvegarde()
        return id


    def generate_id(self, length: int) -> int:
        """Crée un identifiant qui n'est pas encore utilisé"""
        id = self.random_int_with_length(length)
        while id in self.users:
            id = self.random_int_with_length(length)

        return id
        
    def random_int_with_length(self, length : int) -> int:
        """Génère un nombre aléatoire d'une certaine longueure"""
        id = 0
        for i in range(length):
            id += random.randint(1,9) * 10**i
        
        return id

    def sauvegarde(self):
        with open(self.user_file, "w") as users:
            json.dump(self.users, users)
