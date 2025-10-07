# Dragon Parade Disney Star On Parade - Serveur Modbus & Supervision

Ce projet simule le système de flamme du char dragon Disney Star On Parade.
Il inclut un serveur Modbus TCP (pymodbus v3) et une interface graphique Tkinter pour la supervision.

## Fonctionnalités
- Serveur Modbus TCP (port 5020)
- Cycle automatique : montée de la tête, gestion de la pompe, autorisation flamme
- Mode manuel : contrôle direct via interface ou client Modbus
- Recharge pompe, activation flamme, affichage des niveaux
- Interface graphique : visualisation du cycle, boutons de commande

## Adresses Modbus
| Adresse | Type     | Description                       |
|---------|----------|-----------------------------------|
| 0       | holding  | Niveau isopar (L)                 |
| 1       | holding  | Niveau pompe (cl)                 |
| 2       | holding  | Position tête (0-15)              |
| 3       | coil     | Autorisation flamme               |
| 4       | coil     | Activation flamme                 |
| 5       | holding  | Mode (0=auto, 1=manuel)           |

## Cycle de fonctionnement
- Saisie du niveau isopar (0-10L, min 3L pour flamme)
- Pompe chargée à 1L (1000cl) si isopar >= 1L
- Tête monte de 0 à 15
- À tête=15 et isopar>=3L, autorisation flamme
- Activation flamme consomme 250cl (25%) de la pompe
- Recharge pompe possible si isopar >= 1L

## Interface
- Affiche tous les niveaux et états
- Boutons : Mode Auto/Manuel, Démarrer/Arrêter cycle, Recharge pompe, Activer flamme

## Installation
1. Installer Python 3.8+
2. Installer pymodbus et tkinter :
   ```
   pip install pymodbus
   ```
   (Tkinter est inclus avec Python)
3. Lancer le serveur :
   ```
   python server.py
   ```

## Utilisation
- Lancer le serveur, utiliser l'interface pour piloter le cycle et la flamme
- Un client Modbus peut se connecter sur le port 5020 pour supervision ou contrôle manuel

---
Projet complet dans `server.py` uniquement, aucune dépendance externe complexe.
	```

## Variables Modbus

| Adresse | Description                | Type      | Valeur         |
|---------|----------------------------|-----------|----------------|
| 0       | Niveau isopar (L)          | Holding   | 0-10           |
| 1       | Niveau pompe (cl)          | Holding   | 0-100          |
| 2       | Position tête (0-15)       | Holding   | 0-15           |
| 3       | Autorisation flamme        | Coil      | 0/1            |
| 4       | Activation flamme          | Coil      | 0/1            |
| 5       | Aile haut (fin de course)  | Coil      | 0/1            |
| 6       | Aile bas (fin de course)   | Coil      | 0/1            |
| 7       | Mode (0=auto, 1=manuel)    | Holding   | 0/1            |
| 8       | Commande tête +            | Coil      | 0/1            |
| 9       | Commande tête -            | Coil      | 0/1            |
| 10      | Commande aile haut         | Coil      | 0/1            |
| 11      | Commande aile bas          | Coil      | 0/1            |
| 12      | Commande recharge pompe    | Coil      | 0/1            |

## Cycle de fonctionnement

1. Entrer le niveau d’isopar (min 3L)
2. Charger la pompe à 1L (100cl)
3. Monter la tête (0→15)
4. À 15, ouvrir la bouche, autoriser la flamme
5. Activer la flamme (consomme 250ml, 20% de la pompe)
6. Mouvements des ailes simulés

## Mode manuel

- Contrôle direct de la tête (haut/bas)
- Contrôle direct des ailes (haut/bas)
- Recharge manuelle de la pompe
- Activation de la flamme si autorisée

## Auteur

Projet réalisé avec Python, pymodbus et Tkinter.
