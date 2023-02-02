import sys

from YouLikeHits import Youlikehits
from models import User

'''-------------- Variables declaration --------------'''

if __name__ == "__main__":
    user = User('ablo340', 'Bepc2011')
    youlikehits = Youlikehits()

    youlikehits.get_points(user)

    sys.exit(0)

