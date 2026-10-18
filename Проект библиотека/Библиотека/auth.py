from database import connection
from database import find_user

def authenticate_user(username, password):
    if username.strip() == "" or password == "":
        return None

    return find_user(username, password)

def get_guest_user():
    return(0, "guest", 1, "Гость", "guest")