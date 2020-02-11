from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms

import os
import random
import json
import logging

import boto3

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'phase_one'
    players_per_group = 2
    num_rounds = 1
    multiplier = 5


class Subsession(BaseSubsession):
    def creating_session(self):
        logger = logging.getLogger(__name__)

        # Reads Json from Amazon S3
        BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME') 
        FILE_TO_READ = 'generation.json'
        client = boto3.client('s3', 
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        result = client.get_object(Bucket=BUCKET, Key=FILE_TO_READ)
        text = result["Body"].read().decode()
        all_advice = json.loads(text)
        print(all_advice)

        if self.round_number == 1:
            for index, player in enumerate(self.get_players()):
                player.participant.vars['all_advice'] = all_advice

        # number_of_players = 2
        # for i in range(number_of_players):
        #     all_advice.append({
        #         'third': self.session.config['third_party'],
        #         'advice': self.session.config['advice_{}'.format(i)],
        #         'verbal': self.session.config['verbal_{}'.format(i)]
        #     })

        # Process the advice (i.e. randomly shuffle, etc.)
        # random.shuffle(all_advice)

        # Assigning the advice to each player

class Group(BaseGroup):
    def set_advice(self):
        all_advice = {}
        for player_id in range(1, Constants.players_per_group + 1):
            player_key = 'player_{}'.format(player_id)
            all_advice[str(player_id)] = {
                "1": {
                    "advice": self.session.vars[player_key]["advice_1"],
                    "verbal": self.session.vars[player_key]["verbal_1"]
                },
                "2": {
                    "advice": self.session.vars[player_key]["advice_2"],
                    "verbal": self.session.vars[player_key]["verbal_2"]
                }
            }

        # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        # file_name = 'generation_{}.json'.format(int(self.session.config['generation_number']) + 1)
        # generation_file = os.path.join(os.path.dirname(BASE_DIR), "matching", "advice", file_name)

        # Writing Json to Amazon S3
        BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME') 
        FILE_TO_READ = 'generation.json'
        client = boto3.client('s3', 
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        response = client.put_object(Bucket=BUCKET, Body=json.dumps(all_advice), Key=FILE_TO_READ)

        # # Writing Json to file
        # try:
        #     with open(generation_file, 'w') as file:
        #         file.write(json.dumps(all_advice))
        # except IOError as e:
        #     print("Error writing json file: {}".format(e))




class Player(BasePlayer):
    advice_1 = models.StringField()
    verbal_1 = models.StringField()
    advice_2 = models.StringField()
    verbal_2 = models.StringField()
    q1 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", ""), ("2", ""), ("3", ""))))
    b = models.BooleanField(initial=False)
    type_number = models.CharField(max_length=1)
