"""The bellow lines solves the issue:

sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Character(characters)], expression 'Film' failed to locate a name ('Film'). If this is a class name, consider adding this relationship() to the <class 'src.characters.models.Character'> class after both dependent classes have been defined.

Just by importing the models in the __init__.py file of the package and
importing the module src.__init__ in the alembic env.py file.
"""

from src.characters.models import Character
from src.films.models import Film
from src.models import film_characters, starship_films
from src.starships.models import Starship
