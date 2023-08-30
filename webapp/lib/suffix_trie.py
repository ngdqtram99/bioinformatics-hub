class TrieNode:
    def __init__(self):
        self.children = {} # die Schlüssels sind die Charaktere des nächsten Nodes, während die Werte ihres Node sind
        self.positions = [] # Position der mögliche Suffix mit diesem Charakter

    def is_end_node(self):
        return len(self.children) == 0
    
# Baut ein Suffix Trie aus einem Text auf
def build_suffix_trie(text: str, endchar: str):
    assert len(endchar) == 1
    text += endchar
    root = TrieNode()

    for i in range(len(text)):
        node = root
        for j in range(i, len(text)): # Suffix von der Stelle i
            char = text[j]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.positions.append(i)

    return root

# Sucht nach Treffer mit Suffix Trie
def find_hits(node: TrieNode, pattern: str):
    if not pattern:
        return node.positions
    
    char = pattern[0]
    if char in node.children:
        return find_hits(node.children[char], pattern[1:])
    else:
        return []
    
import graphviz
# Erzeugt Digraph und speichert das Bild des Suffix-Tries in PNG-Datei
def create_digraph(trie: TrieNode, hits_pos:list):
    dot = graphviz.Digraph()
    node_id = 0
    
    # Prüft, ob die Liste der Positionen eines Nodes die selben der Treffer enthält  
    def has_hits_pos(positions: list):
        for i in positions:
            for j in hits_pos:
                if i == j: 
                    print('positions', positions)
                    return True
        return False

    # Addiert Noden und Kanten in Digraph
    def generate_dot(node: TrieNode, parent_id: int):
        nonlocal node_id
        current_id = node_id
        node_id += 1
        
        if node.is_end_node():

            if has_hits_pos(node.positions):
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}",style='filled',fillcolor='lightblue')
            else:
                dot.node(name=f"{current_id}",label=f"{node.positions[-1]}")
            
            return current_id
            
        dot.node(name=f"{current_id}", label=' ')

        for edge_label, child_node in node.children.items():

            child_id = generate_dot(child_node,current_id)
            if has_hits_pos(child_node.positions):
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}", color='blue')
            else:
                dot.edge(f"{current_id}", f"{child_id}",label = f"{edge_label}")
            
        return current_id
    
    generate_dot(trie, -1)
    dot.render('suffix_trie',format='png',cleanup=True, view= True)

import base64
# Erzeugt ein Code des Bildes des Suffix-Tries
def create_image_base64(png_file_name):
    image = open(png_file_name, 'rb')
    image_64_decode = base64.b64encode(image.read()).decode()
    image.close()
    return(image_64_decode)

# Gibt das Ergebnis zurück
def get_result(text: str, pattern: str, endchar: str):
    trie = build_suffix_trie(text)
    hits_pos = find_hits(trie,pattern)
    create_digraph(trie,hits_pos)
    
    return create_image_base64('suffix_trie.png')

# Beispiel
text = "banana"
pattern = "na"

# Sucht nach die Positionen der Treffer
trie = build_suffix_trie(text)
all_hits = find_hits(trie, pattern)
#print("Pattern hits at positions:", all_hits)

# Erzeugt Digraph und Image des Suffix-Tries
create_digraph(trie,all_hits)

# Erzeugt base64 Image
base64_image = create_image_base64('suffix_trie.png')
#print(base64_image)