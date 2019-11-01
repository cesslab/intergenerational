from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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
        if self.round_number == 1:
            for index, player in enumerate(self.get_players()):
                print(self.session.config["advice_{}".format(index)])
                player.participant.vars['advice'] = self.session.config['advice_{}'.format(index)]
                player.participant.vars['verbal'] = self.session.config['verbal_{}'.format(index)]




class Group(BaseGroup):
    pass



class Player(BasePlayer):
    advice = models.StringField()
    verbal = models.StringField()
