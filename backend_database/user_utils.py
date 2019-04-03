from . import (
    pwd_context,
    User,
)


def create_user(username, password):
    password_hash = pwd_context.hash(password)

    query = User.insert().values(username=username, password_hash=password_hash)

    last_record_id = await database.execute(query)
