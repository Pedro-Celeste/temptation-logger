import json
import os
import re
import inquirer

# --- Variables ---

CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "config.json")

# --- Helper Functions ---

def validate_not_empty(answers, current):
        if not re.match(r".+", current):
            raise inquirer.errors.ValidationError("",
                reason = "An empty message isn't allowed.")
        return True

def prompt_temptation():
    answer = inquirer.list_input("What is tempting you",
        choices  = ["... Add a new temptation", *get_config_list("temptation_list")])
    if answer == "... Add a new temptation":
        answer = inquirer.text(message = "Enter the new temptation",
            validate = validate_not_empty)
        print("\n")
        CONFIG["temptation_list"].append(answer)
        save_config()
    return answer

def prompt_intensity():
    def intensity_validation(answers, current):
        if not re.match(r"\b[1-5]\b", current):
            raise inquirer.errors.ValidationError("",
                reason = "Only numbers from 1 to 5.")
        return True

    question = [inquirer.Text(name = "intensity",
        message = "From 1 to 5, how intense is the temptation",
        validate = intensity_validation)]
    
    answer = inquirer.prompt(question)
    print("\n")
    return answer["intensity"]

def prompt_cue():
    answer = inquirer.list_input("The cue that prompted it",
        choices  = ["... Add a new cue", *get_config_list("cue_list")])
    if answer == "... Add a new cue":
        answer = inquirer.text(message = "Enter the new cue",
            validate = validate_not_empty)
        print("\n")
        CONFIG["cue_list"].append(answer)
        save_config()
    return answer

def create_log():
    log = {}
    log["temptation"] = prompt_temptation()
    log["intensity"] =  prompt_intensity()
    log["cue"] = prompt_cue()

    # Optional Description
    add_description = inquirer.confirm(
        "Do you want to add a description?", default=False)
    if add_description:
        log["description"] = inquirer.text(
            message = "Write a short description of what happened: ",
            validate = validate_not_empty)
    else:
        log["description"] = None

    return log

def load_config():
    # Create a config file if it doesn't exist
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as config_file:
            json.dump({}, config_file, indent = 2)
    
    with open(CONFIG_PATH, "r") as config_file:
        return json.load(config_file)

def save_config():
    global CONFIG
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(CONFIG, config_file, indent = 2)


def set_archive_path(path):
    global CONFIG
    CONFIG["archive_path"] = path

def get_config_list(list_name):
    global CONFIG
    if list_name not in CONFIG.keys():
        CONFIG[list_name] = []
    return CONFIG[list_name]


CONFIG = load_config()
print(create_log())