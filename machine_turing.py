import sys

DROITE = +1
SUR_PLACE = 0
GAUCHE = -1
VIDE = "_"


class MachineTuring:
    """
    Met en oeuvre une machine de Turing sur un ruban
    Les règles sont un dictionnaire {(etat, caractère_lu): (nouvel_etat, caractère_écrit, déplacement)}
    L'état final est un des états cités dans les règles.
    Les états sont des chaînes de caractères
    Les caractères sont des chaînes de caractères de longueur 0 ou 1
    """

    def __init__(self, regles, etat_final):
        self.taille = 100
        self.ruban = [VIDE] * self.taille
        self.position_tete = None
        self.etat = None
        self.etat_final = etat_final
        self.regles = regles
        self.taille_augmentation = self.taille
        self.taille_affichage = 21

    def demarrage(self, ruban, position_tete, etat_initial):
        """
        Initialise la machine
        On passe en paramètres:
        - la liste des caractères présents sur le ruban
        - la position intiale de la tête -> l'indice d'un carcatère dans la liste
        - l'état initial
        """
        if type(ruban) is not list:
            raise ValueError("La ruban doit être une liste")
        if any(type(c) is not str or len(c) > 1 for c in ruban):
            raise ValueError("Les caractères du ruban doivent être des chaînes de taille <= 1")
        if not 0 <= position_tete < len(ruban):
            raise ValueError("La tête doit initialement être sur le ruban")

        self.ruban = [VIDE] * self.taille_augmentation + ruban + [VIDE] * self.taille_augmentation
        self.etat = etat_initial
        self.position_tete = position_tete + self.taille_augmentation

    def etape(self):
        """
        Effectue une transition sur la machine
        Lève une erreur si le couple (état, caractère lu) n'apparaît pas dans les règles
        Termine l'exécution si l'état est l'état final de la machine
        """
        if self.etat == self.etat_final:
            print("La machine a atteint son état final")
            sys.exit(0)
        caractere_lu = self.ruban[self.position_tete]
        if (self.etat, caractere_lu) not in self.regles:
            raise ValueError(f"Le couple {self.etat, caractere_lu} n'est pas associé à une règle")
        nouvel_etat, caractere_ecrit, deplacement = self.regles[self.etat, caractere_lu]
        if not (
            self.taille_affichage // 2
            <= self.position_tete + deplacement
            < len(self.ruban) - self.taille_affichage // 2
        ):
            if deplacement == GAUCHE:
                self.ruban = [VIDE] * self.taille_augmentation + self.ruban
                self.position_tete += self.taille_augmentation
            else:
                self.ruban.extend([VIDE] * self.taille_augmentation)
        self.etat = nouvel_etat
        self.ruban[self.position_tete] = caractere_ecrit
        self.position_tete += deplacement

    def affiche(self):
        """
        Affiche la configuration actuelle de la machine :
        - état actuel,
        - caractère lu,
        - état du ruban
        Le ruban étant de taille variable on pourra n'en afficher qu'une partie en prenant soin de le centrer
        sur la tête de lecture
        """
        print(f"État : {self.etat}\nCaractère lu : {self.ruban[self.position_tete]}")
        print(
            "".join(
                self.ruban[
                    self.position_tete - self.taille_affichage // 2 : self.position_tete + self.taille_affichage // 2
                ]
            )
        )
        print(" " * (self.taille_affichage // 2) + "^")
regles_ini = {
    ("q1", VIDE): ("q2", "0", DROITE),
    ("q2", VIDE): ("q3", VIDE, DROITE),
    ("q3", VIDE): ("q4", "1", DROITE),
    ("q4", VIDE): ("q5", VIDE, DROITE),
    ("q5", VIDE): ("q1", VIDE, SUR_PLACE),
}

regles_train_infinie = {
    #regarder la valeur 
    ("q1", VIDE): ("q1", "_", DROITE),
    ("q1", "0"):  ("q2", "_", DROITE),
    ("q1", "1" ) :("q6", "_", DROITE),

    #la valeur =  0
    #si la valeur = 0 (va tout a jusquau milieu)
    ("q2", VIDE ) :("q3", VIDE, DROITE),
    ("q2", "0" ) :("q2", "0", DROITE),
    ("q2", "1" ) :("q2", "1", DROITE),
    
    #si la valeur = 0 (va tout au bout)
    ("q3", VIDE ) :("q4", "0", GAUCHE),
    ("q3", "1" ) :("q3", "1", DROITE),
    ("q3", "0" ) :("q3", "0", DROITE),

    #retour au milieu
    ("q4", VIDE ) :("q5", VIDE, GAUCHE),
    ("q4", "0" ) :("q4", "0", GAUCHE),
    ("q4", "1" ) :("q4", "1", GAUCHE),
    
    #retour jusquau debut en rementant le 0
    ("q5", VIDE ) :("q1", "0", DROITE),
    ("q5", "0" ) :("q5", "0", GAUCHE),
    ("q5", "1" ) :("q5", "1", GAUCHE),

#la valeur = 1
    #si la valeur = 1 (va tout a jusquau milieu)
    ("q6", VIDE ) :("q7", VIDE, DROITE),
    ("q6", "0" ) :("q6", "0", DROITE),
    ("q6", "1" ) :("q6", "1", DROITE),
    
    #si la valeur = 1 (va tout au bout)
    ("q7", VIDE ) :("q8", "1", GAUCHE),
    ("q7", "1" ) :("q7", "1", DROITE),
    ("q7", "0" ) :("q7", "0", DROITE),

    #retour au milieu
    ("q8", VIDE ) :("q9", VIDE, GAUCHE),
    ("q8", "0" ) :("q8", "0", GAUCHE),
    ("q8", "1" ) :("q8", "1", GAUCHE),
    
    #retour jusquau debut en rementant le 1
    ("q9", VIDE ) :("q1", "1", DROITE),
    ("q9", "0" ) :("q9", "0", GAUCHE),
    ("q9", "1" ) :("q9", "1", GAUCHE),
}


mt = MachineTuring(regles=regles_ini, etat_final="q150000")
mt.demarrage(ruban=list("____"), position_tete=0, etat_initial="q1")

while True:
    mt.affiche()
    mt.etape()
    input("Appuyer sur \"Entrée\" pour continuer. Faire \"Ctrl + C\" pour arêter.")
