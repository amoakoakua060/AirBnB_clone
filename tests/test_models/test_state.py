#!/usr/bin/python3

""" Test module for testing State class """


from models.state import State
import unittest
from datetime import datetime
import io
import sys


class TestState(unittest.TestCase):
    """ A TestCase for testing the State class """

    def test_initialization(self):
        """ test the initialization of the State class """

        _state = State()
        self.assertIsInstance(_state, State)
        self.assertIsInstance(_state.id, str)
        self.assertIsInstance(_state.created_at, datetime)
        self.assertIsInstance(_state.updated_at, datetime)

        _state = State("name")
        self.assertIsInstance(_state, State)
        self.assertIsInstance(_state.id, str)
        self.assertIsInstance(_state.created_at, datetime)
        self.assertIsInstance(_state.updated_at, datetime)
        self.assertIsInstance(_state.name, str)
        self.assertEqual(_state.name, "")

        _state.name = "Jane"
        _state_dict = _state.to_dict()
        _state1 = State(**_state_dict)
        self.assertIsInstance(_state1, State)
        self.assertIsInstance(_state1.id, str)
        self.assertIsInstance(_state1.created_at, datetime)
        self.assertIsInstance(_state1.updated_at, datetime)
        self.assertEqual(_state.id, _state1.id)
        self.assertEqual(_state.name, _state1.name)
        self.assertEqual(_state.created_at, _state1.created_at)
        self.assertEqual(_state.updated_at, _state1.updated_at)
        self.assertFalse(isinstance(getattr(_state, "__class__", None), str))

        _state1 = State(
            id=_state_dict["id"], name="James",
            created_at=_state_dict["created_at"])
        self.assertIsInstance(_state1, State)
        self.assertIsInstance(_state1.id, str)
        self.assertIsInstance(_state1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(_state1, "updated_at", None), datetime))
        self.assertEqual(_state.id, _state1.id)
        self.assertNotEqual(_state.name, _state1.name)
        self.assertEqual(_state.created_at, _state1.created_at)
        self.assertNotEqual(
            getattr(_state1, "updated_at", None), _state.updated_at)

        with self.assertRaises(ValueError) as ctx:
            _state1 = State(
                id=_state_dict["id"], name="James",
                created_at=_state_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the State class """

        _state = State()
        date = _state.updated_at
        _state.save()
        self.assertNotEqual(date, _state.updated_at)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the State Class """

        _state = State()
        m_dict = _state.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        _state = State()
        _state.name = "Jane"
        _state.age = 50
        m_dict = _state.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = _state.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the State """

        _state = State()
        _stdout = io.StringIO()
        sys.stdout = _stdout

        print(_state)

        m_str = _stdout.getvalue()
        self.assertIn("[State]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{_state.__class__.__name__}] ({_state.id}) {_state.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
