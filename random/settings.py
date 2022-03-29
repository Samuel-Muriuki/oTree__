from os import environ

SESSION_CONFIGS = [
    dict(
        name='experiment',
        display_name = "Randomly assign a new partner in each round.",
        app_sequence=['experiment'],
        num_demo_participants=20,
    )
    ]
    


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'app_payoffs',
    'expiry',
    'finished_rounds',
    'language',
    'num_rounds',
    'partner_history',
    'past_group_id',
    'progress',
    'quiz_num_correct',
    'selected_round',
    'task_rounds',
    'time_pressure',
    'wait_page_arrival',
]

SESSION_FIELDS = [
    'completions_by_treatment',
    'past_groups',
    'matrices',
    'wait_for_ids',
    'arrived_ids',
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2900644133881'

INSTALLED_APPS = ['otree']
