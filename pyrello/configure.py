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
        start_columns = input("What are the column names that represent the"\
                " beginning of your lead time? (use comma to separate multiple"\
                " columns)\n")
        end_columns = input("What are the column names that represent the"\
                " end of your lead time? (use comma to separate multiple"\
                " columns)\n")

        more = input("Do you want to export another board? (Y/N): ").upper()
        config[board_name.upper()] = {
                'id' : board_id,
                'start_columns' : start_columns,
                'end_columns' : end_columns
        }

    with open('config', 'w') as configfile:
        config.write(configfile)

    exit("Ready to go.")

if __name__ == "__main__":
    create_config_file()
