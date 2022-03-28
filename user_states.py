from collections import defaultdict

# Three states - to start, then add address then add comment
START, ADD_ADDRESS, ADD_COMMENT = range(3)
USER_STATE = defaultdict(lambda x: START)
# Temporary save the address in this variable to pass from _add_address to _add_comment func
ADDRESS = ''


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state
