import os
import base64  # For encoding credentials
import requests  # For making HTTP requests
import webbrowser  # For opening the authorization URL in the browser
from loguru import logger  # For logging information

def construct_init_auth_url() -> tuple[str, str, str]:

    #Construct the initial authorization URL and return app credentials.

    app_key = "l9S9cagSL6X4sjWGtlbb6SR0PgHVRcWi"  # Application key
    app_secret = "E3sbVNSooJQGYlt4"  # Application secret

    # Construct the authorization URL with the client ID and redirect URI
    auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={app_key}&redirect_uri=https://127.0.0.1"
    
    logger.info("Click to authenticate:")  # Log the message to click the URL
    logger.info(auth_url)  # Log the actual URL
    
    return app_key, app_secret, auth_url  # Return the credentials and URL

def construct_headers_and_payload(returned_url: str, app_key: str, app_secret: str) -> tuple[dict, dict]:
    
    #Construct the headers and payload for the token request.

    # Extract the response code from the returned URL
    response_code = f"{returned_url[returned_url.index('code=') + 5: returned_url.index('%40')]}@"
    
    # Create the base64 encoded credentials
    credentials = f"{app_key}:{app_secret}"
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    # Construct the headers for the token request
    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    # Construct the payload for the token request
    payload = {
        "grant_type": "authorization_code",
        "code": response_code,
        "redirect_uri": "https://127.0.0.1",
    }
    
    return headers, payload  # Return the headers and payload

def retrieve_tokens(headers: dict, payload: dict) -> dict:
    
    #Retrieve OAuth tokens using the provided headers and payload.

    # Make a POST request to the token endpoint to retrieve tokens
    init_token_response = requests.post(
        url="https://api.schwabapi.com/v1/oauth/token",
        headers=headers,
        data=payload,
    )
    
    # Parse the JSON response into a dictionary
    init_tokens_dict = init_token_response.json()
    
    return init_tokens_dict  # Return the tokens dictionary

def main():

    app_key, app_secret, cs_auth_url = construct_init_auth_url()  # Get the initial auth URL and credentials
    webbrowser.open(cs_auth_url)  # Open the authorization URL in the default web browser
    
    logger.info("Paste Returned URL:")  # Prompt user to paste the returned URL
    returned_url = input()  # Get the URL input from the user
    
    # Construct headers and payload for the token request
    init_token_headers, init_token_payload = construct_headers_and_payload(returned_url, app_key, app_secret)
    
    # Retrieve the tokens using the constructed headers and payload
    init_tokens_dict = retrieve_tokens(headers=init_token_headers, payload=init_token_payload)
    
    logger.debug(init_tokens_dict)  # Log the retrieved tokens for debugging
    return "Done!" 

if __name__ == "__main__":
    main() 
