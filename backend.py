import random
import requests
import json
import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
import pyfiglet

console = Console()

# Constants
LIVES = 5
WORD_API = "https://random-word-api.herokuapp.com/word?number=1"
DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
HIGH_SCORE_FILE = "highscore.json"

def fetch_word():
    """Fetch a random word from an online API."""
    try:
        response = requests.get(WORD_API)
        response.raise_for_status()
        word = response.json()[0].upper()
        if len(word) > 5:
            return fetch_word()
        return word if word.isalpha() else fetch_word()  # Ensure valid word
    except requests.RequestException:
        return random.choice(["PYTHON", "PROGRAMMING", "HANGMAN", "GITHUB", "DEVELOPER"])  # Fallback
    
def fetch_hint(word):
    """Fetch a subtle hint for the word."""
    try:
        response = requests.get(DICT_API + word.lower(), timeout=5)
        response.raise_for_status()
        data = response.json()

        # Check if data structure is valid and contains definitions
        if isinstance(data, list) and "meanings" in data[0]:
            meaning = data[0]["meanings"][0]["definitions"][0].get("definition", "").strip()
            if meaning:  # Ensure it's not empty
                return meaning.encode('utf-8').decode('utf-8')  # Fix encoding
    except requests.RequestException:
        pass  # API error, fallback

    return "No hint available."  # Default fallback if no definition is found


def save_high_score(score):
    """Save high score to a file."""
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {"high_score": 0}
        
        if score > data["high_score"]:
            data["high_score"] = score
            with open(HIGH_SCORE_FILE, "w") as f:
                json.dump(data, f)
            return True
    except (IOError, json.JSONDecodeError):
        pass
    return False

def load_high_score():
    """Load high score from a file."""
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                return json.load(f).get("high_score", 0)
    except (IOError, json.JSONDecodeError):
        pass
    return 0



def play_game():
    word = fetch_word()
    guessed_letters = set()
    correct_letters = set(word)
    hidden_word = ["_" if letter.isalpha() else letter for letter in word]
    lives = LIVES
    score = 0
    hint_shown = False  # Track if hint was shown
    display_title()
    console.print(f"[bold magenta]High Score: {load_high_score()}[/bold magenta]")

    while lives > 0 and "_" in hidden_word:
        console.print("\n" + " ".join(hidden_word), style="bold yellow")
        console.print(f"Lives: {lives} ❤️ | Score: {score} 🏆", style="bold red")

        guess = console.input("[bold green]Guess a letter: [/bold green]").strip().upper()

        if not guess or len(guess) != 1 or not guess.isalpha():
            console.print("[bold red]Invalid input! Enter a single letter.[/bold red]")
            continue

        if guess in guessed_letters:
            console.print("[bold yellow]You already guessed that letter![/bold yellow]")
            continue

        guessed_letters.add(guess)

        if guess in correct_letters:
            for idx, letter in enumerate(word):
                if letter == guess:
                    hidden_word[idx] = guess
            score += 10
        else:
            lives -= 1
            score -= 5  # Penalty for wrong guess
            console.print(f"[bold red]Wrong guess! {lives} lives remaining.[/bold red]")

            # Show hint after first wrong guess
            if not hint_shown:
                hint = fetch_hint(word)
                console.print(f"[bold blue]💡 Hint: {hint}[/bold blue]")
                hint_shown = True

    # Game Over
    if "_" not in hidden_word:
        console.print(f"\n[bold green]🎉 You won! The word was {word}. Score: {score} 🏆[/bold green]")
    else:
        console.print(f"\n[bold red]💀 Game Over! The word was {word}.[/bold red]")

    # Update high score
    if save_high_score(score):
        console.print("[bold cyan]🎊 New High Score![/bold cyan]")

    # Play again?
    if console.input("[bold magenta]Play again? (y/n): [/bold magenta]").strip().lower() == 'y':
        play_game()

