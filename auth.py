import base64
import requests
from loguru import logger

def construct_init_auth_url(app_key: str, app_secret: str) -> tuple[str, str, str]:
    """Construct the initial authorization URL and return app credentials."""
    auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={app_key}&redirect_uri=https://127.0.0.1"
    logger.info("Click to authenticate:")
    logger.info(auth_url)
    return app_key, app_secret, auth_url

def construct_headers_and_payload(returned_url: str, app_key: str, app_secret: str) -> tuple[dict, dict]:
    """Construct the headers and payload for the token request."""
    try:
        response_code = returned_url.split("code=")[1].split('&')[0]
    except IndexError:
        logger.error("Failed to extract code from the URL.")
        raise ValueError("Invalid returned URL format.")

    credentials = f"{app_key}:{app_secret}"
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": response_code,
        "redirect_uri": "https://127.0.0.1",
    }

    return headers, payload

def retrieve_tokens(headers: dict, payload: dict) -> dict:
    """Retrieve OAuth tokens using the provided headers and payload."""
    try:
        init_token_response = requests.post(
            url="https://api.schwabapi.com/v1/oauth/token",
            headers=headers,
            data=payload,
        )
        init_token_response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Token retrieval failed: {e}")
        raise

    init_tokens_dict = init_token_response.json()
    return init_tokens_dict
