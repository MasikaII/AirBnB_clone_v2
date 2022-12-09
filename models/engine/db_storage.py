from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
#from sqlalchemy.orm import relationship

class DBStorage():
    """This class uses mysql as the storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        "Initializes the Engine"
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format
            (user, password, host, database, pool_pre_ping=True))

        if (env == "test"):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Method queries all current database session"""
        query_dict = {}
        if cls is None:
            classes = {
                'State': State,
                'City': City,
                'User': User,
                'Place': Place,
                'Review': Review,
                'Amenity': Amenity}
            for key, val in classes.items():
                my_obj = self.__session.query(val).all()
                for obj in my_obj:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    query_dict[key] = obj
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            my_obj = self.__session.query(cls)
            for obj in my_obj:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                query_dict[key] = obj

        return query_dict

    def new(self, obj):
        """Adds object to current db session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current db session obj"""
        if obj is not None:
            self.__session.delete(obj)
        else:
            pass

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
