from ursina import *
from random import randint

class Tuyau(Entity):
    def __init__(self, x, y, img):
        super().__init__()
        self.model = 'quad'  # Modèle de base
        self.scale = (1, 7)  # Taille du tuyau
        self.color = color.green  # Couleur par défaut
        self.x = x  # Position initiale sur l'axe x
        self.y = y  # Position initiale sur l'axe y
        self.texture = img  # Texture à appliquer
        self.collider = 'box'  # Type de collision
        self.score_tag = True  # Permet de compter le score

def update():
    global offset, en_cours, n_frame, score, texte, vitesse_oiseau

    if en_cours:
        # Jouer un son périodiquement
        n_frame += 1
        if n_frame > 100:
            Audio('assets/Ursina-Engine_Flappy-Bird_assets_bird_chirp.mp3')
            n_frame = 0

        # Défilement de l'arrière-plan
        offset += time.dt * 0.2  # Réduit la vitesse de défilement
        setattr(bg, "texture_offset", (offset, 0))

        # Appliquer la gravité à l'oiseau
        oiseau.y += vitesse_oiseau * time.dt
        vitesse_oiseau -= gravite * time.dt

        # Déplacement des tuyaux
        for m in range(nombre):
            tuyaux_haut[m].x -= time.dt * 1.5  # Réduit la vitesse des tuyaux
            tuyaux_bas[m].x -= time.dt * 1.5

            # Réinitialisation des tuyaux quand ils sortent de l'écran
            if tuyaux_haut[m].x < -8:
                tuyaux_haut[m].x += 4 * nombre
                tuyaux_bas[m].x += 4 * nombre
                tuyaux_haut[m].score_tag = True

            # Augmenter le score si l'oiseau passe un tuyau
            if tuyaux_haut[m].x < oiseau.x and tuyaux_haut[m].score_tag:
                score += 1
                texte.text = f"Score : {score}"
                tuyaux_haut[m].score_tag = False

        # Vérifier les collisions
        hit_info = oiseau.intersects()
        if hit_info.hit or oiseau.y < -5 or oiseau.y > 5:
            en_cours = False
            invoke(Func(oiseau.shake, duration=2))  # Secouer l'oiseau
            invoke(Func(oiseau.fade_out, duration=3))  # Faire disparaître l'oiseau
            invoke(ecran_crash, delay=3)

def ecran_crash():
    global texte_restart
    texte_restart = Text(text='Crashé ! Appuyez sur R pour recommencer !', origin=(0, 0), scale=2, color=color.red)

def input(touche):
    global en_cours, vitesse_oiseau, texte_restart
    if en_cours:
        if touche == "space":
            vitesse_oiseau = 2.5  # Diminue la force de saut pour un meilleur contrôle
    if touche == "r" and not en_cours:
        redemarrer_jeu()
        if texte_restart:
            destroy(texte_restart)

def redemarrer_jeu():
    global en_cours, score, vitesse_oiseau, tuyaux_haut, tuyaux_bas, texte
    en_cours = True
    score = 0
    vitesse_oiseau = 0
    oiseau.y = 1.5
    oiseau.fade_in(duration=1)  # Faire réapparaître l'oiseau
    for m in range(nombre):
        tuyaux_haut[m].x = 6 + 4 * m
        tuyaux_bas[m].x = 6 + 4 * m
    texte.text = f"Score : {score}"

# Code principal
app = Ursina()

# Variables globales
offset = 0
en_cours = True
n_frame = 0
nombre = 5
x = 6
score = 0
gravite = 5  # Réduit la gravité pour ralentir la descente
vitesse_oiseau = 0

# Arrière-plan
bg = Entity(model='quad', scale=(20, 10), texture='assets/BG2.png', z=0.1)

# Oiseau
oiseau = Animation(
    'assets/bird',
    collider='box',
    scale=(1.3, 0.8),
    y=1.5
)

# Tuyaux
tuyaux_bas = [None] * nombre
tuyaux_bas[0] = Tuyau(x, -4, 'assets/pipe_bottom.png')

tuyaux_haut = [None] * nombre
tuyaux_haut[0] = Tuyau(x, -4 + 9, 'assets/pipe_top.png')

for m in range(1, nombre):
    x += 4
    y = -7 + randint(0, 50) / 10
    tuyaux_bas[m] = Tuyau(x, y, 'assets/pipe_bottom.png')
    tuyaux_haut[m] = Tuyau(x, y + 9, 'assets/pipe_top.png')

# Texte du score
texte = Text(text=f"Score : {score}", position=(-0.65, 0.4), origin=(0, 0), scale=2, color=color.yellow, background=True)

app.run()

      