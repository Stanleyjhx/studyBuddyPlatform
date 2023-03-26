Authentication_req = {
    "identifier": {
        "type": str,
        "required": True
    },
    "password": {
        "type": str,
        "required": True,
    }
}


def unauthenticated_response():
    return {
        "status": 401,
        "error": "Invalid or password or status."
    }


def authenticated_response(token):
    return {
        "status": 200,
        "data": {
            "token": token
        }
    }
