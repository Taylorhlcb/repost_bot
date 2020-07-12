from configparser import ConfigParser, ExtendedInterpolation
import textwrap
import os
import sys
import logging


class config:
    def __init__(self):
        self.config_parser = ConfigParser(interpolation=ExtendedInterpolation())
        try:
            if sys.argv[2] == "home":
                self.config_manage_path = os.path.expanduser("~") + os.sep + "repost_bot"
        except:
            self.config_manage_path = os.path.dirname(os.path.realpath(__file__))
        try:
            self.config_name = sys.argv[1]
        except:
            self.config_name = input(textwrap.dedent(
                            """
                            # This is a name appended to the config file for referencing multiple configs
                            Enter the config_name you wish to use : """))
        self.config_file_name = ("repost_bot_config_{}.ini").format(self.config_name)
        self.config_file_path = self.config_manage_path + os.sep + self.config_file_name
        ### Logger ###
        self.logger_file_name = ("repost_bot_logger_{}.log").format(self.config_name)
        self.logger = logging.getLogger(self.logger_file_name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.fh = logging.FileHandler(self.config_manage_path + os.sep + self.logger_file_name)
        self.fh.setLevel(logging.INFO)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        try:
            self.read_config()
            self.config_parser.read(self.config_file_path)
            print(textwrap.dedent(
            """
            # Reading from '{}' config file:
            # {}
            """.format(self.config_name, self.config_file_path)))
        except:
            print(textwrap.dedent(
            """\n
            ##################################################################
            # This is the default setup config for repost_bot                #
            # You're seeing this because no config was found by that name    #
            # Please enter the requested information                         #
            ##################################################################
            """))
            bot_token = input(textwrap.dedent(
                    """\n
                    # For help with getting your bot token visit
                    # https://core.telegram.org/bots#botfather
                    Enter bot_token : """))
            chat_id = input(textwrap.dedent(
                    """\n
                    # Note this is the chat room the bot will check for new users in
                    # For help with getting your chatroom ID visit
                    # https://answers.splunk.com/answers/590658/telegram-alert-action-where-do-you-get-a-chat-id.html
                    Enter chat_id for bot to monitor : """))
            bot_name = input(textwrap.dedent(
                    """\n
                    # Note this is the name that users will type to issue commands ex: '/botname command params'
                    # If a bot_name is not supplied bot commands will be disabled (This is no commands for this yet lol)
                    Enter bot_name for bot send alerts to : """))
            self.config_parser['bot_info_settings'] = {
                'bot_token' : bot_token,
                'chat_id' : chat_id,
                'bot_name' : bot_name
            }
            self.config_parser['bot_api_settings'] = {
                'pipe_timeout' : 10, # Number of seconds the pipe stays open when requesting new data
                'pipe_offset' : -50, # Number of messages displayed when requesting an update
                'pipe_limit' : 50
            }
            self.config_parser[bot_name] = {
                "text" : "I am an authentication bot. For commands type '/${bot_info_settings:bot_name} command_list'",
                "cooldown" : "0",
                "admin_only" : False
            }
            self.config_parser['version'] = {
                "text" : "'/${bot_info_settings:bot_name} version' : Displays the current version",
                "cooldown" : "0",
                "admin_only" : False
            }
            self.write_config()
            print("\nCreated {}".format(self.config_file_path))

    def read_config(self):
        with open(self.config_file_path, "r") as config_file:
            return config_file.read()

    def write_config(self):
        with open(self.config_file_path, "w+") as config_file:
            self.config_parser.write(config_file)

def main():
    cfg = config()
    print(cfg.config_parser.get('bot_info_settings', 'bot_token'))

if __name__ == '__main__':
    main()