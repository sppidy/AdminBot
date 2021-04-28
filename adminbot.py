from bot import *
from telethon import events, functions, types
from telethon.utils import pack_bot_file_id
from bot.sql.welcomesql  import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from bot.sql.filtersql import (
    add_filter,
    get_all_filters,
    remove_all_filters,
    remove_filter,
)
from bot.sql.notessql import (
	get_snips,
	add_snip,
	remove_snip,
	get_all_snips,
	remove_all_snip,
)
import bot.sql.antifloodsql as ansql
import os
from telethon import *
from telethon.tl import *
from typing import Optional
import bot.sql.rulessql as sql
import logging
from logging import DEBUG, INFO, basicConfig, getLogger,WARNING
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
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
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
basicConfig(format="%(name)s - %(message)s", level=WARNING)
OWNER_ID = int(os.environ.get("OWNER_ID", None))

#==========================================================================
# For Inlines Of bot

@callback("backer")
async def _(event):	
    botun = (await adminbot.get_me()).username
    botname = (await adminbot.get_me()).first_name
    await event.edit(
	    f"Hi There, I am {botname},\nI Help Admins To Manage Their Chats Easily\n\n - This Bot is Purely Made in Telethon",
	    buttons=[
		    [
			    Button.inline("Help", data="helpstarter"),
		    ],
		    [
			    Button.url("Updates Channel", url="https://t.me/ProBotz"),
			    Button.url("Support Group", url="https://t.me/ProBotzSupport"),
		    ],
		    [
			    Button.url("Add To Group  👥", f"https://t.me/{botun}?startgroup=true"),
		    ],
	    ],
    )

@callback("helpstarter")
async def _(event):
    botun = (await adminbot.get_me()).username
    botname = (await adminbot.get_me()).first_name
    await event.edit(
	    f"Hey there! I am {botname}.\nI help admins manage their groups with Pro Features!\nHave a look at the following for an idea of some of the things I can help you with.\n\nAll commands can either be used with /.\nAnd You May Check The Help for Plugins :"
	    ,buttons=[
		    [
			    Button.inline("Antiflood", data="antifloodhelp"),
			    Button.inline("Bans", data="banhelp"),
			    Button.inline("Blacklists" , data="blacklisthelp"),
		    ],
		    [
			    Button.inline("Promote" , data="promotehelp"),
			    Button.inline("Kick" , data="kickhelp"),
			    Button.inline("Pin/Unpin", data="pinhelp"),
		    ],
		    [
			    Button.inline("Purge" , data="purgehelp"),
			    Button.inline("Filters" , data="filterhelp"),
			    Button.inline("Rules" , data="ruleshelp"),
		    ],
		    [
			    Button.inline("Locks", data="lockhelp"),
			    Button.inline("Notes", data="noteshelp"),
			    Button.inline("Warns", data="warnhelp"),
		    ],
		    [
			    Button.inline("Welcome / Goodbye" , data="welcomehelp"),
		    ],
		    [
			    Button.inline("<-- Back" , data="backer"),
		    ],
	    ],
    )

#======================================================================================================
# For Pms Of Bot
@admin_cmd("start", is_args="simple")
async def _(event):
	if event.is_group:
	    botun = (await adminbot.get_me()).username
	    botname = (await adminbot.get_me()).first_name
	    return await event.reply(f"Hi There, I am {botname}\nTo know More PM Me",buttons=[Button.url("Start Me In PM", url=f"https://t.me/{botun}?start")])
	elif not event.is_group:
		botun = (await adminbot.get_me()).username
		botname = (await adminbot.get_me()).first_name
		return await event.reply(
			f"Hi There, I am {botname},\nI Help Admins To Mange Their Chats Easily\n\n - This Bot is Purely Made in Telethon",
			buttons=[
				[
					Button.inline("Help", data="helpstarter"),
			        ],
			        [
					Button.url("Updates Channel", url="https://t.me/ProBotz"),
					Button.url("Support Group", url="https://t.me/ProBotzSupport"),
				],
				[      
				        Button.url("Add To Group  👥", f"https://t.me/{botun}?startgroup=true"),
			        ],
			],
		)
	
#==========================================================================
# Admin Module
@admin_cmd("ban", is_args=True)
@only_groups
@is_bot_admin
@is_admin
@can_restrict
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
@can_restrict
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
@can_promote
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
@can_promote
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
@can_pin
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
@can_restrict
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
@can_restrict
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
@can_restrict
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
@can_delete
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
@can_delete
@only_groups
@is_bot_admin
@is_admin
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

@admin_cmd("unpin", is_args="unpin")
@only_groups
@is_bot_admin
@is_admin
@can_pin
async def _(event):
    ch = (event.pattern_match.group(1)).strip()
    msg = event.reply_to_msg_id
    if msg and not ch:
        try:
            await adminbot.unpin_message(event.chat_id, msg)
        except BadRequestError:
            return await event.reply("Insufficient Permissions")
        except Exception as e:
            return await event.reply(f"**ERROR:**\n`{str(e)}`")
    elif ch == "all":
        try:
            await adminbot.unpin_message(event.chat_id)
        except BadRequestError:
            return await event.reply("Insufficient Permissions")
        except Exception as e:
            return await event.reply(f"**ERROR:**`{str(e)}`")
    else:
        return await event.reply(f"Either reply to a message, or, use `/unpin all`")
    if not msg and ch != "all":
        return await event.reply(f"Either reply to a message, or, use `/unpin all`")
    await event.reply("`Unpinned!`")

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
###########====================================================================================================
#LockTypes

@admin_cmd("lock", is_args="simple")
@only_groups
@is_bot_admin
@is_admin
@change_info
async def locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = True
        what = "messages"
    elif input_str == "media":
        media = True
        what = "media"
    elif input_str == "sticker":
        sticker = True
        what = "stickers"
    elif input_str == "gif":
        gif = True
        what = "GIFs"
    elif input_str == "game":
        gamee = True
        what = "games"
    elif input_str == "inline":
        ainline = True
        what = "inline bots"
    elif input_str == "poll":
        gpoll = True
        what = "polls"
    elif input_str == "invite":
        adduser = True
        what = "invites"
    elif input_str == "pin":
        cpin = True
        what = "pins"
    elif input_str == "info":
        changeinfo = True
        what = "chat info"
    elif input_str == "all":
        msg = True
        media = True
        sticker = True
        gif = True
        gamee = True
        ainline = True
        gpoll = True
        adduser = True
        cpin = True
        changeinfo = True
        what = "everything"
    else:
        if not input_str:
            await event.reply("Specify to What to Lock !!")
            return
        else:
            await event.reply(f"Invalid lock type: `{input_str}` .\nSee /locktypes for more info")
            return

    lock_rights = types.ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights)
        )
        await event.reply(f"`Locked {what} !`")
    except BaseException as e:
        await event.reply(f"**Error Occured:** {str(e)}")
        return


@admin_cmd("unlock", is_args="simple")
@only_groups
@is_bot_admin
@is_admin
@change_info
async def rem_locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = False
        what = "messages"
    elif input_str == "media":
        media = False
        what = "media"
    elif input_str == "sticker":
        sticker = False
        what = "stickers"
    elif input_str == "gif":
        gif = False
        what = "GIFs"
    elif input_str == "game":
        gamee = False
        what = "games"
    elif input_str == "inline":
        ainline = False
        what = "inline bots"
    elif input_str == "poll":
        gpoll = False
        what = "polls"
    elif input_str == "invite":
        adduser = False
        what = "invites"
    elif input_str == "pin":
        cpin = False
        what = "pins"
    elif input_str == "info":
        changeinfo = False
        what = "chat info"
    elif input_str == "all":
        msg = False
        media = False
        sticker = False
        gif = False
        gamee = False
        ainline = False
        gpoll = False
        adduser = False
        cpin = False
        changeinfo = False
        what = "everything"
    else:
        if not input_str:
            await event.reply("`Specify What to Unlock !!`")
            return
        else:
            await event.reply(f"Invalid lock type: `{input_str}` .\nSee /locktypes for more info")
            return

    unlock_rights = types.ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(
                peer=peer_id, banned_rights=unlock_rights
            )
        )
        await event.reply(f"Unlocked {what} !!")
    except BaseException as e:
        await event.reply(f"**Error Occured:\n** {str(e)}")
        return

@admin_cmd("locktypes", is_args=False)
async def locktypes(event):
    await event.reply(lockktypes)
#==============================================================================================================
#Welcome
@adminbot.on(events.ChatAction())
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await adminbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()

            title = chat.title if chat.title else "this chat"
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
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)

            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=cws.media_file_id,
            )
            update_previous_welcome(event.chat_id, current_message.id)


@admin_cmd("savewelcome",is_args=True)
@only_groups
@is_bot_admin
@is_admin
@change_info
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        bot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, True, 0, bot_api_file_id)
        await event.reply("Welcome note saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0, None)
        await event.reply("Welcome note saved. ")


@admin_cmd("clearwelcome",is_args=True)
@only_groups
@is_bot_admin
@is_admin
@change_info
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.reply(
        "Welcome note cleared. "
        + "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )


@admin_cmd("welcome", is_args="False")
@only_groups
@is_bot_admin
@is_admin
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, "custom_welcome_message"):
        await event.reply(
            "Welcome note found. "
            + "Your welcome message is\n\n`{}`.".format(cws.custom_welcome_message)
        )
    else:
        await event.reply("No Welcome Message found")
#===================================================================================================
#Global
DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


global last_triggered_filters
last_triggered_filters = {}  # pylint:disable=E0602
# ===================================================================================================
#Filters
@adminbot.on(events.NewMessage(incoming=True))
async def on_snip(event):
    global last_triggered_filters
    name = event.raw_text
    if event.chat_id in last_triggered_filters:
        if name in last_triggered_filters[event.chat_id]:
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                else:
                    media = None
                event.message.id
                if event.reply_to_msg_id:
                    event.reply_to_msg_id
                await event.reply(snip.reply, file=media)
                if event.chat_id not in last_triggered_filters:
                    last_triggered_filters[event.chat_id] = []
                last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters[event.chat_id].remove(name)


@admin_cmd("savefilter",is_args=True)
@only_groups
@is_bot_admin
@is_admin
@change_info
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {"type": TYPE_TEXT, "text": msg.message or ""}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip["type"] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip["type"] = TYPE_DOCUMENT
            if media:
                snip["id"] = media.id
                snip["hash"] = media.access_hash
                snip["fr"] = media.file_reference
        add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )
        await event.reply(f"Filter {name} saved successfully. Get it with `{name}`")
    else:
        await event.reply("Reply to a message with `/savefilter <keyword>` to save the filter")


@admin_cmd("filters",is_args=True)
@only_groups
@is_bot_admin
async def on_snip_list(event):
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Available Filters in the Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f" - {a_snip.keyword} \n"
    else:
        OUT_STR = "No Filters in Current Chat"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await adminbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.reply(OUT_STR)


@admin_cmd("stop",is_args=True)
@only_groups
@is_bot_admin
@is_admin
@change_info
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await event.reply(f"Filter `{name}` deleted successfully")


@admin_cmd("clearallfilters",is_args=False)
@only_groups
@is_bot_admin
@is_admin
@chat_creator
async def on_all_snip_delete(event):
    remove_all_filters(event.chat_id)
    await event.reply(f"Filters **in current chat** deleted successfully")
#====================================================================================================
#Notes
@adminbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def on_snip(event):
    name = event.pattern_match.group(1)
    snip = get_snips(event.chat_id, name)
    if snip:
        if snip.snip_type == TYPE_PHOTO:
            media = types.InputPhoto(
                int(snip.media_id),
                int(snip.media_access_hash),
                snip.media_file_reference
            )
        elif snip.snip_type == TYPE_DOCUMENT:
            media = types.InputDocument(
                int(snip.media_id),
                int(snip.media_access_hash),
                snip.media_file_reference
            )
        else:
            media = None
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        await event.client.send_message(
            event.chat_id,
            snip.reply,
            reply_to=message_id,
            file=media
        )

@admin_cmd("savenote",is_args="simple")
@only_groups
@is_bot_admin
@is_admin
@change_info
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip['type'] = TYPE_DOCUMENT
            if media:
                snip['id'] = media.id
                snip['hash'] = media.access_hash
                snip['fr'] = media.file_reference
        add_snip(event.chat_id ,name , snip['text'], snip['type'], snip.get('id'), snip.get('hash'), snip.get('fr'))
        await event.reply("Note {name} saved successfully. Get it with #{name}".format(name=name))
    else:
        await event.reply("Reply to a message with `/savenote ` to save the Note!!")


@admin_cmd("notes", is_args=False)
@only_groups
@is_bot_admin
async def on_snip_list(event):
    all_snips = get_all_snips(event.chat_id)
    OUT_STR = "Notes Available in Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f" - `#{a_snip.snip}` \n"
    else:
        OUT_STR = "No Notes Found in This Chat"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "notes.txt"
            await adminbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Notes in This Chat",
                reply_to=event
            )
            await event.delete()
    else:
        await event.reply(OUT_STR)


@admin_cmd("clear", is_args="notes1")
@only_groups
@is_bot_admin
@is_admin
@change_info
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_snip(event.chat_id,name)
    await event.reply("Note `#{}` deleted successfully".format(name))

@admin_cmd("clearallnotes",is_args=False)
@only_groups
@is_bot_admin
@is_admin
@chat_creator
async def on_all_snip_delete(event):
    remove_all_snip(event.chat_id)
    await event.reply(f"Notes **in current chat** deleted successfully")
#======================================================================================
# No Feds
#======================================================================================
# Rules
@admin_cmd("rules",is_args=False)
@only_groups
@is_bot_admin
async def _(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    sender = event.sender_id
    rules = sql.get_rules(chat_id)
    if rules:
        await event.reply(
            "Click on the below button to get this group's rules 👇",
            buttons=[[Button.inline("Rules", data=f"start-rules-{sender}")]],
        )
    else:
        await event.reply(
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!"
        )


@adminbot.on(events.CallbackQuery(pattern=r"start-rules-(\d+)"))
async def rm_warn(event):
    rules = sql.get_rules(event.chat_id)
    # print(rules)
    user_id = int(event.pattern_match.group(1))
    if not event.sender_id == user_id:
        await event.answer("You haven't send that command !")
        return
    text = f"The rules for **{event.chat.title}** are:\n\n{rules}"
    try:
        await adminbot.send_message(
            user_id, text, parse_mode="markdown", link_preview=False
        )
    except Exception:
        await event.answer(
            "I can't send you the rules as you haven't started me in PM, first start me !",
            alert=True,
        )

@admin_cmd("setrules",is_args="normal")
@only_groups
@is_bot_admin
@change_info
async def _(event):
    chat_id = event.chat_id
    raw_text = event.text
    args = raw_text.split(None, 1)
    if len(args) == 2:
        txt = args[1]
        sql.set_rules(chat_id, txt)
        await event.reply("Successfully set rules for this group.")


@admin_cmd("clearrules",is_args=False)
@change_info
@only_groups
@is_bot_admin
async def _(event):
    chat_id = event.chat_id
    sql.set_rules(chat_id, "")
    await event.reply("Successfully cleared rules for this chat !")
#======================================================================
#Warns

import html
import os
from telethon import *
from telethon.tl import *
import bot.sql.warnsql as wsql
from telethon.tl.types import ChatBannedRights
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *
import bot.sql.rulessql as rulesql


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await adminbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True

@admin_cmd("warn", is_args=True)
@can_restrict
@is_bot_admin
async def _(event):
    BOT_ID = (await adminbot.get_me()).id
    try:
        if event.fwd_from:
            return
        if event.is_private:
            return
        if event.is_group:
                pass
        else:
                return
        quew = event.pattern_match.group(1)

        if event.reply_to_msg_id:
            warn_reason = event.text[len("/warn ") :]
            if not warn_reason:
                await event.reply("Please provide a reason for warning.")
                return
            reply_message = await event.get_reply_message()
            if not await is_register_admin(event.input_chat, reply_message.sender_id):
                pass
            else:
                await event.reply("I am not gonna warn an admin")
                return
            if reply_message.sender_id == BOT_ID:
                await event.reply("Why are you trying to warn me ?")
                return
            limit, soft_warn = wsql.get_warn_setting(event.chat_id)
            num_warns, reasons = wsql.warn_user(
                reply_message.sender_id, event.chat_id, warn_reason
            )
            if num_warns >= limit:
                wsql.reset_warns(reply_message.sender_id, event.chat_id)
                if wsql.get_warn_strength(event.chat_id) == "kick":
                    await adminbot.kick_participant(event.chat_id, reply_message.sender_id)
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been kicked!".format(
                        limit, reply_message.sender_id, reply_message.sender.first_name
                    )
                    await event.reply(reply, parse_mode="html")
                    return
                if wsql.get_warn_strength(event.chat_id) == "ban":
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
                    await adminbot(
                        EditBannedRequest(
                            event.chat_id, reply_message.sender_id, BANNED_RIGHTS
                        )
                    )
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been banned!".format(
                        limit, reply_message.sender_id, reply_message.sender.first_name
                    )
                    await event.reply(reply, parse_mode="html")
                    return
                if wsql.get_warn_strength(event.chat_id) == "mute":
                    MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
                    await adminbot(
                        EditBannedRequest(
                            event.chat_id, reply_message.sender_id, MUTE_RIGHTS
                        )
                    )
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been muted!".format(
                        limit, reply_message.sender_id, reply_message.sender.first_name
                    )
                    await event.reply(reply, parse_mode="html")
                    return
            else:
                reply = "<u><a href='tg://user?id={}'>{}</a></u> has {}/{} warnings... watch out!".format(
                    reply_message.sender_id,
                    reply_message.sender.first_name,
                    num_warns,
                    limit,
                )
                if warn_reason:
                    reply += "\nReason: {}".format(html.escape(warn_reason))
            chat_id = event.chat_id
            rules = rulesql.get_rules(chat_id)
            if rules:
                await event.reply(
                    reply,
                    buttons=[
                        [
                            Button.inline(
                                "Remove Warn ✖️",
                                data=f"rm_warn-{reply_message.sender_id}",
                            ),
			],
		        [
                            Button.inline(
                                "Rules ✝️",
                                data=f"start-ruleswarn-{reply_message.sender_id}",
                            ),
                        ],
                    ],
                    parse_mode="html",
                )
            else:
                await event.reply(
                    reply,
                    buttons=[
                        [
                            Button.inline(
                                "Remove Warn ✖️",
                                data=f"rm_warn-{reply_message.sender_id}",
                            )
                        ]
                    ],
                    parse_mode="html",
                )
        if not event.reply_to_msg_id and quew:
            if "|" in quew:
                iid, reasonn = quew.split("|")
            cid = iid.strip()
            reason = reasonn.strip()
            if cid.isnumeric():
                cid = int(cid)
            entity = await adminbot.get_entity(cid)
            try:
                r_sender_id = entity.id
                r_sender_fname = entity.first_name
            except Exception:
                await event.reply("Couldn't fetch that user.")
                return
            if not reason:
                await event.reply("Please provide a reason for warning.")
                return
            warn_reason = reason
            if not await is_register_admin(event.input_chat, r_sender_id):
                pass
            else:
                await event.reply("I am not gonna warn an admin")
                return
            if r_sender_id == BOT_ID:
                await event.reply("Why are you trying to warn me ?")
                return
            limit, soft_warn = wsql.get_warn_setting(event.chat_id)
            num_warns, reasons = wsql.warn_user(r_sender_id, event.chat_id, warn_reason)
            if num_warns >= limit:
                wsql.reset_warns(r_sender_id, event.chat_id)
                if wsql.get_warn_strength(event.chat_id) == "kick":
                    await adminbot.kick_participant(event.chat_id, r_sender_id)
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been kicked!".format(
                        limit, r_sender_id, r_sender_fname
                    )
                    await event.reply(reply, parse_mode="html")
                    return
                if wsql.get_warn_strength(event.chat_id) == "ban":
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
                    await adminbot(
                        EditBannedRequest(event.chat_id, r_sender_id, BANNED_RIGHTS)
                    )
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been banned!".format(
                        limit, r_sender_id, r_sender_fname
                    )
                    await event.reply(reply, parse_mode="html")
                    return
                if wsql.get_warn_strength(event.chat_id) == "mute":
                    MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
                    await adminbot(
                        EditBannedRequest(event.chat_id, r_sender_id, MUTE_RIGHTS)
                    )
                    reply = "{} warnings, <u><a href='tg://user?id={}'>{}</a></u> has been muted!".format(
                        limit, r_sender_id, r_sender_fname
                    )
                    await event.reply(reply, parse_mode="html")
                    return
            else:
                reply = "<u><a href='tg://user?id={}'>{}</a></u> has {}/{} warnings... watch out!".format(
                    r_sender_id, r_sender_fname, num_warns, limit
                )
                if warn_reason:
                    reply += "\nReason: {}".format(html.escape(warn_reason))
            chat_id = event.chat_id
            rules = rulesql.get_rules(chat_id)
            if rules:
                await event.reply(
                    reply,
                    buttons=[
                        [
                            Button.inline(
                                "Remove Warn ✖️", data=f"rm_warn-{r_sender_id}"
                            ),
			],
			[
                            Button.inline(
                                "Rules ✝️", data=f"start-ruleswarn-{r_sender_id}"
                            ),
                        ],
                    ],
                    parse_mode="html",
                )
            else:
                await event.reply(
                    reply,
                    buttons=[
                        [Button.inline("Remove Warn ✖️", data=f"rm_warn-{r_sender_id}")]
                    ],
                    parse_mode="html",
                )
    except Exception as e:
        print(e)


@adminbot.on(events.CallbackQuery(pattern=r"start-ruleswarn-(\d+)"))
async def rm_warn(event):
    rules = rulesql.get_rules(event.chat_id)
    if not rules:
        rules = "No Rules Set For This Chat Currently"
    user_id = int(event.pattern_match.group(1))
    if not event.sender_id == user_id:
        await event.answer("You haven't been warned !")
        return
    text = f"The rules for **{event.chat.title}** are:\n\n{rules}"
    try:
        await adminbot.send_message(
            user_id, text, parse_mode="markdown", link_preview=False
        )
    except Exception:
        await event.answer(
            "I can't send you the rules as you haven't started me in PM, first start me !",
            alert=True,
        )


@adminbot.on(events.CallbackQuery(pattern=r"rm_warn-(\d+)"))
async def rm_warn(event):
    try:
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                await event.answer("You need to be an admin to do this", alert=False)
                return
            sender = await event.get_sender()
            sid = sender.id
            user_id = int(event.pattern_match.group(1))
            result = wsql.get_warns(user_id, event.chat_id)
            if not result and result[0] != 0:
                await event.answer("This user hasn't got any warnings!", alert=False)
                return
            wsql.remove_warn(user_id, event.chat_id)
            await event.edit(
                f"Warn removed by <u><a href='tg://user?id={sid}'>Admin</a></u> ",
                parse_mode="html",
            )
        else:
            return
    except:
        await event.answer(
            "Sorry the button link has expired, pls use /removelastwarn to manually remove warns",
            alert=True,
        )


@admin_cmd("getwarns",is_args=False)
@is_bot_admin
@can_restrict
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
        pass
    else:
        await event.reply("I am not gonna get warns of an admin")
        return
    result = wsql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = wsql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(
                num_warns, limit
            )
            text += "\r\n"
            text += reasons
            await event.reply(text)
        else:
            await event.reply(
                "This user has {} / {} warning, but no reasons for any of them.".format(
                    num_warns, limit
                )
            )
    else:
        await event.reply("This user hasn't got any warnings!")


@admin_cmd("dellastwarn", is_args=False)
@can_restrict
@is_bot_admin
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
        pass
    else:
        await event.reply("I am not gonna remove warn of an admin")
        return
    result = wsql.get_warns(reply_message.sender_id, event.chat_id)
    if not result and result[0] != 0:
        await event.reply("This user hasn't got any warnings!")
        return
    wsql.remove_warn(reply_message.sender_id, event.chat_id)
    await event.reply("Removed last warn of that user.")


@admin_cmd("resetwarns",is_args=False)
@can_restrict
@is_bot_admin
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    reply_message = await event.get_reply_message()
    if not await is_register_admin(event.input_chat, reply_message.sender_id):
        pass
    else:
        await event.reply("I am not gonna reset warn of an admin")
        return
    wsql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.reply("Warns for this user have been reset!")


@admin_cmd("setwarnmode",is_args="simple")
@can_restrict
@is_bot_admin
@change_info
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        pass
    else:
        return
    input = event.pattern_match.group(1)
    if not input == "kick" and not input == "mute" and not input == "ban":
        await event.reply("I only understand by kick/ban/mute")
        return
    wsql.set_warn_strength(event.chat_id, input)
    await event.reply(f"Too many warns will now result in **{input}**")
#======================================================================
#Antiflood

import html
from typing import Optional, List
import re, time
from telethon.tl.functions.channels import EditBannedRequest
from telethon import *
from telethon.tl.types import *

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

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)


async def is_user_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await adminbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


async def can_change_info(message):
    result = await adminbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await message.reply("Invalid time amount specified.")
            return ""

        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return


@adminbot.on(events.NewMessage(pattern=None))
async def _(event):
    if event.is_private:
        return
    user = event.sender  # type: Optional[User]
    chat = event.chat_id  # type: Optional[Chat]

    # ignore admins and owner
    if await is_user_admin(chat, user.id) or user.id == OWNER_ID:
        ansql.update_flood(chat, None)
        return

    should_ban = ansql.update_flood(chat, user.id)
    if not should_ban:
        return

    try:
        getmode, getvalue = ansql.get_flood_setting(chat)
        if getmode == 1:
            await adminbot(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            execstrings = "Banned"

        elif getmode == 2:
            await adminbot.kick_participant(chat, user.id)
            execstrings = "Kicked"

        elif getmode == 3:
            await adminbot(EditBannedRequest(chat, user.id, MUTE_RIGHTS))
            execstrings = "Muted"

        elif getmode == 4:
            bantime = await extract_time(event, getvalue)
            NEW_RIGHTS = ChatBannedRights(
                until_date=bantime,
                view_messages=True,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True,
            )
            await adminbot(EditBannedRequest(chat, user.id, NEW_RIGHTS))
            execstrings = "Banned for {}".format(getvalue)

        elif getmode == 5:
            mutetime = await extract_time(event, getvalue)
            print(mutetime)
            NEW_RIGHTS = ChatBannedRights(until_date=mutetime, send_messages=True)
            await adminbot(EditBannedRequest(chat, user.id, NEW_RIGHTS))
            execstrings = "Muted for {}".format(getvalue)

        await event.reply("Spammer Detected !\n{}!".format(execstrings))

    except Exception:
        await event.reply(
            "I can't restrict people here, give me permissions first! Until then, I'll disable anti-flood."
        )
        ansql.set_flood(chat, 0)


@admin_cmd("setfloodlimit", is_args="simple")
async def _(event):
    if event.is_private:
        return
    if event.is_group:
        if not await can_change_info(message=event):
            return
    chat_id = event.chat_id
    args = event.pattern_match.group(1)
    if not args:
        await event.reply(
            (
                "Use `/setflood number` to enable anti-flood.\nOr use `/setflood off` to disable antiflood!."
            ),
            parse_mode="markdown",
        )
        return

    if args == "off":
        ansql.set_flood(chat_id, 0)
        await event.reply("Antiflood has been disabled.")

    elif args.isdigit():
        amount = int(args)
        if amount <= 0:
            ansql.set_flood(chat_id, 0)
            await event.reply("Antiflood has been disabled.")

        elif amount < 3:
            await event.reply(
                "Antiflood must be either 0 (disabled) or number greater than 2!",
            )
            return
        else:
            ansql.set_flood(chat_id, amount)
            await event.reply(
                "Successfully updated anti-flood limit to {}!".format(amount)
            )
    else:
        await event.reply("Invalid argument please use a number or 'off'")


@admin_cmd("flood", is_args=False)
async def _(event):
    if event.is_private:
        return
    if event.is_group:
        if not await can_change_info(message=event):
            return
    chat_id = event.chat_id
    limit = ansql.get_flood_limit(chat_id)
    if limit == 0:
        await event.reply("I'm not enforcing any flood control here!")
    else:
        await event.reply(
            "I'm currently restricting members after {} consecutive messages.".format(
                limit
            )
        )


@admin_cmd("setfloodmode", is_args="simple")
async def _(event):
    try:
        if event.is_private:
            return
        if event.is_group:
            if not await can_change_info(message=event):
                return
        chat_id = event.chat_id
        args = event.pattern_match.group(1)
        time = args.split()
        if time[0]:
            if time[0] == "ban":
                settypeflood = "ban"
                ansql.set_flood_strength(chat_id, 1, "0")
            elif time[0] == "kick":
                settypeflood = "kick"
                ansql.set_flood_strength(chat_id, 2, "0")
            elif time[0] == "mute":
                settypeflood = "mute"
                ansql.set_flood_strength(chat_id, 3, "0")
            elif time[0] == "tban":
                try:
                    ttime = time[1]
                except:
                    await event.reply("Please provide the tban time interval.")
                    return
                if len(ttime) == 1:
                    teks = """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tban <timevalue>`.
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                    await event.reply(teks, parse_mode="markdown")
                    return
                if not any(ttime.endswith(unit) for unit in ("m", "h", "d")):
                    await event.reply(
                        "Invalid time type specified. Expected m,h, or d, got: {}".format(
                            ttime
                        )
                    )
                    return
                settypeflood = "tban for {}".format(ttime)
                ansql.set_flood_strength(chat_id, 4, str(ttime))
            elif time[0] == "tmute":
                try:
                    ttime = time[1]
                except:
                    await event.reply("Please provide the tmute time interval.")
                    return
                if len(ttime) == 1:
                    teks = """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tmute <timevalue>`.
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                    await event.reply(teks, parse_mode="markdown")
                    return
                if not any(ttime.endswith(unit) for unit in ("m", "h", "d")):
                    await event.reply(
                        "Invalid time type specified. Expected m,h, or d, got: {}".format(
                            ttime
                        )
                    )
                    return
                settypeflood = "tmute for {}".format(ttime)
                ansql.set_flood_strength(chat_id, 5, str(ttime))
            else:
                await event.reply("I only understand ban/kick/mute/tban/tmute!")
                return

            await event.reply(
                "Exceeding consecutive flood limit will result in {}!".format(
                    settypeflood
                )
            )
        else:
            getmode, getvalue = ansql.get_flood_setting(chat_id)
            if getmode == 1:
                settypeflood = "ban"
            elif getmode == 2:
                settypeflood = "kick"
            elif getmode == 3:
                settypeflood = "mute"
            elif getmode == 4:
                settypeflood = "tban for {}".format(getvalue)
            elif getmode == 5:
                settypeflood = "tmute for {}".format(getvalue)

            await event.reply(
                "Sending more message than flood limit will result in {}.".format(
                    settypeflood
                )
            )
    except Exception as e:
        print(e)
#======================================================================
#Blacklist

import os
import re
from telethon import events
import bot.sql.blacklistsql as bsql
import bot.sql.urlblacklistsql as urlsql
from julia.events import register
from telethon import types
from telethon.tl import functions
import html
import tldextract


async def can_change_info(message):
    result = await adminbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await adminbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@adminbot.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    # TODO: exempt admins from locks
    if event.is_private:
        return
    if await is_register_admin(event.input_chat, event.message.sender_id):
        return

    name = event.text
    snips = bsql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        # print(re.search(pattern, name, flags=re.IGNORECASE))
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception as e:
                print(e)


@admin_cmd("addblacklist", is_args="blacklist")
async def on_add_black_list(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    for trigger in to_blacklist:
        bsql.add_to_blacklist(event.chat_id, trigger.lower())
    await event.reply(
        "Added {} triggers to the blacklist in the current chat".format(
            len(to_blacklist)
        )
    )


@admin_cmd("listblacklist", is_args=False)
async def on_view_blacklist(event):
    all_blacklisted = bsql.get_chat_blacklist(event.chat_id)
    OUT_STR = "**Blacklists in the Current Chat:\n**"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "No BlackLists. Start Adding using /addblacklist"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await adminbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="BlackLists in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.reply(OUT_STR)


@admin_cmd("rmblacklist", is_args="blacklist")
async def on_delete_blacklist(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = 0
    for trigger in to_unblacklist:
        if bsql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await event.reply(
        f"Removed {successful} / {len(to_unblacklist)} from the blacklist"
    )


@admin_cmd("addurl", is_args="normal")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    urls = event.text.split(None, 1)
    if len(urls) > 1:
        urls = urls[1]
        to_blacklist = list({uri.strip() for uri in urls.split("\n") if uri.strip()})
        blacklisted = []

        for uri in to_blacklist:
            extract_url = tldextract.extract(uri)
            if extract_url.domain and extract_url.suffix:
                blacklisted.append(extract_url.domain + "." + extract_url.suffix)
                urlsql.blacklist_url(
                    chat.id, extract_url.domain + "." + extract_url.suffix
                )

        if len(to_blacklist) == 1:
            extract_url = tldextract.extract(to_blacklist[0])
            if extract_url.domain and extract_url.suffix:
                await event.reply(
                    "Added <code>{}</code> domain to the blacklist!".format(
                        html.escape(extract_url.domain + "." + extract_url.suffix)
                    ),
                    parse_mode="html",
                )
            else:
                await event.reply("You are trying to blacklist an invalid url")
        else:
            await event.reply(
                "Added <code>{}</code> domains to the blacklist.".format(
                    len(blacklisted)
                ),
                parse_mode="html",
            )
    else:
        await event.reply("Tell me which urls you would like to add to the blacklist.")


@admin_cmd("delurl", is_args="normal")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    urls = event.text.split(None, 1)

    if len(urls) > 1:
        urls = urls[1]
        to_unblacklist = list({uri.strip() for uri in urls.split("\n") if uri.strip()})
        unblacklisted = 0
        for uri in to_unblacklist:
            extract_url = tldextract.extract(uri)
            success = urlsql.rm_url_from_blacklist(
                chat.id, extract_url.domain + "." + extract_url.suffix
            )
            if success:
                unblacklisted += 1

        if len(to_unblacklist) == 1:
            if unblacklisted:
                await event.reply(
                    "Removed <code>{}</code> from the blacklist!".format(
                        html.escape(to_unblacklist[0])
                    ),
                    parse_mode="html",
                )
            else:
                await event.reply("This isn't a blacklisted domain...!")
        elif unblacklisted == len(to_unblacklist):
            await event.reply(
                "Removed <code>{}</code> domains from the blacklist.".format(
                    unblacklisted
                ),
                parse_mode="html",
            )
        elif not unblacklisted:
            await event.reply("None of these domains exist, so they weren't removed.")
        else:
            await event.reply(
                "Removed <code>{}</code> domains from the blacklist. {} did not exist, so were not removed.".format(
                    unblacklisted, len(to_unblacklist) - unblacklisted
                ),
                parse_mode="html",
            )
    else:
        await event.reply(
            "Tell me which domains you would like to remove from the blacklist."
        )


@adminbot.on(events.NewMessage(incoming=True))
async def on_url_message(event):
    if event.is_private:
        return
    chat = event.chat
    extracted_domains = []
    for (ent, txt) in event.get_entities_text():
        if ent.offset != 0:
            break
        if isinstance(ent, types.MessageEntityUrl):
            url = txt
            extract_url = tldextract.extract(url)
            extracted_domains.append(extract_url.domain + "." + extract_url.suffix)
    for url in urlsql.get_blacklisted_urls(chat.id):
        if url in extracted_domains:
            try:
                await event.delete()
            except:
                return


@admin_cmd("geturl", is_args=False)
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    base_string = "Current <b>blacklisted</b> domains:\n"
    blacklisted = urlsql.get_blacklisted_urls(chat.id)
    if not blacklisted:
        await event.reply("There are no blacklisted domains here!")
        return
    for domain in blacklisted:
        base_string += "- <code>{}</code>\n".format(domain)
    await event.reply(base_string, parse_mode="html")


#======================================================================
print("Admin Bot Started !!")


def startbot():
    adminbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
