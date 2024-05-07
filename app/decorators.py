from db.engine import session_maker

session_maker = session_maker()


def enter_session(f):
    async def session_wrapper(*args, **kwargs):
        async with session_maker() as session:
            async with session.begin():
                return await f(session=session, *args, **kwargs)
    return session_wrapper
