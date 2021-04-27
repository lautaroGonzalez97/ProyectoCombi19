def authenticated(session):
    return session.get("id")