#!/usr/bin/env python

# Import dependencies
import copy
import re
import time
import pandas as pd
import requests
import json
import collections

class Game:

  # Initialize a Game object from the html "logs" of a BGA game
  def __init__(self, tableID, email, password):
    self.tableID = str(tableID)
    self.get(tableID, email, password)

  def get(self, tableID, email, password):

    tableID = str(tableID)

    # Define parameters to access to Board Game Arena
    url_login = "http://en.boardgamearena.com/account/account/login.html"
    prm_login = {'email': email, 'password': password, 'rememberme': 'on',
           'redirect': 'join', 'form_id': 'loginform'}
    url_tableinfo = "https://boardgamearena.com/table/table/tableinfos.html?id=" + tableID

    with requests.session() as c:

      # Login to Board Game Arena
      r = c.post(url_login, params = prm_login)
      if r.status_code != 200:
        print("Error trying to login!")

      # Generate the table file
      r = c.get(url_tableinfo)
      if r.status_code != 200:
        print("Error trying to load the table page!")
      table_info = r.text

    self.table_info = json.loads(table_info)


def main():
  # game = Game(89746387, 'email@gmail.com', 'password')
  # # print(json.dumps(game.table_info, indent=2))
  # table_info = game.table_info
  # print(table_info['data']['result']['game_name'])
  # print(len(table_info['data']['game_player_number']))
  # print(table_info['data']['result']['stats']['table']['winning_clan']['valuelabel'])
  # # clansofcaledonia

  counter = collections.Counter()
  for i in range (89746380, 89746390):
    print('Game ' + str(i))
    game = Game(i, 'email@gmail.com', 'password')
    # print(json.dumps(game.table_info, indent=2))
    table_info = game.table_info
    if 'data' not in table_info:
      continue
    if 'result' not in table_info['data']:
      continue
    if table_info['data']['result']['game_name'] != 'clansofcaledonia':
      continue
    if len(table_info['data']['game_player_number']) != 4:
      continue
    counter[table_info['data']['result']['stats']['table']['winning_clan']['valuelabel']] += 1
    print(counter)

  print(counter)

if __name__ == "__main__":
  main()
