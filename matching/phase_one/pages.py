from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class ValueAdvice(Page):
    form_model = 'player'
    form_fields = ['type_number']


class ReceiveAdvice(Page):
    def vars_for_template(self):
        all_advice = self.player.participant.vars['all_advice']
        print(all_advice)

        return {
            'advice': all_advice[self.player.type_number][str(self.player.id_in_group)]['advice'],
            'verbal': all_advice[self.player.type_number][str(self.player.id_in_group)]['verbal'],
        }


class GiveAdvice(Page):
    form_model = 'player'
    form_fields = ['advice_1', 'verbal_1', 'advice_2', 'verbal_2', 'q1']

    def before_next_page(self):
        key = 'player_{}'.format(self.player.id_in_group)
        self.session.vars[key] = {
            'advice_1': self.player.advice_1,
            'verbal_1': self.player.verbal_1,
            'advice_2': self.player.advice_2,
            'verbal_2': self.player.verbal_2,
        }


class End(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_advice()

page_sequence = [ValueAdvice, ReceiveAdvice, GiveAdvice, End]
