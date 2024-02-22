from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review


engine = create_engine('sqlite:///db/restaurants.db')
Base.metadata.bind = engine


Session = sessionmaker(bind=engine)
session = Session()


session.query(Review).delete()
session.query(Restaurant).delete()
session.query(Customer).delete()

restaurant1 = Restaurant(name='Restaurant A', price=3)
restaurant2 = Restaurant(name='Restaurant B', price=2)
restaurant3 = Restaurant(name='Restaurant C', price=4)

session.add_all([restaurant1, restaurant2, restaurant3])
session.commit()


customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')
customer3 = Customer(first_name='Alice', last_name='Johnson')

session.add_all([customer1, customer2, customer3])
session.commit()


review1 = Review(restaurant_id=restaurant1.id, customer_id=customer1.id, star_rating=4)
review2 = Review(restaurant_id=restaurant2.id, customer_id=customer2.id, star_rating=5)
review3 = Review(restaurant_id=restaurant3.id, customer_id=customer3.id, star_rating=3)

session.add_all([review1, review2, review3])
session.commit()

session.close()

print("Data has been seeded successfully!")