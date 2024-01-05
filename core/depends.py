from sqlalchemy import exc

from shared.database import session


# def sync_db_session() -> Generator[Session, None]:
def sync_db_session():
    """Create new SYNC database session.

    Yields:
        Database session.
    """
    with session() as db_session:
        try:
            yield db_session
        except exc.SQLAlchemyError as error:
            db_session.rollback()
            raise

# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     engine = create_async_engine(DATABASE_URI)
#     factory = async_sessionmaker(engine)
#     async with factory() as session:
#         try:
#             yield session
#             await session.commit()
#         except exc.SQLAlchemyError as error:
#             await session.rollback()
#             raise
