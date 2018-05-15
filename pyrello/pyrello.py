import requests
import json
import configparser
import sys
from . import configure

def write_csv_header(lists, board_name):
    first_line = "id, name,labels,start,end,"
    
    for card_list in lists:
        first_line+='"%s",' % card_list['name']

    with open("board_%s.csv" % board_name, 'w') as csv_file:
        csv_file.write("%s\n" % first_line)
 
def write_csv_cards(card_dict, lists, board_name):
    line = '"%s", "%s", "%s" ,"%s", "%s",' % (
            card_dict["id"], 
            card_dict["name"],
            card_dict["labels"],
            card_dict["start"],
            card_dict["end"]
            )
     
    for card_list in lists:
        if card_list["id"] in card_dict:
            line += '"%s",' % card_dict[card_list["id"]]
        else:
            line += ','
    with open("board_%s.csv" % board_name, 'a') as csv_file:
        csv_file.write("%s\n" % line)

def get_list_name(list_id):
    url = "https://api.trello.com/1/lists/%s" % list_id
    list_response = requests.request("GET", url)
    if list_response.status_code!=200:
        list_name = ""
    else:
        list_json = json.loads(list_response.text)
        list_name=list_json['name']

    return list_name


def get_labels_column(labels_list):
    label_column = ""
    for label in labels_list:
        label_column += "%s," % label["name"]
    return label_column[:len(label_column)-1]

def response_error(response):
    exit(response.text)

def get_action_value(action):
    if action['type']=="updateCard" and 'listAfter' in action['data']:
        list_key = "listAfter"
    elif action['type'] in ("createCard","copyCard"):
        list_key = "list"
    else:
        return None
    try:

        action_dict={
                'list_id' : action['data'][list_key]['id'],
                'list_name' : action['data'][list_key]['name'],
                'date' : action['date'][:10]
        }
    except Exception as e:
        action_dict={
                'list_id' : action['data'][list_key]['id'],
                'list_name' : get_list_name(action['data'][list_key]['id']),
                'date' : action['date'][:10]
        }
    return action_dict

def get_leadtime_date(selected_columns, lists, card_dict):
    leadtime_date=""
    for selected_column in selected_columns:
        list_id=""
        for board_list in lists:
            if board_list["name"].upper()==selected_column.upper():
                list_id = board_list["id"]
        if list_id in card_dict and card_dict[list_id]!="":
            leadtime_date=card_dict[list_id]
    return leadtime_date

def get_card_list(board_id):
    card_params = "labels=all&actions=copyCard,createCard,updateCard&lists=all"
    card_url="https://api.trello.com/1/boards/%s/cards?%s" % (board_id,card_params)
    card_response = requests.request("GET", card_url, params=querystring)
    if card_response.status_code!=200: response_error(card_response)

    data = json.loads(card_response.text)
    return data


def main():
    if len(sys.argv)>1 and sys.argv[1]=="--configure":
        configure.create_config_file()


    config = configparser.ConfigParser()
    config.read('config')

    try:
        if "AUTH" in config:
            querystring = {
                    "key": config["AUTH"]["Key"],
                    "token": config["AUTH"]["Token"]
            }
        else:
            exit("Try 'pyrello --configure' first")
    except Exception as e:
        exit(e)

    boards = config.sections()
    boards.remove("AUTH")

    for board in boards:
        print("%s - exporting..." % board)

        board_id = config[board]["id"]
        board_name = board
        start_columns = config[board]["start_columns"].split(",")
        end_columns = config[board]["end_columns"].split(",")

        lists_url="https://api.trello.com/1/boards/%s/lists/all" % board_id
        
        list_response = requests.request("GET", lists_url, params=querystring)
        if list_response.status_code!=200: response_error(list_response)
        
        lists = json.loads(list_response.text)
        write_csv_header(lists, board_name)
        
        card_list = get_card_list(board_id)
        for card in card_list:
            card_dict = { 
                    'id': card["id"],
                    "name": card["name"],
                    "labels": get_labels_column(card["labels"]),
                    "start": "",
                    "end": ""
            }
            
            for action in card['actions']:
                action_value = get_action_value(action)
                if action_value != None:
                    card_dict[action_value['list_id']] = action_value['date']
             
            card_dict['start'] = get_leadtime_date(start_columns, lists, card_dict)
            card_dict['end'] = get_leadtime_date(end_columns, lists, card_dict)

            if card_dict['start']=="": card_dict['start']=card_dict['end']

            write_csv_cards(card_dict, lists, board_name)
        print("board_%s.csv created" % board_name)

    exit("Done")

if __name__ == "__main__":
    main()
