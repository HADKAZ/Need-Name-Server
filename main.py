from modules.authentification import Authentification
from modules.carte import Carte
import socket, json, _thread, time

class Server:
    def __init__(self, settings) -> None:
        self.settings = self.load_settings(settings_file=settings)
        self.carte = Carte(self.settings["map_file"])
        self.authentification = Authentification(self.settings["user_file"])
        self.answers = {
            "new_user" : self.new_user,
            "get_user" : self.get_user,
            "get_map" : self.get_map,
            "pixel_modification" : self.pixel_modification
        }

        #Création du serveur
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.settings["ip"], self.settings["port"]))
        self.sock.listen(5)

    def load_settings(self, settings_file : str) -> dict:
        """Charge les paramètres"""
        with open(settings_file) as settings:
            s = json.load(settings)

        return s

    def translation_from(self, message : bytes, encoding : str = 'utf-8'):
        """Traduit un messages en bytes vers une forme python"""
        message = message.decode(encoding)
        return json.loads(message)

    def translation_to(self, message, encoding : str = 'utf-8'):
        message = json.dumps(message)
        return message.encode(encoding)

    def processing(self, data : dict) -> dict:
        """Renvoie une réponse possible pour le client"""
        if data["request"] in self.answers:
            return self.answers[data["request"]](data)

        return {"status" : 3, "payload" : {}}

    def connection(self, client, address) -> None:
        """Gère une connection entre le client et le serveur"""
        while True:
            data = client.recv(1024)
            if not data: break

            data = self.translation_from(data)
            data["ip"] = address
            ans = self.processing(data)
            client.send(self.translation_to(ans))
        client.close()

    # Traitement des requêtes

    def new_user(self, request : dict) -> dict:
        """Renvoie l'identifiant du nouvel utilisateur"""
        if "name" in request["payload"]: # Vérifie l'intégrité de la charge
            return {
                "status" : 1,
                "id" : self.authentification.add_user(request)
            }

        return {"status" : 4, "payload" : {}}

    def get_user(self, request : dict) -> dict:
        """Renvoie les données de l'utilisateur"""
        if "id" in request:
            id = request["id"]
            if self.authentification.check_id(id):
                return {
                    "status" : 1,
                    "payload" : self.authentification.load_user(id)
                    }

        return {"status" : 4, "payload" : {}}

    def get_map(self, request : dict):
        """Renvoie la carte"""
        return {"status" : 1, "payload" : self.carte.map}

    def pixel_modification(self, request : dict):
        """Modifie un pixel à la demmande d'un client"""
        if self.authentification.check_id(request["id"]):
            user = self.authentification.load_user(request["id"])
            if time.time() - user["last_modification"] >= self.settings["delay"]:
                self.carte.set_pixel(request["payload"]["position"],
                self.carte.formating({"color" : request["payload"]["color"]}))
                self.authentification.new_modification(request["id"])

                return {"status" : 1, "payload" : {}}
            return {"status" : 2, "payload" : {}}
        return {"status" : 4, "payload" : {}}


if __name__ == "__main__":
    host = Server("./data/settings.json")
    while True:
        client, address = host.sock.accept()
        print(f"new client : {address}")
        try:
            _thread.start_new_thread(host.connection(client, address))
        except:
            pass
