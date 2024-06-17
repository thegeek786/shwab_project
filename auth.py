import base64
import requests
from loguru import logger

def construct_init_auth_url(app_key: str, app_secret: str) -> tuple[str, str, str]:
    # Construct the initial authorization URL and return app credentials.
    
    auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={app_key}&redirect_uri=https://127.0.0.1"  
    
    # Construct the auth URL
    
    logger.info("Click to authenticate:")  # Log the message to click the URL
    logger.info(auth_url)  # Log the actual URL
    return app_key, app_secret, auth_url  # Return the app key, secret, and auth URL

def construct_headers_and_payload(returned_url: str, app_key: str, app_secret: str) -> tuple[dict, dict]:
    
    # Construct the headers and payload for the token request.
    
    try:
        # Extract the response code from the returned URL
        response_code = returned_url.split("code=")[1].split('&')[0]  
    except IndexError:
        logger.error("Failed to extract code from the URL.")  # Log error if extraction fails
        raise ValueError("Invalid returned URL format.")  # Raise exception if URL format is invalid

    credentials = f"{app_key}:{app_secret}"  # Concatenate app key and secret
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")  # Encode credentials in base64

    headers = {
        "Authorization": f"Basic {base64_credentials}",  # Authorization header with base64 credentials
        "Content-Type": "application/x-www-form-urlencoded",  # Content type for form URL encoding
    }
    
    payload = {
        "grant_type": "authorization_code",  # Grant type for the payload
        "code": response_code,  # Extracted code from the URL
        "redirect_uri": "https://127.0.0.1",  # Redirect URI
    }

    return headers, payload  # Return the headers and payload

def retrieve_tokens(headers: dict, payload: dict) -> dict:
    """Retrieve OAuth tokens using the provided headers and payload."""
    try:
        # Make the token request
        init_token_response = requests.post(
            url="https://api.schwabapi.com/v1/oauth/token",  # Token URL
            headers=headers,  # Headers for the request
            data=payload,  # Payload for the request
        )
        init_token_response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        logger.error(f"Token retrieval failed: {e}")  # Log error if token retrieval fails
        raise

    init_tokens_dict = init_token_response.json()  # Parse the JSON response
    return init_tokens_dict  # Return the tokens dictionary
