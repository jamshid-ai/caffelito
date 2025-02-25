import datetime as dt
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey

# Create a base class for declarative class definitions
Base = declarative_base()

# Abstract base model class with common fields
class BaseModel(Base):
    __abstract__ = True  # Indicates this class is abstract and not mapped to a table

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# User model representing a user in the system
class User(BaseModel):
    __tablename__ = "users"  # Table name in the database

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String, default="user")  # Possible roles: 'user', 'admin'
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    # cart: Mapped["Cart"] = relationship(back_populates="user")

    def __repr__(self):
        # String representation of the User object
        return f"<User id={self.id} email={self.email} username={self.username} role={self.role}>"

# Category model representing a product category
class Category(BaseModel):
    __tablename__ = "categories"  # Table name in the database

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name} description={self.description}>"

# Product model representing a product
class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="products")
    order_products: Mapped[list["OrderProduct"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product id={self.id} name={self.name} price={self.price}>"

# Order model representing a customer's order
class Order(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="orders")
    order_products: Mapped[list["OrderProduct"]] = relationship(back_populates="order")

    def __repr__(self):
        return f"<Order id={self.id} user_id={self.user_id}>"

# OrderProduct model representing the association between orders and products
class OrderProduct(BaseModel):
    __tablename__ = "order_products"

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    order: Mapped["Order"] = relationship(back_populates="order_products")
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship(back_populates="order_products")

    def __repr__(self):
        return f"<OrderProduct id={self.id} order_id={self.order_id} product_id={self.product_id}>"

# Cart model representing a user's shopping cart (commented out)
# class Cart(BaseModel):
#     __tablename__ = "carts"

#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
#     user: Mapped["User"] = relationship(back_populates="cart")
#     products: Mapped[list["Product"]] = relationship(back_populates="cart")

#     def __repr__(self):
#         return f"<Cart id={self.id} user_id={self.user_id}>"
