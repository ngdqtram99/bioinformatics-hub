comparsion = 0 #Anzahl der Vergleiche

def get_result(pattern, sequence, backward = True):
    global comparsion
    comparsion = 0 #Setzen den Wert immer 0, falls er nach einer vorherigen Suche geändert ist
    shift_table = dict()
    length_pattern = len(pattern)
    length_sequence = len(sequence)
    results = list() #Liste der Positionen der Treffer

    def match(substring):
        global comparsion
        if backward:
            for i in range(length_pattern-1,-1,-1):
                comparsion += 1
                if (pattern[i] != substring[i]): return False
        else:
            for i in range(length_pattern-1):
                comparsion += 1
                if (pattern[i] != substring[i]): return False
        return True

    #Bilden die Shift-Tabelle mit nur Charaktere (Buchstaben) im Pattern, außer den letzten
    for i in range(length_pattern-1): #Nehmen alle Indexe des Patterns außer den letzten
        shift_table[pattern[i]] = length_pattern-i-1 #Weil i von 0...length_pattern-2 ist

    pos = 0
    while pos < length_sequence-length_pattern+1:
        substring = sequence[pos:pos+length_pattern] #Leserahme
        if match(substring): results.append(pos)

        if(substring[length_pattern-1]) in shift_table.keys():
            pos += shift_table[substring[length_pattern-1]]
        else: pos += length_pattern
    
    return {'comparsions_count':comparsion,
            'results': results}