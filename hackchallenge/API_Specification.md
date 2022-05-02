# API Specification
## Get all foods  
	GET /foods/ 
 
Response:

	<HTTP RESPONSE CODE 200>
	{
	    "foods": [
	        {
	            "id": 1,
	            "name": "ice cream",
	            "description": "Cornell Dairy",
	            "calories": 34,
	            "tags": [
	                {
	                    "id": 1,
	                    "name": "sweet",
	                    "color": "green"
	                },
	                {
	                    "id": 2,
	                    "name": "dessert",
	                    "color": "red"
	                }
	            ]
	        }, 
	        ...
	    ]
	}  

## Create a food  
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
>Note: In the request body, “name” must be nonempty; “description” must be nonempty; “calories” must be nonnegative integer. If the request is illegal, respond with an error message with status code 400.  
 
## Get food by id  
	GET /foods/{food_id}/  

Response

	<HTTP STATUS CODE 200>
	{
	    "id": 1,
	    "name": "ice cream",
	    "description": "Cornell Dairy",
	    "calories": 34,
	    "tags": [
	        {
	            "id": 1,
	            "name": "sweet",
	            "color": "green"
	        },
	        {
	            "id": 2,
	            "name": "dessert",
	            "color": "red"
	        }
	    ]
	}
  
>Note: If no food has the given id, respond with an error message.  
  
## Get food by name  
	GET /foods/{food_name}/  
 
Since multiple food entries are allowed to have have the same name, this route will return a __list__ of foods. If there are no foods with the given name, return an __empty list__ (not an error message). If exactly one food is matched with the given name, return a __list of one element__.
 
 Response

	<HTTP RESPONSE CODE 200>
	{
	    "foods": [
	        {
	            "id": 1,
	            "name": "ice cream",
	            "description": "Cornell Dairy",
	            "calories": 34,
	            "tags": [
	                {
	                    "id": 1,
	                    "name": "sweet",
	                    "color": "green"
	                },
	                {
	                    "id": 2,
	                    "name": "dessert",
	                    "color": "red"
	                }
	            ]
	        },
	        {
	            "id": 2,
	            "name": "ice cream",
	            "description": "Haagen Daz",
	            "calories": 32,
	            "tags": []
	        }
	    ]
	}
  
   
## Update food by id
	POST /foods/{food_id}/  

Request

	{
	    "name": "french fries",
	    "description": "with ketchup",
	    "calories": 35
	}

Response

	<HTTP RESPONSE CODE 200>
	{
	    "id": 3,
	    "name": "french fries",
	    "description": "with ketchup",
	    "calories": 35,
	    "tags": []
	}


  
>Note: If any field is not specified, then this route simply leaves that field unchanged. An error message will be returned if the calories field is not a nonnegative integer.  
 
## Delete food by id

	DELETE /foods/{food_id}/  

Return the deleted food

Response

	<HTTP RESPONSE CODE 200>
	{
	    "id": 2,
	    "name": "ice cream",
	    "description": "Haagen Daz",
	    "calories": 32,
	    "tags": [
	        {
	            "id": 1,
	            "name": "sweet",
	            "color": "green"
	        },
	        {
	            "id": 2,
	            "name": "dessert",
	            "color": "red"
	        }
	    ]
	}

## Get all tags  
	GET /tags/  
  
  Response

	<HTTP STATUS CODE 200>
	{
	    "tags": [
	        {
	            "id": 1,
	            "name": "dessert",
	            "color": "red",
	            "foods": []
	        },
	        {
	            "id": 2,
	            "name": "sweet",
	            "color": "green",
	            "foods": [
	                {
	                    "id": 2,
	                    "name": "ice cream",
	                    "description": "Haagen Daz",
	                    "calories": 32
	                }
	            ]
	        }
	    ]
	}
  
  
## Create a new tag  
	POST /tags/ 

Request

	{
	    "name": "sweet",
	    "color": "green"
	} 

Response

	<HTTP RESPONSE CODE 201>
	{
	    "id": 1,
	    "name": "sweet",
	    "color": "green",
	    "foods": []
	}

>Note: Return an error message is "name" or "color" field does not exist
  
## Get tag by id  

	GET /tags/{tag_id}/  

Response  

	<HTTP STATUS CODE 200>
	{
	    "id": 1,
	    "name": "sweet",
	    "color": "green",
	    "foods": [
	        {
	            "id": 2,
	            "name": "ice cream",
	            "description": "Haagen Daz",
	            "calories": 32
	        }
	    ]
	}

## Get tag by name
	GET /tags/{tag_name}/

Return a __list__ of tag whose name is the same as {tag_name}. If no tags are matched, return __an empty list__. If exactly one tag is matched, return __a list of one element__.

Response

	<HTTP STATUS 200>
	{
	    "tags": [
	        {
	            "id": 1,
	            "name": "sweet",
	            "color": "green",
	            "foods": [
	                {
	                    "id": 2,
	                    "name": "ice cream",
	                    "description": "Haagen Daz",
	                    "calories": 32
	                }
	            ]
	        }
	    ]
	}


## Add tag to food  

	POST /foods/{food_id}/add/  

Request:  

	{  
		"tag_id": <USER INPUT>  
	}

Response:

Return the food after adding the tag. 

	<HTTP STATUS CODE 200>
	{
	    "id": 2,
	    "name": "ice cream",
	    "description": "Haagen Daz",
	    "calories": 32,
	    "tags": [
	        {
	            "id": 2,
	            "name": "dessert",
	            "color": "red"
	        }
	    ]
	}

> Note: Return an error message if "tag_id" is not given in the request body. 

## Delete tag by id
	DELETE /tags/{tag_id}/

Response

	<HTTP STATUS CODE 200>
	{
	    "id": 1,
	    "name": "sweet",
	    "color": "green",
	    "foods": [
	        {
	            "id": 2,
	            "name": "ice cream",
	            "description": "Haagen Daz",
	            "calories": 32
	        }
	    ]
	}
