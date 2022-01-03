from random import randint, sample
import math
from matplotlib import pyplot as plt


class Ville:
    """
    Une ville est represente par une coordonnee x, y et un identifiant unique

    """
    n = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ident = Ville.n
        Ville.n += 1


def distance(v1, v2):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)


def tour_cost(tour):
    cpt = 0
    for i in range(-1, len(tour) - 1):
        cpt += distance(tour[i], tour[i + 1])
    return cpt

nbr_ville = 30

villes = [Ville(randint(0, 1000), randint(0, 1000)) for _ in range(nbr_ville)]
villes = [Ville(0,5),Ville(1,1),Ville(3,3),Ville(7,3),Ville(6,5),Ville(6,0)]

def Prim(villes,villes_visited,x):
    val=0
    Marked=[x]
    Cities=[v for v in villes if v not in villes_visited] #ENLEVER LES VILLES DEJA VISITEES
    while(len(Marked)!=len(Cities)):
        L=[]
        min=2147483647
        noeud_choisi=None
        for i in range(len(Marked)):
            noeud=Marked[i]
            for v in Cities:
                if v in Marked : #IGNOGER LES SOMMETS MARQUES
                    continue
                else:
                    if(distance(noeud,v)<min):
                        noeud_choisi=v
                        min=distance(noeud,v)
        if noeud_choisi!=None:
            print(noeud_choisi.x," ",noeud_choisi.y)
            val+=min
            Marked.append(noeud_choisi)
    return val

print(Prim(villes,[],villes[1]))

########################
# ALGO A star #
########################
def Astar():
    return



########################
# ALGO DE LA PANTHERE  #
########################

class Panthere:

    def __init__(self, villes):

        self.tour = sample(villes, len(villes))

    def placeAfter(self, villeA, villeB):
        a = self.chercher(villeA)
        b = self.chercher(villeB)
        l = []
        for i in range(len(self.tour)):
            if i != a and i != b:
                l.append(self.tour[i])
            elif i == a:
                l.append(self.tour[i])
                l.append(self.tour[b])

        self.tour = l

    def chercher(self, n):
        for i in range(len(self.tour)):
            if self.tour[i].ident == n:
                return i

        print("ville non trouvee")

    def grow(self, f):

        nbVoisins = 5

        l = []

        for _ in range(nbVoisins):
            l.append(permuter(self.tour, 2))

        self.tour = min(l + [self.tour], key=tour_cost)


def permuter(l, nbr):
    l2 = l[:]
    for _ in range(nbr):
        a = randint(0, len(l) - 1)
        b = randint(0, len(l) - 1)
        l2[a], l2[b] = l2[b], l2[a]
    return l2


def teach_hunting(pop, best):
    coefficient = 0.10
    numbers = int(len(best.tour) * coefficient)

    for panthere in pop:
        if panthere != best:
            for _ in range(numbers):
                a = randint(0, len(best.tour) - 1)
                b = (a + 1) % len(best.tour)

                panthere.placeAfter(best.tour[a].ident, best.tour[b].ident)


# test d'une solution aleatoire
first = Panthere(villes)
print("random solution", tour_cost(first.tour))

pop_size = 40
iterations = 100
mature = 20
objective_function = lambda x: tour_cost(x.tour)
population = [Panthere(villes) for _ in range(pop_size)]
print("best without iteration", objective_function(min(population, key=objective_function)))
first = min(population, key=objective_function)
for _ in range(iterations):
    for panthere in population:
        for _ in range(mature):
            panthere.grow(objective_function)

    best_panthere = min(population, key=objective_function)
    teach_hunting(population, best_panthere)
    population = sorted(population, key=objective_function)[:pop_size // 2]

    for i in range(pop_size // 2):
        p = Panthere(villes)
        p.tour = permuter(population[0].tour, 10)
        teach_hunting([p], population[0])
        population.append(p)

best = population[0]

print("solution panthereuse", objective_function(best))

lines = []

for i in range(-1, len(best.tour) - 1):
    x = [best.tour[i].x, best.tour[i + 1].x]
    y = [best.tour[i].y, best.tour[i + 1].y]
    lines.append([x, y])

plt.figure("Panthere")
plt.plot([t.x for t in best.tour], [t.y for t in best.tour], 'ro')
plt.plot([t[0] for t in lines], [t[1] for t in lines])
plt.axis([0, 1000, 0, 1000])

lines2 = []

for i in range(-1, len(first.tour) - 1):
    x = [first.tour[i].x, first.tour[i + 1].x]
    y = [first.tour[i].y, first.tour[i + 1].y]
    lines2.append([x, y])

plt.figure("random")
plt.plot([t.x for t in best.tour], [t.y for t in best.tour], 'ro')
plt.plot([t[0] for t in lines2], [t[1] for t in lines2])
plt.axis([0, 1000, 0, 1000])
plt.show()