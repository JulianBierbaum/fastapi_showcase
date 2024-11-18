# What is FastApi

**FastAPI** is a web framework for building APIs quickly and easily with Python. It uses **type hints** to automatically check and process your data, and it creates **interactive documentation** for your API so you can test it right in your browser.


# Setup for FastApi

To install fastapi and all other needed packages run this command in your VS-Code Terminal

    pip install -r ./requirements.txt

it installs fastapi and some optional dependencies 

# Using FastApi

now you can create your python file 'filename.py' and if you want to run it you need to use this command

    fastapi dev filename.py

now you can access your api in your browser using
    
    http://127.0.0.1:8000

or
    
    localhost:8000

A useful tool are the automatic Interactive API docs using Swagger UI and ReDoc allowing you to test and explore your endpoints in a web interface by visiting

    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc

# JWT explained

* JWT (JSON Web Token) is a standard for securely transmitting information between parties as a JSON object.
* A JWT consists of three parts: a header, a payload (claims), and a signature.
  * Header
    * Contains metadata about the token, such as the type of token (JWT) and the signing algorithm used (e.g., HS256 or RS256).

example header:
```
{
"alg": "HS256",
"typ": "JWT"
}
```

  * Payload
    * Contains the claims (information) about the user or entity. Claims can be:
      * Registered Claims (e.g., sub, exp, iss).
      * Public Claims (custom claims, agreed upon by both parties).
      * Private Claims (custom claims used between the sender and receiver).
example payload:
```
{
  "name": "John Doe",
  "age": 30,
  "email": "john.doe@example.com",
  "isActive": true
}
```

  * Signature
    * Used to verify the authenticity of the token and ensure it hasn’t been tampered with. It is generated by signing the encoded header and payload with a secret key (or private key in case of asymmetric signing).
example signature:
```
HMACSHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload),
    secret)
```
* Authentication with JWT involves generating a token after the user logs in and sending it back for future requests.
* Authorization uses the information within the JWT (like roles or permissions) to control access to resources.
* Benefits of JWT include being compact, self-contained, stateless, and cross-platform.
* Security concerns include keeping the secret key safe, using strong signing algorithms, setting token expiration, and managing token revocation effectively.