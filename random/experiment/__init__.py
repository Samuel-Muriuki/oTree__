from otree.api import *


doc = """
********************************************************
Pythoneer: sammkimberly@gmail.com
********************************************************
group by arrival time, but in each round assign to a new partner.
"""


class C(BaseConstants):
    NAME_IN_URL = 'experiment'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 19
    TREATMENTS = [True, False]
    INSTRUCTIONS_TEMPLATE = 'experiment/instructions.html'
    INSTRUCTION_TEMPLATE = 'experiment/instruction.html'
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.2
    BONUS_PAYOFF = cu(50)

class Subsession(BaseSubsession):
    num_groups_created = models.IntegerField(initial=0)


class Group(BaseGroup):
    sent_message = models.StringField(
        label = "A has sent you the following message: "
    )
    write_message = models.StringField(
        label = "Write down the message you picked."
    )
    write_words = models.StringField(
        label = "You will receive 70% of the revenue and I will receive 30% of the revenue."
    )
    choose_message = models.IntegerField(
        choices=[[1, 'Yes'],[2, 'No']],
        widget=widgets.RadioSelect,
    )
    guess_investment = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="Enter an amount from 0 to 100:",
    )
    guess_investment_b = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="Enter an amount from 0 to 100:",
    )
    investment_amount = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="Enter an investment amount from 0 to 100:",
    )
    investment_amount_b = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="Enter an investment amount from 0 to 100:",
    )
    confident_b = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    confident_a = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    )

class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'A'
        if self.id_in_group == 2:
            return 'B'

    message_list = models.IntegerField(
        choices = [[1, 'Hi'], [2, 'No']],
        label="I choose:",
    )
    

    choose_message = models.IntegerField(
        choices=[[1, 'Yes'],[2, 'No']],
        widget=widgets.RadioSelect,
        label="Will you choose the message you selected?",
    
    )
    
    
    most_popular_message = models.IntegerField(
        choices=[[1, 'Hi'],[2, 'No']],
        widget=widgets.RadioSelect,
        label="The most popular message is:",
    )

    is_popular = models.BooleanField()


# Functions
def creating_session(subsession: Subsession):
    session = subsession.session
    session.past_groups = []


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    session = subsession.session

    import itertools

    # this generates all possible pairs of waiting players and checks if the group would be valid.
    for possible_group in itertools.combinations(waiting_players, 2):
        # use a set, so that we can easily compare even if order is different e.g. {1, 2} == {2, 1}
        pair_ids = set(p.id_in_subsession for p in possible_group)
        # if this pair of players has not already been played
        if pair_ids not in session.past_groups:
            # mark this group as used, so we don't repeat it in the next round.
            session.past_groups.append(pair_ids)
            # in this function, 'return' means we are creating a new group with this selected pair
            return possible_group


def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.BONUS_PAYOFF
    p2.payoff = C.BONUS_PAYOFF


# Pages
class RandomAssignPage(WaitPage):
    after_all_players_arrive = set_payoffs
    group_by_arrival_time = True
    body_text = "Waiting to pair you with someone you haven't already played with"

class ResultsWaitPage(WaitPage):
    pass

class Introduction(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(partner=player.get_others_in_group()[0])

class ListMessage(Page):
    form_model = 'player'
    form_fields = ['message_list']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(partner=player.get_others_in_group()[0])

class PopularMessage(Page):
    form_model = 'player'
    form_fields = ['most_popular_message']

class Choice(Page):
    form_model = 'group'
    form_fields = ['write_message']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())

class ChooseMessage(Page):
    form_model = 'group'
    form_fields = ['write_words']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1
    
class PickedMessage(Page):
    form_model = 'player'
    form_fields = ['choose_message']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class SecondChoice(Page):


    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

class SentMessage(Page):
    form_model = 'group'
    form_fields = ['choose_message']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

class GuessA(Page):
    form_model = 'group'
    form_fields = ['guess_investment']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class GuessB(Page):
    form_model = 'group'
    form_fields = ['guess_investment_b']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class InvestmentA(Page):
    form_model = 'group'
    form_fields = ['investment_amount']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class InvestmentB(Page):
    form_model = 'group'
    form_fields = ['investment_amount_b']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2
    
class ChoiceAConfidence(Page):
    form_model = 'group'
    form_fields =['confident_a']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class ChoiceBConfidence(Page):
    form_model = 'group'
    form_fields = ['confident_b']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2
class ResultsPage(Page):
    pass
page_sequence = [
    RandomAssignPage,
    ResultsWaitPage, 
    Introduction, 
    ListMessage, 
    ResultsWaitPage,
    PopularMessage,
    ResultsWaitPage,
    Choice,
    ResultsWaitPage,
    PickedMessage,
    ResultsWaitPage,
    ChooseMessage,
    ResultsWaitPage,
    SecondChoice,
    ResultsWaitPage,
    SentMessage,
    ResultsWaitPage,
    GuessA,
    ResultsWaitPage,
    GuessB,
    ResultsWaitPage,
    ChoiceAConfidence,
    ResultsWaitPage,
    ChoiceBConfidence,
    ResultsWaitPage,
    InvestmentA,
    ResultsWaitPage,
    InvestmentB,
    ResultsWaitPage,
    ResultsPage,
    ResultsWaitPage
    ]
