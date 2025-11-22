from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://postgres:admin@postgres:5432/postgres")
Base = declarative_base()

class ItemList(Base):
    __tablename__ = "item_list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    item_descript = Column(String, nullable=False)
    item_price = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_all_items():
    with Session() as session:
        items = session.query(ItemList).order_by(ItemList.id.asc()).all()
        return items

def add_new_item_record(item_name, item_descript, item_price):
    with Session() as session:
        new_record = ItemList(
            item_name=item_name,
            item_descript=item_descript,
            item_price=item_price
        )
        session.add(new_record)
        session.commit()


def update_exist_item_record(id, item_name=None, item_descript=None, item_price=None):
    with Session() as session:
        record = session.query(ItemList).filter_by(id=id).first()
        if not record:
            raise ValueError("Item record not found")

        if item_name is not None:
            record.item_name = item_name

        if item_descript is not None:
            record.item_descript = item_descript

        if item_price is not None:
            record.item_price = item_price

        session.commit()


def delete_item_record(id):
    with Session() as session:
        record = session.query(ItemList).filter_by(id=id).first()
        if not record:
            raise ValueError("Item record not found")

        session.delete(record)
        session.commit()
