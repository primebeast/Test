import telegram
import os
import asyncio

# Define the bot token and chat ID here
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = -1001234567890


async def get_admins():
    bot = telegram.Bot(token=BOT_TOKEN)
    chat_admins = await bot.get_chat_administrators(chat_id=CHAT_ID)
    admins = [admin.user.id for admin in chat_admins]

    return admins


async def main():
    loop = asyncio.get_event_loop()
    admins = await get_admins()
    bot = telegram.Bot(token=BOT_TOKEN)
    while True:
        members_count = await bot.get_chat_member_count(chat_id=CHAT_ID)
        chat_members = [await bot.get_chat_member(chat_id=CHAT_ID, user_id=i) for i in range(members_count)]

        for member in chat_members:
            if member.user.id not in admins:
                messages = member.user.total_count
                if messages == 0:
                    bot.kick_chat_member(chat_id=CHAT_ID, user_id=member.user.id)
                    bot.unban_chat_member(chat_id=CHAT_ID, user_id=member.user.id)
                    print(f"User {member.user.id} has been removed from the group.")
        await asyncio.sleep(86400) # check every 24 hours


if __name__ == "__main__":
    asyncio.run(main())
