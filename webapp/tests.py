from django.test import TestCase
from .lib import dotplot, simple_search, horspool, glocal_alignment, needleman_wunsch, smith_waterman, viterbi, neighbour_joining, suffix_array
from .forms import DotplotForm, GlocalAlignmentForm, NeedlemanWunschForm, SmithWatermanForm, ViterbiForm, SuffixTreeTrieForm, OverlapForm, UpgmaNjForm


class TestDotplot(TestCase):

    def test_get_result(self):
        # Fall 1: Sequenzen mit der gleichen Länge
        res1 = [[' ', 'A', 'T', 'A', 'C'],
                ['A', 1, 0, 1, 0],
                ['C', 0, 0, 0, 1],
                ['C', 0, 0, 0, 1],
                ['A', 1, 0, 1, 0]]
        self.assertEqual(dotplot.get_result('ATAC', 'ACCA'), res1)

        # Fall 2: Sequenzen mit unterschiedlicher Längen
        res2 = [[' ', 'A', 'T', 'A', 'C'],
                ['A', 1, 0, 1, 0],
                ['C', 0, 0, 0, 1],
                ['C', 0, 0, 0, 1]]
        self.assertEqual(dotplot.get_result('ATAC', 'ACC'), res2)

        # Fall 3: Eine Sequenz fehlt
        res3 = [[' ', 'A', 'A', 'A', 'C']]
        self.assertEqual(dotplot.get_result('AAAC', ''), res3)

        res4 = [[' '],
                ['C'],
                ['C'],
                ['G']]
        self.assertEqual(dotplot.get_result('', 'CCG'), res4)

        # Fall 4: Keine Sequenzen
        res5 = [[' ']]
        self.assertEqual(dotplot.get_result('', ''), res5)


class TestDotplotForm(TestCase):

    def test_latin_letters(self):
        form = DotplotForm(data={'sequence1': 'ATR-R', 'sequence2': 'XX*WQ'})
        form.is_valid()
        self.assertEqual(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEqual(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])


# Simple Search Tests
class TestSimpleSearch(TestCase):
    def test_comparsions_count(self):
        # ein Vergleich
        # kein Ergebnis
        result = simple_search.get_result('T', 'A')

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [])

        # ein Ergebnis
        result = simple_search.get_result('A', 'A')

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [0])

        # mehrere Vergleiche
        # kein Ergebnis
        result = simple_search.get_result('UA', 'ACGUCAC')

        self.assertEquals(result['comparisons_count'], 7)
        self.assertEquals(result['results'], [])

        # ein Ergebnis
        result = simple_search.get_result('UA', 'ACGUUAC')

        self.assertEquals(result['comparisons_count'], 8)
        self.assertEquals(result['results'], [4])

        # mehrere Ergebnisse
        result = simple_search.get_result('UA', 'AUACGUUAUA')

        self.assertEquals(result['comparisons_count'], 13)
        self.assertEquals(result['results'], [1, 6, 8])

    def test_no_result(self):
        # Sequenz zu kurz
        result = simple_search.get_result('ACA', 'U')

        self.assertEquals(result['comparisons_count'], 0)
        self.assertEquals(result['results'], [])

        # Pattern nicht in Sequenz
        result = simple_search.get_result('U', 'ACA')

        self.assertEquals(result['comparisons_count'], 3)
        self.assertEquals(result['results'], [])


# Horspool tests
class TestHorspool(TestCase):
    # es werden alle möglichen Ergebnisse für Rückwärts getestet
    def test_comparisons_count_backwards(self):
        # kein Vergleich
        # keine Matches
        result = horspool.get_result('', '')

        self.assertEquals(result['comparisons_count'], 0)
        self.assertEquals(result['result'], [])

        # ein Vergleich
        # keine Matches
        result = horspool.get_result('T', 'A')

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [])

        # ein Vergleich
        # ein Match
        result = horspool.get_result('A', 'A')

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [0])

        # mehrere Vergleich
        # keine Matches
        result = horspool.get_result('A', 'TGCTGCC')

        self.assertEquals(result['comparisons_count'], 7)
        self.assertEquals(result['results'], [])

        # mehrere Vergleiche
        # ein Match
        result = horspool.get_result('A', 'TGATGCC')

        self.assertEquals(result['comparisons_count'], 7)
        self.assertEquals(result['results'], [2])

        # mehrere Vergleiche
        # mehrere Matches
        result = horspool.get_result('TG', 'TGATGCC')

        self.assertEquals(result['comparisons_count'], 6)
        self.assertEquals(result['results'], [0, 3])

    # es werden alle möglichen Ergebnisse für vorwärts getestet
    def test_comparisons_count_forward(self):
        # kein Vergleich
        # keine Matches
        result = horspool.get_result('', '', False)

        self.assertEquals(result['comparisons_count'], 0)
        self.assertEquals(result['result'], [])

        # ein Vergleich
        # keine Matches
        result = horspool.get_result('T', 'A', False)

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [])

        # ein Vergleich
        # ein Match
        result = horspool.get_result('A', 'A')

        self.assertEquals(result['comparisons_count'], 1)
        self.assertEquals(result['results'], [0])

        # mehrere Vergleich
        # keine Matches
        result = horspool.get_result('A', 'TGCTGCC')

        self.assertEquals(result['comparisons_count'], 7)
        self.assertEquals(result['results'], [])

        # mehrere Vergleiche
        # ein Match
        result = horspool.get_result('A', 'TGATGCC')

        self.assertEquals(result['comparisons_count'], 7)
        self.assertEquals(result['results'], [2])

        # mehrere Vergleiche
        # mehrere Matches
        result = horspool.get_result('TG', 'TGATGCC')

        self.assertEquals(result['comparisons_count'], 6)
        self.assertEquals(result['results'], [0, 3])


# glocal_alignment tests
class TestGlocalAlignment(TestCase):

    # testet ob das richtige Alignment zurück kommt
    def test_get_alignment(self):
        # alignment mit Gap in der Sequenz
        alignment = glocal_alignment.get_alignment('-GCTAGC', '-GCT', ['hor', 'diag', 'diag'], [2, 3])
        self.assertEquals(alignment, ['GC-TAGC', '||     ', 'GCT    '])

        # alignment mit Gap im Pattern
        alignment = glocal_alignment.get_alignment('-GCTAGC', '-GT', ['diag', 'vert', 'diag'], [3, 2])
        self.assertEquals(alignment, ['GCTAGC', '| |   ', 'G-T   '])

        # alignment ohne Gap
        alignment = glocal_alignment.get_alignment('-GCTAGC', '-GCT', ['diag', 'diag', 'diag'], [3, 3])
        self.assertEquals(alignment, ['GCTAGC', '|||   ', 'GCT   '])

    # testet ob die richtige traceback value zurück gegeben wird
    def test_traceback_value(self):
        # Similarity ist auf False, der kleinste Wert wird gewählt - hier vert
        traceback_value = glocal_alignment.traceback_value(2, 1, 3, False)
        self.assertEquals(traceback_value, 'vert')

        # Similarity ist auf True, der größte Wert wird gewählt - hier diag
        traceback_value = glocal_alignment.traceback_value(6, 2, 3, True)
        self.assertEquals(traceback_value, 'diag')

        # mehrere Werte sind gleich
        traceback_value = glocal_alignment.traceback_value(3, 3, 5, False)
        self.assertEquals(traceback_value, ['diag', 'vert'])

        traceback_value = glocal_alignment.traceback_value(4, 5, 4, False)
        self.assertEquals(traceback_value, ['diag', 'hor'])

        traceback_value = glocal_alignment.traceback_value(5, 3, 3, False)
        self.assertEquals(traceback_value, ['vert', 'hor'])

    # testet den Schwellwert
    def test_threshold(self):
        # Nur Alignments mit einem Score 2 oder weniger werden ausgegeben
        result = glocal_alignment.get_result('PONY', 'PONY', 0, 1, 1, False, 2)

        self.assertFalse({3, 4, 5}.issubset(result['score']))
        self.assertEquals(len(result['score']), 3)

        # Der Schwellwert ist bei 8, also wird kein Score heraus gefiltert
        result = glocal_alignment.get_result('PONY', 'PONY', 0, 1, 1, False, 8)

        self.assertTrue({0, 1, 2, 3, 4}.issubset(result['score']))
        self.assertEquals(len(result['score']), 5)

        # Der Schwellwert liegt so niedrig das kein Alignment diesen Score hat und nichts wird ausgegeben
        result = glocal_alignment.get_result('PONY', 'PONY', 0, 1, 1, False, -1)

        self.assertEquals(len(result['score']), 0)

    # testet die Funktion similarity
    def test_similarity_matrix(self):
        # similarity ist auf False gesetzt, somit wird immer der minimalste Wert gewählt
        result = glocal_alignment.get_result('PXPOYXPONY', 'PONY', 0, 1, 1, False, 1)

        distance_matrix= [[0, 1, 2, 3, 4],
                         [0, 0, 1, 2, 3],
                         [0, 1, 1, 2, 3],
                         [0, 0, 1, 2, 3],
                         [0, 1, 0, 1, 2],
                         [0, 1, 1, 1, 1],
                         [0, 1, 2, 2, 2],
                         [0, 0, 1, 2, 3],
                         [0, 1, 0, 1, 2],
                         [0, 1, 1, 0, 1],
                         [0, 1, 2, 1, 0]]

        self.assertEquals(distance_matrix, result['matrix'])

        # similarity wird auf True gesetzt, somit wird immer der maximale Wert gewählt
        result = glocal_alignment.get_result('PXPOYXPONY', 'PONY', 0, 1, 1, True, 1)

        similarity_matrix = [[0, 1, 2, 3, 4],
                             [0, 2, 3, 4, 5],
                             [0, 3, 4, 5, 6],
                             [0, 4, 5, 6, 7],
                             [0, 5, 6, 7, 8],
                             [0, 6, 7, 8, 9],
                             [0, 7, 8, 9, 10],
                             [0, 8, 9, 10, 11],
                             [0, 9, 10, 11, 12],
                             [0, 10, 11, 12, 13],
                             [0, 11, 12, 13, 14]]

        self.assertEquals(similarity_matrix, result['matrix'])

# testet Form von Glocal Alignments
class TestGlocalAlignmentForm(TestCase):

    # nicht korrekte Eingabe soll Fehler zurück geben
    def test_latin_letters(self):
        form = GlocalAlignmentForm(data={'sequence1': 'GTC_BCD', 'sequence2': 'V*?RT'})
        form.is_valid()
        self.assertEqual(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEqual(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])

# tests für Needleman wunsch
class TestNeedlemanWunsch(TestCase):

    # testet ob das richtige Alignment zurück kommt
    def test_get_alignment(self):
        # alignment mit Gap in Sequenz 1
        path = ['vert', 'vert', 'diag', 'hor', 'diag', 'vert']
        alignment = needleman_wunsch.get_alignment('-GCAGC', '-CTA', path)

        self.assertEquals(alignment, ['GC-AGC', ' | |  ', '-CTA--'])

        # alignment mit Gap in der Sequenz 2
        path = ['vert', 'vert', 'vert', 'diag', 'vert', 'diag']
        alignment = needleman_wunsch.get_alignment('-GCTAGC', '-GT', path)

        self.assertEquals(alignment, ['GCTAGC', '| |   ', 'G-T---'])

        # alignment ohne Gap
        path = ['vert', 'vert', 'vert', 'diag', 'diag', 'diag']
        alignment = needleman_wunsch.get_alignment('-GCTAGC', '-GCT', path)

        self.assertEquals(alignment, ['GCTAGC', '|||   ', 'GCT---'])

        # obwohl alles diag ist sollen nur bei den Matches Striche stehen
        path = ['diag', 'diag', 'diag', 'diag']
        alignment = needleman_wunsch.get_alignment('-CTSS', 'AGSS', path)

        self.assertEquals(alignment, ['CTSS', '  ||', 'AGSS'])

    # testet ob alle Alignments gefunden wurden
    def test_number_of_alignments(self):

        # Es sollen drei Alignments gefunden werden
        result = needleman_wunsch.get_result('GCTAGC', 'GC', 0, 1, 1, False)
        self.assertEquals(len(result['alignments']), 3)

        # Es sollen nur 100 Alignments zurück gegeben werden, obwohl es mehr gibt
        result = needleman_wunsch.get_result('GCTAGCCTTGAACTGCATGCATGCCGCTAGCG', 'GCG', 0, 1, 1, False)
        self.assertEquals(len(result['alignments']), 100)

    # testet ob der richtige Score zurück gegeben wird
    def test_score(self):
        result = needleman_wunsch.get_result('AGCTAG', 'ATGCTS', 0, 1, 1, False)
        self.assertEquals(result['score'], 3)

        result = needleman_wunsch.get_result('GCTASAST', 'ATGCTS', 0, 1, 1, False)
        self.assertEquals(result['score'], 6)

    # testet ob die richtige traceback value zurück gegeben wird
    def test_traceback_value(self):
        # Similarity ist auf False, der kleinste Wert wird gewählt - hier vert
        traceback_value = needleman_wunsch.traceback_value(2, 1, 3, False)
        self.assertEquals(traceback_value, 'vert')

        # Similarity ist auf True, der größte Wert wird gewählt - hier diag
        traceback_value = needleman_wunsch.traceback_value(6, 2, 3, True)
        self.assertEquals(traceback_value, 'diag')

        # mehrere Werte sind gleich
        traceback_value = needleman_wunsch.traceback_value(3, 3, 5, False)
        self.assertEquals(traceback_value, ['diag', 'vert'])

        traceback_value = needleman_wunsch.traceback_value(4, 5, 4, False)
        self.assertEquals(traceback_value, ['diag', 'hor'])

        traceback_value = needleman_wunsch.traceback_value(5, 3, 3, False)
        self.assertEquals(traceback_value, ['vert', 'hor'])

    # testet die Funktion similarity
    def test_similarity_matrix(self):
        result = needleman_wunsch.get_result('AGTC', 'ACGTC', 0, 1, 1, False)

        distance_matrix = [[0, 1, 2, 3, 4, 5],
                           [1, 0, 1, 2, 3, 4],
                           [2, 1, 1, 1, 2, 3],
                           [3, 2, 2, 2, 1, 2],
                           [4, 3, 2, 3, 2, 1]]

        self.assertEquals(result['matrix'], distance_matrix)

        result = needleman_wunsch.get_result('AGTC', 'ACGTC', 0, 1, 1, True)

        similarity_matrix = [[0, 1, 2, 3, 4, 5],
                             [1, 2, 3, 4, 5, 6],
                             [2, 3, 4, 5, 6, 7],
                             [3, 4, 5, 6, 7, 8],
                             [4, 5, 6, 7, 8, 9]]

        self.assertEquals(result['matrix'], similarity_matrix)

# testet die Form von Needleman Wunsch
class TestNeedlemanWunschForm(TestCase):

    # testet korrekten Input
    def test_input(self):
        # Sequenz darf nicht leer sein
        form = NeedlemanWunschForm(data={'sequence1': '', 'sequence2': 'CGT'})
        self.assertEquals(form.errors['sequence1'], ['This field is required.'])

        # match Input darf nicht über 1000 oder unter -1000 sein
        form = NeedlemanWunschForm(data={'match': 1001})
        self.assertEquals(form.errors['match'], ['Ensure this value is less than or equal to 1000.'])

        form = NeedlemanWunschForm(data={'match': -1001})
        self.assertEquals(form.errors['match'], ['Ensure this value is greater than or equal to -1000.'])

        # missmatch Input darf nicht über 1000 oder unter -1000 sein
        form = NeedlemanWunschForm(data={'mismatch': 1001})
        self.assertEquals(form.errors['mismatch'], ['Ensure this value is less than or equal to 1000.'])

        form = NeedlemanWunschForm(data={'mismatch': -1001})
        self.assertEquals(form.errors['mismatch'], ['Ensure this value is greater than or equal to -1000.'])

        # gap-penalty darf nicht über 1000 oder unter -1000 sein
        form = NeedlemanWunschForm(data={'gap_penalty': 1001})
        self.assertEquals(form.errors['gap_penalty'], ['Ensure this value is less than or equal to 1000.'])

        form = NeedlemanWunschForm(data={'gap_penalty': -1001})
        self.assertEquals(form.errors['gap_penalty'], ['Ensure this value is greater than or equal to -1000.'])

    # nicht korrekte Eingabe soll Fehler zurück geben
    def test_latin_letters(self):
        form = NeedlemanWunschForm(data={'sequence1': 'GTC_BCD', 'sequence2': 'V*?RT'})
        form.is_valid()
        self.assertEquals(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEquals(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])

# tests für Smith Waterman
class TestSmithWaterman(TestCase):

    # testet ob das richtige Alignment zurück kommt
    def test_get_aignment(self):
        # Gap in Sequenz 1
        alignment = smith_waterman.get_alignment('-ATGGTG', '-ATCG', ['diag', 'hor', 'diag', 'diag'], [3, 4])
        self.assertEquals(alignment, ['AT-GGTG', '|| |   ', 'ATCG   '])

        # Gap in Sequenz 2
        alignment = smith_waterman.get_alignment('-ATCGGTG', '-ATG', ['diag', 'vert', 'diag', 'diag'], [4, 3])
        self.assertEquals(alignment, ['ATCGGTG', '|| |   ', 'AT-G   '])

    def test_number_of_alignments(self):
        # es sollen 4 Alignments gefunden werden
        result = smith_waterman.get_result('ATGGTGCAT', 'ATGCGGTGC', 1, -1, 1)
        self.assertEquals(len(result['alignments']), 4)

        # es sollen nur 100 ALignments zurück gegeben werden, obwohl es mehr gibt
        longSeq = 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'
        result = smith_waterman.get_result(longSeq, 'C', 1, -1, 1)
        print(len(result['alignments']))

    # testet ob der richtige Score zurück gegeben wird
    def test_score(self):

        result = smith_waterman.get_result('ATGGTGCAT', 'ATGCGGTGC', 1, -1, 1)
        self.assertEquals(result['score'], 5)

        # es existiert mehrfach der gleiche Score
        result = smith_waterman.get_result('AGCTAGCT', 'AGC', 1, -1, 1)
        self.assertEquals(result['score'], 3)

    def test_traceback_value(self):

        # größter Wert wird gewählt - hor
        traceback_value = smith_waterman.traceback_value(2, 1, 3, 0)
        self.assertEquals(traceback_value, 'hor')

        # mehrere Werte sind gleich
        traceback_value = smith_waterman.traceback_value(0 ,0 ,0, 0)
        self.assertEquals(traceback_value, ['diag', 'vert', 'hor', None])

        traceback_value = smith_waterman.traceback_value(2, 1, 2, 2)
        self.assertEquals(traceback_value, ['diag', 'hor', None])


    def test_matrix(self):

        result = smith_waterman.get_result('ATGGTGCAT', 'ATGCGGTGC', 1, -1, 1)

        matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 2, 1, 0, 0, 0, 1, 0, 0],
                  [0, 0, 1, 3, 2, 1, 1, 0, 2, 1],
                  [0, 0, 0, 2, 2, 3, 2, 1, 1, 1],
                  [0, 0, 1, 1, 1, 2, 2, 3, 2, 1],
                  [0, 0, 0, 2, 1, 2, 3, 2, 4, 3],
                  [0, 0, 0, 1, 3, 2, 2, 2, 3, 5],
                  [0, 1, 0, 0, 2, 2, 1, 1, 2, 4],
                  [0, 0, 2, 1, 1, 1, 1, 2, 1, 3]]

        self.assertEquals(result['matrix'], matrix)

# test für SmithWatermanForm
class TestSmithWatermanForm(TestCase):

    # testet die Eingaben
    def test_input(self):
        # Sequenz darf nicht leer sein
        form = SmithWatermanForm(data={'sequence1': '', 'sequence2': 'CGT'})
        self.assertEquals(form.errors['sequence1'], ['This field is required.'])

        # match Input darf nicht über 1000 oder unter -1000 sein
        form = SmithWatermanForm(data={'match': 1001})
        self.assertEquals(form.errors['match'], ['Ensure this value is less than or equal to 1000.'])

        form = SmithWatermanForm(data={'match': -1001})
        self.assertEquals(form.errors['match'], ['Ensure this value is greater than or equal to -1000.'])

        # missmatch Input darf nicht über 1000 oder unter -1000 sein
        form = SmithWatermanForm(data={'mismatch': 1001})
        self.assertEquals(form.errors['mismatch'], ['Ensure this value is less than or equal to 1000.'])

        form = SmithWatermanForm(data={'mismatch': -1001})
        self.assertEquals(form.errors['mismatch'], ['Ensure this value is greater than or equal to -1000.'])

        # gap-penalty darf nicht über 1000 oder unter -1000 sein
        form = SmithWatermanForm(data={'gap_penalty': 1001})
        self.assertEquals(form.errors['gap_penalty'], ['Ensure this value is less than or equal to 1000.'])

        form = SmithWatermanForm(data={'gap_penalty': -1001})
        self.assertEquals(form.errors['gap_penalty'], ['Ensure this value is greater than or equal to -1000.'])


    # nicht korrekte Eingabe soll Fehler zurück geben
    def test_latin_letters(self):
        form = SmithWatermanForm(data={'sequence1': 'GTC_BCD', 'sequence2': 'V*?RT'})
        form.is_valid()
        self.assertEquals(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEquals(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])

# test für ViterbiForm
class TestViterbiForm(TestCase):
    
    def test_sequence_is_alphabet(self):
        form = ViterbiForm(data={'sequence': 'XazÄ*', 'states': '+;-'}) # * ist keine Buchstabe
        form2 = ViterbiForm(data={'sequence': 'XazÄ2', 'states': '+;-' }) # 2 ist keine Buchstabe
        form3 = ViterbiForm(data={'sequence': '', 'states': '+;-' }) # leer nicht erlaubt

        form.is_valid()
        form2.is_valid()
        form3.is_valid()
        self.assertEqual(form.errors['sequence'],["Nur Buchstaben sind erlaubt."] ) 
        self.assertEqual(form2.errors['sequence'],["Nur Buchstaben sind erlaubt."] )
        self.assertEqual(form3.errors['sequence'],["This field is required."] ) 

    def test_number_of_states(self):
        form = ViterbiForm(data={'sequence':'abcd', 'states': 'q;w;e;r;T;%&;$;i;o;s;tr;sr;er'}) # Mehr als 10 Zustände
        form2 = ViterbiForm(data={'sequence':'abcd', 'states': 'a' }) # Weniger als 2 Zutände
        form3 = ViterbiForm(data={'sequence':'abcd', 'states': 'a,b,v,c' }) # Zustände werden nicht durch Semikolon getrennt
        form.is_valid()
        form2.is_valid()
        form3.is_valid()
        self.assertEqual(form.errors['states'], ['Geben Sie nicht mehr als 10  und nicht weniger als 2 Zustände ein, separiert mit Semikolon. Eingegebener \'Start\'-Zustand wird nicht berücksichtigt.'])
        self.assertEqual(form2.errors['states'], ['Geben Sie nicht mehr als 10  und nicht weniger als 2 Zustände ein, separiert mit Semikolon. Eingegebener \'Start\'-Zustand wird nicht berücksichtigt.'])
        self.assertEqual(form3.errors['states'], ['Geben Sie nicht mehr als 10  und nicht weniger als 2 Zustände ein, separiert mit Semikolon. Eingegebener \'Start\'-Zustand wird nicht berücksichtigt.'])

# test für Suffix Array
class TestSuffixArray(TestCase):
    def test_suffix_array(self):
        text = "brandenburg"
        test_sa = [['', 'Suffix', 'Position'],
                   [0, 'andenburg', 2], 
                   [1, 'brandenburg', 0], 
                   [2, 'burg', 7], 
                   [3, 'denburg', 4], 
                   [4, 'enburg', 5], 
                   [5, 'g', 10], 
                   [6, 'nburg', 6], 
                   [7, 'ndenburg', 3], 
                   [8, 'randenburg', 1], 
                   [9, 'rg', 9], 
                   [10, 'urg', 8]]
        res = suffix_array.get_results('',text)
        sa = res['suffix_array']
        self.assertEqual(test_sa, sa)

    def test_found(self):
        text = 'lamborghini'
        pattern1 = 'ghin'
        res1 = suffix_array.get_results(pattern1,text)
        self.assertTrue(res1['found'])

        pattern2 = 'nini'
        res2 = suffix_array.get_results(pattern2,text)
        self.assertFalse(res2['found'])   

        pattern3 = 'lamborghinin' # Pattern ist länger als Text
        res3 = suffix_array.get_results(pattern3,text)
        self.assertFalse(res3['found'])  

        pattern4 = ''
        res4 = suffix_array.get_results(pattern4,text)
        self.assertIsNone(res4['found'])  

# test für SuffixTreeTrieForm
class TestSuffixTreeTrieForm(TestCase):
    
    def test_endchar_not_in_sequence(self):
        form = SuffixTreeTrieForm({'sequence': 'anaRna', 'endchar':'R'}) 
        form.is_valid()
        self.assertEqual(form.errors['sequence'], ['Endzeichen darf nicht im Text enthalten sein'])
    
    def test_endchar_not_in_pattern(self):
        form2 = SuffixTreeTrieForm({'pattern':'Alf§f', 'endchar':'§'})
        form2.is_valid()
        self.assertEqual(form2.errors['pattern'], ['Endzeichen darf nicht im Muster enthalten sein'])

# test für OverlapForm
class TestOverlapForm(TestCase):

    def test_latin_letters(self):
        form = OverlapForm(data={'sequence1': 'ABGX$', 'sequence2': 'Ö%ll'}) # Nicht latinische Buchstaben
        form.is_valid()
        self.assertEqual(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEqual(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])

# tests für Neighbour joining
class TestNeighbourJoining(TestCase):

    # testet newick
    def test_newick(self):
        matrix = [[0],
                  [5, 0],
                  [9, 10, 0],
                  [9, 10, 8, 0],
                  [8, 9, 7, 3, 0]]

        result = neighbour_joining.get_results(['A', 'B', 'C', 'D', 'E'], matrix)
        self.assertEquals(result['newick'], '(((((((A:2.0,B:3.0):3.0),C:4.0):2.0),D:2.0):0),E:1.0)')

        matrix = [[0],
                  [17, 0],
                  [21, 30, 0],
                  [31, 34, 28, 0],
                  [23, 21, 39, 43, 0]]

        result = neighbour_joining.get_results(['A', 'B', 'C', 'D', 'E'], matrix)
        self.assertEquals(result['newick'], '(((E:14.5,((((D:17.0,C:11.0):7.0),A:5.0):4.5)):0),B:6.75)')

# test upgma,nj Form
class TestUpgmaNjForm(TestCase):
    def test_number_of_names(self):
        form = UpgmaNjForm(data={'names': 'a;b;c',
                        'csv_data': '0; ; ; \n1; 2; ; \n2;3;0; \n3;6;5;0'})
        form.is_valid()
        self.assertEqual(form.errors['names'],["Die Anzahl von Namen sollte mit der Anzahl von Spalten/Zeilen übereinstimmen. Bitte geben Sie die Namen ein, separiert mit Semikolon oder lassen Sie das Eingabefeld frei, dann werden die Namen automatisch generiert"])

    def test_number_of_columns_and_rows(self):
        form = UpgmaNjForm(data={
                        'csv_data': '1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n'})
        form.is_valid()
        self.assertTrue("Die Anzahl der Zeilen soll gleich der Anzahl der Spalten sein" in form.errors['csv_data'])

    def test_diagonal_0_values(self):
        form = UpgmaNjForm(data={
                        'csv_data': '0; ; ; \n1; 2; ; \n2;3;0; '})
        form.is_valid()
        self.assertEqual(form.errors['csv_data'],["Auf der Diagonale dürfen nur 0 stehen"])

    def test_maximal_number_of_sequence(self):
        form = UpgmaNjForm(data={'csv_data': '1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0\n1;0'})
        form.is_valid()
        self.assertTrue("Die Anzahl der Zeilen darf maximal 20 sein" in form.errors['csv_data'])

    def test_size_of_csv_data(self):
        form = UpgmaNjForm(data={'csv_data': '1;0\n'})
        form.is_valid()
        self.assertTrue("Die Matrix soll aus mindestens zwei Zeilen bestehen" in form.errors['csv_data'])
    
    def test_csv_data_is_complete(self):
        form = UpgmaNjForm(data={'csv_data': '2;0\n1;1;0\n0;5\n'})
        form.is_valid()
        self.assertTrue("Die Matrix ist nicht diagonal oder nicht vollständig" in form.errors['csv_data'])
