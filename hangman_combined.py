# import random
# import requests
# import json
# import os
# import tkinter as tk
# from tkinter import messagebox

# # Constants
# LIVES = 5
# WORD_API = "https://random-word-api.herokuapp.com/word?number=1"
# DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
# HIGH_SCORE_FILE = "highscore.json"

# # ==============================
# # Word Fetching and Hint System
# # ==============================

# def fetch_word():
#     """Fetch a random word from an online API."""
#     try:
#         response = requests.get(WORD_API)
#         response.raise_for_status()
#         word = response.json()[0].upper()
#         if len(word) > 5:
#             return fetch_word()
#         return word if word.isalpha() else fetch_word()  # Ensure valid word
#     except requests.RequestException:
#         return random.choice(["PYTHON", "PROGRAMMING", "HANGMAN", "GITHUB", "DEVELOPER"])  # Fallback

# def fetch_hint(word):
#     """Fetch a hint for the word from the dictionary API."""
#     try:
#         response = requests.get(DICT_API + word.lower(), timeout=5)
#         response.raise_for_status()
#         data = response.json()
#         if isinstance(data, list) and "meanings" in data[0]:
#             return data[0]["meanings"][0]["definitions"][0].get("definition", "No hint available.")
#     except requests.RequestException:
#         pass  
#     return "No hint available."

# # ==============================
# # High Score Management
# # ==============================

# def save_high_score(score):
#     """Save high score to a file."""
#     try:
#         if os.path.exists(HIGH_SCORE_FILE):
#             with open(HIGH_SCORE_FILE, "r") as f:
#                 data = json.load(f)
#         else:
#             data = {"high_score": 0}
        
#         if score > data["high_score"]:
#             data["high_score"] = score
#             with open(HIGH_SCORE_FILE, "w") as f:
#                 json.dump(data, f)
#             return True
#     except (IOError, json.JSONDecodeError):
#         pass
#     return False

# def load_high_score():
#     """Load high score from a file."""
#     try:
#         if os.path.exists(HIGH_SCORE_FILE):
#             with open(HIGH_SCORE_FILE, "r") as f:
#                 return json.load(f).get("high_score", 0)
#     except (IOError, json.JSONDecodeError):
#         pass
#     return 0

# # ==============================
# # Core Game Logic
# # ==============================

# class HangmanGame:
#     """Hangman game logic to be controlled by Tkinter frontend."""
    
#     def __init__(self):
#         self.word = fetch_word()
#         self.guessed_letters = set()
#         self.correct_letters = set(self.word)
#         self.hidden_word = ["_" if letter.isalpha() else letter for letter in self.word]
#         self.lives = LIVES
#         self.score = 0
#         self.hint_shown = False

#     def get_hidden_word(self):
#         """Return the current hidden word."""
#         return " ".join(self.hidden_word)

#     def guess_letter(self, guess):
#         """Process a guessed letter."""
#         guess = guess.strip().upper()
#         if not guess or len(guess) != 1 or not guess.isalpha():
#             return "Invalid input! Enter a single letter."
        
#         if guess in self.guessed_letters:
#             return "You already guessed that letter!"

#         self.guessed_letters.add(guess)

#         if guess in self.correct_letters:
#             for idx, letter in enumerate(self.word):
#                 if letter == guess:
#                     self.hidden_word[idx] = guess
#             self.score += 10
#             return f"Correct! {guess} is in the word."
#         else:
#             self.lives -= 1
#             self.score -= 5
#             if not self.hint_shown:
#                 self.hint_shown = True
#                 return f"Wrong guess! {self.lives} lives remaining. 💡 Hint: {fetch_hint(self.word)}"
#             return f"Wrong guess! {self.lives} lives remaining."

#     def is_game_over(self):
#         """Check if the game has ended."""
#         return self.lives <= 0 or "_" not in self.hidden_word

#     def get_final_result(self):
#         """Return the final result when the game ends."""
#         if "_" not in self.hidden_word:
#             if save_high_score(self.score):
#                 return f"🎉 You won! The word was {self.word}. New High Score: {self.score}"
#             return f"🎉 You won! The word was {self.word}. Score: {self.score}"
#         return f"💀 Game Over! The word was {self.word}."

# # ==============================
# # Tkinter UI Setup
# # ==============================

# # Initialize the game
# game = HangmanGame()

# # UI Setup
# root = tk.Tk()
# root.title("Hangman Game")
# root.geometry("600x300")

# frame = tk.Frame(root)
# frame.pack(fill="both", expand=True)

# canvas = tk.Canvas(frame, width=200, height=200, bg="white")
# canvas.grid(row=0, column=0, padx=10, pady=10)

# word_label = tk.Canvas(frame, width=400, height=80, bg="white")
# word_label.grid(row=0, column=1, padx=10, pady=10)

# hint_label = tk.Label(frame, text=f"Hint: {fetch_hint(game.word)}", font=("Arial", 14))
# hint_label.grid(row=1, column=1, padx=10, pady=10)

# # Load GIFs
# gif_paths = {
#     5: "5_lives.gif",
#     4: "4_lives.gif",
#     3: "3_lives.gif",
#     2: "2_lives.gif",
#     1: "1_lives.gif",
#     0: "dead.gif"
# }
# gifs = {lives: tk.PhotoImage(file=path) for lives, path in gif_paths.items()}

# def update_display():
#     """Update the word display and hint label."""
#     word_label.delete("all")
#     for i, letter in enumerate(game.hidden_word):
#         word_label.create_rectangle(50 + i * 40, 20, 80 + i * 40, 60, outline="black")
#         word_label.create_text(65 + i * 40, 40, text=letter, font=("Arial", 24))
#     hint_label.config(text=f"Hint: {fetch_hint(game.word)}")

# def draw_hangman():
#     """Draw hangman parts based on incorrect guesses."""
#     canvas.delete("all")
#     gif = gifs[game.lives]
#     canvas.create_image(0, 0, anchor=tk.NW, image=gif)
#     canvas.image = gif  # Keep a reference to avoid garbage collection

# def guess_letter(event):
#     """Handle the letter guessing and update UI."""
#     letter = event.char.upper()
#     if not letter.isalpha() or len(letter) != 1:
#         return
#     result = game.guess_letter(letter)
#     messagebox.showinfo("Hangman", result)
#     update_display()
#     draw_hangman()
#     check_game_status()

# def check_game_status():
#     """Check if the game is over and show the result."""
#     if game.is_game_over():
#         messagebox.showinfo("Hangman", game.get_final_result())
#         root.quit()

# root.bind("<KeyPress>", guess_letter)
# update_display()
# draw_hangman()
# root.mainloop()
