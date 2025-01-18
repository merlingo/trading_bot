from dotenv import load_dotenv
import os

def read_env_file(env_file_path):
    """
    Reads environment variables from the specified .env file.

    Args:
        env_file_path (str): The path to the .env file.

    Returns:
        dict: A dictionary containing the environment variables.
    """
    # Load the environment variables from the specified file
    load_dotenv(env_file_path)
    
    # Retrieve the environment variables
    env_vars = {key: os.getenv(key) for key in os.environ.keys()}

    return env_vars

if __name__ == '__main__':
    # Example usage:
    env_file_path = '.env_variable_file'
    env_vars = read_env_file(env_file_path)
    print(env_vars)