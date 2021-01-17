
class User:
    def __init__(self, data: tuple):
        self.id: int = data[0]
        self.user_id: int = data[1]
        self.lang: str = data[2]
        self.money: int = data[3]
        self.wins: int = data[4]
        self.loses: int = data[5]
        self.documents: int = data[6]
        self.active_roles: int = data[7]

    def __repr__(self):
        return f"<UserObject: ID, User_id, lang, money, wins, loses, documents, active_roles\n" \
               f"             {self.id}, {self.user_id}, {self.lang},  {self.money},     {self.wins}," \
               f"    {self.loses},    {self.documents},         {self.active_roles}         >"


class Chat:
    def __init__(self, data: tuple):
        self.id: int = data[0]
        self.chat_id: int = data[1]
        self.chat_title: str = data[2]
        self.chat_username: str = data[3]
        self.chat_lang: str = data[4]
        self.is_active_boosts: bool = bool(data[5])
        self.is_dead_talk: bool = bool(data[6])
        self.is_nonplayers_talk: bool = bool(data[7])
        self.is_nights_talk: bool = bool(data[8])
        self.register_time: int = data[9]
        self.night_time: int = data[10]
        self.day_time: int = data[11]
        self.vote_time: int = data[12]
        self.accept_time: int = data[13]
        self.is_show_dead_roles: bool = bool(data[14])
        self.is_show_day_votes: bool = bool(data[15])
        self.is_pin_register: bool = bool(data[16])
        self.is_show_hello_msg: bool = bool(data[17])
        self.is_allow_attachments_unmute: bool = bool(data[18])

    def __repr__(self):
        return f"<ChatObject: ID, chat_id, chat_title, chat_username\n" \
               f"             {self.id},  {self.chat_id}, {self.chat_title}, {self.chat_username}   >"