#!/usr/bin/python3

""" Test module for base__city module """


from models.city import City
import unittest
from datetime import datetime
import io
import sys


class TestCity(unittest.TestCase):
    """ A TestCase for testing City class """

    def test_initialization(self):
        """ test the initialization of the City class """

        _city = City()
        self.assertIsInstance(_city, City)
        self.assertIsInstance(_city.id, str)
        self.assertIsInstance(_city.created_at, datetime)
        self.assertIsInstance(_city.updated_at, datetime)
        self.assertIsInstance(_city.name, str)
        self.assertIsInstance(_city.state_id, str)
        self.assertEqual(_city.name, "")
        self.assertEqual(_city.state_id, "")

        _city = City("name")
        self.assertIsInstance(_city, City)
        self.assertIsInstance(_city.id, str)
        self.assertIsInstance(_city.created_at, datetime)
        self.assertIsInstance(_city.updated_at, datetime)

        _city.name = "Jane"
        _city_dict = _city.to_dict()
        _city1 = City(**_city_dict)
        self.assertIsInstance(_city1, City)
        self.assertIsInstance(_city1.id, str)
        self.assertIsInstance(_city1.created_at, datetime)
        self.assertIsInstance(_city1.updated_at, datetime)
        self.assertEqual(_city.id, _city1.id)
        self.assertEqual(_city.name, _city1.name)
        self.assertEqual(_city.created_at, _city1.created_at)
        self.assertEqual(_city.updated_at, _city1.updated_at)
        self.assertFalse(isinstance(getattr(_city, "__class__", None), str))

        _city1 = City(
            id=_city_dict["id"], name="James",
            created_at=_city_dict["created_at"])
        self.assertIsInstance(_city1, City)
        self.assertIsInstance(_city1.id, str)
        self.assertIsInstance(_city1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_city1, "updated_at", None), datetime))
        self.assertEqual(_city.id, _city1.id)
        self.assertNotEqual(_city.name, _city1.name)
        self.assertEqual(_city.created_at, _city1.created_at)
        self.assertNotEqual(
            getattr(_city1, "updated_at", None), _city.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _city1 = City(
                id=_city_dict["id"], name="James",
                created_at=_city_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the City class """

        _city = City()
        date = _city.updated_at
        _city.save()
        self.assertNotEqual(date, _city.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the City Class """

        _city = City()
        m_dict = _city.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _city = City()
        _city.name = "Jane"
        _city.age = 50
        m_dict = _city.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _city.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the City """

        _city = City()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_city)

        m_str = _stdout.getvalue()
        self.assertIn("[City]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_city.__class__.__name__}] ({_city.id}) {_city.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
