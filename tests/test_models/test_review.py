#!/usr/bin/python3

""" Test module for testing Review class """


from models.review import Review
import unittest
from datetime import datetime
import io
import sys


class TestReview(unittest.TestCase):
    """ A TestCase for testing the Review class """

    def test_initialization(self):
        """ test the initialization of the Review class """

        _rev = Review()
        self.assertIsInstance(_rev, Review)
        self.assertIsInstance(_rev.id, str)
        self.assertIsInstance(_rev.created_at, datetime)
        self.assertIsInstance(_rev.updated_at, datetime)

        _rev = Review("name")
        self.assertIsInstance(_rev, Review)
        self.assertIsInstance(_rev.id, str)
        self.assertIsInstance(_rev.created_at, datetime)
        self.assertIsInstance(_rev.updated_at, datetime)
        self.assertIsInstance(_rev.place_id, str)
        self.assertIsInstance(_rev.user_id, str)
        self.assertIsInstance(_rev.text, str)
        self.assertEqual(_rev.place_id, "")
        self.assertEqual(_rev.user_id, "")
        self.assertEqual(_rev.text, "")

        _rev.name = "Jane"
        _rev_dict = _rev.to_dict()
        _rev1 = Review(**_rev_dict)
        self.assertIsInstance(_rev1, Review)
        self.assertIsInstance(_rev1.id, str)
        self.assertIsInstance(_rev1.created_at, datetime)
        self.assertIsInstance(_rev1.updated_at, datetime)
        self.assertEqual(_rev.id, _rev1.id)
        self.assertEqual(_rev.name, _rev1.name)
        self.assertEqual(_rev.created_at, _rev1.created_at)
        self.assertEqual(_rev.updated_at, _rev1.updated_at)
        self.assertFalse(isinstance(getattr(_rev, "__class__", None), str))

        _rev1 = Review(
            id=_rev_dict["id"], name="James",
            created_at=_rev_dict["created_at"])
        self.assertIsInstance(_rev1, Review)
        self.assertIsInstance(_rev1.id, str)
        self.assertIsInstance(_rev1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_rev1, "updated_at", None), datetime))
        self.assertEqual(_rev.id, _rev1.id)
        self.assertNotEqual(_rev.name, _rev1.name)
        self.assertEqual(_rev.created_at, _rev1.created_at)
        self.assertNotEqual(
            getattr(_rev1, "updated_at", None), _rev.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _rev1 = Review(
                id=_rev_dict["id"], name="James",
                created_at=_rev_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the Review class """

        _rev = Review()
        date = _rev.updated_at
        _rev.save()
        self.assertNotEqual(date, _rev.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the Review Class """

        _rev = Review()
        m_dict = _rev.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _rev = Review()
        _rev.name = "Jane"
        _rev.age = 50
        m_dict = _rev.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _rev.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the Review """

        _rev = Review()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_rev)

        m_str = _stdout.getvalue()
        self.assertIn("[Review]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_rev.__class__.__name__}] ({_rev.id}) {_rev.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
