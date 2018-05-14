import configparser
def create_config_file():
    config = configparser.ConfigParser()

    print("First we need to configure your Trello Auth. Get your key and token "\
            "access at developer.trello.com")

    config['AUTH'] = {'Key': input("User KEY: "),
            'Token': input("User TOKEN: ")}

    print("Export your board using the Json option and get your board ID")

    more="Y"

    while more=="Y":

        board_name = input("Board Name: ")
        board_id = input("Board ID: ")
        start_collumn = input("What's the name of the collumn that represents "\
                "the begning of your LeadTime? ")
        end_collumn = input("What's the name of the collumn that represents "\
                "the end of your LeadTime? ")

        more = input("Do you want to export another board? (Y/N): ").upper()
        config[board_name.upper()] = {
                'id' : board_id,
                'start_collumn' : start_collumn,
                'end_collumn' : end_collumn
        }

    with open('config', 'w') as configfile:
        config.write(configfile)

    exit("Ready to go.")

if __name__ == "__main__":
    create_config_file()
