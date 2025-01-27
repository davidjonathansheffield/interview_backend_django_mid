# Challenge 8: Adding an Item to Inventory with Metadata

## Step 1. Creating an Inventory Item through the API.

Our API has a multi-purpose create and list endpoint.  This endpoint is:

/inventory/

If you use a GET request, you will get a list of all inventory items.  
If you use a POST request, you can create a new inventory item.

You will want to create a new inventory item thusly by:

POST /inventory/ 

With the appropriate data in the body of the request, which is:
```python
{
    "name": "A string name",
    "type": {"name": "Type name, must be unique"},
    "language": {"name": "Language name, must be unique"},
    "metadata": {
        "key": "value",
        "key2": "value2"
    }
    "tags": [
        {"name": "tag1"},
        {"name": "tag2"},
    ],
}
```

You'll always want to include the following metadata tags:

- `year`
- `actor`
- `imdb_rating`
- `rotten_tomatoes_rating`
- `film_locations`
