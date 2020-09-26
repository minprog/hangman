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

	2.  Print out how many **wrong** guesses the user has remaining, along with any letters the player has guessed and the current blanked-out version of the word.

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
        while word_length > 0 and word_length < 45:
            word_length = int(input("Please choose a number between 1 and 44!\n"))
    
        # load words
        lexicon = Lexicon(word_length)
    
        # prompt and re-prompt for number of guesses
        number_guesses = int(input("How many guesses are allowed?\n"))
        while number_guesses > 0:
            number_guesses = int(input("Negative guesses makes no sense.\n"))
    
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
                if len(letter) != 1 or game.allows(letter):
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
                print("Sad, you lost ¯\_(ツ)_/¯. This was your word: {word}")

## What to do

Your task is to design and implement two classes called `Hangman` and `Lexicon`, which provide all functionality to make the starter code work without changes.

In order to allow you to check on your progress, we have provided a check50. 


- The first thing to implement is a class called `Lexicon`, which has the responsibility of managing the full word list and extracting words of a given length. It can be loaded once and asked for a word whenever a new game is started.

  > Note that the loading of words was demonstrated in last week's [Python lecture](/lectures/python)! It uses a **set** to store words, but you can modify it to use a list instead. Recall how to add items to a list?

- You can now test using `check50` for the first time!

	    check50 minprog/cs50x/2019/hangman/classic --local

- So now we have a class to manage the word list. We can also create a class that manages playing a game of Hangman. Let's think about what is needed to "play" a game.

- TEST

- 

### 7. Debugging with assertions

What happens when you want to create a Hangman game that does not follow the specifications? For example, what should happen if someone uses your class like the following:

	game = Hangman(-5, 6)

Try it yourself! Most likely, your code will indeed try to create a hangman game with a word of length -5. But that is not going not work (ever!).

Because the `Hangman` object does not interface directly with the user, it makes no sense for it to re-prompt the user for new input. However, it also makes no sense to just continue the program. It would only lead to errors further down the line. We can take this opportunity to proactively check for problems in our code. To do this, we use Python **assertions**. To create an assertion, we need to understand what would be *correct* input. We have two parameters that influence the inner workings of the Hangman object:

- The parameter `length` is the length of a word to play Hangman with. Negative length is not going to work - and 0-length words will not lead to a working game either. Other options we have to think about a little bit harder: is a game for words of size 1 fun? Do 1-letter words even exist? You can check that yourself. The same goes for 2-letter words. And at the other end you could check that the `length` isn't longer than say... 10?

- For `num_guesses` you should also think about what realistic input would be. But don't take it too far. We're mostly looking to constrain the parameters to *sane* values - values that make sure the program/algorithm will not crash and will provide the "right answer".

After having defined those constraints, you can formulate an assertion:

    assert length > 0 and length < 10

Putting this simple stament in your code will make sure that Python halts the program if at that point the assertion "fails".

    class Hangman:
        def __init__(self, length, num_guesses):
            assert length > 0 and length < 10
            # ... and here follows other code.

Now if for some reason you (or someone else) tries to create a program that creates a Hangman object using a `length` of -5, Python will halt it immediately. You can then immediately see why it halted: the assertion failed, which means the parameter had an "impossible" value. You can than trace back **why** that parameter was -5 in the first place. Probably a mistake!

Note that `check50` for this problem expects that such assertions are present in your code. In particular, you should **also** handle invalid input for the `guess()` method, as specified by `check50`.


## Testing

	check50 minprog/cs50x/2020/hangman/classic --local


## Submitting

To submit this assignment, you need to submit all of your source files.
