# Classic Hangman

> Note: the analysis for this problem must be done individually. Instructions for the analysis are included in the assignments below.
{:.bg-warning}

## tl;dr

Implement a program that allows someone to play the classic Hangman game against the computer.

	$ python hangman.py
	WELCOME TO HANGMAN ツ
	I have a word in my mind of 8 letters.
	Guess a letter: a
	That's not in the word :(
	Guess a letter: n
	It's in the word! :))
	_____N__
	Guess a letter: ...


## Background

In case you aren't familiar with the game Hangman, the rules are as follows:

1. One player chooses a secret word, then writes out a number of dashes equal to the word length.

2. The other player begins guessing letters. Whenever she guesses a letter contained in the hidden word, the first player reveals each instance of that letter in the word. Otherwise, the guess is wrong.

3. The game ends either when all the letters in the word have been revealed or when the guesser has run out of guesses.

Fundamental to the game is the fact the first player accurately represents the word she has chosen. That way, when the other players guess letters, she can reveal whether that letter is in the word.


## Specification

Your assignment is to write a computer program which plays a game of Hangman using the game rules above. In fact, you will be provided with the main program, but all game logic is missing. Your task is to design and implement two classes called `Hangman` and `Lexicon`, which provide all functionality to make the starter code work *without changes*.

- `Lexicon` objects are used to retrieve words for the game from a dictionary. Eventually, the `Lexicon` class will be based on the file `dictionary.txt`, which contains the full contents of the Official Scrabble Player's Dictionary, Second Edition. This word list has over 120,000 words, which should be more than enough for our purposes.

- A `Hangman` object will include all of the logic needed to play the game. It will keep track of the current status of the game, and it will be able to update the status of the game when a letter is guessed. However, a Hangman object will not directly interact with the user (the person playing the game). In other words, it may not use anything like `print` or `input` functions.


## Getting started

Download the word lexicon via:

    mkdir ~/hangman
    cd ~/hangman
    wget https://github.com/minprog/hangman/raw/main/classic/dictionary.zip
    unzip dictionary.zip
    rm -f dictionary.zip

Then create a file called `hangman.py` and add the following code.

    if __name__ == '__main__':
    
        print("WELCOME TO HANGMAN ツ")
    
        # prompt and re-prompt for word length
        word_length = int(input("What length of word would you like to play with?\n"))
        while word_length < 1 or word_length > 44:
            word_length = int(input("Please choose a number between 1 and 44!\n"))
    
        # load words
        lexicon = Lexicon(word_length)
    
        # prompt and re-prompt for number of guesses
        number_guesses = int(input("How many guesses are allowed?\n"))
        while number_guesses <= 0:
            number_guesses = int(input("Negative or zero guesses make no sense.\n"))
    
        # run an infinite number of games
        while True:
        
            # game set-up
            print(f"I have a word in my mind of {word_length} letters.")
            word = lexicon.get_word()
            game = Hangman(word, number_guesses)
        
            # allow guessing and provide guesses to the game
            while game.is_running():
            
                # prompt and re-prompt for single letter
                letter = input(f"Guess a letter ({game.guesses_left} left): ")
                if len(letter) != 1 or not game.is_valid_guess(letter):
                    continue
            
                # provide feedback
                if game.guess(letter):
                    print("It's in the word! :))")
                else:
                    print("That's not in the word :(")
                    
                print(game.current_pattern())
        
            # after game ends, present the conclusion
            if game.won():
                print("Whoa, you won!!! Let's play again.")
            else:
                print(f"Sad, you lost ¯\_(ツ)_/¯. This was your word: {word}")


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

Note that the loading of words was demonstrated in last week's [Python lecture](/lectures/python-david)! It uses a **set** to store words, but that is not necessarily the best choice for this problem. Adapt the code as needed.

Because the `Hangman` class is still missing, you can't really test the `Lexicon` class yet using the started code that we provided. Instead, you can use `check50` to check the basic functionality of your new class:

    check50 -l minprog/hangman/main/classic


## Assignment 3

Now you are going to analyse the `Hangman` class and define an *interface* for it.

1. Peruse the starter code and note how the `Hangman` class is instantiated. What kind of parameters are needed to make a valid instance of `Hangman`?

2. Find all occurrences of the `Hangman` object in the code. What methods are called on this object? What parameters are needed and what should the method return?

3. Draw a UML class from the information that you gathered. Because you're starting out and trying to understand the problem, put as much information in there as possible, including return types and parameters.

4. Think about the internal structure of the class: what variables do you need to support all expected operations? Write your ideas below the diagram.

Finally, take your class diagram and, again, discuss it with a teaching assistant (via Zoom!) before you continue with the next step. Do not share your diagram with other students until after the assignment is fully completed by everyone.

Add your diagram and comments to a file called `analysis.pdf`.


## Assignment 4

Now implement the `Hangman` class. Again, use `check50` to check your progress.


## Assignment 5

What happens when you want to create a Lexicon that does not follow the specifications? For example, what should happen if someone uses your class like the following:

	words = Lexicon(-5)

Try it yourself! Most likely, your code will indeed try to create a Lexicon with a word length of -5. But that is not going not work (ever!).

Because the `Lexicon` object does not interface directly with the user, it makes no sense for it to re-prompt the user for new input. However, it also makes no sense to just continue the program. It would only lead to errors further down the line. We can take this opportunity to proactively check for problems in our code. To do this, we use Python **assertions**. Because we know that the Lexicon can only provide words of certain length, you can add the following assertion to the initialiser:

    assert word_length > 0 and word_length < 44

Putting this simple stament in your code will make sure that Python **halts** the program if at that point the assertion "fails".

Now if for some reason you (or someone else) tries to create a program that creates a Lexicon object using a `length` of -5, Python will halt it immediately. You can then immediately see why it halted: the assertion failed, which means the parameter had an "impossible" value. You can than trace back **why** that parameter was -5 in the first place. Probably a mistake!

Note that `check50` for this problem expects that such assertions are present in your code. In particular, you should **also** handle invalid input for initializing a `Hangman` object and the `guess()` method in `Hangman`, as specified by `check50`.


## Manual testing

Hangman should now be a fully functional game! Test it and double-check if everything is still according to specification. If all is well, congratulations!


## Final testing

Make sure to test one final time before submitting:

    check50 -l minprog/hangman/main/classic


## Submitting

To submit this assignment, you need to submit all of your source files.
