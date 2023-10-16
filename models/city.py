#!/usr/bin/python3

"""
module containing the City class
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class which inherits from BaseModel
    """

    state_id = ""
    name = ""
