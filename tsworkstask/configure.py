from configparser import ConfigParser

def reading_config():
    config = ConfigParser()

    config.read("company_names.ini")

    # Reading Company list inside of .ini file
    config_data = config["Company"]
    return config_data
