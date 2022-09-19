# Define symbols

symbolVecs = {'0': (1, 0), 'X': (0,1)}
# dictionaries heben key en value, gescheiden door dubbele punt

symbolsChars = dict ((value, key) for key, value in symbolVecs.items ())

# Define datasets (training set should normally be much larger than test set for best results)

trainingSet = (
    ((
        (1, 1, 1),
        (1, 0, 1),
        (1, 1, 1)
    ), '0'),
    ((
        (0, 1, 0),
        (1, 0, 1),
        (0, 1, 0)
    ), '0'),
    ((
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 0)
    ), 'X'),
    ((
        (1, 0, 1),
        (0, 1, 0),
        (1, 0, 1)
    ), 'X')
)

# We beginnen gewoon even in deze file. Later kijken we nog wel even hoe we ze hieruit kunnen uitlezen.

# Aantal printopdrachten om te zien hoe we de data kunnen 'uitkleden'
print(trainingSet[1])
print(type(trainingSet))
print("The first element of the second set is ", trainingSet[1][0]) # dit willen we dus, zodat die laatste eraf X/O eraf valt
print("The second element of the third set is ", trainingSet[2][1])
# nog een niveau dieper
print("2e rij uit 1e element van de 3e set is: ", trainingSet[2][0][1])

# Converteer de tuple naar lijst
matrixUitTupleList =[trainingSet[1][0]]
print('de tuple is nu een lijst: ', matrixUitTupleList)

# Convert 3x3 matrix to 9x1 vector
def matr2Vect(matr):

    vect = [] # vect = list() zou ook kunnen, maar eerste is korter en sneller

    rows = len(matr)

    for row in range(0, rows):

        cols = len(matr[row])

        for col in range(0, cols):

            vect.append(matr[row][col])

    return vect

# Testen van deze functie op 1 vd tuples uit de traingsset:

deVector = matr2Vect(trainingSet[1][0])
print(deVector)

# Dan alle gewichten op een waarde (in ons geval 1) zetten

def initWeights(vect):

    n = len(vect)

    weights = []

    for i in range(0,n):

        weights.append(1.0)

    return weights


def in2out(vec, weights):

    n = len(vec)

    Sum = 0.0

    # Compute vec[i] * weights[i]
    for i in range(0, n):

        Sum += vec[i] * weights[i]

    # TODO: softmax
    return math.sqrt(Sum)


v = mat2vec(s[0])
w = initWeights(v)
out = in2out(v, w)

print(out)