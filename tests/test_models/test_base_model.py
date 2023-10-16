#!/usr/bin/python3

""" module to test base_model class """


from models.base_model import BaseModel
import unittest
from datetime import datetime
import io
import sys


class TestBaseModel(unittest.TestCase):
    """ A TestCase for BaseModel class """

    def test_initialization(self):
        """ test the initialization of the BaseModel class """

        _base = BaseModel()
        self.assertIsInstance(_base, BaseModel)
        self.assertIsInstance(_base.id, str)
        self.assertIsInstance(_base.created_at, datetime)
        self.assertIsInstance(_base.updated_at, datetime)

        _base = BaseModel("name")
        self.assertIsInstance(_base, BaseModel)
        self.assertIsInstance(_base.id, str)
        self.assertIsInstance(_base.created_at, datetime)
        self.assertIsInstance(_base.updated_at, datetime)

        _base.name = "Jane"
        _base_dict = _base.to_dict()
        _base1 = BaseModel(**_base_dict)
        self.assertIsInstance(_base1, BaseModel)
        self.assertIsInstance(_base1.id, str)
        self.assertIsInstance(_base1.created_at, datetime)
        self.assertIsInstance(_base1.updated_at, datetime)
        self.assertEqual(_base.id, _base1.id)
        self.assertEqual(_base.name, _base1.name)
        self.assertEqual(_base.created_at, _base1.created_at)
        self.assertEqual(_base.updated_at, _base1.updated_at)
        self.assertFalse(isinstance(getattr(_base, "__class__", None), str))

        _base1 = BaseModel(
            id=_base_dict["id"], name="James",
            created_at=_base_dict["created_at"])
        self.assertIsInstance(_base1, BaseModel)
        self.assertIsInstance(_base1.id, str)
        self.assertIsInstance(_base1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_base1, "updated_at", None), datetime))
        self.assertEqual(_base.id, _base1.id)
        self.assertNotEqual(_base.name, _base1.name)
        self.assertEqual(_base.created_at, _base1.created_at)
        self.assertNotEqual(
            getattr(_base1, "updated_at", None), _base.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _base1 = BaseModel(
                id=_base_dict["id"], name="James",
                created_at=_base_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the BaseModel class """

        _base = BaseModel()
        date = _base.updated_at
        _base.save()
        self.assertNotEqual(date, _base.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the BaseModel Class """

        _base = BaseModel()
        m_dict = _base.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _base = BaseModel()
        _base.name = "Jane"
        _base.age = 50
        m_dict = _base.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _base.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the BaseModel """

        _base = BaseModel()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_base)

        m_str = _stdout.getvalue()
        self.assertIn("[BaseModel]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_base.__class__.__name__}] ({_base.id}) {_base.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
