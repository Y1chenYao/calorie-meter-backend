Implemented db.py app.py


Tested via postman

# API Specification

## Get all foods
> __GET__ /foods/
Response:
Adding a food to the database
POST /foods/
Request:
{
    "name": "ice cream",
    "description": "vanilla Cornell Dairy",
    "calories": 40
}
Response:
<HTTP STATUS CODE 201>
{
    "id": 1,
    "name": "ice cream",
    "description": "vanilla Cornell Dairy",
    "calories": 40,
    "tags": []
}
Note: For request body, “name” must be nonempty; “description” must be nonempty; “calories” must be nonnegative integer. If the request is illegal, respond with an error message with status code 400.

Get Food by id
GET /foods/{food_id}/

Note: If no food has the given id, respond with an error message.


Get food by name
GET /foods/{food_name}/

Note: Return a list of foods with the given name, since multiple food entries can have the same name. If there are no foods with the given name, return an empty list (not an error message).

POST /foods/{food_id}/
Update a food by id. 

Note: If any field is not specified, then does not change that field. However, will return an error message if the calories field is not a nonnegative integer.

DELETE /foods/{food_id}/
Deleting a food by id
