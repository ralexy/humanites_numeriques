import numpy
import json
from operator import attrgetter

# Source : https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    #printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]

def printDistances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()




##### Lecture dans notre fichier #####

# 1 Si on connaît pas le truc on l'ajoute
# 2 On mate la distance du +1 par rapport au n
# 3 Si elle est proche on créé un lien
# 4 On continue


intervenants_interm = []
intervenant = {}
intervenants = []


# Ouverture du fichier
f = open("individuals.txt", encoding='utf8')
num_lines = sum(1 for line in open("individuals.txt", encoding='utf8'))
i = 0


with open('individuals.txt', encoding='utf8') as file:
    lines = file.readlines()

# Levenstein première passe


while i < num_lines:


    temp = []

    intervenant1 = (lines[i].split('#'))[0]
    occurences1 = (lines[i].split('#'))[1]

    temp.append({"nom" : intervenant1, "nbr" : int(occurences1) })

    j = i+1
    
    if j < num_lines:
        intervenant2 = (lines[j].split('#'))[0]

    while levenshteinDistanceDP(intervenant1.lower(), intervenant2.lower()) < len(intervenant1.lower()) / 4 and j < num_lines :
        occurences2 = (lines[j].split('#'))[1]
        temp.append({"nom" : intervenant2, "nbr" : int(occurences2) })
        j += 1
        intervenant2 = (lines[j].split('#'))[0]


    # To sort the list in place...

    temp = sorted(temp, key= lambda x: x["nbr"], reverse=True)

    intervenants_interm.append(temp)

    i = j

for liste in intervenants_interm:
    intervenant["représentant"] = liste[0]
    if len(liste)>1:
        intervenant["alias"] = liste[1:len(liste)]
    else:
        intervenant["alias"] = []
    intervenant_copy = intervenant.copy()
    intervenants.append(intervenant_copy)


#print(intervenants)


# Levenstein deuxième passe

temp = []
intervenant = {}
already_treated = []

i = 0


for i in range(len(intervenants)):
    if intervenants[i] not in already_treated:

        already_treated.append(intervenants[i])

        intervenant1 = intervenants[i]["représentant"]
        nom_intervenant1 = intervenant1["nom"]
        alias1 = intervenants[i]["alias"]
        temp.append(intervenant1)
        [temp.append(elt) for elt in alias1]
        for j in range(i+1, len(intervenants_interm)):
            intervenant2 = intervenants[j]["représentant"]
            nom_intervenant2 = intervenant2["nom"]
            alias2 = intervenants[j]["alias"] 
            if levenshteinDistanceDP(nom_intervenant1.lower(), nom_intervenant2.lower()) < len(nom_intervenant1.lower()) / 4:
                print(nom_intervenant1, " ", nom_intervenant2)
                if intervenants[j] not in already_treated:
                    temp.append(intervenant2)
                    [temp.append(elt) for elt in alias2]
                    already_treated.append(intervenants[j])
                
        temp = sorted(temp, key= lambda x: x["nbr"], reverse=True)
        intervenant[i] = {}
        intervenant[i]["représentant"] = temp[0]
        intervenant[i]["alias"] = (temp[1:len(temp)])

    #print(temp, "\n")
    #print(intervenant, "\n")
    temp = []
    i += 1

            #intervenants_interm[j] = {"nom" : "", "nbr" : "" }


with open("intervenants.json", 'w', encoding='utf8') as f:
    json.dump(intervenant, f)

   

f.close()
