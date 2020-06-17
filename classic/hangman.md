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

Your assignment is to write a computer program which plays a game of Hangman using this "Evil Hangman" algorithm. In particular, your program should do the following:

1. Read the file `dictionary.txt`, which contains the full contents of the Official Scrabble Player's Dictionary, Second Edition. This word list has over 120,000 words, which should be more than enough for our purposes.

2. Prompt the user for a word length, reprompting as necessary until she enters a number such that there's at least one word that's exactly that long. That is, if the user wants to play with words of length -42 or 137, since no English words are that long, you should reprompt her.

3. Prompt the user for a number of guesses, which must be an integer greater than zero. Don't worry about unusually large numbers of guesses – after all, having more than 26 guesses is clearly not going to help your opponent!

4. Play a game of Hangman as described below:

	1.  Choose a random dictionary word of the requested length.

	2.  Print out how many guesses the user has remaining, along with any letters the player has guessed and the current blanked-out version of the word.

	3.  Prompt the user for a single letter guess, reprompting until the user enters a letter that she hasn't guessed yet. Make sure that the input is exactly one character long and that it's a letter of the alphabet.

	4.  Check if the word contains that guessed letter, and update the user with a blanked-out version of the word - but with the new letter now filled in.

	5.  If the player has run out of guesses, pick a word from the word list and display it as the word that the computer initially "chose."

	6.  If the player correctly guesses the word, congratulate her.

		Ask if the user wants to play again and loop or exit accordingly.


## Architecture

Your program will consist of three major parts.

1. The Lexicon class: Lexicon objects are used to retrieve words for the game from a dictionary.

2. The Hangman class: a *Hangman* object will include all of the logic needed to play the Hangman game. It will keep track of the current status of the game, and it will be able to update the status of the game when a letter is guessed. However, a Hangman object will not directly interact with the user (the person playing the game).

3. The user interface: this is a piece of code that interacts with the user. It displays messages to the user about the game, and prompts her for new guesses. This piece of code will use the Hangman class to keep track of the game itself.

For the Lexicon and Hangman classes, we will prescribe how they should work, like in previous assignments. They can be checked with `check50`. For the user interface, you have some freedom, but be careful to stick to the specification.

By the way, watch out for gaps in the dictionary. When the user specifies a word length, you will need to check that there are indeed words of that length in the dictionary. You might initially assume that if the requested word length is less than the length of the longest word in the dictionary, there must be some word of that length. Unfortunately, the dictionary contains a few "gaps." The longest word in the dictionary has length 29, but there are no words of length 26. Be sure to take this into account when checking if a word length is valid.


## Steps

### 0. Before you get started

Testing for this assignment will again work automatically. Because you are going to write classes, it is now possible to test each class's functionality separately from the other parts of the program.

### 1. The `Lexicon` class

The first thing to implement is a class called `Lexicon`, which has the responsibility of managing the full word list and extracting words of a given length. It can be loaded once and asked for words whenever a new game is started.

Download the lexicons via:

	cd ~/module8
	wget https://prog2.mprog.nl/course/problems/hangman-classic/dictionary.zip
	unzip dictionary.zip
    rm -f dictionary.zip

Create a file called `hangman.py` and add a `Lexicon` class. This class should have two methods: `__init__()` to initialize, and `get_words()` to extract a list of words with a  specific length to play Hangman:

    import random
    
    class Lexicon:

        def __init__(self):
            self.words = []
            # Load the dictionary of words.
            # TODO

        def get_words(self, length):
            # Return a list of all words from the dictionary of the given length.
            # TODO

        def get_word(self, length):
            # Return a single random word of given length. Uses `get_words` above.
            return random.choice(self.get_words(length))

In our code, we will use a **list** to store the master word list. That's why we have `self.words = []` at the top of the initializer method.

Now, implement those two methods.

> Note that the loading of words was demonstrated in last week's [Python lecture](/lectures/python)! It uses a **set** to store words, but you can modify it to use a list instead. Recall how to add items to a list?

### 2. Testing the `Lexicon`

Before we move on to the next step, we want to test if the class is working correctly. For example, try to get words of length 8 and see if the result seems reasonable. Start Python *interactively* using:

	python -i hangman.py

If you followed step 0 correctly, it should just load the Lexicon class and do nothing else. Then you could try some of the following.

	lex = Lexicon()
	lex.get_word(8)
	lex.get_word(8)
	lex.get_word(8)

Check if everything is in order. Are the words reasonable, i.e., of the right length? Do you get a different word each time? If something is still wrong, consider testing `get_words()` specifically, instead of `get_word()`. For example, if you `print(lex.get_words(2))`, are all printed words of length 2?

> You should not put testing code like the above in `hangman.py` like you might have done in earlier assignments. This is because `check50` should be able to load your program and perform its own tests. Your tests would interfere with the checks. This is why `python -i` is a handy tool for testing.

You can now test using `check50` for the first time!

	check50 minprog/cs50x/2019/hangman/classic --local

### 3. The `Hangman` class

So now we have a class to manage the word list. We can also create a class that manages playing a game of Hangman. Let's think about what is needed to "play" a game.

-   First of all, a game is played based on a particular word length. Also, we decide upfront how many guesses will be allowed. These two are the only pieces of information that a Hangman game object needs to get started. This means that we know how it may be eventually initialized:

        game = Hangman(length=8, num_guesses=5)

-   Second, we need a method to enter a guess. Maybe we'd like to try the letter A:

		game.guess("a")

So that specifies how the class should work when testing. Here's a minimal skeleton, which you should copy-paste below your `Lexicon` class.

    class Hangman:
        def __init__(self, length, num_guesses):
            # Initialize game by choosing a word and creating an empty pattern.
            self.length = length
            self.num_guesses = num_guesses
            # TODO

        def guess(self, letter):
            # Update the game for a guess of letter. Return True if the letter
            # is added to the pattern, return False if it is not.
            # TODO

        def pattern(self):
            # Return a nice version of the pattern, for printing.
            # TODO

To implement it, consider the following:

For the initializer:

1.  you need to create a variable to contain the random word. You should instantiate a Lexicon object and ask it for that word.

2.  you need a variable to hold the "pattern" of guessed letters. Initially, this should simply be an array of N underscores, where N is the chosen word length. For example, if the length is 4, the empty pattern should be the array `["_", "_", "_", "_"]`.

    > We choose an array here instead of a string because the array is **mutable**. We would like to add guessed letters to the pattern as the game progresses, so we need to mutate (change) the array.

3.  you need a variable to hold the letters that have been guessed. For the same reason as above, you should use an array, adding guessed letters as the game progresses.

For the `guess` method:

1.  you need to add the letter to the list of "guessed" letters, so we keep track of all earlier guesses.

1.  you need to see if the chosen letter occurs somewhere in the random word. The letter may occur more than once! Wherever it occurs, that letter should replace the `_` in the pattern.

2.  you need to make sure that you `return` either True or False depending on whether the letter was indeed found in the word (at least once).

For the `pattern` method:

1.  you need to create a string version of the pattern, because it's an ugly list. When printing, it should be nicely readable. In this case, feel free to use an internet search for [list to string python](https://duckduckgo.com/?q=list+to+string+python).


### 4. Testing the `Hangman` game

Let's test our game logic. We should be able to start a new game, and repeatedly guess letters. Again, run

    python -i hangman.py

and enter the following commands, or a variation thereof:

	game = Hangman(8, 6)
	game.guess("e")
	print(game.pattern())
    game.guess("a")
	print(game.pattern())
    game.guess("o")
    game.guess("i")
    game.guess("u")
	print(game.pattern())

Does it all seem reasonable? Feel free to add a `print` somewhere to debug your code (for example, to show the chosen random word as the game starts). As long as you remove the prints before going to the next section!


### 5. Winning

A user should be able to win or lose the game, and our computer version should be able to check if a game has been won or lost. Let's add a few methods to the `Hangman` class:

    def won(self):
        # Return True if the game is finished and the player has won, 
        # otherwise False.
        # TODO

When has the game been won? Think about it. You should be able to program this method without introducing new `self` variables, but instead, calculating if the game has been won by checking out the letters in `self.guessed`.

    def lost(self):
        # Return True if the game is finished and the player has lost, 
        # otherwise False.
        # TODO

And for this method the same applies: you should be able to calculate if the game has been lost by checking the number of previously guessed letters, and comparing to `self.num_guesses`.

    def finished(self):
        # Return True if the game is finished, otherwise False.
        # TODO

Finally, `finished` may be used to check if any more input is allowed. If the game has either been lost or won, it is also finished. So feel free to use the `lost()` and `won()` methods to decide!


### 6. Testing the `Hangman` game again

Let's test our game logic. We should be able to start a new game, and repeatedly guess letters. Again, run

    python -i hangman.py

and enter the following commands, or a variation thereof:

	game = Hangman(8, 6)
	game.guess("e")
	print(game)
    game.guess("a")
	print(game)
    print(game.finished())
    game.guess("o")
    game.guess("i")
    game.guess("u")
    print(game)

For automatic testing, we'd like to gain a more in-depth look into your algorithms. Add the following method, which should provide upon request the full list of previously guessed letters, in order:

    def guessed_string(self):
        # Produce a string of all letters guessed so far, in the order they
        # were guessed.
        # TODO

And having done that, this may be the time to run `check50` again.


### 7. Debugging with assertions

What happens when you want to create a Hangman game that does not follow the specifications? For example, what should happen if someone uses your class like the following:

	game = Hangman(-5, 6)

Try it yourself! Most likely, your code will indeed try to create a hangman game with a word of length -5. But that is not going not work (ever!).

Because the `Hangman` object does not interface directly with the user, it makes no sense for it to re-prompt the user for new input. However, it also makes no sense to just continue the program. It would only lead to errors further down the line. We can take this opportunity to proactively check for problems in our code. To do this, we use Python **assertions**. To create an assertion, we need to understand what would be *correct* input. We have two parameters that influence the inner workings of the Hangman object:

- The parameter `length` is the length of a word to play Hangman with. Negative length is not going to work - and 0-length words will not lead to a working game either. Other options we have to think about a little bit harder: is a game for words of size 1 fun? Do 1-letter words even exist? You can check that yourself. The same goes for 2-letter words. And at the other end you could check that the `length` isn't much longer than the maximum 'length' that corresponds with the longest word from the dictionary.

- For `num_guesses` you should also think about what realistic input would be. But don't take it too far. We're mostly looking to constrain the parameters to *sane* values - values that make sure the program/algorithm will not crash and will provide the "right answer".

After having defined those constraints, you can formulate an assertion:

    assert length > [MIN] and length < [MAX]

Putting this simple stament in your code will make sure that Python halts the program if at that point the assertion "fails". Of course, [MIN] and [MAX] should be replaced with the actual minimum and maximum values you want to enforce.

    class Hangman:
        def __init__(self, length, num_guesses):
            assert length > [MIN] and length < [MAX]
            # ... and here follows other code.

Now if for some reason you (or someone else) tries to create a program that creates a Hangman object using a `length` of -5, Python will halt it immediately. You can then immediately see why it halted: the assertion failed, which means the parameter had an "impossible" value. You can than trace back **why** that parameter was -5 in the first place. Probably a mistake!

Note that `check50` for this problem expects that such assertions are present in your code. In particular, you should **also** handle invalid input for the `guess()` method, as specified by `check50`.


### 8. Implementing user interaction

While the `Hangman` class has all you need to play Hangman, someone who does not know your program won't understand that you have to write things like `game = Hangman(8, 6)` to start a game and `game.guess("e")` to guess a letter. So, let's make a **user interface**.

Your user interface should at least:

1. Prompt the user for how many letters the Hangman word should have. If the input is not a positive integer, or there is no word with that many letters, repeat the prompt until you get correct input.

2. Prompt the user for how many guesses she should get until she loses. This should be a positive integer.

4. Play the game: repeatedly do the following

    1. Prompt the user for a guess. The guess should be a single letter that
       has not yet been guessed.

    2. Show an updated pattern, and the number of guesses remaining.

    4. If the game has finished, either congratulate the player (on a win), or
       tell the player the Hangman word (any word that is consistent with the
       current pattern). Then ask the player if she wants to play again.

Like in "Game of Cards", the game code should be added inside an `if __name__ == '__main__':` condition. This ensures that that code will not run when checking, but will run when you test the program yourself using `python hangman.py`.


## Testing

	check50 minprog/cs50x/2019/hangman/classic --local


## Submitting

To submit this assignment, you need to submit all of your source files.
