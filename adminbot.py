"""
**✘ Help ✘**

• `/promote <reply to user/userid/username>`
    **Promote the user in the chat.**

• `/demote <reply to user/userid/username>`
    **Demote the user in the chat.**

• `/ban <reply to user/userid/username> <reason>`
    **Ban the user from the chat.**

• `/unban <reply to user/userid/username> <reason>`
    **Unban the user from the chat.**

• `/kick <reply to user/userid/username> <reason>`
    **Kick the user from the chat.**

• `/pin <reply to message>`
    **Pin the message in the chat**
    **For Loud pin use (`/pin loud`).**
    
• `/purge <reply to message>`
    **Purge all messages from the replied message.**

"""


import os
import telethon
import requests
from config import Config
import functools
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChatAdminRights,ChatBannedRights,MessageEntityMentionName
from telethon import TelegramClient, events, functions, Button

#==================================================

bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
adminbot = bot.start(bot_token=Config.BOT_TOKEN)

#==================================================
def callback(sed):
    def callbacks(func):
        data = sed
        adminbot.add_event_handler(
            func, events.callbackquery.CallbackQuery(data=data)
        )

    return callbacks

def admin_cmd(add_cmd, is_args=False):
    def cmd(func):
        if is_args :
        	pattern = "^/" + add_cmd + "(?: |$)(.*)"
        elif is_args== "simple" :
            pattern = "^/" + add_cmd + " ?(.*)"
        elif is_args=="normal":
            pattern = "^/" + add_cmd
        else:
            pattern = "^/" + add_cmd + "$"
        adminbot.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )
    return cmd

def ainline():
    def inline(func):
        gtransbot.add_event_handler(func, events.InlineQuery)
    return inline

def is_admin():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            sed = await adminbot.get_permissions(event.chat_id, event.sender_id)
            user = event.sender_id
            if sed.is_admin:
                await func(event)
            if not user:
                pass
            if not sed.is_admin:
                await event.reply("Only Admins Can Use it.")
        return wrapper
    return decorator


def is_bot_admin():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            pep = await adminbot.get_me()
            sed = await adminbot.get_permissions(event.chat_id, pep)
            if sed.is_admin:
                await func(event)
            else:
                await event.reply("I Must Be Admin To Do This.")
        return wrapper
    return decorator


def only_groups():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                await func(event)
            else:
                await event.reply("This Command Only Works On Groups.")
        return wrapper
    return decorator

def only_pm():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                pass
            else:
                await func(event)

        return wrapper

    return decorator
#==================================================

is_admin = is_admin()
is_bot_admin = is_bot_admin()
only_groups = only_groups()
only_pm = only_pm()

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = (
    "`I don't have sufficient permissions! This is so sed. Alexa play Tera Baap Aaya`"
)
NO_SQL = "`Almost Done! Wait...`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
adminbot = adminbot
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
#==========================================================================
# For PMs Of bot

@callback("backer")
async def _(event):
	await event.edit("Hi There, I am a Simple Bot With All Admin Commands",buttons=[Button.inline("Hᴇʟᴘ", data="helpstarter")])

@callback("helpstarter")
async def _(event):
    await event.edit(f"{__doc__}",buttons=[Button.inline(" <-- Bᴀᴄᴋ", data="backer")])

#==========================================================================

@admin_cmd("start", is_args="simple")
async def _(event):
	if event.is_group:
	    botun = (await adminbot.get_me()).username
	    return await event.reply("Hi There, I am a Simple Bot With All Admin Commands To know More PM Me",buttons=[Button.url("Start Me In PM", url=f"https://t.me/{botun}?start")])
	elif not event.is_group:
		return await event.reply("Hi There, I am a Simple Bot With All Admin Commands",buttons=[Button.inline("Hᴇʟᴘ", data="helpstarter")])

#==========================================================================
@admin_cmd("ban", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def ban(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    user, reason = await get_user_from_event(event)
    kekme = await adminbot.get_permissions(event.chat_id, user)
    momos = user
    momoz = momos.first_name
    if kekme.is_admin:
        await event.reply("Oh, Yeah? Lets Start Banning Admins.")
        return
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await event.reply("I Could't Ban That User Probably Due To Less Permissions.")
        return
    if reason:
        await event.reply(f"Banned {momoz} For \nReason: {reason}")
    else:
        await event.reply(f"Banned {momoz} !")


@admin_cmd("unban", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def nothanos(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await event.reply("`Unbanned Successfully. Granting another chance.🚶`")
    except BadRequestError:
        await event.reply("I Could't UnBan That User Probably Due To Less Permissions.")
        return


@admin_cmd("promote", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def promote(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=False,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    kekme = await adminbot.get_permissions(event.chat_id, user)
    if kekme.is_admin:
        await event.reply("Oh, Yeah? Promote A Admin?")
        return
    if not rank:
        rank = "Admin"
    if user:
        pass
    else:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await event.reply("Promoted Successfully! Now give Party")
    except BadRequestError:
        await event.reply(
            "I Could't Promote That User Probably Due To Less Permissions."
        )
        return


@admin_cmd("demote", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def demote(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    rank = "Admin"
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await event.reply(
            "I Could't Demote That User Probably Due To Less Permissions."
        )
        return
    await event.reply("Demoted This User Sucessfully.")


@admin_cmd("pin", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def pin(event):
    await event.get_chat()
    to_pin = event.reply_to_msg_id
    if not to_pin:
        await event.reply("`Reply to a message to pin it.`")
        return
    options = event.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await event.client(UpdatePinnedMessageRequest(event.to_id, to_pin, is_silent))
    except BadRequestError:
        await event.reply(
            "I Could't Pin That Message Probably Due To Less Permissions."
        )
        return
    await event.reply("Pinned This Message Sucessfully.")
    await get_user_sender_id(event.sender_id, event)


@admin_cmd("kick", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def kick(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    user, reason = await get_user_from_event(event)
    kekme = await adminbot.get_permissions(event.chat_id, user)
    momos = user
    momos.first_name
    if kekme.is_admin:
        await event.reply("Oh, Yeah? Lets Start kicking Admins.")
        retur
    if not user:
        await event.reply("Mention A User")
        return
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except:
        await event.reply("I Could't Kick That User Probably Due To Less Permissions.")
        return
    if reason:
        await event.reply(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await event.reply(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")


@admin_cmd("mute", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def mute(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    user, reason = await get_user_from_event(event)
    kekme = await adminbot.get_permissions(event.chat_id, user)
    momos = user
    momos.first_name
    if kekme.is_admin:
        await event.reply("Oh, Mutting? Lets Start Banning Admins.")
        retur
    if not user:
        await event.reply("Mention A User")
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
    except:
        await event.reply("I Could't Mute That User Probably Due To Less Permissions.")
        return
    if reason:
        await event.reply(
            f"`Muted` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await event.reply(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")


@admin_cmd("unmute", is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def mute(event):
    chat = await event.get_chat()
    chat.admin_rights
    chat.creator
    user, reason = await get_user_from_event(event)
    if not user:
        await event.reply("Mention A User")
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNMUTE_RIGHTS))
    except:
        await event.reply(
            "I Could't UnMute That User Probably Due To Less Permissions."
        )
        return
    if reason:
        await event.reply(
            f"`UnMuted` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await event.reply(f"`Unmute` [{user.first_name}](tg://user?id={user.id})`!`")

@admin_cmd("purge")
@only_groups
@is_bot_admin
@is_admin
async def purge(event):
    chat = event.chat_id
    msgs = []

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await adminbot.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await adminbot.delete_messages(chat, msgs)
                msgs = []

        await adminbot.delete_messages(chat, msgs)
        del_res = await adminbot.send_message(
            event.chat_id, f"Fast Purged {count} messages."
        )
        await del_res.delete()
        await asyncio.sleep(4)
        
    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@admin_cmd("del", is_args=False)
async def delete_msg(event):

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await adminbot.delete_messages(chat, rm)

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj

@adminbot.on(events.ChatAction())
@only_groups
async def _(event):
    if event.user_joined:
        a_user = await event.get_user()
        a_chat = await event.get_chat()
        title = a_chat.title if a_chat.title else "this chat"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
        first = a_user.first_name
        last = a_user.last_name
        if last:
            fullname = f"{first} {last}"
        else:
            fullname = first
        userid = a_user.id
        mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
        await event.reply("Hi {mention},\nWelcome to {title}\nYou are {count}\nStay On-Topic\nHave Common Sense\n Have Safe Journey in Telegram With Ultroid",button=Button.url("Join Our Channel",url="https://t.me/TheUltroid"))

print("Admin Bot Started !!")


def startbot():
    adminbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()