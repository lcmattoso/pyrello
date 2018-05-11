import requests
import json
import configparser
import sys
from . import configure

def write_csv_header(lists, board_id):
    first_line = "id, name,labels,"
    
    for card_list in lists:
        first_line+='"%s",' % card_list['name']

    with open("%s.csv" % board_id, 'w') as csv_file:
        csv_file.write("%s\n" % first_line)
 
def write_csv_cards(card_dict, lists, board_id):
    line = '"%s", "%s", "%s",' % (
            card_dict["id"], 
            card_dict["name"],
            card_dict["labels"])
     
    for card_list in lists:
        if card_list["id"] in card_dict:
            line += '"%s",' % card_dict[card_list["id"]]
        else:
            line += ','
    with open("%s.csv" % board_id, 'a') as csv_file:
        csv_file.write("%s\n" % line)


def get_labels_collumn(labels_list):
    label_collumn = ""
    for label in labels_list:
        label_collumn += "%s," % label["name"]
    return label_collumn[:len(label_collumn)-1]

def response_error(response):
    exit(response.text)

def get_action_value(action):
    if action['type']=="updateCard" and 'listAfter' in action['data']:
        list_key = "listAfter"
    elif action['type'] in ("createCard","copyCard"):
        list_key = "list"
    else:
        return None

    action_dict={
            'id_list': action['data'][list_key]['id'],
            'date': action['date'][:10]
    }
    return action_dict

 
def main():
    if len(sys.argv)>1 and sys.argv[1]=="--configure":
        configure.create_config_file()


    config = configparser.ConfigParser()
    config.read('config')

    try:
        if "AUTH" in config and "BOARDS" in config:
            querystring = {
                    "key": config["AUTH"]["Key"],
                    "token": config["AUTH"]["Token"]
            }
        else:
            exit("Try 'pyrello --configure' first")
    except Exception as e:
        exit(e)


    for board_id in eval(config['BOARDS']['BoardList']):
        print("%s - exporting..." % board_id) 
        lists_url="https://api.trello.com/1/boards/%s/lists/all" % board_id
        
        list_response = requests.request("GET", lists_url, params=querystring)
        if list_response.status_code!=200: response_error(list_response)
        
        lists = json.loads(list_response.text)

        card_params = "labels=all&actions=copyCard,createCard,updateCard&lists=all"
        card_url="https://api.trello.com/1/boards/%s/cards?%s" % (board_id,card_params)
        card_response = requests.request("GET", card_url, params=querystring)
        if card_response.status_code!=200: response_error(card_response)

        data = json.loads(card_response.text)

        write_csv_header(lists, board_id)
        for card in data:
            card_dict = { 
                    'id': card["id"],
                    "name": card["name"],
                    "labels": get_labels_collumn(card["labels"])
            }

            for action in card['actions']:
                action_value = get_action_value(action)
                if action_value != None:
                    card_dict[action_value['id_list']] = action_value['date']
        
            write_csv_cards(card_dict, lists, board_id)
        print("%s.csv created" % board_id)

    exit("Done")

if __name__ == "__main__":
    main()
