# E-Commerce RESTful API  

## Overview  
This is a production-ready RESTful API for an e-commerce platform that allows users to:  
- View available products  
- Add new products  
- Place orders with stock validation  

## Technologies Used  
- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- Docker  

## Setup  

### 1. Clone the Repository  
```bash
git clone <repo-url>
cd e-commerce-api
```

### 2. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3. Run the Application  
```bash
uvicorn main:app --reload
```

### 4. Run with Docker  
```bash
sudo docker build -t my-fastapi-app .
sudo docker run -p 8000:80 my-fastapi-app
```

## API Endpoints  
- **GET /products** → Retrieve all products  
- **POST /products** → Add a new product  
- **POST /orders** → Place an order  

## Testing  
Run tests using:  
```bash
pytest
```

## Author  
Your Name  
