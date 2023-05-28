import json
import os

# --- Helper Functions ---

def create_log():
    log = {}
    log["temptation"] = input("What is tempting you? ")
    log["intensity"] =  (input("From 1 to 5, how intense is the temptation? "))
    log["cue"] = input("What was the cue that prompted it? ")

    # Optional Description
    add_description = input("Do you want to add a description? (Y/n) ").lower()
    if add_description == "y" or add_description == "yes":
        log["description"] = input("Write a short description of what happened: ")

    return log

def load_config():
    # Create a config file if it doesn't exist
    CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "config.json")
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as config_file:
            json.dump({}, config_file, indent = 2)
    
    with open(CONFIG_PATH, "r") as config_file:
        return json.load(config_file)

def set_archive_path(path):
    global CONFIG
    CONFIG["archive_path"] = path
