# Receipt Processor Challenge Solution for Fetch


This is my solution to the given challange. We're using Flask framework to create a simple webapp for processing receipts and calculating reward points.
We have implemented two API endpoints: 
1. Process Receipts. [POST]
2. Get point. [GET]

# Installation
### Prerequisites
* Python 3.7+
* pip
* pytest
  
### Steps
1. Clone the repository:
```
git clone https://github.com/Mikheil-U/receipt-processor-challenge_solution.git
cd processor_app
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the Flask app:
```
python app.py ($ python3 app.py for linux/macos)
```
4. Access the application at:
```
http://127.0.0.1:5000
```

# API Endpoints
**
Make sure that the Flask server is running. Next provide a sample JSON payload(example below), Use cURL or Postman to test the endpoint. 
**
### Method: POST
```
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "15:01",
  "items": [
    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
  ],
  "total": "35.35"
}

```
* Response:
```
{
   id: "8f1fa1ad-6ef8-4fc4-b865-b166cc4cd7c4"
}
```
### MethodL: GET
* Response:
```
{
  "points": 30
}
```

# To run tests:
1. Install pytest module for Python testing.
```
pip install pytest
```
2. Run the tests:
```
python -m unittest test_processor.py
```




