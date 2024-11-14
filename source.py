import hmac
import hashlib
import time
import urllib.parse

class ValidationError(Exception):
    """Exception raised for errors in the validation process."""
    pass

def _secret_key(bot_token: str) -> bytes:
    """
    Generates a secret key using the bot token and the constant string "WebAppData".
    
    Args:
        bot_token (str): The bot token provided by Telegram.
    
    Returns:
        bytes: The generated secret key using HMAC-SHA-256.
    """
    return hmac.new(b"WebAppData", bot_token.encode('utf-8'), hashlib.sha256).digest()


def _hmac_hash(secret_key: bytes, data_check_string: str) -> str:
    """
    Computes HMAC-SHA-256 of the data_check_string using the secret_key.
    
    Args:
        secret_key (bytes): The secret key derived from the bot token.
        data_check_string (str): The data string to be hashed.
    
    Returns:
        str: The calculated HMAC hash in hexadecimal format.
    """
    return hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()


def validate_init_data(init_data: str, bot_token: str, expiration_time: int = 3600) -> bool:
    """
    Validates the initialization data received from the Telegram WebApp.
    
    Args:
        init_data (str): The initialization data received from Telegram WebApp.
        bot_token (str): The bot token provided by Telegram.
        expiration_time (int): The expiration time for the data in seconds (default 3600 seconds = 1 hour).
    
    Returns:
        bool: True if the data is valid, False if the data is invalid or expired.
    
    Raises:
        ValidationError: If the data is missing required parameters or is expired.
    """
    
    # Ensure required parameters are present in the init_data.
    data_requirements = ['user', 'chat_instance', 'chat_type', 'auth_date', 'hash']
    for data_req in data_requirements:
        if data_req not in init_data:
            raise ValidationError(f"Invalid format: Missing {data_req} in init_data.")
    
    # Parse the URL-encoded data into a dictionary.
    data = dict(urllib.parse.parse_qsl(init_data))
    
    # Extract the 'hash' field and remove it from the data dictionary.
    received_hash = data.pop('hash')
    
    # Construct the data string to check against the hash.
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items())])
    
    # Compute the HMAC hash using the secret key and the data string.
    secret_key = _secret_key(bot_token)
    calculated_hash = _hmac_hash(secret_key, data_check_string)
    
    # Compare the received hash with the calculated hash.
    if received_hash != calculated_hash:
        return False
        
    # Verify the expiration time.
    try:
        auth_date = int(data.get('auth_date'))
    except (TypeError, ValueError):
        raise ValidationError("Invalid 'auth_date' value in init_data.")
    
    current_time = int(time.time())
    if current_time - auth_date > expiration_time:
        return False
        
    return True