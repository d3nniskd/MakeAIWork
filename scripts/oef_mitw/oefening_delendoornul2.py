def divide(a,b)
    a = int (input ('Geef getal A: '))
    b = int (input ('Geef getal B: '))

if b == 0:
	print (f'Je mag niet delen door nul')
else:
	print (f'A/B = {a/b}')

def sum(param1, param2):
    """
    Deze functie berekent de som van twee getallen:
    param1 + param2
    """
    print(param1, " plus ", param2, " = ", param1+param2)

    return param1+param2

print(sum.__doc__)
sum(15,12)