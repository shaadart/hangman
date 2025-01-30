from flask import Flask, jsonify, render_template
from random_word import RandomWords
from nltk.corpus import wordnet
import random
import nltk

# Ensure required NLTK data is downloaded
nltk.download("wordnet")

app = Flask(__name__)

# Initialize the RandomWords library
random_words = RandomWords()

# Fallback word list with hints
WORDS = [
    {"word": "tiger", "hint": "It is a wild animal."},
    {"word": "elephant", "hint": "The largest land animal."},
    {"word": "python", "hint": "A type of snake and a programming language."},
    {"word": "dolphin", "hint": "A highly intelligent marine mammal."},
    {"word": "eagle", "hint": "A bird known for its sharp vision."},
    {"word": "astronaut", "hint": "A person trained to travel in space."},
    {"word": "volcano", "hint": "A mountain that erupts lava."},
    {"word": "umbrella", "hint": "Used to protect from rain or sunlight."},
]

@app.route('/get_word')
def get_word():
    try:
        for _ in range(10):  # Try up to 10 times to get a valid word with a hint
            # Generate a random word
            random_word = random_words.get_random_word()
            if not random_word:
                continue

            # Fetch the definition using NLTK WordNet
            synsets = wordnet.synsets(random_word)
            if synsets:
                hint = synsets[0].definition()  # Get the first definition
                if hint != "No hint available for this word.":
                    return jsonify(word=random_word, hint=hint)

        # If no valid word is found, fallback to predefined word list
        raise Exception("Failed to get a valid word with a hint.")
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")

        # Fallback to predefined word list
        fallback_word = random.choice(WORDS)
        return jsonify(word=fallback_word["word"], hint=fallback_word["hint"])

@app.route('/')
def index():
    return render_template('hangman_game_ui.html')

if __name__ == '__main__':
    app.run(debug=True)
