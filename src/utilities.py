from datetime import datetime
import json

def save_log(name, log_dictionary):
    """
        Fonction pour sauvegarder les nombres generes lors de l'execution
    """
    with open("../logs/"+name+str(datetime.now())+".json", 'w') as fp:
        json.dump(log_dictionary, fp)