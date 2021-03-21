from bot import *
admin_cmd = cmd
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
adminbot = adminbot
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

basicConfig(format="%(name)s - %(message)s", level=WARNING)
#==========================================================================
# For PMs Of bot

@callback("backer")
async def _(event):
	await event.edit(
		"Hi There, I am Adminstrator,\nI Help Admins To Mange Their Chats Easily\n\n - This Bot is Purely Made in Telethon",
		buttons=[
			[
				Button.inline("Help", data="helpstarter"),
			],
			[
	              		Button.url("Updates Channel", url="https://t.me/ProBotz"),
			        Button.url("Support Group", url="https://t.me/ProBotzSupport"),
			],
		],
	)

@callback("helpstarter")
async def _(event):
    await event.edit(
	    "Hey there! I am Administrator.\nI help admins manage their groups with Pro Features!\nHave a look at the following for an idea of some of the things I can help you with.\n\nAll commands can either be used with /.\nAnd You May Check The Help for Plugins :"
	    ,buttons=[
		    [
			    Button.inline("Bans", data="banhelp"),
			    Button.inline("Promote" , data="promotehelp"),
			    Button.inline("Kick" , data="kickhelp"),
		    ],
		    [
			    Button.inline("Pin/Unpin", data="pinhelp"),
			    Button.inline("Purge" , data="purgehelp"),
			    Button.inline("Filters" , data="filterhelp"),
		    ],
		    [
			    Button.inline("Notes", data="noteshelp"),
			    Button.inline("Welcome" , data="welcomehelp"),
		    ],
		    [
			    Button.inline("<-- Back" , data="backer")
		    ],
	    ],
    )

@callback("banhelp")
async def _(event):
    await event.edit(f"{banhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("promotehelp")
async def _(event):
    await event.edit(f"{promotehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("kickhelp")
async def _(event):
    await event.edit(f"{kickhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("pinhelp")
async def _(event):
    await event.edit(f"{pinhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("purgehelp")
async def _(event):
    await event.edit(f"{purgehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("filterhelp")
async def _(event):
    await event.edit(f"{filterrhelp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("noteshelp")
async def _(event):
    await event.edit(f"{notesshelp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("welcomehelp")
async def _(event):
    await event.edit(f"{welcomehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

welcomehelpp = """

Admin commands:
 - /savewelcome <text>: Set a new welcome message. Supports markdown and fillings.
 - /welcome : See Your Current Welcome Message
 - /clearwelcome : Clears Your Current Welcome Message
"""

filterrhelp = """
Here is the help for the Filters module:

 • /filters: List all active filters saved in the chat.

Admin only:
 • /savefilter <keyword> <reply message>: Add a filter to this chat. The bot will now reply that message whenever 'keyword'is mentioned. If you reply to a sticker with a keyword, the bot will reply with that sticker. NOTE: all filter keywords are in lowercase.

 • /stop <filter keyword>: Stop that filter.

Chat creator only:
 • /removeallfilters: Remove all chat filters at once.
"""

promotehelpp = """
**Here is the help for the Promote Module**

• /promote `<reply to user/userid/username>`
    **Promote the user in the chat.**

• /demote `<reply to user/userid/username>`
    **Demote the user in the chat.**
"""

banhelpp = """
**Here is the help for the Bans Module**

• /ban `<reply to user/userid/username> <reason>`
    **Ban the user from the chat.**

• /unban `<reply to user/userid/username> <reason>`
    **Unban the user from the chat.**
"""

kickhelpp = """
**Here is the help for the Kick Module**

• /kick `<reply to user/userid/username> <reason>`
    **Kick the user from the chat.**
"""

pinhelpp = """
**Here is the help for the Pin/Unpin Module**

• /pin `<reply to message>`
    **Pin the message in the chat**
    **For Loud pin use (`/pin loud`).**

• /unpin `<reply to message>`
    **Unpin the message in the chat**
    **For Unpinning All Messages Use (`/unpin all`).**

"""
purgehelpp = """
**Here is the help for the Purge Module**

• /purge `<reply to message>`
    **Purge all messages from the replied message.**

• /del `<reply to message>`
    **Deletes The Replied Message.**
"""
notesshelp = """
Here is the help for the Notes module:

 • `#<notename>`: To Get The Note
 • /notes : list all saved notes in this chat
 
Admins only:
 • /save <notename> <reply message> :  save the replied message as a note with name notename
 • /clear <notename>: clear note with this name
 
 Chat Creator Only:
 • /removeallnotes: removes all notes from the group
 
 Note: Note names are case-insensitive, and they are automatically converted to lowercase before getting saved.
 """
lockktypes = """
Available message types to lock/unlock are: 
- all 
- msg 
- media
- sticker
- gif
- game
- inline
- poll
- invite
- pin
- info
"""
#==========================================================================

@admin_cmd("start", is_args="simple")
async def _(event):
	if event.is_group:
	    botun = (await adminbot.get_me()).username
	    return await event.reply("Hi There, I am Adminstrator\nTo know More PM Me",buttons=[Button.url("Start Me In PM", url=f"https://t.me/{botun}?start")])
	elif not event.is_group:
		return await event.reply(
			"Hi There, I am Adminstrator,\nI Help Admins To Mange Their Chats Easily\n\n - This Bot is Purely Made in Telethon",
			buttons=[
				[
					Button.inline("Help", data="helpstarter"),
			        ],
			        [
					Button.url("Updates Channel", url="https://t.me/ProBotz"),
					Button.url("Support Group", url="https://t.me/ProBotzSupport"),
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
print("Admin Bot Started !!")


def startbot():
    adminbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
