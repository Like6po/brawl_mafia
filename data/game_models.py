import random
from typing import Optional, List, Union

from aiogram.utils.markdown import hlink


class Effect:

    def __init__(self, type_effect: str, ttl: int):
        self.type: str = type_effect
        self.ttl: int = ttl

    def __repr__(self):
        return f"( {self.type}: {self.ttl} )"

    def __eq__(self, other):
        if other is None:
            return False
        if self.type == other.type:
            return True
        else:
            return False


class Heal_self(Effect):
    def __init__(self):
        super().__init__('heal_self', 100)


class Mute(Effect):
    def __init__(self):
        super().__init__('mute', 2)


class Kill(Effect):
    def __init__(self, killer: str = 'killer_name'):
        super().__init__('kill', 100)
        self.killer = killer

    def __repr__(self):
        return f"( {self.type}: {self.ttl}, dead_from: {self.killer} )"


class Dead(Effect):
    def __init__(self):
        super().__init__('dead', 100)


class Dead_day(Effect):
    def __init__(self):
        super().__init__('dead_day', 100)


class Player:

    def __init__(self, user_id: int, user_name: str, active_role: int = 0):
        self.id = user_id
        self.name = user_name
        self.active_role = active_role

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.active_role} )"


class Peace(Player):

    def __init__(self, player: Player):
        super().__init__(player.id, player.name)
        self.role = 'peace'
        self.effects: List[Union[Kill, Dead_day, Mute, Heal_self, Dead]] = []
        self.day_voting_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, {self.effects})"


class Comissar(Peace):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'cop'
        self.fails: int = 0
        self.check_to: Optional[int] = None
        self.kill_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Чек: {self.check_to}, Kill: {self.kill_to}," \
               f" effects: {self.effects} )"


class Mafia(Peace):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'mafia'
        self.go_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Go_to {self.go_to} , {self.effects})"


class Don(Mafia):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'don'
        self.go_to: Optional[int] = None
        self.check_to: Optional[int] = None
        self.fails: int = 0

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Чек {self.check_to}," \
               f" {self.effects}, Go_to {self.go_to} )"


class Homeless(Peace):

    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'homeless'
        self.fails: int = 0
        self.go_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Go_to {self.go_to} , " \
               f"{self.effects})"


class Suicide(Peace):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'suicide'


class Whore(Peace):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'whore'
        self.fails: int = 0
        self.go_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Go_to {self.go_to}, {self.effects} )"


class Doctor(Peace):
    def __init__(self, player: Peace):
        super().__init__(player)
        self.role: str = 'doctor'
        self.fails: int = 0
        self.go_to: Optional[int] = None

    def __repr__(self):
        return f"( ID {self.id}, {self.name}, {self.role}, Go_to {self.go_to} , {self.effects} )"


class Conv:

    def __init__(self, chat_id: int, is_pin_register: bool, is_active_boosts: bool, is_dead_talk: bool,
                 register_message_id: int, is_nonplayers_talk: bool, register_time: int, night_time: int,
                 day_time: int, vote_time: int, accept_time: int, is_show_dead_roles: bool, is_show_day_votes: bool,
                 is_allow_attachments_unmute: bool):

        self.id: int = chat_id
        self.registered: List[Player] = []
        self.players: List[Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless]] = []
        self.dead_players: List[Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless]] = []
        self.don: Optional[Don] = None
        self.cop: Optional[Comissar] = None
        self.doctor: Optional[Doctor] = None
        self.suicide: Optional[Suicide] = None
        self.whore: Optional[Whore] = None
        self.homeless: Optional[Homeless] = None
        self.mafia: List[Union[Mafia, Don]] = []

        self.register_is_end_ahead_of_time: bool = False
        self.extend_time_register: bool = False
        self.is_new_player_join: bool = False

        self.register_message_id: int = register_message_id
        self.is_pin_register: bool = is_pin_register
        self.is_active_boosts: bool = is_active_boosts

        self.is_dead_talk: bool = is_dead_talk
        self.is_nonplayers_talk: bool = is_nonplayers_talk

        self.is_show_dead_roles: bool = is_show_dead_roles
        self.is_show_day_votes: bool = is_show_day_votes

        self.register_time: int = register_time
        self.night_time: int = night_time
        self.day_time: int = day_time
        self.vote_time: int = vote_time
        self.accept_time: int = accept_time

        self.phase: str = 'starting'
        self.day: int = 0

        self.day_votes_ids: List[int] = []
        self.accept_votes_like: List[Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless]] = []
        self.accept_votes_dislike: List[Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless]] = []
        self.mafia_votes_ids: List[int] = []

        self.is_new_vote: bool = False
        self.is_accept_end: bool = False
        self.is_allow_attachments_unmute: bool = is_allow_attachments_unmute

    def __repr__(self):
        text = f"[ ID {self.id}                ]\n" \
               f"[ День {self.day}              ]\n" \
               f"[ Фаза {self.phase}       ]\n"
        text += f"[ Игроки:             ]\n"
        for player in self.players:
            text += f"  [+++ {player}  ]\n"
        text += f"[ Мертвые             ]\n"
        for dead_player in self.dead_players:
            text += f"  [--- {dead_player}  ]\n"

        text += f"[ Регистрация          ]\n"
        for reg_player in self.registered:
            text += f"  [+++ {reg_player}  ]\n"
        return text

    def clear_day_votes(self):
        self.day_votes_ids = []
        self.accept_votes_like = []
        self.accept_votes_dislike = []
        for player in self.players:
            player.day_voting_to = None

    def clear_effects(self):
        for player_obj in self.players:
            for effect in player_obj.effects:
                if effect.ttl > 0:
                    effect.ttl -= 1
                else:
                    player_obj.effects.remove(effect)

    def kill(self, player: Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless],
             reason=Dead()):
        try:
            self.players.remove(player)
            player.effects = [reason]
            self.dead_players.append(player)
            if player.role == 'don':
                self.don = None
            elif player.role == 'cop':
                self.cop = None
            elif player.role == 'doctor':
                self.doctor = None
            elif player.role == 'suicide':
                self.suicide = None
            elif player.role == 'whore':
                self.whore = None
            elif player.role == 'homeless':
                self.homeless = None
            elif player.role == 'mafia':
                self.mafia.remove(player)
        except ValueError:
            pass

    def move_dead_to_dead(self):
        for player in self.players:
            for effect in player.effects:
                if effect == Kill():
                    self.kill(player)
                    break

    def doctor_results_night(self) -> Optional[List[Union[str, int]]]:
        if self.doctor:
            if self.doctor.go_to:
                player_healed = self.get_player(self.doctor.go_to)
                if self.doctor.go_to == self.doctor.id:
                    self.doctor.effects.append(Heal_self())
                for effect in player_healed.effects:
                    if effect == Mute():
                        player_healed.effects.remove(effect)
                    elif effect == Kill():
                        player_healed.effects.remove(effect)
                        result = ['doctor_heal', self.doctor.go_to]
                        self.doctor.go_to = None
                        return result
                result = ['doctor_not_heal', self.doctor.go_to]
                self.doctor.go_to = None
                return result
            else:
                self.doctor.fails += 1
                if self.doctor.fails > 3:
                    self.doctor.effects.append(Kill('afk'))
                return None
        return None

    def cop_results_night(self) -> Optional[List[Union[str, int]]]:
        if self.cop:
            if self.cop.check_to:
                result = ['cop_check', self.cop.check_to]
                self.cop.check_to = None
                self.cop.kill_to = None
                return result

            elif self.cop.kill_to:
                self.get_player(self.cop.kill_to).effects.append(Kill('cop'))
                result = ['cop_kill', self.cop.kill_to]
                self.cop.check_to = None
                self.cop.kill_to = None
                return result

            else:
                self.cop.fails += 1
                if self.cop.fails > 3:
                    self.cop.effects.append(Kill('afk'))
                return None
        return None

    def don_results_night(self) -> Optional[List[Union[str, int]]]:
        if self.don:
            if self.don.check_to:
                result = ['don_check', self.don.check_to]
                self.don.check_to = None
                return result
            else:
                if self.cop:
                    self.don.fails += 1
                    if self.don.fails > 3:
                        self.don.effects.append(Kill('afk'))
                return None
        return None

    def whore_results_night(self) -> Optional[List[Union[str, int]]]:
        if self.whore:
            if self.whore.go_to:
                self.get_player(self.whore.go_to).effects.append(Mute())
                result = ['whore_go_to', self.whore.go_to]
                self.whore.go_to = None
                return result

            else:
                self.whore.fails += 1
                if self.whore.fails > 3:
                    self.whore.effects.append(Kill('afk'))
                return None
        return None

    def homeless_results_night(self) -> Optional[List[Union[str, int]]]:
        if self.homeless:
            if self.homeless.go_to:
                result = ['homeless_go_to', self.homeless.go_to]
                self.homeless.go_to = None
                return result
            else:
                self.homeless.fails += 1
                if self.homeless.fails > 3:
                    self.homeless.effects.append(Kill('afk'))
                return None
        return None

    def mafia_results_night(self) -> Optional[List[Union[str, int]]]:
        for mafia in self.mafia:
            mafia.go_to = None
        if self.don:
            self.don.go_to = None
        maximum_votes: int = 0
        temp_id: int = 0
        for player_id in set(self.mafia_votes_ids):
            count_votes_to_id: int = self.mafia_votes_ids.count(player_id)
            if count_votes_to_id > maximum_votes:
                temp_id = int(player_id)
                maximum_votes = count_votes_to_id
        self.mafia_votes_ids = []
        if temp_id:
            player = self.get_player(temp_id)
            if player:
                player.effects.append(Kill('mafia'))
                return ['mafia_kill', temp_id]
            return None
        return None

    def register_player(self, player):
        self.registered.append(player)

    def get_alive_players_count(self) -> int:
        count: int = 0
        for player in self.players:
            if Kill() not in player.effects:
                count += 1
        return count

    def get_player(self, user_id) -> Union[Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless, None]:
        for player in self.players:
            if player.id == user_id:
                return player
        else:
            return None

    def get_registered_player(self, user_id) -> Optional[Player]:
        for player in self.registered:
            if player.id == user_id:
                return player
        else:
            return None

    def get_text_alive_roles(self) -> str:
        text_roles: list = []
        peace: int = 0
        mafia: int = 0
        temp: list = list(self.players)
        random.shuffle(temp)
        for player in temp:
            if Kill() not in player.effects:
                if player.role == 'peace':
                    peace += 1
                elif player.role == 'mafia':
                    mafia += 1
                elif player.role == 'doctor':
                    text_roles.append('🚑👩🏼‍⚕️ Пэм')
                elif player.role == 'cop':
                    text_roles.append('🔫🕵️ Кольт')
                elif player.role == 'whore':
                    text_roles.append('☂️💃 Пайпер')
                elif player.role == 'don':
                    text_roles.append('🐃 Булл')
                elif player.role == 'suicide':
                    text_roles.append('💣 Тик')
                elif player.role == 'homeless':
                    text_roles.append('🍾 Барли')

        if peace:
            if peace == 1:
                text_roles.insert(0, '🙎‍♀️ Шелли')
            else:
                text_roles.insert(0, f"🙎‍♀️ Шелли: {peace}")
        if mafia:
            if mafia == 1:
                text_roles.append('🦅 Ворон')
            else:
                text_roles.append(f"🦅 Ворон: {mafia}")

        return f"{', '.join(text_roles)}"

    def get_text_registered_players(self) -> str:
        text_players: str = ''
        i: int = 1
        for player in self.registered:
            text_players += f"\n{i}. {hlink(player.name, f'tg://user?id={player.id}')}"
            i += 1
        return text_players

    def get_text_alive_players(self) -> str:
        text_players: str = ''
        i: int = 1
        for player in self.players:
            if Kill() not in player.effects:
                text_players += f"\n{i}. {hlink(player.name, f'tg://user?id={player.id}')}"
                i += 1
        return text_players

    def register_players(self) -> List[int]:
        count_players: int = len(self.registered)
        players_with_active_role: List[Player] = []
        players_without_active_role: List[Player] = []
        for player in self.registered:
            if player.active_role:
                players_with_active_role.append(player)
            else:
                players_without_active_role.append(player)
        roles_list: List[str] = []
        mafia_count: int = count_players // 4
        roles_list.append('don')
        mafia_count -= 1
        for x in range(mafia_count):
            roles_list.append('mafia')
        roles_list.append('doctor')
        if count_players > 4:
            roles_list.append('whore')
        if count_players > 5:
            roles_list.append('cop')
        if count_players > 8:  # 6
            roles_list.append('homeless')
        if count_players > 10:  # 7
            roles_list.append('suicide')
        random.shuffle(roles_list)
        players_who_need_back_active_role_to_database: List[int] = []
        for player in players_with_active_role:
            if len(roles_list) > 0:
                role = roles_list.pop()
                if role == 'cop':
                    self.cop = Comissar(Peace(player))
                    self.players.append(self.cop)
                elif role == 'doctor':
                    self.doctor = Doctor(Peace(player))
                    self.players.append(self.doctor)
                elif role == 'whore':
                    self.whore = Whore(Peace(player))
                    self.players.append(self.whore)
                elif role == 'don':
                    self.don = Don(Peace(player))
                    self.players.append(self.don)
                elif role == 'mafia':
                    mafia = Mafia(Peace(player))
                    self.mafia.append(mafia)
                    self.players.append(mafia)
                elif role == 'homeless':
                    self.homeless = Homeless(Peace(player))
                    self.players.append(self.homeless)
                elif role == 'suicide':
                    self.suicide = Suicide(Peace(player))
                    self.players.append(self.suicide)
            else:
                self.players.append(Peace(player))
                players_who_need_back_active_role_to_database.append(player.id)
            self.registered.remove(player)

        for player in players_without_active_role:
            if len(roles_list) > 0:
                role = roles_list.pop()
                if role == 'cop':
                    self.cop = Comissar(Peace(player))
                    self.players.append(self.cop)
                elif role == 'doctor':
                    self.doctor = Doctor(Peace(player))
                    self.players.append(self.doctor)
                elif role == 'whore':
                    self.whore = Whore(Peace(player))
                    self.players.append(self.whore)
                elif role == 'don':
                    self.don = Don(Peace(player))
                    self.players.append(self.don)
                elif role == 'mafia':
                    mafia = Mafia(Peace(player))
                    self.mafia.append(mafia)
                    self.players.append(mafia)
                elif role == 'homeless':
                    self.homeless = Homeless(Peace(player))
                    self.players.append(self.homeless)
                elif role == 'suicide':
                    self.suicide = Suicide(Peace(player))
                    self.players.append(self.suicide)
            else:
                self.players.append((Peace(player)))
            self.registered.remove(player)

        return players_who_need_back_active_role_to_database


class Games:
    def __init__(self):
        self.active_chats: List[Conv] = []

    def add_chat(self, chat: Conv):
        self.active_chats.append(chat)

    def get_chat(self, find_id) -> Optional[Conv]:
        for chat in self.active_chats:
            if chat.id == find_id:
                return chat
        else:
            return None

    def remove_chat(self, chat: Conv):
        try:
            self.active_chats.remove(chat)
        except:
            pass

    def search_player(self, user_id: int) -> Optional[List[Union[Conv, Peace, Comissar, Mafia, Don, Doctor, Whore, Suicide, Homeless]]]:
        for chat in self.active_chats:
            for player in chat.players:
                if player.id == user_id:
                    return [chat, player]
        else:
            return None


