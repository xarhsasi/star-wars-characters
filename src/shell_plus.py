"""Support for interactive IPython shell with preloaded objects."""

import sys
from pathlib import Path

# Insert the path to the root of your application at the beginning of sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from IPython.terminal.embed import InteractiveShellEmbed
from traitlets.config import Config

from src.characters.models import Character
from src.characters.service import CharacterService
from src.films.models import Film
from src.films.service import FilmService
from src.integrations.swapi.plugin import SwapiPlugin
from src.starships.models import Starship
from src.starships.service import StarshipService
from src.users.repository import UserRepository
from src.utils.session import async_session

# Optionally add more imports or utilities

# Set up an asynchronous session for async ORM use
session = async_session()

# Load objects into interactive shell
shell_vars = {
    "session": session,
    "Starship": Starship,
    "Film": Film,
    "Character": Character,
    "character_service": CharacterService(session=session),
    "film_service": FilmService(session=session),
    "starship_service": StarshipService(session=session),
    "swapi": SwapiPlugin(),
    # Add any other objects you want to auto-load here
}

# Load external confi
config = Config()
# Example config lines: add any specific IPython settings here if needed
config.InteractiveShellApp.exec_lines = [
    "print('Welcome to the interactive IPython shell!')",
]
# Start IPython or ptpython shell
shell = InteractiveShellEmbed(config=config, user_ns=shell_vars)
shell()
