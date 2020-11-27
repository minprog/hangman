import check50
import os
import sys
import random
import string

def raise_timeout():
    raise Exception("Timeout")

@check50.check()
def exists():
    """hangman.py exists"""
    check50.exists("hangman.py")
    check50.include("dictionary.txt")

@check50.check(exists, timeout=3)
def can_import():
    """hangman.py loads without printing anything"""
    res = check50.run('python3 -c "import hangman"').stdout(timeout=2)
    if res != "":
        raise check50.Failure("code produced output when imported.", 
            help='make sure you do not edit the distribution code.')

@check50.check(can_import)
def load_lexicon():
    """lexicon object with 4-letter words can be created"""
    sys.path.append(os.getcwd())
    import hangman
    try:
        Lexicon = hangman.Lexicon
        lex = Lexicon(4)
    except Exception as e:
        error='unable to create a lexicon object using "Lexicon(4)"'
        help=f"got exception {str(e)}."
        raise check50.Failure(error, help=help)

@check50.check(load_lexicon)
def test_lexicon():
    """lexicon object correctly extracts 4-letter words from dictionary.txt"""
    sys.path.append(os.getcwd())
    import hangman
    Lexicon = hangman.Lexicon
    lex = Lexicon(4)

    try:
        word = lex.get_word()
    except Exception as e:
        error='unable to get words of length 4 from lexicon object with "Lexicon.get_word()"'
        help=f"got exception {str(e)}."
        raise check50.Failure(error, help=help)

    ten_words = [lex.get_word() for _ in range(10)]

    if all(ten_words[0] == word for word in ten_words):
        raise check50.Failure('retrieved words are not random', 
            help='Lexicon.get_word() retrieves the same word each time')
    
    if any(len(word) != 4 for word in ten_words):
        raise check50.Failure('retrieved words are not (always) the correct length')

@check50.check(can_import)
def load_hangman():
    """creating a hangman game with parameters word="hello", number_guesses=5 succeeds"""
    sys.path.append(os.getcwd())
    import hangman
    try:
        Hangman = hangman.Hangman
    except Exception as e:
        raise check50.Failure("cannot find the Hangman class")

    try:
        game = Hangman("hello", 5)
    except Exception as e:
        raise check50.Failure('failed to create a Hangman object with ' \
                'word "hello" and 5 guesses',
                help=f'got exception {e}.')

@check50.check(load_hangman)
def empty_game():
    """is_running and won respond correctly for a brand new game"""
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    game = Hangman("hello", 5)
    try:
        running = game.is_running()
        won = game.won()
    except Exception as e:
        raise check50.Failure("unable to call " \
                "won, or is_running on Hangman object",
                help=f"Got the exception {e}")

    for expected, actual, method in [(True, running, "is_running()"), (False, won, "won()")]:
        if expected != actual:
            raise check50.Mismatch(str(expected), str(actual),
                help=f"incorrect return value of Hangman.{method} for new game")

@check50.check(empty_game)
def win_games():
    """it is possible to win a game given enough guesses (26)"""
    for _ in range(5):
        play_game(win=True)

@check50.check(empty_game)
def lose_games():
    """it is possible to lose a game (game is not running and not won) given only 5 guesses"""
    for _ in range(5):
        play_game(win=False)

@check50.check(load_hangman)
def wrong_lexicon():
    """creating a Lexicon with incorrect parameters fails an assertion"""
    sys.path.append(os.getcwd())
    import hangman
    Lexicon = hangman.Lexicon

    params = [-2, 29]
    messages = ["negative word length",
                "word length that does not appear anywhere in the dictionary"]

    for param, message in zip(params, messages):
        lex = None
        try:
            lex = Lexicon(param)
        except AssertionError as e:
            pass
        except Exception as e: 
            raise check50.Failure("got error but not an assertion failure",
                help=f"got exception {e}")

        if lex is not None:
            raise check50.Failure("created a Lexicon object for a " + message)

@check50.check(load_hangman)
def wrong_hangman():
    """creating a Hangman object with incorrect parameters fails an assertion"""
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman

    params = [("hello", 0), ("hello", -1)]
    messages = ["0 guesses, which is too few",
                "-1 guesses, which is too few"]

    for pars, message in zip(params, messages):
        game = None
        try:
            lex = Hangman(*pars)
        except AssertionError as e:
            pass
        except Exception as e: 
            raise check50.Failure("got error but not an assertion failure",
                help=f"got exception {e}")

        if game is not None:
            raise check50.Failure("created a Hangman object for " + message)

@check50.check(load_hangman)
def wrong_guesses():
    """calling hangman.guess() with an incorrect parameter fails an assertion"""
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    game = Hangman("hello", 5)

    inputs = ["blaat", " ", "6"]
    for wrong_input in inputs:
        accepted = True
        try:
            game.guess(wrong_input)
        except AssertionError:
            accepted = False
        except Exception:
            raise check50.Failure(f"got error but not an assertion failure for guess of {repr(wrong_input)}")

        if accepted:
            raise check50.Failure(f"guess of {repr(wrong_input)} was accepted, " \
                    "but any input other than a single letter should fail " \
                    "an assertion")
    try:
        game.guess('A')
    except AssertionError:
        raise check50.Failure(f"first guess of letter 'A' should not raise an AssertionError.")

    accepted = True
    try:
        game.guess('A')
    except AssertionError:
        accepted = False

    if accepted:
        raise check50.Failure("Guessing an already guessed letter should give " \
                "an AssertionError.")

def play_game(win):
    """Win a game (given enough guesses)."""
    word = ""
 
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    if win:
        word = "hello"
        game = Hangman(word, 26)
    else:
        word = "supercalifragilisticexpialidocious"
        game = Hangman(word, 5)
    
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    guesses = []
    num_wrong_guesses = 0

    for letter in alphabet:
        guesses.append(letter)
        
        remaining = game.guesses_left
        game.is_valid_guess(letter)

        if game.guesses_left != remaining:
            error = "state changes after calling Hangman.is_valid_guess()"
            help = f"Hangman.is_valid_guess() is not to supposed to update anything, only to check if a guess would be valid"
            raise check50.Failure(error, help=help)
        
        correct = game.guess(letter)
        if not correct:
            num_wrong_guesses += 1

        if len(game.current_pattern()) != len(word):
            error = "invalid pattern length"
            help = f"used word {word} but got a pattern of length {len(game.current_pattern())}"
            raise check50.Failure(error, help=help)

        if correct != (letter in game.current_pattern().lower()):
            error = "The return value of game.guess(letter) should be True if " \
                    "the guess was correct, and False otherwise."
            help = f'Got the return value {correct}.'
            raise check50.Failure(error, help=help)

        if not all(x in guesses for x in game.current_pattern().lower() if x != "_"):
            error = "The game pattern contains characters other than guessed " \
                    "letters and underscores."
            help = f"I found pattern {game.current_pattern()} with guesses " \
                   f"{''.join(guesses)}."
            raise check50.Failure(error, help=help)
        
        if not game.is_running():
            break
        
        if not win and num_wrong_guesses >= 5:
            error = "The game is not finished, but I should have run out of " \
                    "guesses."
            help = "I started a game with 5 guesses, and after 5 wrong guesses " \
                   "I am still playing."
            raise check50.Failure(error, help=help)
    else:
        error = "The game is not finished, but I guessed every letter in the " \
                "alphabet."
        help = "Did you implement game.is_running() correctly?"
        raise check50.Failure(error, help=help)
    
    if win: 
        if game.won() != True:
            error = "I did not win the game, even while guessing all 26 letters " \
                    "in the alphabet."
            help = "Did you implement game.won() correctly?"
            raise check50.Failure(error, help=help)

        if "_" in game.current_pattern():
            error = "Blanks in pattern after victorious game."
            help = f"Expected a full word, but the pattern is {game.current_pattern()}."
            raise check50.Failure(error, help=help)

    else:
        if game.won() != False:
            error = "Won the game with 5 random guesses for a " \
                    "12-letter word."
            help = "Did you implement game.won() correctly?"
            raise check50.Failure(error, help=help)

        if not "_" in game.current_pattern():
            error = "The game's pattern is filled in, even though I lost."
            help = f"Got pattern {game.current_pattern()}, expected a pattern with "\
                    "underscores."
            raise check50.Failure(error, help=help)
