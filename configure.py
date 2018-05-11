import configparser

config = configparser.ConfigParser()

print("First we need to configure your Trello Auth. Get your key and token "\
        "access at developer.trello.com")

config['AUTH'] = {'Key': input("User KEY: "),
        'Token': input("User TOKEN: ")}

print("Now, export your board using the Json option and get your board ID")

more="Y"
board_list = []

while more=="Y":
    board_id = input("Board ID: ")
    more = input("Do you want to export another board? (Y/N): ").upper()
    board_list.append(board_id)

config['BOARDS'] = {"BoardList": board_list}

with open('config', 'w') as configfile:
    config.write(configfile)

exit("Ready to go.")
