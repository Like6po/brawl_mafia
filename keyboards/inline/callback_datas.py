from aiogram.utils.callback_data import CallbackData

start_callback = CallbackData('start', 'type')

help_callback = CallbackData('help', 'type')

#######################
profile_callback = CallbackData('profile', 'type')

shop_callback = CallbackData('shop', 'type')
########################

night_cop_callback = CallbackData('night_cop',
                                  'action',
                                  'chat_id')

night_vote_callback = CallbackData('night_vote',
                                   'player_id',
                                   'chat_id')

night_vote_cop_callback = CallbackData('night_vote',
                                       'action',
                                       'player_id',
                                       'chat_id')

night_vote_mafia_callback = CallbackData('night_vote_mafia',
                                         'player_id',
                                         'chat_id')

day_vote_callback = CallbackData('day_vote',
                                 'player_id',
                                 'chat_id')

voting_callback = CallbackData('voting',
                               'action',
                               'player_id',
                               'chat_id')

####################################

settings_callback = CallbackData('stg',
                                 'action',
                                 'chat_id')

settings_mute_dead_callback = CallbackData('stg_md',
                                           'action',
                                           'chat_id')
settings_mute_no_players_callback = CallbackData('stg_mnp',
                                                 'action',
                                                 'chat_id')

settings_reg_time_callback = CallbackData('reg_time',
                                          'action',
                                          'chat_id')

settings_night_time_callback = CallbackData('night_time',
                                            'action',
                                            'chat_id')

settings_day_time_callback = CallbackData('day_time',
                                          'action',
                                          'chat_id')

settings_voting_time_callback = CallbackData('voting_time',
                                             'action',
                                             'chat_id')

settings_accept_time_callback = CallbackData('accept_time',
                                             'action',
                                             'chat_id')

settings_pin_callback = CallbackData('stg_pin',
                                     'action',
                                     'chat_id')

settings_boosts_callback = CallbackData('stg_boosts',
                                        'action',
                                        'chat_id')

settings_show_roles_callback = CallbackData('stg_show_roles',
                                            'action',
                                            'chat_id')

settings_show_votes_callback = CallbackData('stg_show_votes',
                                            'action',
                                            'chat_id')
