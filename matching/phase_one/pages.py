from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ReceiveAdvice(Page):
    def vars_for_template(self):
        return {
            'advice': self.player.participant.vars['advice'],
            'verbal': self.player.participant.vars['verbal'],
        }


class GiveAdvice(Page):
    form_model = 'player'
    form_fields = ['advice', 'verbal']


page_sequence = [ReceiveAdvice, GiveAdvice]
