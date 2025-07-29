import sys
import asyncio

from src.game import Game

if __name__ == "__main__": 
    g = Game()
    asyncio.run(g.run())
    
    sys.exit()
