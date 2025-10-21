#install the library first:       pip install python-constraint
from constraint import *
from tabulate import tabulate

problem = Problem()

houses = range(1, 6) # 5 houses

# variables and domains
color = ["red", "green", "white", "yellow", "blue"]
country = ["Brit", "Swede", "Dane", "Norwegian", "German"]
drink = ["tea", "coffee", "milk", "beer", "water"]
cigarette = ["PallMall", "Dunhill", "Blends", "Camel", "Marlborough"]
pet = ["dog", "birds", "cats", "horses", "fish"]

problem.addVariables(color, houses)
problem.addVariables(country, houses)
problem.addVariables(drink, houses)
problem.addVariables(cigarette, houses)
problem.addVariables(pet, houses)

#  AllDifferentConstraint()：all the values need to be different
problem.addConstraint(AllDifferentConstraint(), color)
problem.addConstraint(AllDifferentConstraint(), country)
problem.addConstraint(AllDifferentConstraint(), drink)
problem.addConstraint(AllDifferentConstraint(), cigarette)
problem.addConstraint(AllDifferentConstraint(), pet)

# 15 clues
#1	The Brit lives in a red house
problem.addConstraint(lambda b, r: b == r, ("Brit", "red"))
#2	The Swede keeps a dog
problem.addConstraint(lambda s, d: s == d, ("Swede", "dog")) 
#3	The Dane drinks tea
problem.addConstraint(lambda d, t: d == t, ("Dane", "tea"))
#4	The green house is directly to the left of the white house
problem.addConstraint(lambda g, w: w - g == 1, ("green", "white")) 
#5	The green house owner drinks coffee
problem.addConstraint(lambda g, c: g == c, ("green", "coffee")) 
#6	The person who smokes Pall Mall keeps birds
problem.addConstraint(lambda p, b: p == b, ("PallMall", "birds"))
#7	The owner of the yellow house smokes Dunhill
problem.addConstraint(lambda y, d: y == d, ("yellow", "Dunhill"))
#8 The man living in the house right in the center drinks milk
problem.addConstraint(lambda m: m == 3, ("milk",))
#9	The Norwegian lives in the first house
problem.addConstraint(lambda n: n == 1, ("Norwegian",))
#10	The man who smokes Blends lives next to the one who keeps cats
problem.addConstraint(lambda b, c: abs(b - c) == 1, ("Blends", "cats"))
#11	The man who keeps horses lives next to the man who smokes Dunhill
problem.addConstraint(lambda h, d: abs(h - d) == 1, ("horses", "Dunhill"))
#12	The owner who smokes Camel drinks beer
problem.addConstraint(lambda c, b: c == b, ("Camel", "beer"))
#13	The German smokes Marlborough
problem.addConstraint(lambda g, m: g == m, ("German", "Marlborough"))
#14	The Norwegian lives next to the blue house
problem.addConstraint(lambda n, b: abs(n - b) == 1, ("Norwegian", "blue"))
#15	The man who smokes Blends has a neighbor who drinks water
problem.addConstraint(lambda b, w: abs(b - w) == 1, ("Blends", "water"))

# get solutions
solutions = problem.getSolutions()

#print(solutions)

# Print the values for each house as a table
for solution in solutions:
    print("House assignments:")
    print("=" * 60)

    # Create table data
    table_data = []
    headers = ["House", "Color", "Country", "Drink", "Cigarette", "Pet"]

    # Fill in the table data for each house
    for house_num in sorted(houses):
        row = [f"House {house_num}"]

        # Find the attribute for each category in this house
        for category in [color, country, drink, cigarette, pet]:
            found_item = None
            for item in category:
                if item in solution and solution[item] == house_num:
                    found_item = item
                    break
            row.append(found_item if found_item else "")

        table_data.append(row)

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()

    # Find who is in the same house as the fish
    fish_house = solution["fish"]
    print("Solution:")
    print("=" * 30)
    print(f"The fish is in house {fish_house}")

    # Find the person (country) who owns the fish
    for person in country:
        if person in solution and solution[person] == fish_house:
            print(f"\nANSWER: The {person} owns the fish!")
            break

#print("\nThe German keeps the fish.")