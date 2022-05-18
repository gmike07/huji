import sys
from PCF.pacman import runGames, readCommand

if __name__ == '__main__':
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGames(**args)
