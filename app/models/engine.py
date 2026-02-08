from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///./dota2.db")


def get_db():
    with Session(bind=engine) as session:
        yield session
