comparsion = 0 #Anzahl der Vergleiche

def get_result(pattern, sequence):
    global comparsion
    comparsion = 0 # Null setzen, weil der Wert von comparsion nach einem Vergleich geändert ist. (!= 0)
    
    length_pattern = len(pattern)
    length_sequence = len(sequence)
    result = list() #Liste der Positionen der Treffer

    # Falls Pattern oder Sequenz ist nicht eingegeben
    if length_pattern == 0 or length_sequence == 0:
        return {'comparsions_count':0,
                'result':[]}

    def match(substring):

        for i in range(length_pattern):
            global comparsion 
            comparsion += 1
            if (pattern[i] != substring[i]): return False
        return True
    
    for pos in range(length_sequence-length_pattern+1):
        substring = sequence[pos:pos+length_pattern] #Leserahme im String, dessen Länge dieselbe des Patterns entspricht

        if match(substring):
            result.append(pos)
    
    return {'comparsions_count':comparsion,
            'results':result}

res = get_result("","ATA")
print(res)
#res2 = get_result("ATC","ATCAATC")
#print(res2)