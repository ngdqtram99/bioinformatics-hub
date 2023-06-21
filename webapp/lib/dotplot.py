
def get_result(seq1, seq2):

    length1 = len(seq1)
    length2 = len(seq2)
    result = [[0] * (length1 + 1) for _ in range(length2 + 1)]

    # prepare the result list for output
    result[0][0] = ','
    result[0][1:] = [*seq1]
    dum = 1
    for x in [*seq2]:
        result[dum][0] = x
        dum = dum + 1

    # iterate trough the sequences and search for matches
    for i in range(length1):
        for j in range(length2):
            if seq1[i] == seq2[j]:
                # write matches with 1 in result
                result[i+1][j+1] = 1

    return result



