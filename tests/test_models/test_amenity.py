#!/usr/bin/python3

""" module for testing Amenity class """


from models.amenity import Amenity
import unittest
from datetime import datetime
import io
import sys


class TestAmenity(unittest.TestCase):
    """ A TestCase class that tests the Amenity class """

    def test_initialization(self):
        """ test the initialization of objects """

        _amenity = Amenity()
        self.assertIsInstance(_amenity, Amenity)
        self.assertIsInstance(_amenity.id, str)
        self.assertIsInstance(_amenity.created_at, datetime)
        self.assertIsInstance(_amenity.updated_at, datetime)

        _amenity = Amenity("name")
        self.assertIsInstance(_amenity, Amenity)
        self.assertIsInstance(_amenity.id, str)
        self.assertIsInstance(_amenity.created_at, datetime)
        self.assertIsInstance(_amenity.updated_at, datetime)
        self.assertIsInstance(_amenity.name, str)
        self.assertEqual(_amenity.name, "")

        _amenity.name = "Jane"
        _amenity_dict = _amenity.to_dict()
        _amenity1 = Amenity(**_amenity_dict)
        self.assertIsInstance(_amenity1, Amenity)
        self.assertIsInstance(_amenity1.id, str)
        self.assertIsInstance(_amenity1.created_at, datetime)
        self.assertIsInstance(_amenity1.updated_at, datetime)
        self.assertEqual(_amenity.id, _amenity1.id)
        self.assertEqual(_amenity.name, _amenity1.name)
        self.assertEqual(_amenity.created_at, _amenity1.created_at)
        self.assertEqual(_amenity.updated_at, _amenity1.updated_at)
        self.assertFalse(isinstance(getattr(_amenity, "__class__", None), str))

        _amenity1 = Amenity(
            id=_amenity_dict["id"], name="James",
            created_at=_amenity_dict["created_at"])
        self.assertIsInstance(_amenity1, Amenity)
        self.assertIsInstance(_amenity1.id, str)
        self.assertIsInstance(_amenity1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_amenity1, "updated_at", None), datetime))
        self.assertEqual(_amenity.id, _amenity1.id)
        self.assertNotEqual(_amenity.name, _amenity1.name)
        self.assertEqual(_amenity.created_at, _amenity1.created_at)
        self.assertNotEqual(
            getattr(_amenity1, "updated_at", None), _amenity.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _amenity1 = Amenity(
                id=_amenity_dict["id"], name="James",
                created_at=_amenity_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method """

        _amenity = Amenity()
        date = _amenity.updated_at
        _amenity.save()
        self.assertNotEqual(date, _amenity.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the Amenity Class """

        _amenity = Amenity()
        m_dict = _amenity.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _amenity = Amenity()
        _amenity.name = "Jane"
        _amenity.age = 50
        m_dict = _amenity.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _amenity.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the Amenity """

        _amen = Amenity()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_amen)

        m_str = _stdout.getvalue()
        self.assertIn("[Amenity]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_amen.__class__.__name__}] ({_amen.id}) {_amen.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
