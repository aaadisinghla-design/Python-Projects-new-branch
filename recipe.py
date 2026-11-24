import re

# 1. Five sample recipes
recipes = {
    "Garlic Butter Pasta": "Boil pasta until tender. Melt butter with minced garlic and toss with parmesan.",
    "Classic Pancakes": "Whisk flour, milk, eggs, and baking powder. Cook on a hot buttered griddle.",
    "Tomato Basil Soup": "Simmer crushed tomatoes, garlic, vegetable broth, and fresh basil until smooth.",
    "Avocado Toast": "Mash ripe avocado with lemon juice and salt. Spread over toasted sourdough bread.",
    "Chicken Stir Fry": "Saute diced chicken, broccoli, and bell peppers in soy sauce and sesame oil."
}

def tokenize(text):
    return re.findall(r"[a-z]+", text.lower())

# 2. Build an inverted index: word -> set of recipe titles
index = {}
for title, body in recipes.items():
    for word in set(tokenize(f"{title} {body}")):
        index.setdefault(word, set()).add(title)

# 3. Score each recipe by counting matching query words
def search(query):
    scores = {title: 0 for title in recipes}
    for word in tokenize(query):
        for title in index.get(word, []):
            scores[title] += 1
    best_match = max(scores, key=scores.get)
    return best_match if scores[best_match] > 0 else "No match found"

# 4. Test queries and count mistakes
test_cases = [
    ("garlic pasta parmesan", "Garlic Butter Pasta"),
    ("fluffy breakfast flour milk", "Classic Pancakes"),
    ("warm tomato basil", "Tomato Basil Soup"),
    ("bread with lemon and avocado", "Avocado Toast"),
    ("soy sauce broccoli", "Chicken Stir Fry"),
    ("buttered toast", "Avocado Toast"),  # Likely mistake: "butter" vs "buttered"
]

mistakes = 0
for query, expected in test_cases:
    result = search(query)
    if result != expected:
        mistakes += 1
        print(f"Mistake on '{query}': got '{result}', expected '{expected}'")

print(f"\nTotal mistakes: {mistakes} out of {len(test_cases)}")
