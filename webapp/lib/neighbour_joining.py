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

        # Kopiert Distanzmatrix
        dm = copy.deepcopy(distance_matrix)
        # Initialisierung:
        # Knoten-Liste
        clades = [BaseTree.Clade(None, name) for name in dm.names]
        # Minimaler Index
        min_i = 0
        min_j = 0
        # Nötige Liste
        list_edited_min_dist = [] # Liste der minimalen Distanz in der bearbeiteten Distanzmatrix
        intermatrixes = []  # Liste der Dictionaries, die jeweils Infos der Zwischenmatrizen enthalten. Format (für len(dm) > 2)
                            # {'matrix':list[list], 'names':list, 'edited_matrix':list[list], 'edited_min_dist': float}

        # Besondere Fälle
        if len(dm) == 1: # wenn nur eine Sequenz eingegeben ist
            root = clades[0]

            return BaseTree.Tree(root, rooted=False)
        elif len(dm) == 2: # wenn nur 2 Sequenzen eingegeben sind
            # Die minimale Distanz ist immer [1,0]
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
            # Liste der Netto Divergenzen. Die dienen als die durchschnitten Distanzen
            # von jedem Taxon zu jedem anderen
            node_dist = [0] * len(dm)
            
            if len(dm) == 2:
                intermatrixes.append({'names': dm.names, 'matrix': dm.matrix})
                #print('inner_clade',inner_clade)
                break

            # Berechnet Netto Divergenzen
            for i in range(len(dm)):
                node_dist[i] = 0
                for j in range(len(dm)):
                    node_dist[i] += dm[i, j]
                node_dist[i] = int(node_dist[i] / (len(dm) - 2))
            #print('check node_list', node_dist)
            
            # Addiert dm.names mit einer Zeile für Netto Divergenzen
            # und dm.matrix mit Werte in der node_dist-Liste
            # in ein Dictionary für eine Zwischenmatrizen
            names_with_node_dist = copy.deepcopy(dm.names)
            names_with_node_dist.append('r') # Die Netto Divergenz ist r benannt
            matrix_with_node_dist = copy.deepcopy(dm.matrix)
            matrix_with_node_dist.append(copy.deepcopy(node_dist))

            intermatrixes.append({'names':names_with_node_dist,
                                'matrix':matrix_with_node_dist})    
            
            # Findet die minimale Distanz 
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
            intermatrixes[-1]['edited_matrix'] = edited_matrix.matrix

            # Erstellt Knoten
            clade1 = clades[min_i]
            clade2 = clades[min_j]

            inner_clade = BaseTree.Clade(None, f"({clade1.name},{clade2.name})")
            inner_clade.clades.append(clade1)
            inner_clade.clades.append(clade2)

            # Berechnet die Länge der Branchen
            clade1.branch_length = (dm[min_i, min_j] + node_dist[min_i] - node_dist[min_j]) / 2.0
            clade2.branch_length = dm[min_i, min_j] - clade1.branch_length

            # Aktualisiert die Knoten-Liste
            clades[min_j] = inner_clade
            del clades[min_i]

            # Baut die Distanzmatrix um
            # Setzt die Distanzen der neuen Knoten in dem Index von min_j
            for k in range(0, len(dm)):
                if k != min_i and k != min_j:
                    dm[min_j, k] = (dm[min_i, k] + dm[min_j, k] - dm[min_i, min_j]) / 2.0

            dm.names[min_j] = inner_clade.name
            del dm[min_i]

        # Setzt die letzte Knote als ein Kind der inner_clade
        # Setzt den Wurzel
        root = None
        #print('clades', clades)
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

        #print('check root in nj',root)
        
        # Addiert Minimum in dem entsprenchenden Dictionary der Zwischenmatrizen
        for i in range(len(list_edited_min_dist)):
            intermatrixes[i]['edited_min_dist'] = list_edited_min_dist[i]
        
        #for i in intermatrixes: print(i)

        return {'tree': BaseTree.Tree(root, rooted=True),
                'intermatrixes': intermatrixes}
    
# Erstellt Newwick String
def newwick(tree: BaseTree.Tree):
    #print('check root in newwick',tree.root.clades)
    
    def add(clade: BaseTree.Clade):
        if clade.is_terminal(): return f"{clade.name}:{round(clade.branch_length,4)}"
        
        clade1 = clade.clades[0]
        clade2 = clade.clades[1]
        
        if len(clade.clades) == 2:
            newwick = f"(({add(clade1)},{add(clade2)}):{round(clade.branch_length,4)})" 
        else: # == 3
            clade3 = clade.clades[2]
            newwick = f"((({add(clade1)},{add(clade2)}):0),{add(clade3)})"
        
        #print('check newwick in newwick',newwick)
        return newwick
    
    return add(tree.clade)


# Input Beispiel:
names = ['A', 'B', 'C', 'D','E']
matrix = [[0], 
          [5, 0], 
          [9, 10, 0], 
          [9,10,18, 0],
          [8,9,17,3,0]]

def get_results(names: list, matrix: list):
    # Erstellt Distanzmatrix aus Input
    distance_matrix = DistanceMatrix(names,matrix)
    
    # Erstellt Constructor
    constructor = NewDistanceTreeConstructor(method="nj")

    # Erstellt Neighbour Joining Baum und Zwischenmatrizen
    nj_res = constructor.nj(distance_matrix)
    tree = nj_res['tree']

    # Erstellt Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    Phylo.draw(tree, axes=ax, do_show=False)  # Zeigt das Bild nicht

    # Erstelle eine temporäre Datei für den Plot
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_plot_file:
        plot_file_path = temp_plot_file.name
        fig.savefig(plot_file_path, format="png")
        temp_plot_path = Path(plot_file_path)
    svg_io = io.StringIO()
    fig.savefig(svg_io, format="svg")
    svg_content = svg_io.getvalue()
    svg_io.close()

    plt.close(fig)  # Schließt den Plot

    # Liest den Plot aus der Datei ein und konvertiert ihn in Base64
    with open(plot_file_path, "rb") as plot_file:
        plot_data = plot_file.read()
    base64_plot = base64.b64encode(plot_data).decode()

    # Löscht die temporäre Plot-Datei
    temp_plot_path.unlink()

    return {'intermatrixes': nj_res['intermatrixes'],
            'newick': newwick(tree),
            'base64_plot': base64_plot,
            'svg' : svg_content}

get_results(names, matrix)


