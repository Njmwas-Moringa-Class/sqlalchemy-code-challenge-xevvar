
import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)

    reviews = relationship("Review", back_populates="restaurant")

    def __repr__(self):
        return f'Restaurant: {self.name}'
    
    def reviews(self):
        return self.reviews

    def customers(self):
        return [review.customer for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]
    


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship("Review", back_populates="customer")

    def __repr__(self):
        return f'Customer: {self.first_name}'
    
    def reviews(self):
        return self.reviews

    def get_restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = session.query(Review).filter_by(customer_id=self.id, restaurant_id=restaurant.id).all()
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()
    
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    star_rating = Column(Integer)

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def __repr__(self):
        return f"<Review(restaurant_id={self.restaurant_id}, customer_id={self.customer_id}, star_rating={self.star_rating})>"
    
    def customer(self):
        return self.customer

    def restaurant(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."
