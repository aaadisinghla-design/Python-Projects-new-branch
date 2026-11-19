"""
"Did You Mean?" - NLP Activity 7 (Pet Edition)
Grades 8-12 | Python 3, standard library only

Pet adoption apps get "goldn retriver", "chihuhua" and "parot" all day long
and still find the right animal. The trick is EDIT DISTANCE: the smallest
number of single-letter fixes (insert, delete, change) that turn one word into another.
We compute it with dynamic programming: a table where every cell reuses
the answers already worked out in the cells next to it.
"""

# Adoptions/searches this month in our (made-up) pet app. Used to break ties.
PETS = {
    "dog": 980, "cat": 950, "golden retriever": 890, "german shepherd": 760,
    "french bulldog": 810, "poodle": 640, "beagle": 580, "chihuahua": 610,
    "husky": 720, "labrador": 850, "siamese cat": 530, "maine coon": 490,
    "persian cat": 460, "rabbit": 670, "hamster": 590, "guinea pig": 510,
    "parrot": 440, "cockatiel": 320, "budgie": 390, "goldfish": 740,
    "betta fish": 680, "turtle": 550, "tortoise": 310, "bearded dragon": 420,
    "leopard gecko": 380, "ball python": 290, "ferret": 340, "chinchilla": 270,
    "hedgehog": 360, "axolotl": 410,
}

USE_KEYBOARD = True   # Upgrade 1: typing a NEIGHBOURING key costs only 0.5
USE_SWAPS = True      # Upgrade 2: swapped letters (ferert) cost 1, not 2

KEY_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
KEY_POS = {key: (row, col) for row, keys in enumerate(KEY_ROWS) for col, key in enumerate(keys)}


# ---------------------------------------------------------------
# Step 1: How much does it cost to change letter x into letter y?
# ---------------------------------------------------------------
def are_neighbours(x, y):
    if x == y or x not in KEY_POS or y not in KEY_POS:
        return False
    (r1, c1), (r2, c2) = KEY_POS[x], KEY_POS[y]
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1


def change_cost(x, y):
    if x == y:
        return 0
    if USE_KEYBOARD and are_neighbours(x, y):
        return 0.5      # fat-finger typo: very likely!
    return 1


# ---------------------------------------------------------------
# Step 2: The edit-distance table
#   table[i][j] = cost to turn the first i letters of a
#                 into the first j letters of b
# ---------------------------------------------------------------
def build_table(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        table[i][0] = i                 # delete all i letters
    for j in range(len(b) + 1):
        table[0][j] = j                 # insert all j letters

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            delete = table[i - 1][j] + 1
            insert = table[i][j - 1] + 1
            change = table[i - 1][j - 1] + change_cost(a[i - 1], b[j - 1])
            table[i][j] = min(delete, insert, change)

            # Upgrade 2: "re" typed as "er" is ONE mistake, not two
            if USE_SWAPS and i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                table[i][j] = min(table[i][j], table[i - 2][j - 2] + 1)
    return table


def edit_distance(a, b):
    return build_table(a, b)[-1][-1]


def print_table(a, b):
    """Print the table so you can check the one you filled in on paper."""
    table = build_table(a, b)
    print("        " + "".join(f"{ch:>5}" for ch in b))
    for i, row in enumerate(table):
        label = a[i - 1] if i > 0 else " "
        print(f"   {label:>2}" + "".join(f"{v:>5g}" for v in row))


# ---------------------------------------------------------------
# Step 3: Rank every pet. Closest first; ties go to the more popular pet.
# ---------------------------------------------------------------
def suggest(query, k=5):
    query = query.lower().strip()
    ranked = []
    for pet, popularity in PETS.items():
        ranked.append((edit_distance(query, pet), -popularity, pet))
    ranked.sort()
    return [(pet, dist, -neg_pop) for dist, neg_pop, pet in ranked[:k]]


def max_typos(query):
    return max(1, len(query) // 4)      # longer words are allowed more mistakes


def did_you_mean(query):
    query = query.lower().strip()
    if query in PETS:
        return query, f"Showing results for {query}"
    best = suggest(query, k=1)
    if not best:
        return None, "Search isn't working yet - finish suggest()!"
    pet, dist, _ = best[0]
    if dist <= max_typos(query):
        return pet, f"Did you mean: {pet}?"
    return None, f"No pets found for '{query}'"


# ---------------------------------------------------------------
# Step 4: A/B/C test. Which version of the search box is best?
# ---------------------------------------------------------------
TYPOS = [
    ("dgo", "dog"), ("goldn retriver", "golden retriever"), ("chihuhua", "chihuahua"),
    ("parot", "parrot"), ("rabit", "rabbit"), ("hamstre", "hamster"),
    ("gunea pig", "guinea pig"), ("goldfsh", "goldfish"), ("trutle", "turtle"),
    ("ferert", "ferret"), ("axoltl", "axolotl"), ("huskie", "husky"),
]


def score_version(keyboard, swaps):
    global USE_KEYBOARD, USE_SWAPS
    USE_KEYBOARD, USE_SWAPS = keyboard, swaps
    return [did_you_mean(typo)[0] for typo, _ in TYPOS]


def ab_test():
    saved = USE_KEYBOARD, USE_SWAPS
    versions = {
        "A: plain": score_version(False, False),
        "B: +keyboard": score_version(True, False),
        "C: +keyboard +swaps": score_version(True, True),
    }
    print(f"{'typed':<16}{'wanted':<18}" + "".join(f"{name:<22}" for name in versions))
    for row, (typo, wanted) in enumerate(TYPOS):
        cells = ""
        for results in versions.values():
            got = results[row] or "(nothing)"
            cells += f"{('OK ' if got == wanted else 'XX ') + got:<22}"
        print(f"{typo:<16}{wanted:<18}{cells}")
    totals = "".join(f"{f'{sum(r == w for r, (_, w) in zip(res, TYPOS))}/{len(TYPOS)}':<22}"
                     for res in versions.values())
    print(f"{'SCORE':<34}{totals}")
    restore(*saved)


def restore(keyboard, swaps):
    global USE_KEYBOARD, USE_SWAPS
    USE_KEYBOARD, USE_SWAPS = keyboard, swaps


if __name__ == "__main__":
    print("Warm-up: fill in the table for 'dog' -> 'cat' on paper, then check it:\n")
    print_table("dog", "cat")
    print()
    ab_test()
    print("\nSearch for a pet ('quit' to stop)")
    while True:
        query = input("\n> ")
        if query.strip().lower() == "quit":
            break
        print("  ", did_you_mean(query)[1])
        for pet, dist, popularity in suggest(query, k=3):
            print(f"     {pet:<18} distance {dist:<4g} ({popularity} searches)")
