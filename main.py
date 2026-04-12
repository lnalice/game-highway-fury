"""pygbag entry point for browser execution via WebAssembly."""

import asyncio
from game import Game

async def main():
    game = Game()
    await game.run_async()

asyncio.run(main())
