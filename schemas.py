PRODUCT_ITEM_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "brand", "category"],
    "properties": {
        "id":    {"type": "integer"},
        "name":  {"type": "string"},
        "price": {"type": "string"},
        "brand": {"type": "string"},
        "category": {
            "type": "object",
            "required": ["usertype", "category"],
            "properties": {
                "usertype": {
                    "type": "object",
                    "required": ["usertype"],
                    "properties": {
                        "usertype": {"type": "string"}
                    }
                },
                "category": {"type": "string"}
            }
        }
    }
}

PRODUCTS_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "products"],
    "properties": {
        "responseCode": {"type": "integer"},
        "products": {
            "type": "array",
            "items": PRODUCT_ITEM_SCHEMA
        }
    }
}

BRANDS_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "brands"],
    "properties": {
        "responseCode": {"type": "integer"},
        "brands": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "brand"],
                "properties": {
                    "id":    {"type": "integer"},
                    "brand": {"type": "string"}
                }
            }
        }
    }
}

USER_DETAIL_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "user"],
    "properties": {
        "responseCode": {"type": "integer"},
        "user": {
            "type": "object",
            "required": ["id", "name", "email"],
            "properties": {
                "id":    {"type": "integer"},
                "name":  {"type": "string"},
                "email": {"type": "string"}
            }
        }
    }
}

MESSAGE_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["responseCode", "message"],
    "properties": {
        "responseCode": {"type": "integer"},
        "message":      {"type": "string"}
    }
}
