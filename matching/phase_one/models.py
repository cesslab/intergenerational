from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'phase_one'
    players_per_group = None
    num_rounds = 1
    multiplier = 5


class Subsession(BaseSubsession):
    def creating_session(self):
        # Reading in the advice
        all_advice = []
        number_of_players = 2
        for i in range(number_of_players):
            all_advice.append({
                'advice': self.session.config['advice_{}'.format(i)],
                'verbal': self.session.config['verbal_{}'.format(i)]
            })

        # Process the advice (i.e. randomly shuffle, etc.)
        random.shuffle(all_advice)

        # Assigning the advice to each player
        if self.round_number == 1:
            for index, player in enumerate(self.get_players()):
                print(self.session.config["advice_{}".format(index)])
                player.participant.vars['advice'] = all_advice[index]['advice']
                player.participant.vars['verbal'] = all_advice[index]['verbal']




class Group(BaseGroup):
    pass



class Player(BasePlayer):
    advice = models.StringField()
    verbal = models.StringField()
