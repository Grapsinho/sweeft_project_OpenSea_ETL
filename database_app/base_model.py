from .database import Database

class Model:
    db = Database()

    def __init__(self, **kwargs):
        """
        Initialize the instance with dynamic attributes.
        """
        for field in self.__annotations__:
            setattr(self, field, kwargs.get(field, None))

    @classmethod
    def create_table(cls):
        """Generate and execute SQL to create table based on fields"""
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

    def save(self):
        """Insert the current object into the database"""
        # self.__annotations__ is collection model dict {'name': <class 'str'>}

        fields = [f for f in self.__annotations__ if f != "id"]
        values = [getattr(self, f) for f in fields]

        # print(values)
        # print(fields)

        # we are making a placeholders for values with {', '.join(['%s']*len(values))}

        sql = f"""
        INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)})
        VALUES ({', '.join(['%s']*len(values))})
        """
        self.db.execute(sql, values)
    
    @classmethod
    def bulk_insert(cls, objects):
        """Insert multiple records at once for better efficiency"""
        if not objects:
            return  # No data to insert
        
        fields = [f for f in cls.__annotations__ if f != "id"]
        values_list = [[getattr(obj, f) for f in fields] for obj in objects]

        sql = f"""
        INSERT INTO {cls.__name__.lower()} ({', '.join(fields)})
        VALUES {', '.join(['(' + ', '.join(['%s'] * len(fields)) + ')' for _ in objects])}
        """

        # Flatten values_list to pass as a tuple
        flattened_values = [item for sublist in values_list for item in sublist]
        cls.db.execute(sql, flattened_values)

    @classmethod
    def all(cls):
        """Retrieve all records from the table"""
        sql = f"SELECT * FROM {cls.__name__.lower()}"
        results = cls.db.fetch(sql)

        # creates a list of key names: zip(["id"] + list(cls.__annotations__.keys()
        # row represents the one row of the data that fetched: (1, "Art NFTs", "Modern Art Collection", "A collection of modern NFT artworks.",...
        # with zip we pair kay names and values
        # converts list of tuple into a dict: dict(zip(...))
        # with cls we create collection instances from dicts.

        return [cls(**dict(zip(["id"] + list(cls.__annotations__.keys()), row))) for row in results]

    @classmethod
    def filter(cls, **conditions):
        """Filter records based on conditions"""
        condition_str = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        sql = f"SELECT * FROM {cls.__name__.lower()} WHERE {condition_str}"
        results = cls.db.fetch(sql, tuple(conditions.values()))
        return [cls(**dict(zip(["id"] + list(cls.__annotations__.keys()), row))) for row in results]
