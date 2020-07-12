#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Description
This module is dedicated to reeing at reposters



"""

# https://core.telegram.org/bots/api

# Built-in imports
import urllib
import json
import sqlite3
import re as regex
import os
import io
import sys
import string
from time import time, sleep
from random import choice
from pprint import pprint

# Libs
import requests
from PIL import Image
import imagehash

# Own modules
import config_manager

class repost_bot:
    def __init__(self):
        ### Config settings ###
        # Bot info settings #
        self.config_manager_obj = config_manager.config()
        # Start logger #
        self.logger = self.config_manager_obj.logger
        self.logger.info("Starting auth_bot with {} config.".format(self.config_manager_obj.config_name))
        self.cfg = self.config_manager_obj.config_parser
        self.bot_token = self.cfg.get('bot_info_settings', 'bot_token')
        self.chat_id = self.cfg.getint('bot_info_settings', 'chat_id')
        self.bot_name = self.cfg.get('bot_info_settings', 'bot_name')
        # Bot api settings #
        #self.update_string = "getUpdates"
        self.update_string = "getUpdates?timeout={}&offset={}&limit={}".format(
                self.cfg.getint('bot_api_settings', 'pipe_timeout'),
                self.cfg.getint('bot_api_settings', 'pipe_offset'),
                self.cfg.getint('bot_api_settings', 'pipe_limit'))
        print(self.update_string)
        ### END of Config settings ###
        # self.dbname = "storage.sqlite"
        # self.conn = sqlite3.connect(self.config_manager_obj.config_manage_path + os.sep + self.dbname)
        self.url = "https://api.telegram.org/bot{}/".format(self.bot_token)
        self.update_string = self.url + self.update_string
        #What?
        self.management = list()
        self.storage_path = os.path.join(self.config_manager_obj.config_manage_path, "images")
        #average_hashes
        self.average_hash_file = os.path.join(self.storage_path, "average_hashes.json")
        self.average_hashes = self.open_storage(self.average_hash_file)
        #differance_hashes
        self.difference_hash_file = os.path.join(self.storage_path, "difference_hashes.json")
        self.difference_hashes = self.open_storage(self.difference_hash_file)
        #wavelet_hashes
        self.wavelet_hash_file = os.path.join(self.storage_path, "wavelet_hashes.json")
        self.wavelet_hashes = self.open_storage(self.wavelet_hash_file)
        #perceptive_hashes
        self.perceptive_hash_file =  os.path.join(self.storage_path, "perceptive_hashes.json")
        self.perceptive_hashes = self.open_storage(self.perceptive_hash_file)

    def open_storage(self, path):
        if (os.path.isfile(path)):
            with open(path) as storage_file:
                hash_dict = json.load(storage_file)
        else:
            print("Failed to find {}".format(path))
            with open(path, 'w') as storage_file:
                storage_file.writelines("{}")
            hash_dict = {}
        return hash_dict

    # Simply fetch the json update list
    # https://core.telegram.org/bots/api#getupdates
    def get_Updates_return_json(self):
        while True:
            response = self.request_url(self.update_string)
            json_response_data = json.loads(response.content)# Use json lib return parsed response
            if "result" in json_response_data:
                return json_response_data["result"]
            print("Error when gathering results from json object")
            print(response)
            sleep(1)

    def request_url(self, url):
        start_time = time()
        while True:
            try:
                #print("Request URL")
                #start_time = time()
                #print(url)
                response = requests.get(url)
                #print("Response = {} Time = {}".format(response, time() - start_time))
                response.raise_for_status()
                if response.json():
                    return response
                else:
                    print("Request returned a response that is not JSON.")
            except requests.exceptions.HTTPError as errHTTP:
                print("Http Error: ",errHTTP)
            except requests.exceptions.ConnectionError as errConnection:
                print("Error Connecting: ",errConnection)
            except requests.exceptions.Timeout as errTimeout:
                print("Timeout Error: ",errTimeout)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else ",err)
            print("Retrying in 10 seconds... (Exception for {} seconds)".format(int(time()) - int(start_time)))
            sleep(10)
            print("Retrying now")

    def request_url_once(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.json():
                return response
            else:
                print("Request returned a response that is not JSON.")
                return None
        except requests.exceptions.HTTPError as errHTTP:
            print("Http Error: ",errHTTP)
            return(errHTTP)
        except requests.exceptions.ConnectionError as errConnection:
            print("Error Connecting: ",errConnection)
            return(errConnection)
        except requests.exceptions.Timeout as errTimeout:
            print("Timeout Error: ",errTimeout)
            return(errTimeout)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else ",err)
            return(err)


    def request_url_stream(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as errHTTP:
            print("Http Error: ",errHTTP)
            return(errHTTP)
        except requests.exceptions.ConnectionError as errConnection:
            print("Error Connecting: ",errConnection)
            return(errConnection)
        except requests.exceptions.Timeout as errTimeout:
            print("Timeout Error: ",errTimeout)
            return(errTimeout)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else ",err)
            return(err)

    # https://core.telegram.org/bots/api#sendmessage
    def send_plain_text(self, chat_id, plain_text, markup = '', disable_web_page_preview = ''):
        address = self.url + "sendMessage?chat_id={}&text={}{}{}".format(chat_id, urllib.parse.quote_plus(plain_text), markup, disable_web_page_preview)
        print("Request send_plain_text in chat_id '{}', with text '{}'".format(chat_id, plain_text))
        start_time = time()
        response = self.request_url(address)
        print("Response = {} Time = {}".format(response, time() - start_time))

    # https://core.telegram.org/bots/api#senddocument
    def send_media_message(self, chat_id, document_id):
        address = self.url + "sendDocument?chat_id={}&document={}".format(chat_id, document_id)
        print("Request send_media_message in chat_id '{},' with document_id '{}'".format(chat_id, document_id))
        start_time = time()
        response = self.request_url(address)
        print("Response = {} Time = {}".format(response, time() - start_time))

    # https://core.telegram.org/bots/api#deletemessage
    def delete_message(self, chat_id, message_id):
        address = self.url + "deleteMessage?chat_id={}&message_id={}".format(self.chat_id, message_id)
        print("Request delete_message in chat_id '{},' with message_id '{}'".format(chat_id, message_id))
        start_time = time()
        response = self.request_url_once(address)
        print("Response = {} Time = {}".format(response, time() - start_time))

    # Make a request and return content and status code
    def take_message_return_username(self, user):
        member_username = "###"
        try:
            member_username = user["first_name"] + " " + user["last_name"]
        except:
            member_username = user["first_name"]
        return member_username
    
    def split_params(self, split):
        try:
            echo_name = str(split.split(" ", 1)[0])
            echo_text = str(split.split(" ", 1)[1])
        except: 
            echo_name = None
            echo_text = None
        return echo_name, echo_text

    def filter_Ascii(self, member_username):
        return list(filter(lambda x: x in set(string.printable), member_username))

    def voice_lines(self):
        voice_line_list = [
            "OBJECTION",
            "STOP RIGHT THERE CRIMINAL SCUM",
            "UMMM HELLO?"
        ]
        return choice(voice_line_list)
    
    def cache_ids_on_startup(self):
        chat = self.get_Updates_return_json()
        for message in chat:
            #if message["update_id"] not in self.management: # Only check message if it has not been processed already
            self.management.append(message["update_id"]) # Take message id and store it in a list
        print("Cached {} messages on startup.".format(len(self.management)))

    def delete_real_bot (self, user_id, message_id, member_username):
        self.delete_message(chat_id = self.chat_id, message_id = message_id)

        self.kick_user(chat_id = self.chat_id, user_id = user_id)

        self.send_plain_text(
            chat_id = self.chat_id,
            plain_text = "ree")

    def get_image_from_chat(self, file_id):
        address = self.url + "getFile?file_id={}".format(file_id)
        print(address)
        response = self.request_url_stream(address)
        print(response.content)
        image = json.loads(response.content)['result']
        return image['file_path'], image['file_id']
    
    def hash_compare(self, hash_string, hashes):
        if hash_string in hashes:
            return True, hashes[hash_string]['username']
        else:
            return False, None

    def hash_dump(self, hash_dict, data, hash_file):
        hash_dict[data['hash_string']] = {
            "username":data['username'],
            "user_id":data['user_id'],
            "chat_id":data['chat_id'],
            "chat_name":data['chat_name'],
            "date":data['date'],
            "update_id":data['update_id']
        }
        with open(hash_file, 'w') as storage_file:
            json.dump(hash_dict, storage_file, indent = 2)
    
    def check_if_image_post_is_reposted(self, chat_id, username, user_dict, chat_dict, date, update_id, file_path, file_id):
        address = self.url + "{}".format(file_path)
        address = "https://api.telegram.org/file/bot{token}/{file_path}".format(token = self.bot_token, file_path = file_path)
        print("Request getFile in chat_id '{}', with file_id '{}'".format(chat_id, file_path))
        print(address)
        data = {
            "hash_string":"",
            "username":username,
            "user_id":user_dict['id'],
            "chat_id":chat_dict['id'],
            "chat_name":chat_dict['title'],
            "date":date,
            "update_id":update_id
        }
        image = Image.open(io.BytesIO(self.request_url_stream(address).content))
        repost = False
        ## Average hash
        data['hash_string'] = str(imagehash.average_hash(image))
        exists, username = self.hash_compare(hash_string = data['hash_string'], hashes = self.average_hashes)
        if not exists:
            self.hash_dump(self.average_hashes, data, self.average_hash_file)
        else:
            repost = True
        ## Perceptive hash
        data['hash_string'] = str(imagehash.phash(image))
        exists, username = self.hash_compare(hash_string = data['hash_string'], hashes = self.perceptive_hashes)
        if not exists:
            self.hash_dump(self.perceptive_hashes, data, self.perceptive_hash_file)
        ## Wavelet hash
        data['hash_string'] = str(imagehash.whash(image))
        exists, username = self.hash_compare(hash_string = data['hash_string'], hashes = self.wavelet_hashes)
        if not exists:
            self.hash_dump(self.wavelet_hashes, data, self.wavelet_hash_file)
        ## Difference hash
        data['hash_string'] = str(imagehash.dhash(image))
        exists, username = self.hash_compare(hash_string = data['hash_string'], hashes = self.difference_hashes)
        if not exists:
            self.hash_dump(self.difference_hashes, data, self.difference_hash_file)
        return repost, username
        # else:
        #     self.average_hashes[average_hash] = {
        #         "user":username,
        #         "user_id":from_user['id'],
        #         "chat_id":from_chat['id'],
        #         "chat_name":from_chat['title'],
        #         "date":from_chat['date'],
        #         "update_id":update_id
        #     }
        # self.perceptive_hashes[
        #     with open(self.average_store, 'w') as storage_file:
        #         json.dump(self.average_hashes, storage_file, indent = 2)
        #     return False, user
        #print("Response = {} Time = {}".format(self.response, time() - start_time))

    # Main loop for checking messages
    def chat_management(self):
        # Fetch events from chat
        chat = self.get_Updates_return_json()
        id_list = []
        # Process messages
        for message in chat:
            # Keep track of current IDs
            id_list.append(message["update_id"])
            if message["update_id"] not in self.management:
                # Take message id and store it in a list
                self.management.append(message["update_id"])
                key = list(message)[1]
                message_chat_id = message[key]["chat"]["id"]
                print("New message:", message["update_id"])
                print("Type:", key)
                print(message[key])
                if 'photo' in message[key]:
                    image = message[key]['photo'][len(message[key]['photo']) - 1]
                    file_path, file_id = self.get_image_from_chat(image['file_id'])
                    username = self.take_message_return_username(message[key]['from'])
                    is_repost, original_poster = self.check_if_image_post_is_reposted(message_chat_id, username, message[key]['from'], message[key]['chat'], message[key]['date'], message["update_id"], file_path, file_id)
                    if is_repost:
                        self.send_plain_text(message_chat_id, "{voice_line}! {username}, you have reposted an image already posted by {original_poster}, you brain-addled scum! Repent or be punished!"\
                            .format(voice_line = self.voice_lines(), username = username, original_poster = original_poster))
        # Make sure management list only contains current IDs
        self.management = id_list

    # # Table to store successfully authed users
    # def setup(self):
    #     cur = self.conn.cursor()
    #     stmt = "CREATE TABLE IF NOT EXISTS imagetable (userID integer)"
    #     cur.execute(stmt)
    #     self.conn.commit()

    # # Place successful users for longterm storage
    # def to_table_to_key_insert_variable(self, table, key, variable):
    #     cur = self.conn.cursor()
    #     stmt = "INSERT INTO {}({}) VALUES(?)".format(table, key)
    #     args = (variable,)
    #     cur.execute(stmt, args)
    #     self.conn.commit()
    #     print("Commit to table '{}', key '{}', variable '{}'".format(table, key, variable))

    # # Try to find user inside of the local db
    # def fetch_user_info(self, userID):
    #     cur = self.conn.cursor()
    #     cur.execute("SELECT * FROM users WHERE userID=?", (int(userID), ))
    #     return(cur.fetchone())

def run(runclass):
    runclass.cache_ids_on_startup()
    while True:
        runclass.chat_management()
        sleep(1)

def main():
    run(repost_bot())

if __name__ == '__main__':
    main()