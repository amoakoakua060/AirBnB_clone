#!/usr/bin/python3

""" Test module for testing User class """


from models.user import User
import unittest
from datetime import datetime
import io
import sys


class TestUser(unittest.TestCase):
    """ A TestCase for testing the User class """

    def test_initialization(self):
        """ test the initialization of the User class """

        _user = User()
        self.assertIsInstance(_user, User)
        self.assertIsInstance(_user.id, str)
        self.assertIsInstance(_user.created_at, datetime)
        self.assertIsInstance(_user.updated_at, datetime)
        self.assertIsInstance(_user.email, str)
        self.assertIsInstance(_user.password, str)
        self.assertIsInstance(_user.first_name, str)
        self.assertIsInstance(_user.last_name, str)
        self.assertEqual(_user.email, "")
        self.assertEqual(_user.password, "")
        self.assertEqual(_user.first_name, "")
        self.assertEqual(_user.last_name, "")

        _user = User("name")
        self.assertIsInstance(_user, User)
        self.assertIsInstance(_user.id, str)
        self.assertIsInstance(_user.created_at, datetime)
        self.assertIsInstance(_user.updated_at, datetime)

        _user.name = "Jane"
        _user_dict = _user.to_dict()
        _user1 = User(**_user_dict)
        self.assertIsInstance(_user1, User)
        self.assertIsInstance(_user1.id, str)
        self.assertIsInstance(_user1.created_at, datetime)
        self.assertIsInstance(_user1.updated_at, datetime)
        self.assertEqual(_user.id, _user1.id)
        self.assertEqual(_user.name, _user1.name)
        self.assertEqual(_user.created_at, _user1.created_at)
        self.assertEqual(_user.updated_at, _user1.updated_at)
        self.assertFalse(isinstance(getattr(_user, "__class__", None), str))

        _user1 = User(
            id=_user_dict["id"], name="James",
            created_at=_user_dict["created_at"])
        self.assertIsInstance(_user1, User)
        self.assertIsInstance(_user1.id, str)
        self.assertIsInstance(_user1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_user1, "updated_at", None), datetime))
        self.assertEqual(_user.id, _user1.id)
        self.assertNotEqual(_user.name, _user1.name)
        self.assertEqual(_user.created_at, _user1.created_at)
        self.assertNotEqual(
            getattr(_user1, "updated_at", None), _user.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _user1 = User(
                id=_user_dict["id"], name="James",
                created_at=_user_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the User class """

        _user = User()
        date = _user.updated_at
        _user.save()
        self.assertNotEqual(date, _user.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the User Class """

        _user = User()
        m_dict = _user.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _user = User()
        _user.name = "Jane"
        _user.age = 50
        m_dict = _user.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _user.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the User """

        _user = User()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_user)

        m_str = _stdout.getvalue()
        self.assertIn("[User]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_user.__class__.__name__}] ({_user.id}) {_user.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
