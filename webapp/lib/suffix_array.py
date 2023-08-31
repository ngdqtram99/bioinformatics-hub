# Suffix(suffix, position)
class Suffix:
    def __init__(self, suffix: str, position: int):
        self.suffix = suffix # Name des Suffixes
        self.position = position

    def __str__(self):
        return f"Suffix: {self.suffix} at position {self.position}"

# Baut ein Suffix-Array 
def build_suffix_array(sequence: str):
    suffix_array = [] # Suffix-Array

    # Addiert die Suffixe der Sequenz in den Suffix-Array
    for i in range(len(sequence)):
        suffix_array.append(Suffix(sequence[i:],i))
    
    # Sortiert den Suffix-Array
    suffix_array.sort(key = lambda s : s.suffix)
    
    #for i,s in enumerate(suffix_array): print(i,s.suffix,s.position)
    
    return suffix_array

# Beispiel
sa = build_suffix_array("ananas")

# Umformatiert den Suffix-Array
def format_suffix_array(suffix_array: list[Suffix]):
    sa = [['','Suffix','Position']]

    for i,s in enumerate(suffix_array):
        sa.append([i,s.suffix,s.position])
    
    return sa
# Beispiel
formated_sa = format_suffix_array(sa)
#for i in formated_sa: print(i)

# Sucht nach ein Pattern in einer Sequenz und gibt die wahrscheinliche Position des Treffers im Suffix-Array
def suffix_array_search(pattern: str, sequence: str): 
    sa = build_suffix_array(sequence) #suffix_array
    len_seq = len(sequence)
    if pattern <= sa[0].suffix: return 0
    if pattern > sa[len_seq-1].suffix: return len_seq

    #Binärsuche
    links = 0
    rechts = len_seq-1

    while rechts - links > 1:
        mitte = int(abs((rechts + links)/2))
        if pattern <= sa[mitte].suffix: rechts = mitte
        else: links = mitte
        
    return rechts # Position des Suffixes, der wahrscheinlich den Treffer beinhaltet

# Beispiel
hit = suffix_array_search('nn','anannas')
#print(hit)

# Gibt die Suffix-Array in der definierten Format und einen boolean-Wert, ob der Pattern gefunden ist, zurück
def get_results(pattern: str, text: str):
    sa = build_suffix_array(text)
    sa_search = suffix_array_search(pattern,text)
    formated_sa = format_suffix_array(sa)

    if len(sa) == sa_search: 
        #print("No pattern in the sequence")
        return {'suffix_array': formated_sa, 
                'found': False} # Es gibt unbedingt kein Pattern in der Sequenz
    

    suffix = sa[sa_search].suffix
    for i in range(len(pattern)):
        if pattern[i] != suffix[i] or i >= len(suffix): 
            #print("No pattern in the sequence")
            return {'suffix_array': formated_sa, 
                'found': False}
        
    #print("Pattern in the sequence")
    return {'suffix_array': formated_sa, 
            'found': True if len(pattern) > 0 else None}

# Beispiel
res = get_results('ana','ananas')
#print(res['found'])

'''
Ergebnis
['', 'Suffix', 'Position']
[0, 'ananas', 0]
[1, 'anas', 2]
[2, 'as', 4]
[3, 'nanas', 1]
[4, 'nas', 3]
[5, 's', 5]
True
'''