from .database import Database
import logging

class Model:
    db = Database()
    logging.basicConfig(level=logging.ERROR)

    def __init__(self, **kwargs):
        """
        Initialize the instance with dynamic attributes.
        """

        # name="Name"
        # description="Description"...

        for field in self.__annotations__:
            setattr(self, field, kwargs.get(field, None))

    @classmethod
    def create_table(cls):
        """Generate and execute SQL to create table based on fields"""
        try:
            fields = []
            for field_name, field_type in cls.__annotations__.items():
                sql_type = cls.get_sql_type(field_type)
                fields.append(f"{field_name} {sql_type}")
            
            # fields: ['collection TEXT', 'name TEXT', 'description TEXT', 'image_url TEXT', 'owner TEXT', 'twitter_username TEXT', 'contracts JSONB']

            sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} (
                id SERIAL PRIMARY KEY,
                {', '.join(fields)}
            )
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error creating table {cls.__name__.lower()}: {e}")

    @staticmethod
    def get_sql_type(field_type):
        """Map Python types to PostgreSQL types"""
        if field_type == str:
            return "TEXT"
        elif field_type == int:
            return "INTEGER"
        elif field_type == float:
            return "REAL"
        elif field_type == dict:
            return "JSONB"
        else:
            return "TEXT"

    # we don't need classmethod here because we are working for only one instance and we want this code to work only for it.
    def save(self):
        """Insert the current object into the database"""
        
        try:
            # self.__annotations__ is collection model dict {'name': <class 'str'>}

            fields = [f for f in self.__annotations__ if f != "id"]
            values = [getattr(self, f) for f in fields]

            # print(values) ['Art NFTs', 'Modern Art Collection',  'nft_artist', {'main': '0xabcdef...'}]
            # print(fields)

            # we are making a placeholders for values with {', '.join(['%s']*len(values))}

            sql = f"""
            INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)})
            VALUES ({', '.join(['%s']*len(values))})
            """

            # INSERT INTO collection (name, description, image_url)
            #    VALUES (%s, %s, %s)


            self.db.execute(sql, values)
        except Exception as e:
            logging.error(f"Error saving record in {self.__class__.__name__.lower()}: {e}")
    
    # we need to operate multiple instances so we are using classmethod to work on any subclass.
    @classmethod
    def bulk_insert(cls, objects):
        """Insert multiple records at once for better efficiency"""
        if not objects:
            return  # No data to insert
        
        try:
            fields = [f for f in cls.__annotations__ if f != "id"]

            # instead of one list now we are getting multiple lists of values 
            values_list = [[getattr(obj, f) for f in fields] for obj in objects]

            sql = f"""
            INSERT INTO {cls.__name__.lower()} ({', '.join(fields)})
            VALUES {', '.join(['(' + ', '.join(['%s'] * len(fields)) + ')' for _ in objects])}
            """

            # VALUES (%s, %s, %s), (%s, %s, %s)

            # Flatten values_list to pass as a tuple
            flattened_values = [item for sublist in values_list for item in sublist]

            # flattened values: flattened_values = [
            #    "Bored Ape", "NFT collection", "some_url",
            #    "CryptoPunks", "Another NFT", "another_url"
            #]

            cls.db.execute(sql, flattened_values)
        except Exception as e:
            logging.error(f"Error in bulk insert for {cls.__name__.lower()}: {e}")

    @classmethod
    def all(cls, order_by=None, desc=False, limit=None):
        """Retrieve all records from the table"""

        try:
            sql = f"SELECT * FROM {cls.__name__.lower()}"

            if order_by and order_by in cls.__annotations__:
                sql += f" ORDER BY {order_by} {'DESC' if desc else 'ASC'}"
            
            if limit and isinstance(limit, int) and limit > 0:
                sql += f" LIMIT {limit}"

            results = cls.db.fetch(sql)

            # creates a list of key names: zip(["id"] + list(cls.__annotations__.keys()
            # row represents the one row of the data that fetched: (1, "Art NFTs", "Modern Art Collection", "A collection of modern NFT artworks.",...
            # with zip we pair kay names and values
            # converts list of tuple into a dict: dict(zip(...))
            # with cls we create collection instances from dicts.

            return [cls(**dict(zip(["id"] + list(cls.__annotations__.keys()), row))) for row in results]
    
        except Exception as e:
            logging.error(f"Error fetching all records from {cls.__name__.lower()}: {e}")
            return []
    
    @classmethod
    def filter(cls, order_by=None, desc=False, limit=None, **conditions):
        """Filter records based on conditions"""

        try:
            condition_clauses = []
            values = []

            for key, value in conditions.items():

                lower_dash_idx = key.find("__")
                if lower_dash_idx == -1:
                    field = key
                    operation = "equals"
                else:
                    field = key[:lower_dash_idx]
                    operation = key[lower_dash_idx + 2:]

                if operation == "icontains":
                    condition_clauses.append(f"{field} ILIKE %s")
                    values.append(f"%{value}%")
                elif operation == "contains":
                    condition_clauses.append(f"{field} LIKE %s")
                    values.append(f"%{value}%")
                else:
                    condition_clauses.append(f"{field} = %s")
                    values.append(value)

            condition_str = " AND ".join(condition_clauses)

            sql = f"SELECT * FROM {cls.__name__.lower()} WHERE {condition_str}"

            if order_by and order_by in cls.__annotations__:
                sql += f" ORDER BY {order_by} {'DESC' if desc else 'ASC'}"

            if limit and isinstance(limit, int) and limit > 0:
                sql += f" LIMIT {limit}"

            results = cls.db.fetch(sql, tuple(values))
            
            objects = []
            for row in results:
                data = dict(zip(["id"] + list(cls.__annotations__.keys()), row))
                objects.append(cls(**data))
            return objects
                    
        except Exception as e:
            logging.error(f"Error filtering records in {cls.__name__.lower()}: {e}")
            return []
