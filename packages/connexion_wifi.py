"""
Module de gestion de la connexion Wi-Fi pour microcontrôleur.
Permet de scanner les réseaux disponibles et de se connecter automatiquement à un réseau connu.
"""

import time
import network

# Dictionnaire pour stocker les SSID et leurs mots de passe
SSID_PASSWORDS = {
    "iPhone de naifu": "akanaifu",
    "Moulin": "kotdessalopes",
    "WIFI_LEMAIRE": "025124940",
    # Ajoutez d'autres SSID et mots de passe ici
}


def connect_to_wifi():
    """
    Connecte à un réseau Wi-Fi en vérifiant si le SSID est déjà connu.
    Si le SSID n'est pas connu, demande le mot de passe à l'utilisateur.
    Affiche les réseaux disponibles et tente de se connecter à chacun.
    """
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    except OSError as e:
        print(f"Erreur lors de l'initialisation du Wi-Fi : {e}")
        return

    # Scanner les réseaux disponibles
    try:
        available_networks = wlan.scan()
    except OSError as e:
        print(f"Erreur lors du scan des réseaux : {e}")
        return

    # Extraire les SSID disponibles
    ssids_available = []
    for net in available_networks:
        try:
            ssid = net[0].decode("utf-8")
            ssids_available.append(ssid)
        except Exception:
            continue

    # Chercher un SSID connu parmi les réseaux disponibles
    known_ssid = None
    for ssid in ssids_available:
        if ssid in SSID_PASSWORDS:
            known_ssid = ssid
            break

    if known_ssid:
        # Tenter de se connecter au réseau connu
        password = SSID_PASSWORDS[known_ssid]
        print(f"Réseau connu trouvé : {known_ssid}. Tentative de connexion...")
        try:
            wlan.connect(known_ssid, password)
            print(
                f"Tentative de connexion à {known_ssid} avec le mot de passe enregistré."
            )
        except Exception as e:
            print(f"Erreur lors de la tentative de connexion à {known_ssid} : {e}")
            return

        for _ in range(10):
            if wlan.isconnected():
                print(f"Connecté à {known_ssid} avec succès !")
                print("Adresse IP :", wlan.ifconfig()[0])
                return
            time.sleep(1)
        print(f"Impossible de se connecter à {known_ssid}.")
    else:
        # Aucun réseau connu, demander le mot de passe pour chaque réseau disponible
        print("Aucun réseau connu trouvé. Réseaux disponibles :")
        for ssid in ssids_available:
            print(f"- {ssid}")
            password = input(f"Entrez le mot de passe pour {ssid} : ")
            SSID_PASSWORDS[ssid] = password
            print(f"Connexion à {ssid}...")
            try:
                wlan.connect(ssid, password)
                print(f"Tentative de connexion à {ssid} avec le mot de passe fourni.")
            except Exception as e:
                print(f"Erreur lors de la tentative de connexion à {ssid} : {e}")
                continue

            for _ in range(10):
                if wlan.isconnected():
                    print(f"Connecté à {ssid} avec succès !")
                    print("Adresse IP :", wlan.ifconfig()[0])
                    return
                time.sleep(1)
            print(f"Impossible de se connecter à {ssid}.")
    print("Aucun réseau disponible ou connexion échouée.")


def scan_networks():
    """
    Scanne et affiche les réseaux Wi-Fi disponibles avec leur force de signal.
    """
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        networks = wlan.scan()
        print("Réseaux disponibles :")
        for net in networks:
            try:
                print(f"SSID : {net[0].decode('utf-8')}, Signal : {net[3]}")
            except (OSError, UnicodeDecodeError) as e:
                print(f"Erreur lors de l'affichage d'un réseau : {e}")
    except OSError as e:
        print(f"Erreur lors du scan des réseaux : {e}")
