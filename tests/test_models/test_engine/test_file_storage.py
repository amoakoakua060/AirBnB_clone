#!/usr/bin/python3


""" containing the TestFileStorage class """


import uuid
import json
import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """ TestCase for testing FileStorage class """

    def setUp(self):
        """ called before each test """

        self.file_path = "file.json"
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_initialization(self):
        """ test what happens on the initialization of instance """

        self.assertFalse(os.path.exists(self.file_path))
        _store = FileStorage()
        self.assertFalse(os.path.exists(self.file_path))

    def test_all_instance_method(self):
        """ tests the all instance method on the FileStorage instance """

        _store = FileStorage()
        all_objects = _store.all()
        self.assertIsInstance(all_objects, dict)
        all_objects_len = len(all_objects)
        self.assertTrue(len(all_objects) == all_objects_len)

        _base1 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(_base1, all_objects.values())

        _base2 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(_base2, all_objects.values())

        with self.assertRaises(TypeError):
            _store.all("name")

    def test_new_instance_method(self):
        """ tests the new instance method on the FileStorage instance """

        _store = FileStorage()
        all_objects = _store.all()
        self.assertIsInstance(all_objects, dict)
        all_objects_len = len(all_objects)
        self.assertTrue(len(all_objects) == all_objects_len)

        _base1 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(_base1, all_objects.values())

        _base2 = BaseModel(**_base1.to_dict())
        all_objects = _store.all()
        self.assertNotIn(_base2, all_objects.values())
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        _base2.id = str(uuid.uuid4())
        _store.new(_base2)
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(_base2, all_objects.values())

        with self.assertRaises(TypeError):
            _store.new()

        with self.assertRaises(TypeError):
            _store.all(_base1, _base2)

        with self.assertRaises(AttributeError):
            _store.new("hey")

        with self.assertRaises(AttributeError):
            _store.new(10)

        with self.assertRaises(AttributeError):
            _store.new({"a": 399})

        with self.assertRaises(AttributeError):
            _store.new((1, 15))

        with self.assertRaises(AttributeError):
            _store.new(1.5434322)

    def test_save_instance_method(self):
        """ tests the save instance method on the FileStorage instance """

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        _store = FileStorage()
        all_objects = _store.all()
        all_objects_len = len(all_objects)

        _base1 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(_base1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        _store.save()
        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r") as file:
            _bases_dict = json.load(file)
            key = _base1.__class__.__name__ + "." + _base1.id
            self.assertEqual(_base1.to_dict(), _bases_dict[key])

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        _base1 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(_base1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        _base1.save()
        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r") as file:
            _bases_dict = json.load(file)
            key = _base1.__class__.__name__ + "." + _base1.id
            self.assertEqual(_base1.to_dict(), _bases_dict[key])

        with self.assertRaises(TypeError):
            _store.save(1)

    def test_save_instance_method(self):
        """ tests the save instance method on the FileStorage instance """

        _store = FileStorage()
        all_objects = _store.all()
        all_objects_len = len(all_objects)

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        _store.reload()

        self.assertTrue(all_objects_len == len(_store.all()))

        _base1 = BaseModel()
        all_objects = _store.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(_base1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        _store.save()
        self.assertTrue(os.path.exists(self.file_path))

        _store.reload()
        key = _base1.__class__.__name__ + "." + _base1.id
        self.assertEqual(_base1.id, _store.all()[key].id)

        if os.path.exists(self.file_path):
            os.remove(self.file_path)
