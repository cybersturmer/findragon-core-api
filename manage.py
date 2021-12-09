#!/usr/bin/env python

import sys


def create_database():
    from models.tables import Base
    from database import engine
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    args = sys.argv[1:]

    decision_tree = {
        'createdatabase': create_database
    }

    try:
        argument = args[0]

        command = decision_tree[argument]
        command()
    except (KeyError, IndexError) as e:
        print('Command not found')
