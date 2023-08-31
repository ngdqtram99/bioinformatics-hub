# Node(childeren, positions) im Suffix-Baum
class Node:
    def __init__(self):
        self.children = {} # die Schlüssels sind die Charaktere des nächsten Nodes, während die Werte ihres Node sind
        self.positions = [] # Position der mögliche Suffix mit diesem Charakter

    def is_end_node(self):
        return len(self.children) == 0
    
# Baut ein Suffix Trie aus einem Text auf (ähnlich Code wie Aufbau des Suffix-Trie aber mit Node statt TrieNode)
def build_suffix_trie(text: str, endchar: str):
    assert len(endchar) == 1 # Prüft, das Endcharakter nur 1 Buchstabe enthält
    
    text += endchar # Addiert Endcharakter am Ende des Textes
    root = Node()

    for i in range(len(text)):
        node = root
        for j in range(i, len(text)): # Suffix von der Stelle i
            char = text[j]
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
            node.positions.append(i)

    return root

# Baut einen Suffix-Baum von einem gabauten Suffix-Trie auf
def build_tree(trie: Node):

    # Fügt die Noden, die nur ein Kind hat, zusammen
    def merge_node(node: Node):
        #print('node',node.children.keys(), node.positions)
        #print('--------------------------')
        
        # Endbedingung, wenn es das Endnode trifft
        if node.is_end_node() : return node

        # Kopiert das Dictionary von node.children, weil node.children in der for-Schleife geändert wird und danach einen Fehler trifft
        current_node_children = node.children.copy()
        for child_name, child in current_node_children.items():
            
            # Fügt Kind- und Enkel-Node zusammen wenn das Kind-Node nur ein Enkel-Node enthält 
            if len(child.children) == 1:
                grandchild = child.children.popitem() # Variable: Namen und des Nodes des Enkel-Nodes
                new_name = child_name + grandchild[0] # Neuer Name von Kind-Node: child_name + grandchild_name
                new_child = grandchild[1] # Enkel-Node
                
                #print('b4 node.children',node.children.keys(),node.positions)

                # Löscht das alte Kind-Node und fügt das neues Kind-Node hinzu
                node.children.pop(child_name) 
                node.children[new_name] = new_child
                
                #print('aft node.children',node.children.keys(), node.positions,'\n')
        
        # Falls kein Kind-Node, das bearbeitet werden kann
        if node.children == current_node_children :
            for name, child in node.children.items():
                node.children[name] = merge_node(child)
            return node
        else: 
            return merge_node(node)
        
    merge_node(trie)
    return trie


# Sucht nach Treffer mit Suffix Trie
def find_hits(node: Node, pattern: str):
    # Subpattern: Wenn einen Teil des Patterns im Baum gefunden ist, wird der Rest weiter gesucht. Er wird als Subpattern genannt  
    # Vergleicht die Längen des Subpatterns und des Namen des Nodes  
    def subpattern_is_longer(name_node: str, subpattern: str):
        if len(name_node) >= len(subpattern): return False
        
        #print(' subpattern is longer', name_node, subpattern)
        
        return True 

    # Vergleicht den Subpattern und den Namen des Nodes
    def compare_char(name_node: str, subpattern: str):
        if not subpattern_is_longer(name_node,subpattern):
            
            #print('check in compare char', name_node,subpattern)
            
            for i in range(len(subpattern)):
                if subpattern[i] != name_node[i]: return False
        else:
            for j in range(len(name_node)):
                if name_node[j] != subpattern[j]: return False
        
        #print('compare_char is true', name_node,subpattern)
        
        return True
    
    # Falls der Pattern leer ist
    if not pattern: return node.positions

    if not node.is_end_node():
        for name in node.children.keys():
            if compare_char(name,pattern):
                #print('true')
                if subpattern_is_longer(name,pattern):
                    return find_hits(node.children[name],pattern[len(name):])
                else:
                    #print('check positions',node.children[name].positions)
                    return node.children[name].positions
        return []
            
import graphviz
# Erzeugt Digraph und gibt es zurück
def create_digraph(trie: Node, hits_pos:list):
    dot = graphviz.Digraph()
    node_id = 0
    
    # Prüft, ob die Liste der Positionen eines Nodes die selben der Treffer enthält  
    def has_hits_pos(positions: list):
        for i in positions:
            for j in hits_pos:
                if i == j: 
                    return True
        return False

    # Addiert Noden und Kanten in Digraph
    def generate_dot(node: Node, parent_id: int):
        nonlocal node_id
        current_id = node_id
        node_id += 1
        if node.is_end_node():
            # Färbt das Node, dessen Position-Liste die Positionen der Treffer enthält
            if has_hits_pos(node.positions):
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}",style='filled',fillcolor='#c7dff8')
            # Normale Noden werden nicht gefärbt
            else:
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}")
            
            return current_id
            
        dot.node(name=f"{current_id}", label=' ')

        for edge_label, child_node in node.children.items():

            child_id = generate_dot(child_node,current_id)
            # Färbt die Kanten, die zur Position der Treffer leiten
            if has_hits_pos(child_node.positions):
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}", color='#007bff')
            else:
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}")
            
        return current_id
    
    generate_dot(trie, -1)

    return dot

'''import base64
from pathlib import Path
# Erzeugt ein Code des Bildes des Suffix-Tries
def create_image_base64(png_file_name):
    tem_png_file = Path(png_file_name)

    image = open(png_file_name, 'rb')
    image_64_decode = base64.b64encode(image.read()).decode()
    image.close()

    tem_png_file.unlink() # Löscht die PNG-Datei nach dem Speichern in base64
    return(image_64_decode)'''

import base64
# Gibt das Ergebnis zurück
def get_results(text: str, pattern: str, endchar: str):
    trie = build_suffix_trie(text, endchar)
    tree = build_tree(trie)
    hits_pos = find_hits(tree,pattern)
    dot = create_digraph(tree,hits_pos)
    found = None if len(pattern) == 0 else (True if len(hits_pos) > 0 else False)
    png_bytes = dot.pipe(format='png')

    return {'svg': dot.pipe(format='svg').decode(),
            'png': base64.b64encode(png_bytes).decode("utf-8"),
            'found': found}


# Beispiel
text = "banana"
pattern = "an"

res = get_results(text,pattern,"§")
#print(res['png'])