# py-mancala

This is an implementation of [MiniMax algorithm](https://en.wikipedia.org/wiki/Minimax) with [alpha-beta prunning](https://en.wikipedia.org/wiki/Alpha–beta_pruning) in [Python 3](https://www.python.org) for creating AI capable of playing a [Mancala game](http://boardgames.about.com/cs/mancala/ht/play_mancala.htm). Implementation makes use of [multiprocessing python module](https://docs.python.org/3.5/library/multiprocessing.html), which overcome the GIL limitation and uses multiple processes to calculate best moves. This way it uses all available CPU.

## Usage

Run ./mancala.py and it will start game simulation console.
