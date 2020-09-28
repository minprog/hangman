# Classic Hangman

> Note: the analysis for this problem must be done individually. Instructions for the analysis are included in the assignments below.
{:.bg-warning}

## tl;dr

Implement a program that allows someone to play the classic Hangman game against the computer.

	$ python hangman.py
	WELCOME TO HANGMAN ツ
	What length of word would you like to play with?
	8
	How many guesses are allowed?\n
	5
	I have a word in my mind of 8 letters:
	________
	Guess a letter: a
	The letter "a" is not in the word, you have 4 guesses left.
	________
	Guess a letter: n
	Good guess! "n" is in the word! :))
	_____N__
	Guess a letter:


## Background

In case you aren't familiar with the game Hangman, the rules are as follows:

1. One player, the computer in this assignment, chooses a secret word, then writes out a number of dashes equal to the word length.

2. The other player begins guessing letters. Whenever she guesses a letter contained in the hidden word, the first player reveals each instance of that letter in the word. Otherwise, the guess is wrong.

3. The game ends either when all the letters in the word have been revealed or when the guesser has run out of guesses.


## Specification

Your assignment is to write a Python program that plays a game of Hangman. To help you with this, the skeleton of the program is provided to you, but all the game logic is missing. Your task then is to design and implement two classes called `Hangman` and `Lexicon`, in such a way that they provide all functionality needed to make the starter code work *without making any changes to the starter code*. The design is as follows:

- `Lexicon` objects are used to retrieve words for the game from a dictionary. Eventually, the `Lexicon` class will be based on the file `dictionary.txt`, which contains the full contents of the Official Scrabble Player's Dictionary, Second Edition. This word list has over 120,000 words, which should be more than enough for our purposes.

- A `Hangman` object includes all of the logic needed to play the game. It keeps track of the current status of the game, and it is able to update the status of the game when a letter is guessed. However, a Hangman object will not directly interact with the user (the person playing the game). In other words, it does display output via `print` or ask for input via `input`. Other parts of the code handle that logic.


## Getting started

Download the word lexicon via:

    mkdir ~/hangman
    cd ~/hangman
    wget https://github.com/minprog/hangman/raw/main/classic/dictionary.zip
    unzip dictionary.zip
    rm -f dictionary.zip

Then create a new file called `hangman.py` and add the following code.

		MIN_WORD_LENGTH = 1
		MAX_WORD_LENGTH = 44


		def prompt_word_length():
				"""Prompt and re-prompt for word length."""
				word_length = int(input("What length of word would you like to play with?\n"))
				while word_length < MIN_WORD_LENGTH or word_length > MAX_WORD_LENGTH:
						word_length = int(input("Please choose a number between 1 and 44!\n"))
				return word_length


		def prompt_number_guesses():
				"""Prompt and re-prompt for number of guesses."""
				number_guesses = int(input("How many guesses are allowed?\n"))
				while number_guesses > 0:
						number_guesses = int(input("Negative guesses makes no sense.\n"))
				return number_guesses


		def prompt_guess(game):
				"""Prompt and re-prompt for a guess."""
				letter = input(f"Guess a letter ({game.guesses_left} left): ")

				# re-prompt in case the player makes an illegal guess
				while len(letter) != 1 or game.allows(letter):

						# remind the player of previously guessed letters
						if not game.allows(letter):
								print(f'You have already guessed the letter "{letter}" before')

						letter = input(f"Guess a letter ({game.guesses_left} left): ")

				return letter


    if __name__ == '__main__':
        print("WELCOME TO HANGMAN ツ")

				# prompt the player for the length of the word
        word_length = prompt_word_length()

        # load words
        lexicon = Lexicon(word_length)

        # prompt and re-prompt for number of guesses
        number_guesses = prompt_number_guesses

        # run an infinite number of games
        while True:

            # pick a word from the lexicon
            word = lexicon.get_word()
            print(f"I have a word in my mind of {len(word)} letters:")
						print(game.current_pattern())

						# set up the game
            game = Hangman(word, number_guesses)

						# play the game
            while game.is_running():

                # prompt and re-prompt for a guess (single letter)
                guess = prompt_guess(game)

                # provide feedback on the guess
                if game.guess(letter):
                    print(f'Good guess! "{letter}" is in the word! :)')
                else:
                    print(f'The letter "{letter}" is not in the word, you have {game.number_guesses} left.')

								print(game.current_pattern())

            # after game ends, present the conclusion
            if game.won():
                print("Whoa, you won!!! Let's play again.")
            else:
                print(f"Aw, you lost ¯\_(ツ)_/¯. This was your word: {word}")


## Assignment 1

Your first task is to understand what the `Lexicon` class should look like and define an *interface* for it (recall from Queue that an interface is defined by the *operations* that are supported by a class).

1. Peruse the starter code and note how the `Lexicon` class is instantiated. What kind of parameter is needed to make a valid instance of `Lexicon`?

2. Find all occurrences of the `Lexicon` object in the code. What methods are called on this object? What parameters are needed and what should the method return?

3. Draw a UML class from the information that you gathered. Because you're starting out and trying to understand the problem, put as much information in there as possible, including return types and parameters.

4. Think about the internal structure of the class: what variables do you need to support all expected operations? Write your ideas below the diagram.

Finally, take your class diagram and discuss it with a teaching assistant (via Zoom!) before you continue with the next step. Do not share your diagram with other students until after the assignment is fully completed by everyone.

Add your diagram and comments to a file called `analysis.pdf`. You will add more to it in assignment 3.


## Assignment 2

Having discussed your diagram and having changed it depending on the feedback and questions from your teaching assistant, you can implement your `Lexicon` class. Place it inside the `hangman.py` source file.

Note that the loading of words was demonstrated in last week's [Python lecture](/lectures/python-david)! It uses a **set** to store words, but that is not necessarily the best choice for this problem. Adapt the code from the lecture as needed.

Because the `Hangman` class is still missing, you can't really test the `Lexicon` class just yet using the started code that we provided. Instead you need to test the code yourself. To do this create a new file called `test_lexicon.py` and paste the following code in it:


		import hangman

		word_length = 5
		lexicon = Lexicon(word_length)
		word = lexicon.get_word()
		assert len(word) == word_length


This code makes use of Python **assertions** to assert that this piece of code behaves as expected. In this code the code checks whether the word coming out of the lexicon is of the same length as provided to the lexicon. If it's not, the assertion will fail and the program will halt.

Now add several assertions of your own to `test_lexicon.py` to test:

* Whether the word from the lexicon is actually a word from the dictionary.
* A new word is provided on each call to `get_word()`.

Don't worry about edge cases such as a negative `word_length` just yet, you will create safeguards for such cases in assignment 5.


## Assignment 3

Now you are going to analyse the `Hangman` class and define an *interface* for it.

1. Peruse the starter code and note how the `Hangman` class is instantiated. What kind of parameters are needed to make a valid instance of `Hangman`?

2. Find all occurrences of the `Hangman` object in the code. What methods are called on this object? What parameters are needed and what should the method return?

3. Draw a UML class from the information that you gathered. Because you're starting out and trying to understand the problem, put as much information in there as possible, including return types and parameters.

4. Think about the internal structure of the class: what variables do you need to support all expected operations? Write your ideas below the diagram.

Finally, take your class diagram and, again, discuss it with a teaching assistant (via Zoom!) before you continue with the next step. Do not share your diagram with other students until after the assignment is fully completed by everyone.

Add your diagram and comments to a file called `analysis.pdf`.


## Assignment 4

Now implement the `Hangman` class. Again, create a new file called `test_hangman.py` and write several test cases using assertions for the hangman class. Be sure to test at least whether:

* Correct guesses are accepted.
* The pattern changes depending on the guesses made.
* The number of guesses decreases.

## Assignment 5

What happens when you want to create a Lexicon that does not follow the specifications? For example, what should happen if someone uses your class like the following:

	words = Lexicon(-5)

Try it yourself! Most likely, your code will indeed try to create a Lexicon with a word length of -5. But that is not going not work (ever!).

Because the `Lexicon` object does not interface directly with the user, it makes no sense for it to re-prompt the user for new input. However, it also makes no sense to just continue the program. It would only lead to errors further down the line. We can take this opportunity to proactively check for problems in our code. To do this, we use Python **assertions**. Because we know that the Lexicon can only provide words of certain length, you can add the following assertion to the initializer:

    assert word_length < MIN_WORD_LENGTH or word_length > MAX_WORD_LENGTH

Putting this simple statement in your code will make sure that Python **halts** the program if at that point the assertion "fails".

Now if for some reason you (or someone else) tries to create a program that creates a Hangman object using a `length` of -5, Python will halt it immediately. You can then immediately see why it halted: the assertion failed, which means the parameter had an "impossible" value. You can than trace back **why** that parameter was -5 in the first place. Probably a mistake!

Add assertions in places where your code takes input from other parts of the program. In particular the `__init__` methods of `Lexicon` and `Hangman`, and the `guess()` method of `Hangman`.

Note that `check50` for this problem expects that such assertions are present in your code.


## Manual testing

Hangman should now be a fully functional game! Test it and double-check if everything is still according to specification. If all is well, congratulations!


## Final testing

Make sure to test one final time before submitting:

    check50 -l minprog/cs50x/2020/hangman/classic


## Submitting

To submit this assignment, you need to submit all of your source files.
