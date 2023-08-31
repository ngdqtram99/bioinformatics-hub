class Node:
    def __init__(self):
        self.children = {} # die Schlüssels sind die Charaktere des nächsten Nodes, während die Werte ihres Node sind
        self.positions = [] # Position der mögliche Suffix mit diesem Charakter

    def is_end_node(self):
        return len(self.children) == 0
    
# Baut ein Suffix Trie aus einem Text auf
def build_suffix_trie(text: str, endchar: str):
    assert len(endchar) == 1
    text += endchar
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

def build_tree(trie: Node):
    root = trie
    def merge_node(node: Node):
        #print('node',node.children.keys(), node.positions)
        #print('--------------------------')
        
        if node.is_end_node() : return node

        current_node_children = node.children.copy()
        for i, (name_child, child) in enumerate(current_node_children.items()):
            
            if len(child.children) == 1:
                grandchild = child.children.popitem()
                new_name = name_child + grandchild[0] # + grandchild_name
                new_child = grandchild[1] # grandchild Node
                
                #print('b4 node.children',node.children.keys(),node.positions)

                node.children.pop(name_child)
                node.children[new_name] = new_child
                
                #print('aft node.children',node.children.keys(), node.positions,'\n')
        
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
    
    def subpattern_is_longer(name_node: str, subpattern: str):
        if len(name_node) >= len(subpattern): return False
        
        #print(' subpattern is longer', name_node, subpattern)
        
        return True 

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
    
    if not pattern: return node.positions

    if not node.is_end_node():
        for i, name in enumerate(node.children.keys()):
            if compare_char(name,pattern):
                #print('true')
                if subpattern_is_longer(name,pattern):
                    return find_hits(node.children[name],pattern[len(name):])
                else:
                    #print('check positions',node.children[name].positions)
                    return node.children[name].positions
            
import graphviz
# Erzeugt Digraph und speichert das Bild des Suffix-Tries in PNG-Datei
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
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}",style='filled',fillcolor='lightblue')
            # Normale Noden werden nicht gefärbt
            else:
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}")
            
            return current_id
            
        dot.node(name=f"{current_id}", label=' ')

        for edge_label, child_node in node.children.items():

            child_id = generate_dot(child_node,current_id)
            # Färbt die Kanten, die zur Position der Treffer leiten
            if has_hits_pos(child_node.positions):
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}", color='blue')
            else:
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}")
            
        return current_id
    
    generate_dot(trie, -1)

    # Speichert das Trie in PNG-Datei
    dot.render('suffix_tree',format='png',cleanup=True, view= True)

import base64
# Erzeugt ein Code des Bildes des Suffix-Tries
def create_image_base64(png_file_name):
    image = open(png_file_name, 'rb')
    image_64_decode = base64.b64encode(image.read()).decode()
    image.close()
    return(image_64_decode)

# Gibt das Ergebnis zurück
def get_result(text: str, pattern: str, endchar: str):
    trie = build_suffix_trie(text, endchar)
    tree = build_tree(trie)
    hits_pos = find_hits(tree,pattern)
    create_digraph(tree,hits_pos)
    
    return create_image_base64('suffix_tree.png')


# Beispiel
text = "banana"
pattern = "an"

get_result(text,pattern,"§")
# Sucht nach die Positionen der Treffer
'''
trie = build_suffix_trie(text, '§')
tree = build_tree(trie)
print_trie(tree)

all_hits = find_hits(tree, pattern)
print("Pattern hits at positions:", all_hits)

# Erzeugt Digraph und Image des Suffix-Tries
create_digraph(trie,all_hits)

# Erzeugt base64 Image
base64_image = create_image_base64('suffix_trie.png')
#print(base64_image)
'''