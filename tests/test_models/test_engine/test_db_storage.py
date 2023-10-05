#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import MySQLdb
import pycodestyle
import unittest
from os import getenv
import inspect

import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        styleGuide = pycodestyle.StyleGuide(quiet=True)
        result = styleGuide.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        styleGuide = pycodestyle.StyleGuide(quiet=True)
        result = styleGuide.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipUnless(
    models.storage_t == 'db',
    "Can't test db storage in file storage"
)
class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up class for testing"""
        host = getenv('HBNB_MYSQL_HOST')
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        database = getenv('HBNB_MYSQL_DB')

        cls.conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database
        )
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """Close mysql db."""
        cls.cursor.close()
        cls.conn.close()

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_count(self):
        """Test the count method of DB storage."""
        count = 0
        for cls in classes.values():
            self.cursor.execute(
                "SELECT COUNT(*) FROM {};".format(cls.__tablename__)
            )
            clsCount = self.cursor.fetchall()[0][0]
            count += clsCount
            self.assertEqual(
                clsCount, models.storage.count(cls),
                "cls = {}".format(cls.__tablename__)
            )
        self.assertEqual(count, models.storage.count())

    def test_get(self):
        """Test the get method"""
        objToGet = State()
        objToGet.name = 'TestState'
        objToGet.save()
        self.assertEqual(objToGet, models.storage.get(State, objToGet.id))
