#!/usr/bin/python3

""" module for testing Place class """


from models.place import Place
import unittest
from datetime import datetime
import io
import sys


class TestPlace(unittest.TestCase):
    """ A TestCase for testing Place class """

    def test_initialization(self):
        """ test the initialization of the Place class """

        _place = Place()
        self.assertIsInstance(_place, Place)
        self.assertIsInstance(_place.id, str)
        self.assertIsInstance(_place.created_at, datetime)
        self.assertIsInstance(_place.updated_at, datetime)

        _place = Place("name")
        self.assertIsInstance(_place, Place)
        self.assertIsInstance(_place.id, str)
        self.assertIsInstance(_place.created_at, datetime)
        self.assertIsInstance(_place.updated_at, datetime)
        self.assertIsInstance(_place.city_id, str)
        self.assertIsInstance(_place.user_id, str)
        self.assertIsInstance(_place.name, str)
        self.assertIsInstance(_place.description, str)
        self.assertIsInstance(_place.number_rooms, int)
        self.assertIsInstance(_place.number_bathrooms, int)
        self.assertIsInstance(_place.max_guest, int)
        self.assertIsInstance(_place.price_by_night, int)
        self.assertIsInstance(_place.latitude, float)
        self.assertIsInstance(_place.longitude, float)
        self.assertIsInstance(_place.amenity_ids, list)
        self.assertEqual(_place.city_id, "")
        self.assertEqual(_place.user_id, "")
        self.assertEqual(_place.name, "")
        self.assertEqual(_place.description, "")
        self.assertEqual(_place.number_rooms, 0)
        self.assertEqual(_place.number_bathrooms, 0)
        self.assertEqual(_place.max_guest, 0)
        self.assertEqual(_place.price_by_night, 0)
        self.assertEqual(_place.latitude, 0.0)
        self.assertEqual(_place.longitude, 0.0)
        self.assertEqual(_place.amenity_ids, [])

        _place.name = "John"
        _place_dict = _place.to_dict()
        _place1 = Place(**_place_dict)
        self.assertIsInstance(_place1, Place)
        self.assertIsInstance(_place1.id, str)
        self.assertIsInstance(_place1.created_at, datetime)
        self.assertIsInstance(_place1.updated_at, datetime)
        self.assertEqual(_place.id, _place1.id)
        self.assertEqual(_place.name, _place1.name)
        self.assertEqual(_place.created_at, _place1.created_at)
        self.assertEqual(_place.updated_at, _place1.updated_at)
        self.assertFalse(isinstance(getattr(_place, "__class__", None), str))

        _place1 = Place(
            id=_place_dict["id"], name="James",
            created_at=_place_dict["created_at"])
        self.assertIsInstance(_place1, Place)
        self.assertIsInstance(_place1.id, str)
        self.assertIsInstance(_place1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_place1, "updated_at", None), datetime))
        self.assertEqual(_place.id, _place1.id)
        self.assertNotEqual(_place.name, _place1.name)
        self.assertEqual(_place.created_at, _place1.created_at)
        self.assertNotEqual(
            getattr(_place1, "updated_at", None), _place.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _place1 = Place(
                id=_place_dict["id"], name="James",
                created_at=_place_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the Place class """

        _place = Place()
        date = _place.updated_at
        _place.save()
        self.assertNotEqual(date, _place.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the Place Class """

        _place = Place()
        m_dict = _place.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _place = Place()
        _place.name = "John"
        _place.age = 50
        m_dict = _place.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _place.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the Place """

        _place = Place()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_place)

        m_str = _stdout.getvalue()
        self.assertIn("[Place]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_place.__class__.__name__}] ({_place.id}) {_place.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
