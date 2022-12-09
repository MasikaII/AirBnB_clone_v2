#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade="all,delete", backref='state')

    @property
    def cities(self):
        """Returns list of city Instances"""
        my_city = []

        cities = storage.all(City).items()
        for city in cities.values():
            if city.state_id == self.id:
                my_city.append(city)
        return my_city
