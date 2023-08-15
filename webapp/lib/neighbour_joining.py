import copy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio.Phylo import BaseTree
from Bio import Phylo
import io
import base64
import tempfile
from pathlib import Path

class NewDistanceTreeConstructor(DistanceTreeConstructor):

    # Überschreibt die Methode nj von DistanceTreeConstructor
    def nj(self, distance_matrix:DistanceMatrix):
        if not isinstance(distance_matrix, DistanceMatrix):
            raise TypeError("Must provide a DistanceMatrix object.")

        # make a copy of the distance matrix to be used
        dm = copy.deepcopy(distance_matrix)
        # init terminal clades
        clades = [BaseTree.Clade(None, name) for name in dm.names]
        # init node distance
        # node_dist = [0] * len(dm)
        
        # init minimum index
        min_i = 0
        min_j = 0
        list_edited_min_dist = [] # Liste der minimalen Distanz in der bearbeiteten Distanzmatrix
        intermatrixes = []  # Liste der Dictionaries, die jeweils Infos der Zwischenmatrizen enthalten. Format (für len(dm) > 2)
                            # {'matrix':list[list], 'names':list, 'edited_matrix':list[list], 'edited_min_dist': float}

        # special cases for Minimum Alignment Matrices ###
        if len(dm) == 1:
            root = clades[0]

            return BaseTree.Tree(root, rooted=False)
        elif len(dm) == 2:
            # minimum distance will always be [1,0]
            min_i = 1
            min_j = 0

            clade1 = clades[min_i]
            clade2 = clades[min_j]
            clade1.branch_length = dm[min_i, min_j] / 2.0
            clade2.branch_length = dm[min_i, min_j] - clade1.branch_length

            inner_clade = BaseTree.Clade(None, f"({clade1.name},{clade2.name})")
            inner_clade.clades.append(clade1)
            inner_clade.clades.append(clade2)

            clades[0] = inner_clade
            root = clades[0]

            return {'tree':BaseTree.Tree(root, rooted=False),
                    'intermatrixes':{'names': dm.names, 'matrix': dm.matrix}}
        
        while len(dm) >= 2: # Startet immer mit len > 2
            node_dist = [0] * len(dm)
            
            if len(dm) == 2:
                intermatrixes.append({'names': dm.names, 'matrix': dm.matrix})
                break

            # calculate nodeDist (r)
            for i in range(len(dm)):
                node_dist[i] = 0
                for j in range(len(dm)):
                    node_dist[i] += dm[i, j]
                node_dist[i] = int(node_dist[i] / (len(dm) - 2))
            #print('check node_list', node_dist)
            
            # Addiert dm.names mit einer Zeile für r (node_dist)
            # und dm.matrix mit Werte in der node_dist-Liste
            # in ein Dictionary für eine Zwischenmatrizen
            names_with_node_dist = copy.deepcopy(dm.names)
            names_with_node_dist.append('r')
            matrix_with_node_dist = copy.deepcopy(dm.matrix)
            matrix_with_node_dist.append(copy.deepcopy(node_dist))

            intermatrixes.append({'names':names_with_node_dist,
                                'matrix':matrix_with_node_dist})    
            
            # find minimum distance pair
            edited_min_dist = dm[1, 0] - node_dist[1] - node_dist[0]
            min_i = 0
            min_j = 1
            
            # Erstellt bearbeitete Distanzmatrix
            edited_matrix = copy.deepcopy(dm)

            for i in range(1, len(dm)):
                for j in range(0, i):
                    # Korrigiert Werte in der bearbeiteten Distanzmatrix
                    # Speichert Wert in temp, um Minimum zu finden
                    edited_matrix[i,j] = temp = dm[i, j] - node_dist[i] - node_dist[j]

                    if edited_min_dist > temp:
                        edited_min_dist = temp
                        min_i = i
                        min_j = j
            # Addiert Min-Wert in die Liste der Minima                  
            list_edited_min_dist.append(edited_min_dist)

            # Addiert die bearbeitete Distanzmatrix in Dictionary
            intermatrixes[-1]['edited_matrix'] = edited_matrix

            # create clade
            clade1 = clades[min_i]
            clade2 = clades[min_j]

            inner_clade = BaseTree.Clade(None, f"({clade1.name},{clade2.name})")
            inner_clade.clades.append(clade1)
            inner_clade.clades.append(clade2)

            # assign branch length
            clade1.branch_length = (dm[min_i, min_j] + node_dist[min_i] - node_dist[min_j]) / 2.0
            clade2.branch_length = dm[min_i, min_j] - clade1.branch_length

            # update node list
            clades[min_j] = inner_clade
            del clades[min_i]

            # rebuild distance matrix,
            # set the distances of new node at the index of min_j
            for k in range(0, len(dm)):
                if k != min_i and k != min_j:
                    dm[min_j, k] = (dm[min_i, k] + dm[min_j, k] - dm[min_i, min_j]) / 2.0

            dm.names[min_j] = inner_clade.name
            del dm[min_i]

        # set the last clade as one of the child of the inner_clade
        root = None
        if clades[0] == inner_clade:
            clades[0].branch_length = 0
            clades[1].branch_length = dm[1, 0]
            clades[0].clades.append(clades[1])
            clades[0].name = f"({clades[0].name},{clades[1].name})"
            root = clades[0]
        else:
            clades[0].branch_length = dm[1, 0]
            clades[1].branch_length = 0
            clades[1].clades.append(clades[0])
            clades[1].name = f"({clades[0].name},{clades[1].name})"
            root = clades[1]

        # Addiert Minimum in dem entsprenchenden Dictionary der Zwischenmatrizen
        for i in range(len(list_edited_min_dist)):
            intermatrixes[i]['edited_min_dist'] = list_edited_min_dist[i]
        
        #for i in intermatrixes: print(i)

        return {'tree': BaseTree.Tree(root, rooted=True),
                'intermatrixes': intermatrixes}
    
# Erstellt Newwick String
def newwick(tree: BaseTree.Tree):
    
    def add(clade: BaseTree.Clade):
        if clade.is_terminal(): return f"{clade.name}:{round(clade.branch_length,4)}"
        
        clade1 = clade.clades[0]
        clade2 = clade.clades[1]
        
        if len(clade.clades) == 2:
            newwick = f"(({add(clade1)},{add(clade2)}):{round(clade.branch_length,4)})" 
        else: # == 3
            clade3 = clade.clades[2]
            newwick = f"({add(clade1)},{add(clade2)},{add(clade3)})"
        return newwick
    
    return add(tree.clade)


# Input Beispiel:
names = ['A', 'B', 'C', 'D','E']
matrix = [[0], 
          [5, 0], 
          [9, 10, 0], 
          [9,10,8, 0],
          [8,9,7,3,0]]

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
    constructor = NewDistanceTreeConstructor(method="nj")

    # Erstellt Neighbour Joining Baum und Zwischenmatrizen
    nj_res = constructor.nj(distance_matrix)
    tree = nj_res['tree']

    print(newwick(tree))
    # Erstellt Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    Phylo.draw(tree, axes=ax, do_show=False)  # Zeigt das Bild nicht

    # Erstelle eine temporäre Datei für den Plot
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_plot_file:
        plot_file_path = temp_plot_file.name
        fig.savefig(plot_file_path, format="png")
        temp_plot_path = Path(plot_file_path)

    plt.close(fig)  # Schließt den Plot

    # Liest den Plot aus der Datei ein und konvertiert ihn in Base64
    with open(plot_file_path, "rb") as plot_file:
        plot_data = plot_file.read()
    base64_plot = base64.b64encode(plot_data).decode()

    # Löscht die temporäre Plot-Datei
    temp_plot_path.unlink()

    return {'intermatrixes': nj_res['intermatrixes'],
            'newick': newwick(tree),
            'base64_plot': base64_plot(tree)}

get_results(names, matrix)


