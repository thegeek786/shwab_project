import webbrowser
from loguru import logger
from auth import construct_init_auth_url, construct_headers_and_payload, retrieve_tokens
from config import load_config

def main():
    # Load configuration
    app_key, app_secret = load_config()
    
    # Get the initial auth URL and credentials
    app_key, app_secret, cs_auth_url = construct_init_auth_url(app_key, app_secret)
    
    # Open the authorization URL in the default web browser
    webbrowser.open(cs_auth_url)
    
    logger.info("Paste Returned URL:")
    returned_url = input().strip()
    
    try:
        # Construct headers and payload for the token request
        init_token_headers, init_token_payload = construct_headers_and_payload(returned_url, app_key, app_secret)
        
        # Retrieve the tokens using the constructed headers and payload
        init_tokens_dict = retrieve_tokens(headers=init_token_headers, payload=init_token_payload)
        
        logger.debug(init_tokens_dict)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return "Done!"

if __name__ == "__main__":
    main()
