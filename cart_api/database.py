import inspect
import os
import sys
from playhouse.postgres_ext import (
    PostgresqlDatabase,
    PostgresqlExtDatabase,
    Model,
    AutoField,
    CharField,
    DoubleField,
    BooleanField,
    IntegerField,
)

database = os.environ.get("POSTGRES_DB", "bootcamp")
user = os.environ.get("POSTGRES_USER", "bootcamp")
password = os.environ.get("POSTGRES_PASSWORD", "bootcamp")
hostname = os.environ.get("POSTGRES_HOST", "localhost")


ext_db = PostgresqlExtDatabase(database, user=user, password=password, host=hostname)


class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase(
            database, user=user, password=password, host=hostname, autorollback=True
        )


class DatabaseProducts(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = CharField(null=True)
    size = CharField(null=True)
    color = CharField(null=True)
    condition = CharField(null=True)
    material = CharField(null=True)
    image_url = CharField(null=True)
    price = DoubleField()
    is_on_sale = BooleanField(default=False)
    sale_price = DoubleField(null=True)

    @classmethod
    def prepopulate(cls):  # pragma: nocover
        products = [
            DatabaseProducts(
                id=1,
                name="Sundress",
                description="Red sundress for the summer",
                size="Small",
                color="Red",
                condition="Used",
                material="Cotton",
                price=14.99,
                is_on_sale=False,
                sale_price=8.99,
            ),
            DatabaseProducts(
                id=2,
                name="Graphic T-Shirt",
                description="Graphic T-Shirt with a picture of Master Chief",
                size="Large",
                color="Green",
                condition="Used",
                material="Cotton",
                price=8.99,
                is_on_sale=True,
                sale_price=5.99,
            ),
            DatabaseProducts(
                id=3,
                name="Sweater",
                description="Wool sweater for the winter",
                size="Medium",
                color="Blue",
                condition="Used",
                material="Wool",
                price=19.99,
                is_on_sale=False,
            ),
            DatabaseProducts(
                id=4,
                name="Sweatpants",
                description="Light blue cotton sweatpants",
                size="Large",
                color="Blue",
                condition="New",
                material="Cotton",
                price=11.99,
                is_on_sale=False,
            ),
            DatabaseProducts(
                id=5,
                name="Leather jacket",
                description="Blue leather jacket",
                size="Small",
                color="Blue",
                condition="Used",
                material="Leather",
                price=18.99,
                is_on_sale=True,
                sale_price=14.99,
            ),
        ]
        DatabaseProducts.bulk_create(products)


# Exercise 1:
# Define an ORM class called DatabaseCartItem which inherits from BaseModel
# and has the properties and types defined by your swagger spec.
# if neccesary, update EXAMPLE_CART_ITEM in cart_api_tests/test_exercises.py to match
class DatabaseCartItem(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=True)
    image_url = CharField(null=True)
    price = DoubleField()
    quantity = IntegerField()

class DatabaseSellItems(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = CharField(null=True)
    size = CharField(null=True)
    color = CharField(null=True)
    condition = CharField(null=True)
    material = CharField(null=True)
    image_url = CharField(null=True)
    price = DoubleField()
    is_on_sale = BooleanField(default=False)
    sale_price = DoubleField(null=True)

# BOOTCAMPERS: Don't modify anything below
ALL_MODELS = [
    c_type
    for c_name, c_type in inspect.getmembers(sys.modules[__name__], inspect.isclass)
    if issubclass(c_type, BaseModel) and c_type not in [BaseModel, Model]
]


def init_tables(table_models=None):  # pragma: nocover
    table_models = table_models or ALL_MODELS

    if isinstance(table_models, Model):
        table_models = [table_models]

    with ext_db.connection_context():
        print(
            f"✅ Creating tables: {', '.join(table.__name__ for table in table_models)}"
        )
        ext_db.drop_tables(table_models, cascade=True)
        ext_db.create_tables(table_models)

        if DatabaseProducts in table_models:
            print(f"✅ Populating table: {DatabaseProducts.__name__}")
            DatabaseProducts.prepopulate()


# Create any tables that don't exist
missing_tables = [table for table in ALL_MODELS if not table.table_exists()]
if missing_tables:  # pragma: nocover
    print(
        f"⚠️ Missing DB Tables: {', '.join(table.__name__ for table in missing_tables)} ⚠️"
    )
    init_tables(missing_tables)

# Else if we explicitly want the tables cleared, recreate them
elif os.environ.get("API_CLEAR_DB", False) in [
    "1",
    1,
    True,
    "true",
    "yes",
]:  # pragma: nocover
    print(
        "⛔⚠️⛔⚠️⛔⚠️⛔ API_CLEAR_DB is set to 1, we are recreating all database tables ⛔⚠️⛔⚠️⛔⚠️⛔"
    )
    init_tables()

else:
    print("The tables already exist! Let's rock and roll 🤘")
