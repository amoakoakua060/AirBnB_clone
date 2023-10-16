#!/usr/bin/python3

"""
module containing the BaseModel class
"""

import uuid
from datetime import datetime
import models


class BaseModel():
    """
    BaseModel will be inherited by all other models in AirBnB
    """

    def __init__(self, *args, **kwargs):
        """ Initialize object with attributes """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs):
            for key, value in kwargs.items():
                if key == "__class__":
                    continue

                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                    continue

                setattr(self, key, value)
            return

        models.storage.new(self)

    def __str__(self):
        """ returns an informal representation of the instance """

        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ updates updated_at and save model to storage """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ converts to a dictionary """

        instance_dict = self.__dict__.copy()
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        instance_dict["__class__"] = self.__class__.__name__

        return (instance_dict)
