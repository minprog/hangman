# Classic Hangman

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

Your assignment is to write a computer program which plays a game of Hangman using the game rules above. In fact, you will be provided with the main program, but all **game logic** is missing. Your task is to design and implement two classes called `Hangman` and `Lexicon`, which together provide all functionality to make the starter code work *without any changes*.

- Objects of class `Lexicon` are used to retrieve words for the game from a dictionary. The `Lexicon` class will be based on the file `dictionary.txt`, which contains the full contents of the Official Scrabble Player's Dictionary, Second Edition. This word list has over 120,000 words, which should be more than enough for our purposes.

- Objects of class `Hangman` will include all of the logic needed to play a single game. The objects keep track of the current status of the game, and are able to update the status of the game when a letter is guessed. However, a Hangman object will not directly interact with the "user" (the person playing the game via the keyboard). In other words, it may not use anything like `print` or `input` functions.


## Getting started

On Linux, WSL or Mac, download the word lexicon via:

    curl -LO https://github.com/minprog/hangman/raw/2020/classic/dictionary.zip
    unzip dictionary.zip
    rm -f dictionary.zip

If you're not using on of those operating systems, copy the link and download the dictionary zip using it.

Then create a file called `hangman.py` and add the following code.

    if __name__ == '__main__':
    
        print("WELCOME TO HANGMAN ツ")
    
        # prompt and re-prompt for word length
        word_length = int(input("What length of word would you like to play with?\n"))
        while word_length > 44:
            word_length = int(input("No words are longer than 44 letters!\n"))
    
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
                letter = input(f"Guess a letter ({game.guesses_left()} left): ")
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

(This code does not contain any type hints. Your classes should contain type hints though!)


## Assignment 1

Your first task is to understand what the `Lexicon` class should look like and define an *interface* for it (recall from Queue that an interface is defined by the *operations* that are supported by a class).

1. Deeply study the starter code and make note in particular of how the `Lexicon` class is instantiated. What kind of parameter is needed to make a valid instance of `Lexicon`?

2. Find all occurrences of the `Lexicon` object in the code (only a single instance is ever made). What methods are called on this object? What parameters are needed and what should the method return?

3. Draw your class in UML class diagram format. Because you're just starting out and trying to understand the problem, put as much information in there as possible, including return types and parameters. In other words, the UML diagram should contain *implementation details*.

4. Think about the internal structure of the class: what variables do you need to support all expected operations? Write your ideas below the diagram.

Do not share your diagram with other students until after the assignment is fully completed by everyone.

Add your diagram and the answers the the questions to a file called `analysis.pdf`. You will add more to it in assignment 3.


## Assignment 2

Having created your diagram, you can implement your `Lexicon` class. Place it inside the `hangman.py` source file above the started code.

In the initializer for `Lexicon`, load words from `dictionary.txt`. The following code can be 

    words = set()
    file = open('dictionary.txt', "r")
    for line in file:
        words.add(line.rstrip())
    file.close()

Make sure that all words of the right length are stored in an instance variable in `Lexicon`. Then complete the remainder of the class (using what you know from studying the `main` code).

Because the `Hangman` class is still missing, you can't really test the `Lexicon` class yet using the started code that we provided, because it will crash. Instead, you may submit your file to check the basic functionality of just the `Lexicon` class. It should yield these positive results:

    :) hangman.py exists
    :) hangman.py loads without printing anything
    :) lexicon object with 4-letter words can be created
    :) lexicon object correctly extracts 4-letter words from dictionary.txt


## Assignment 3

Now you are going to analyse the `Hangman` class and define an *interface* for it.

1. Peruse the starter code and note how the `Hangman` class is instantiated. What kind of parameters are needed to make a valid instance of `Hangman`?

2. Find all occurrences of the `Hangman` object in the code. What methods are called on this object? What parameters are needed and what should the method return?

3. Draw a UML class diagram from the information that you gathered. Because you're starting out and trying to understand the problem, put in all known implementation details.

4. Think about the internal structure of the class: what variables do you need to support all expected operations? Write your ideas below the diagram.

Again, do not share your diagram with other students until after the assignment is fully completed by everyone.

Add your complete diagram and the answers to the questions to a file called `analysis.pdf`.


## Assignment 4

Now implement the `Hangman` class. You can submit your solution to check your progress.


## About assertions

In some sense of the word, your implementation is now done! You should at the very least try it out and see if all is working well. However, automatic testing can only check a limited number of requirements, and it will not always find all bugs. So testing manually is always important. And indeed, we will find that we are able to crash the program!

### Debugging a crash

As we put our game in front of different people, it appears that they are still able to crash it. In particular, the program does not check for negative word lengths. And indeed, when you run your program and provide word length -1, it accepts the number. Unfortunately, while this does not immediately prove to be a problem, the program crashes as soon as the actual game starts.

Have a good look at what happens:

     1 WELCOME TO HANGMAN ツ
     2 What length of word would you like to play with?
     3 -1
     4 How many guesses are allowed?
     5 10
     6 I have a word in my mind of -1 letters.
     7 Traceback (most recent call last):
     8   File "hangman.py", line 115, in <module>
     9     word = lexicon.get_word()
    10   File "hangman.py", line 35, in get_word
    11     return random.choice(self.words)
    12   File "lib/python3.8/random.py", line 290, in choice
    13     raise IndexError('Cannot choose from an empty sequence') from None
    14 IndexError: Cannot choose from an empty sequence

Bummer! A generic error, "Cannot choose from an empty sequence". But what is the **root cause** of our bug? It not immediately obvious from the traceback above.

What you can see on line 11 is that the crash happens in our function `get_word()` when it tries to select a random word. From the error message on line 14 you might understand that `self.words` is an `empty sequence`, or in other words, an list with no words in it.

But that is not the root cause! We must now ask: why was that list empty in the first place? And finally, after some back and forth, you might find that the root cause of the problem is that the class allowed itself to be instantiated with a word length of -1. You've had to take a deep dive into the code to understand that if you didn't know the answer already.

### Fixing the bug

Now an obvious fix is to change the main code (that we provided) to ensure that your game player enters a word length of at least 4 (or so). That might make a nicer game and is a good idea in any case. Fine!

But can't we also prevent the `Lexicon` initialiser from accepting invalid word lengths? It would be much easier to debug our program when this class simply does not accept negative word lengths. And indeed, there is a thing called an **assertion** that we can use. Just add the following line to the very top of the `Lexicon` initialiser:

    assert word_length > 0 and word_length < 44, "Invalid word length for Lexicon"

(Note that we assume your parameter is called `word_length`, but it's fine if it is something else. Just change the assertion in that case.)

Putting this simple stament in your code will make sure that Python "halts" (crashes) the program if at that point the assertion "fails", so to say. In that case the program will not even reach the point of choosing a word from an empty list:

      1 WELCOME TO HANGMAN ツ
      2 What length of word would you like to play with?
      3 -1
      4 Traceback (most recent call last):
      5   File "hangman.py", line 103, in <module>
      6     lexicon = Lexicon(word_length)
      7   File "hangman.py", line 20, in __init__
      8     assert length > 0 and length < 44, "Invalid word length for Lexicon"
      9 AssertionError: Invalid word length for Lexicon

In sharp contrast to the error above, we are now immediately confronted with the root cause of the crash: we tried to instantiate the `Lexicon` class with an invalid word length.


## Assignment 5

The checks for this problem expect that some assertions are present in your code. In particular, you should not only insert the assertion for word length but **also** handle invalid input for initialising a `Hangman` object and the `guess()` method in `Hangman`. If you submit your solution on the website, it might provide some hints as to what assertions could be made.


## Manual testing

Hangman should now be a fully functional game that is also somewhat easier to debug. Test it and double-check if everything is still according to specification. If all is well, congratulations!


## Submitting

To submit this assignment, submit your UML diagrams in a PDF called analysis.pdf, together with your code.
