#!/usr/bin/python3

"""
module containing the Review class
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class which inherits from BaseModel
    """

    place_id = ""
    user_id = ""
    text = ""
