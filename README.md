# Fossile Hunt




### Auteurs
---


Ahmed Hassayoune        <ahmed.hassayoune@epita.fr>
Diane Bellarbi Salah    <diane.bellarbi-salah@epita.fr>
Esteban Dulaurans       <esteban.dulaurans@epita.fr>
Etienne Reverchon       <etienne.reverchon@epita.fr>
Kerian Allaire          <kerian.allaire@epita.fr>
Nicolae Istratii        <nicolae.istratii@epita.fr>
Valentine Tcheou        <valentine.tcheou@epita.fr>

### Contexte 
---


Notre projet effectué dans la cadre de la CodeFest de la majeure IMAGE promotion 2025 consiste à développer un bac à sable virtuel en réalité augmentée, où les utilisateurs pourront chercher et découvrir des fossiles de manière interactive et éducative. En intégrant des technologies avancées de capture de mouvement, de rendu 3D en temps réel, et de simulation physique, nous visons à offrir une expérience immersive qui non seulement divertit, mais aussi éduque les utilisateurs sur l’évolution, l’histoire naturelle et l’importance de la conservation. Ce projet s’adresse à une variété d’acteurs, y compris les écoles, les musées, les chercheurs et le grand public, et se déploie dans divers lieux comme les salles de classe, les musées et les centres commerciaux.



### Instructions de déploiement 
---

Pour le déploiement il faut se munir d'un projecteur et d'une kinect à relier à votre machine
qui servira aussi d'écran.
La kinect ne peux pas détecter d'objet à moins de `50 cm` environ et à plus de `6 m`.

### Manuel utilisateur
---

#### Lancement 

- Premier lancement:
    `make build` puis `make run`
- Si l'image a deja été build:
    `make run`

#### Calibrage 

- Appuyer sur le `Commencer calibration`. 
- Régler les différents côtés du bac à sable.
- Fermer la fenêtre du calibrage.

#### Gestion de la partie

- Sélection un pré réglage ou customizer à la main 
- Appuyer sur `Commencer le jeu`.
- Appuyer sur `Finir la partie` pour intérrompre le jeu.
