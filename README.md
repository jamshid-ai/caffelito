# Caffelito

Caffelito is a web application designed to manage users, orders, and categories for an e-commerce platform. It is built using FastAPI and SQLAlchemy, providing a robust and scalable solution for handling various operations related to users, orders, and categories.

## Features

- User registration, authentication, and management
- Order creation, retrieval, updating, and deletion
- Category creation, retrieval, updating, and deletion
- JWT-based authentication and authorization
- Dependency injection for services and user handling

## Project Structure

The project is organized into several modules, each responsible for a specific aspect of the application:

- `apps/users`: Handles user-related operations such as registration, authentication, and management.
- `apps/orders`: Manages order-related operations including creation, retrieval, updating, and deletion.
- `apps/categories`: Manages category-related operations including creation, retrieval, updating, and deletion.
- `core`: Contains core functionalities such as JWT handling, security, and dependencies.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/caffelito.git
    cd caffelito
    ```

2. Build the Docker image:
    ```bash
    docker compose up --build
    ```

3. Run the Docker container:
    ```bash
    docker compose up
    ```

4. Set up the database:
    ```bash
    docker exec -it fastapi_app alembic upgrade head
    ```

## Installation 2

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/caffelito.git
    cd caffelito
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    alembic upgrade head
    ```

## Usage

### Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

### Access the API documentation:
    ```bash
    http://127.0.0.1:8000/docs
    ```

## API Endpoints

### Users

- `POST /users/registration`: Register a new user
- `POST /users/authentication`: Authenticate a user and obtain a JWT token
- `POST /users/verification`: Verify a user's email
- `GET /users/me`: Get the authenticated user's details
- `GET /users`: Retrieve a list of users
- `GET /users/{user_id}`: Retrieve a specific user by ID
- `PUT /users/{user_id}`: Update a user's details
- `PATCH /users/{user_id}`: Partially update a user's details
- `DELETE /users/{user_id}`: Delete a user

### Orders

- `POST /orders`: Create a new order
- `GET /orders`: Retrieve a list of orders
- `GET /orders/{order_id}`: Retrieve a specific order by ID
- `PUT /orders/{order_id}`: Update an order's details
- `PATCH /orders/{order_id}`: Partially update an order's details

### Categories

- `POST /categories`: Create a new category
- `GET /categories`: Retrieve a list of categories
- `GET /categories/{category_id}`: Retrieve a specific category by ID
- `PUT /categories/{category_id}`: Update a category's details
- `PATCH /categories/{category_id}`: Partially update a category's details

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
