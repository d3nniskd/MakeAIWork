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