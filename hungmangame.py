import random  # Used to randomly select a word from the word list
import os      # Used to clear the console for a clean display

# Predefined list of words for the game
WORD_LIST = ["python", "laptop", "elephant", "computer", "mountain"]
# Maximum number of incorrect guesses allowed
MAX_INCORRECT_GUESSES = 6

HANGMAN_STAGES = [
    """
      ┌───────┐
      │       │
      │
      │
      │
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │
      │
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │       │
      │
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │      /│
      │
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │      /│\\
      │
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │      /│\\
      │      /
      │
    ══╧══════════
    """,
    """
      ┌───────┐
      │       │
      │       O
      │      /│\\
      │      / \\
      │
    ══╧══════════
    """,
]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome_message():
    print("=" * 50)
    print("       ★  WELCOME TO HANGMAN  ★")
    print("=" * 50)
    print()
    print("  Guess the hidden word one letter at a time.")
    print("  You have 6 chances before the man is hanged!")
    print()
    print("=" * 50)
    print()

def choose_word():
    return random.choice(WORD_LIST)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def get_guess(guessed_letters):
    while True:
        guess = input("\n  Enter your guess (a single letter): ").strip()
        if len(guess) == 0:
            print("  ⚠  You didn't enter anything. Please type a letter.")
            continue
        if len(guess) != 1:
            print("  ⚠  Please enter only ONE letter at a time.")
            continue
        if not guess.isalpha():
            print("  ⚠  Invalid input! Only letters (a-z) are accepted.")
            continue
        guess = guess.lower()

        if guess in guessed_letters:
            print(f"  ℹ  You already guessed '{guess}'. Try a different letter.")
            return None
        return guess

def update_game(guess, word, correct_guesses, incorrect_guesses):
    if guess in word:
        correct_guesses.append(guess)
        print(f"\n  ✔  Great! '{guess}' is in the word!")
        return True
    else:
        incorrect_guesses.append(guess)
        print(f"\n  ✖  Sorry! '{guess}' is NOT in the word.")
        return False

def display_game_status(word, correct_guesses, incorrect_guesses):
    num_incorrect = len(incorrect_guesses)
    remaining = MAX_INCORRECT_GUESSES - num_incorrect
    print(HANGMAN_STAGES[num_incorrect])
    word_progress = display_word(word, correct_guesses)
    print(f"  Word: {word_progress}")
    print()
    if incorrect_guesses:
        print(f"  Incorrect letters : {', '.join(incorrect_guesses)}")
    else:
        print("  Incorrect letters : (none)")
    print(f"  Remaining attempts: {remaining}")
    print("  " + "─" * 40)

def check_win(word, correct_guesses):
    for letter in word:
        if letter not in correct_guesses:
            return False
    return True

def check_loss(incorrect_guesses):
    return len(incorrect_guesses) >= MAX_INCORRECT_GUESSES

def play_game():
    word = choose_word()
    correct_guesses = []
    incorrect_guesses = []

    while True:
        clear_screen()
        print("=" * 50)
        print("            ★  HANGMAN GAME  ★")
        print("=" * 50)

        display_game_status(word, correct_guesses, incorrect_guesses)

        if check_win(word, correct_guesses):
            print()
            print("  🎉  CONGRATULATIONS! You guessed the word!")
            print(f"  ★   The word was: {word.upper()}")
            print()
            break

        if check_loss(incorrect_guesses):
            print()
            print("  💀  GAME OVER! The man has been hanged.")
            print(f"  ★   The word was: {word.upper()}")
            print()
            break

        guess = get_guess(correct_guesses + incorrect_guesses)
        if guess:
            update_game(guess, word, correct_guesses, incorrect_guesses)

def main():
    clear_screen()
    display_welcome_message()
    input("  Press Enter to start the game...")

    while True:
        play_game()
        while True:
            choice = input("  Do you want to play again? (Y/N): ").strip().upper()
            if choice in ("Y", "N"):
                break
            print("  ⚠  Please enter 'Y' for Yes or 'N' for No.")
        if choice == "N":
            print()
            print("=" * 50)
            print("   Thank you for playing Hangman! Goodbye! 👋")
            print("=" * 50)
            print()
            break

if __name__ == "__main__":
    main()
