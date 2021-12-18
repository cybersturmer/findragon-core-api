import requests


def get_session() -> requests.Session:
    session = requests.Session()

    try:
        yield session
    finally:
        session.close()
