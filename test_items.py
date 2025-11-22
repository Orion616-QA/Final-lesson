import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import ItemList


DATABASE_URL = "postgresql://postgres:admin@postgres:5432/postgres"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(DATABASE_URL)
    return engine


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(ItemList).delete()
    session.commit()

    yield session

    session.close()


def test_db_connection(engine):
    """Check the database connection"""
    conn = engine.connect()
    assert conn is not None
    conn.close()


def test_add_record(session):
    """Check create a new record in DB"""
    item = ItemList(
        item_name="TestAdd",
        item_descript="Test description",
        item_price=123
    )
    session.add(item)
    session.commit()

    saved = session.query(ItemList).filter_by(item_name="TestAdd").first()
    assert saved is not None
    assert saved.item_price == 123


def test_get_all(session):
    """Check the receiving records from DB"""
    session.add_all([
        ItemList(item_name="A", item_descript="dA", item_price=10),
        ItemList(item_name="B", item_descript="dB", item_price=20),
    ])
    session.commit()

    items = session.query(ItemList).order_by(ItemList.id.asc()).all()

    assert len(items) == 2
    assert items[0].item_name == "A"
    assert items[1].item_name == "B"


def test_update_record(session):
    """Check update data in record in DB"""
    item = ItemList(item_name="OldName", item_descript="Old", item_price=1)
    session.add(item)
    session.commit()

    item.item_name = "NewName"
    item.item_price = 999
    session.commit()

    updated = session.query(ItemList).filter_by(id=item.id).first()
    assert updated.item_name == "NewName"
    assert updated.item_price == 999


def test_delete_record(session):
    """Check delete record from DB"""
    item = ItemList(item_name="ToDelete", item_descript="Del it", item_price=0)
    session.add(item)
    session.commit()

    session.delete(item)
    session.commit()

    deleted = session.query(ItemList).filter_by(id=item.id).first()
    assert deleted is None