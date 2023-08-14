import copy
from matplotlib import pyplot as plt
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio.Phylo import BaseTree
from Bio import Phylo
import io
import base64

class NewDistanceTreeConstructor(DistanceTreeConstructor):
    def upgma(self, distance_matrix: DistanceMatrix):
        if not isinstance(distance_matrix, DistanceMatrix):
                raise TypeError("Es muss ein DistanceMatrix-Object sein.")

        # Erstellt eine Kopie der Distanzmatrix
        dm = copy.deepcopy(distance_matrix)

        # Initialisierung
        # Node-Liste
        clades = [BaseTree.Clade(None, name) for name in dm.names]
        # Minimaler Index
        min_i = 0
        min_j = 0
        intermatrixes = [[dm.names,dm.matrix]] # Liste von Liste von Infos der Zwischenmatrix in Format: [names, matrix, min_dist]
        inter_min_values = []

        while len(dm) > 1:
            min_dist = dm[1, 0] # die erste Wert der Distanzmatrix (von oben links)
            # Findet den minimalen Index
            for i in range(1, len(dm)):
                for j in range(i):
                    if min_dist >= dm[i, j]:  #####
                        min_dist = dm[i, j]
                        min_i = i
                        min_j = j
            
            '''print(min_dist)
            print(min_i,min_j)'''
            # Speichert Min-Wert
            inter_min_values.append(min_dist)

            # Erstellt Obenclade
            clade1 = clades[min_i]
            clade2 = clades[min_j]
            inner_clade = BaseTree.Clade(None, f"({clade1.name}{clade2.name})") # zB. A und B -> (AB); (AB) und C -> ((AB)C) 
            inner_clade.clades.append(clade1)
            inner_clade.clades.append(clade2)

            # Einträgt die Länge des Branches (branch_length)
            if clade1.is_terminal():
                clade1.branch_length = min_dist / 2
            else:
                clade1.branch_length = min_dist / 2 - self._height_of(clade1)

            if clade2.is_terminal():
                clade2.branch_length = min_dist / 2
            else:
                clade2.branch_length = min_dist / 2 - self._height_of(clade2)

            # Aktualisiert die Node-Liste
            clades[min_j] = inner_clade
            del clades[min_i]


            # Baut die Distanzmatrix um
            # Setzt die Distanzen des neuen Node im Index von min_j
            for k in range(0, len(dm)):
                if k != min_i and k != min_j:
                    i = count_subclades(inner_clade.clades[0])
                    j = count_subclades(inner_clade.clades[1])
                    dm[min_j, k] = (dm[min_i, k]*i + dm[min_j, k]*j) / (i+j)

            dm.names[min_j] = inner_clade.name
            del dm[min_i]
            #for i in dm.matrix: print(i)

            # Speichert Zwischenmatrix
            intermatrixes.append([dm.names,dm.matrix])
            
        inner_clade.branch_length = 0 # Wurzel

        # Addiert Min-Wert in to intermatrixes
        for i in range(len(inter_min_values)):
            intermatrixes[i].append(inter_min_values[i])

        return {'tree':BaseTree.Tree(inner_clade),
                'intermatrixes': intermatrixes}
    
# Erstellt Newwick String
def newwick(tree : BaseTree.Tree):
    
    def add(clade: BaseTree.Clade):
        if clade.is_terminal(): return f"{clade.name}:{clade.branch_length}"

        newwick = ""
        clade1 = clade.clades[0]
        clade2 = clade.clades[1]
        newwick = f"(({add(clade1)},{add(clade2)}):{round(clade.branch_length,4)})"
        return newwick
    
    return add(tree.clade)[2:-4] # Löscht die Wurzel (root)

# Zählt die Subclades von einem Clade
def count_subclades(clade: BaseTree.Clade):
    
    if clade.is_terminal(): return 1
    
    count = 0
    for c in clade.clades:
        count += count_subclades(c)

    return count

# Neue Methode UPGMA

'''# Überschreibt UPGMA von DistanceTreeConstructor 
DistanceTreeConstructor.upgma = upgma    
'''
# Input Beispiel:
names = ['Alpha', 'Beta', 'Gamma', 'Delta']
matrix = [[0], 
          [1, 0], 
          [2, 3, 0], 
          [4, 5, 6, 0]]

'''def base64_plot(tree : BaseTree.Tree):
    # Erstellt Plot
    fig, ax = plt.subplot(figsize=(10,10))
    Phylo.draw(tree,axes=
    ax, do_show=False) # Zeigt das Bild nicht

    # Speichert Plot in Buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format= "png")
    buffer.seek(0)

    # Koddiert Buffer in base64
    base64_plot = base64.b64decode(buffer.read()).decode()

    # Schließt alle
    plt.close()
    buffer.close()

    return base64_plot
'''
def get_results(names: list, matrix: list):
    # Erstellt Distanzmatrix aus Input
    distance_matrix = DistanceMatrix(names,matrix)
    
    # Erstellt Constructor
    constructor = NewDistanceTreeConstructor(method="upgma")

    # Erstellt UPGMA Baum und Zwischenmatrizen
    upgma_res = constructor.upgma(distance_matrix)
    tree = upgma_res['tree']

    # Erstellt Plot
    fig, ax = plt.subplots(figsize=(10,10))
    Phylo.draw(tree,axes=ax, do_show=False) # Zeigt das Bild nicht

    # Speichert Plot in Buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format= "png")
    buffer.seek(0)

    # Koddiert Buffer in base64
    base64_plot = base64.b64decode(buffer.read()).decode()

    # Schließt alle
    plt.close()
    buffer.close()

    return {'intermatrixes': upgma_res['intermatrixes'],
            'newwick': newwick(tree),
            'tree_plot': base64_plot(tree)}

get_results(names, matrix)


