from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import USER_ACCESS


class UserAccess(BoundFilter):

    async def check(self, message: types.Message):
        users_access = USER_ACCESS

        id = message.from_user.id

        for user in users_access:
            if int(user) == int(id):
                return True
        return False
