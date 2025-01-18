from utils.env_vars import read_env_file


def main():
    #read config file
    env_file_path = '.env_variable_file'
    env_vars = read_env_file(env_file_path)
    #initialize Decider PositionList Logger Market and Gui
