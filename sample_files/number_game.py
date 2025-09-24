import random

def number_guessing_game():
    number = random.randint(1, 10)
    print("I'm thinking of a number between 1 and 10. Can you guess it?")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            if guess < 1 or guess > 10:
                print("Please guess a number between 1 and 10.")
                continue
        except ValueError:
            print("That's not a valid number. Please enter an integer between 1 and 10.")
            continue

        if guess == number:
            print("Congratulations! You guessed it right!")
            break
        else:
            print("Try again.")

if __name__ == "__main__":
    number_guessing_game()
