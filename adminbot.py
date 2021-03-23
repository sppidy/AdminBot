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
import bot.sql.fedssql as sql
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
	await event.edit(
		"Hi There, I am Adminstrator,\nI Help Admins To Manage Their Chats Easily\n\n - This Bot is Purely Made in Telethon",
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
			    Button.inline("Federations", data="fedhelp"),
			    Button.inline("Locks", data="lockhelp"),
			    Button.inline("Notes", data="noteshelp"),
		    ],
		    [
			    Button.inline("Welcome" , data="welcomehelp"),
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
#=====================================================================================
#Fedrations


# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo and AyraHikari too
# Federation by MrYacha 2018-2019
# Federation rework by Mizukito Akito 2019
# Federation update v2 by Ayra Hikari 2019
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 22+ hours by @peaktogoo
# Time spended on updating version to v2 = 26+ hours by @AyraHikari
# Total spended for making this features is 68+ hours
# LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")
# (Me @sppidy has spent a lot of time Analysing this Module and porting to @grpadminrobot) @MissJulia_Robot has also done a lot of hard work to rewrite this in telethon so add this line as a credit. Please don't remove this if you somewhat respect me.

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


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await adminbot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("Pass the user's username, id or reply!")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await adminbot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await adminbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj

def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@admin_cmd("newfed", is_args="simple")
async def _(event):
    chat = event.chat_id
    user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, user.id):
            pass
        else:
            return
    message = event.pattern_match.group(1)
    if not event.is_private:
        await event.reply("Federations can only be created by privately messaging me.")
        return
    fednam = message
    if not fednam:
        await event.reply("Please write the name of the federation!")
        return
    if fednam:
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        # LOGGER.info(fed_id)

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            await event.reply(
                "Can't create federation!\nPlease contact @MissJuliaRobotSupport if the problem persists."
            )
            return

        await event.reply(
            "**You have successfully created a new federation!**"
            "\nName: `{}`"
            "\nID: `{}`"
            "\n\nUse the command below to join the federation:"
            "\n`/joinfed {}`".format(fed_name, fed_id, fed_id),
            parse_mode="markdown",
        )
    else:
        await event.reply("Please write down the name of the federation")


@admin_cmd("delfed", is_args="simple")
async def _(event):
    try:
        args = event.pattern_match.group(1)
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, user.id):
                pass
            else:
                return
        message = event.message.id
        if not event.is_private:
            await event.reply(
                "Federations can only be deleted by privately messaging me."
            )
            return
        if args:
            is_fed_id = args
            getinfo = sql.get_fed_info(is_fed_id)
            if getinfo is False:
                await event.reply("This federation does not exist.")
                return
            if int(getinfo["owner"]) == int(user.id) or int(user.id) == OWNER_ID:
                fed_id = is_fed_id
            else:
                await event.reply("Only federation owners can do this!")
                return
        else:
            await event.reply("What should I delete?")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only federation owners can do this!")
            return
        await adminbot.send_message(
            event.chat_id,
            "Are You sure you want to delete your federation ?\nThis cannot be reverted, you will lose your entire ban list, and '**{}**' will be permanently lost !".format(
                getinfo["fname"]
            ),
            buttons=[
                [Button.inline("⚠️ Delete Federation", data="rmfed_{}".format(fed_id))],
                [Button.inline("Cancel", data="rmfed_cancel")],
            ],
            reply_to=message,
        )
    except Exception as e:
        print(e)
        pass


@callback(r"rmfed(\_(.*))")
async def delete_fed(event):
    # print("1")
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split("_", 1)[1]
    print(fed_id)
    if not event.is_private:
        return
    if fed_id == "cancel":
        await event.edit("Federation deletion cancelled")
        return
    getfed = sql.get_fed_info(fed_id)
    if getfed:
        delete = sql.del_fed(fed_id)
        if delete:
            await event.edit(
                "You have removed your Federation! Now all the Groups that are connected with '**{}**' do not have a Federation.".format(
                    getfed["fname"]
                ),
                parse_mode="markdown",
            )


@admin_cmd("renamefed", is_args="simple2")
async def _(event):
    args = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if not args:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")
    if not fedid:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")
    fed_id, newname = args, fedid
    verify_fed = sql.get_fed_info(fed_id)
    if not verify_fed:
        return await event.reply("This fed not exist in my database!")
    if is_user_fed_owner(fed_id, user.id):
        sql.rename_fed(fed_id, user.id, newname)
        await event.reply(f"Successfully renamed your fed name to {newname}!")
    else:
        await event.reply("Only federation owner can do this!")


@admin_cmd("chatfed",is_args=False)
async def _(event):
    chat = event.chat_id
    # user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    fed_id = sql.get_fed_id(chat)
    if not fed_id:
        await event.reply("This group is not in any federation!")
        return
    info = sql.get_fed_info(fed_id)
    text = "This group is part of the following federation:"
    text += "\n{} (ID: <code>{}</code>)".format(info["fname"], fed_id)
    await event.reply(text, parse_mode="html")


@admin_cmd("joinfed",is_args="simple")
async def _(event):
    chat = event.chat_id
    user = event.sender
    args = event.pattern_match.group(1)
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return
    if not args:
        await event.reply("Where is the federation ID ?")
        return

    fed_id = sql.get_fed_id(chat)

    if user.id == OWNER_ID:
        pass
    else:
        try:
            async for userr in adminbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(event.sender_id) == int(aid):
                        await event.reply("Only group creators can use this command!")
                        return
        except Exception as e:
            print(e)
    if fed_id:
        await event.reply("You cannot join two federations from one chat")
        return

    if args:
        getfed = sql.search_fed_by_id(args)
        if getfed is False:
            await event.reply("Please enter a valid federation ID")
            return

        x = sql.chat_join_fed(args, event.chat.title, chat)
        if not x:
            await event.reply(
                "Failed to join federation! Please contact @MissJuliaRobotSupport should this problem persist!"
            )
            return

        get_fedlog = sql.get_fed_log(args)
        if get_fedlog:
            try:
                await adminbot.send_message(
                    int(get_fedlog),
                    "Chat **{}** has joined the federation **{}**".format(
                        event.chat.title, getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
            except Exception as e:
                print(e)
                pass
        await event.reply(
            "This group has joined the federation: **{}**".format(getfed["fname"])
        )


@admin_cmd("leavefed",is_args=False)
async def _(event):
    chat = event.chat_id
    user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)
    fed_info = sql.get_fed_info(fed_id)

    if user.id == OWNER_ID:
        pass
    else:
        try:
            async for userr in adminbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(event.sender_id) != int(aid):
                        await event.reply("Only group creators can use this command!")
                        return
        except Exception as e:
            print(e)
    if sql.chat_leave_fed(chat) is True:
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            try:
                await adminbot.send_message(
                    int(get_fedlog),
                    "Chat **{}** has left the federation **{}**".format(
                        event.chat.title, fed_info["fname"]
                    ),
                    parse_mode="markdown",
                )
            except Exception as e:
                print(e)
                pass
        await event.reply(
            "This group has left the federation **{}**".format(fed_info["fname"])
        )
    else:
        await event.reply("How can you leave a federation that you never joined ?")


@admin_cmd("fpromote",is_args=True)
async def _(event):
    chat = event.chat_id
    args = await get_user_from_event(event)
    user = event.sender
    if args:
        pass
    else:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)

    if is_user_fed_owner(fed_id, user.id):
        userid = args
        if not userid:
            await event.reply("Reply to a message or give a entity to promote")
            return
        user_id = userid.id
        getuser = sql.search_user_in_fed(fed_id, user_id)
        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)
        get_owner = eval(info["fusers"])["owner"]
        try:
            async for userr in adminbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(aid) == int(get_owner):
                        await event.reply("Hey that's the federation owner !")
                        return
        except Exception as e:
            print(e)
        if getuser:
            await event.reply(
                "I cannot promote users who are already federation admins! Can remove them if you want!"
            )
            return
        if int(user_id) == int(BOT_ID):
            await event.reply("I already am a federation admin in all federations!")
            return
        res = sql.user_join_fed(fed_id, user_id)
        if res:
            await event.reply("Successfully Promoted!")
        else:
            await event.reply("Failed to promote!")
    else:
        await event.reply("Only federation owners can do this!")


@admin_cmd("fdemote",is_args=True)
async def _(event):
    chat = event.chat_id
    args = await get_user_from_event(event)
    user = event.sender
    if args:
        pass
    else:
        return

    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return

    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)

    if is_user_fed_owner(fed_id, user.id):
        userid = args
        if not userid:
            await event.reply("Reply to a message or give a entity to promote")
            return
        user_id = userid.id

        if user_id == BOT_ID:
            await event.reply("You can't demote me from a federation created by me !")
            return

        if sql.search_user_in_fed(fed_id, user_id) is False:
            await event.reply("I cannot demote people who are not federation admins!")
            return

        res = sql.user_demote_fed(fed_id, user_id)
        if res is True:
            await event.reply("Demoted from Fed Admin!")
        else:
            await event.reply("Demotion failed!")
    else:
        await event.reply("Only federation owners can do this!")
        return


def is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
    if int(user_id) in fed_admins or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@admin_cmd("fedinfo", is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if args:
            fed_id = args
            info = sql.get_fed_info(fed_id)
        else:
            fed_id = sql.get_fed_id(chat)
            if not fed_id:
                await event.reply("This chat is not in any federation!")
                return
            info = sql.get_fed_info(fed_id)

        if not info:
            await event.reply("Couldn't find information about that federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only a federation admin can do this!")
            return

        owner = await adminbot.get_entity(int(info["owner"]))
        try:
            owner_name = owner.first_name + " " + owner.last_name
        except:
            owner_name = owner.first_name
        FEDADMIN = sql.all_fed_users(fed_id)
        TotalAdminFed = len(FEDADMIN)

        text = "<b>ℹ️ Federation Information:</b>"
        text += "\nFedID: <code>{}</code>".format(fed_id)
        text += "\nName: {}".format(info["fname"])
        text += f"\nCreator: <p><a href='tg://user?id={owner.id}'>{owner_name}</a></p>"
        text += "\nAll Admins: <code>{}</code>".format(TotalAdminFed)
        getfban = sql.get_all_fban_users(fed_id)
        text += "\nTotal banned users: <code>{}</code>".format(len(getfban))
        getfchat = sql.all_fed_chats(fed_id)
        text += "\nNumber of groups in this federation: <code>{}</code>".format(
            len(getfchat)
        )
        await event.reply(text, parse_mode="html")
    except Exception as e:
        print(e)
        pass


@admin_cmd("fedadmins",is_args=True)
async def _(event):
    try:
        chat = event.chat_id
        args = False
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if args:
            fed_id = args
            info = sql.get_fed_info(fed_id)
        else:
            fed_id = sql.get_fed_id(chat)
            if not fed_id:
                await event.reply("This chat is not in any federation!")
                return
            info = sql.get_fed_info(fed_id)

        if not info:
            await event.reply("Couldn't find information about that federation!")
            return

        # print(fed_id+"\n"+user.id)
        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        text = "<b>Federation Admin {}:</b>\n\n".format(info["fname"])
        text += "👑 Owner:\n"
        owner = await adminbot.get_entity(int(info["owner"]))
        try:
            owner_name = owner.first_name + " " + owner.last_name
        except:
            owner_name = owner.first_name
        text += f" • <p><a href='tg://user?id={owner.id}'>{owner_name}</a></p>\n"

        members = sql.all_fed_members(fed_id)
        if len(members) == 0:
            text += "\n🔱 There are no admins in this federation"
        else:
            text += "\n🔱 Admin:\n"
            for x in members:
                user = await adminbot.get_entity(int(x))
                unamee = user.first_name
                text += f" • <p><a href='tg://user?id={user.id}'>{unamee}</a></p>\n"

        await event.reply(text, parse_mode="html")
    except Exception as e:
        print(e)
        pass


@admin_cmd("fban",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        info = sql.get_fed_info(fed_id)
        getfednotif = sql.user_feds_report(info["owner"])

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        if "|" in args:
            iid, reasonn = args.split("|")
        cid = iid.strip()
        reason = reasonn.strip()
        if cid.isnumeric():
            cid = int(cid)
        entity = await adminbot.get_input_entity(cid)
        try:
            user_id = entity.user_id
        except Exception:
            await event.reply("Couldn't fetch that user.")
            return
        if not reason:
            await event.reply("Need a reason for fban.")
            return
        fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user_id)

        if not user_id:
            await event.reply("You don't seem to be referring to a user")
            return

        if user_id == BOT_ID:
            await event.reply("Haha you can't fban me.")
            return

        if is_user_fed_owner(fed_id, user_id) is True:
            await event.reply("You are the fed owner.\nI will not fban you !")
            return

        if is_user_fed_admin(fed_id, user_id) is True:
            await event.reply("That's a federation admin, I can't fban.")
            return

        if user_id == OWNER_ID:
            await event.reply("Haha i will never fban my owner !")
            return

        if user_id in [777000, 1087968824]:
            await event.reply("Fool! You can't attack Telegram's native tech!")
            return

        try:
            user_chat = await adminbot.get_entity(user_id)
            isvalid = True
            fban_user_id = user_chat.id
            fban_user_name = user_chat.first_name
            fban_user_lname = user_chat.last_name
            fban_user_uname = user_chat.username
        except Exception as e:
            if not str(user_id).isdigit():
                await event.reply(e)
                return
            elif len(str(user_id)) != 9:
                await event.reply("That's not a user!")
                return
            isvalid = False
            fban_user_id = int(user_id)
            fban_user_name = "user({})".format(user_id)
            fban_user_lname = None
            fban_user_uname = None

        if isvalid and not isinstance(user_chat, User):
            await event.reply("That's not a user!")
            return

        if isvalid:
            user_target = (
                f"<p><a href='tg://user?id={fban_user_id}'>{fban_user_name}</a></p>"
            )
        else:
            user_target = fban_user_name

        if fban:
            fed_name = info["fname"]
            temp = sql.un_fban_user(fed_id, fban_user_id)
            if not temp:
                await event.reply("Failed to update the reason for fedban!")
                return
            x = sql.fban_user(
                fed_id,
                fban_user_id,
                fban_user_name,
                fban_user_lname,
                fban_user_uname,
                reason,
                int(time.time()),
            )
            if not x:
                await event.reply(
                    "Failed to ban from the federation! If this problem continues, contact @MissJuliaRobotSupport."
                )
                return

            fed_chats = sql.all_fed_chats(fed_id)
            # Will send to current chat
            await adminbot.send_message(
                chat,
                "<b>New Federation Ban</b>"
                "\n<b>Federation:</b> {}"
                "\n<b>Federation Admin:</b> {}"
                "\n<b>User:</b> {}"
                "\n<b>User ID:</b> <code>{}</code>"
                "\n<b>Reason:</b> {}".format(
                    fed_name,
                    f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                    user_target,
                    fban_user_id,
                    reason,
                ),
                parse_mode="html",
            )
            # Send message to owner if fednotif is enabled
            if getfednotif:
                try:
                    await adminbot.send_message(
                        int(info["owner"]),
                        "<b>FedBan reason updated</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>"
                        "\n<b>Reason:</b> {}".format(
                            fed_name,
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                            reason,
                        ),
                        parse_mode="html",
                    )
                except Exception as e:
                    print(e)
                    pass
            # If fedlog is set, then send message, except fedlog is current chat
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if int(get_fedlog) != int(chat):
                    try:
                        await adminbot.send_message(
                            int(get_fedlog),
                            "<b>FedBan reason updated</b>"
                            "\n<b>Federation:</b> {}"
                            "\n<b>Federation Admin:</b> {}"
                            "\n<b>User:</b> {}"
                            "\n<b>User ID:</b> <code>{}</code>"
                            "\n<b>Reason:</b> {}".format(
                                fed_name,
                                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                                user_target,
                                fban_user_id,
                                reason,
                            ),
                            parse_mode="html",
                        )
                    except Exception as e:
                        print(e)
                        pass
            for fedschat in fed_chats:
                try:
                    await adminbot.kick_participant(fedschat, fban_user_id)
                except Exception as e:
                    sql.chat_leave_fed(fedschat)
                    print(e)
                    pass

            # Fban for fed subscriber
            subscriber = list(sql.get_subscriber(fed_id))
            if len(subscriber) != 0:
                for fedsid in subscriber:
                    all_fedschat = sql.all_fed_chats(fedsid)
                    for fedschat in all_fedschat:
                        try:
                            await adminbot.kick_participant(fedschat, fban_user_id)
                        except Exception as e:
                            print(e)
                            continue
            return

        fed_name = info["fname"]

        x = sql.fban_user(
            fed_id,
            fban_user_id,
            fban_user_name,
            fban_user_lname,
            fban_user_uname,
            reason,
            int(time.time()),
        )
        if not x:
            await event.reply(
                "Failed to ban from the federation! If this problem continues, contact @OnePunchSupport."
            )
            return

        fed_chats = sql.all_fed_chats(fed_id)
        # Will send to current chat
        await adminbot.send_message(
            chat,
            "<b>FedBan reason updated</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>Federation Admin:</b> {}"
            "\n<b>User:</b> {}"
            "\n<b>User ID:</b> <code>{}</code>"
            "\n<b>Reason:</b> {}".format(
                fed_name,
                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                user_target,
                fban_user_id,
                reason,
            ),
            parse_mode="html",
        )
        # Send message to owner if fednotif is enabled
        if getfednotif:
            try:
                await adminbot.send_message(
                    int(info["owner"]),
                    "<b>FedBan reason updated</b>"
                    "\n<b>Federation:</b> {}"
                    "\n<b>Federation Admin:</b> {}"
                    "\n<b>User:</b> {}"
                    "\n<b>User ID:</b> <code>{}</code>"
                    "\n<b>Reason:</b> {}".format(
                        fed_name,
                        f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                        user_target,
                        fban_user_id,
                        reason,
                    ),
                    parse_mode="html",
                )
            except Exception as e:
                print(e)
                pass
        # If fedlog is set, then send message, except fedlog is current chat
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if int(get_fedlog) != int(chat):
                try:
                    await adminbot.send_message(
                        int(get_fedlog),
                        "<b>FedBan reason updated</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>"
                        "\n<b>Reason:</b> {}".format(
                            fed_name,
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                            reason,
                        ),
                        parse_mode="html",
                    )
                except Exception as e:
                    print(e)
                    pass
        chats_in_fed = 0
        for fedschat in fed_chats:
            chats_in_fed += 1
            try:
                await adminbot.kick_participant(fedschat, fban_user_id)
            except Exception as e:
                print(e)
                pass

            # Fban for fed subscriber
            subscriber = list(sql.get_subscriber(fed_id))
            if len(subscriber) != 0:
                for fedsid in subscriber:
                    all_fedschat = sql.all_fed_chats(fedsid)
                    for fedschat in all_fedschat:
                        try:
                            await adminbot.kick_participant(fedschat, fban_user_id)
                        except Exception as e:
                            print(e)
                            pass
    except Exception as e:
        print(e)
        pass


@admin_cmd("fedrules",is_args=False)
async def _(event):
    chat = event.chat_id
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)
    if not fed_id:
        await event.reply("This group is not in any federation!")
        return

    rules = sql.get_frules(fed_id)
    text = "**Rules for this fed:**\n\n"
    text += rules
    await event.reply(text)


@admin_cmd("setfrules",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only fed admins can do this!")
            return

        if args:
            x = sql.set_frules(fed_id, args)
            if not x:
                await event.reply(
                    "There was an error while setting federation rules!\nPlease go to @MissJuliaRobotSupport to report this."
                )
                return

            rules = sql.get_fed_info(fed_id)["frules"]
            getfed = sql.get_fed_info(fed_id)
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if eval(get_fedlog):
                    try:
                        await adminbot.send_message(
                            int(get_fedlog),
                            "**{}** has updated federation rules for fed **{}**".format(
                                user.first_name, getfed["fname"]
                            ),
                            parse_mode="markdown",
                        )
                    except Exception as e:
                        print(e)
                        pass
            await event.reply(f"Rules have been changed to :\n\n{rules}")
        else:
            await event.reply("Please give some rules to set.")
    except Exception as e:
        print(e)
        pass


@admin_cmd("unfban",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        info = sql.get_fed_info(fed_id)
        getfednotif = sql.user_feds_report(info["owner"])

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        if args.isnumeric():
            cid = int(args)
        else:
            cid = args
        entity = await adminbot.get_input_entity(cid)

        try:
            user_id = entity.user_id
        except Exception:
            await event.reply("Couldn't fetch that user.")
            return

        if not user_id:
            await event.reply("You do not seem to be referring to a user.")
            return

        try:
            user_chat = await adminbot.get_entity(user_id)
            isvalid = True
            fban_user_id = user_chat.id
            fban_user_name = user_chat.first_name
            fban_user_lname = user_chat.last_name
            fban_user_uname = user_chat.username
        except Exception as e:
            if not str(user_id).isdigit():
                await event.reply(e)
                return
            elif len(str(user_id)) != 9:
                await event.reply("That's not a user!")
                return
            isvalid = False
            fban_user_id = int(user_id)
            fban_user_name = "user({})".format(user_id)
            fban_user_lname = None
            fban_user_uname = None

        if isvalid and not isinstance(user_chat, User):
            await event.reply("That's not a user!")
            return

        if isvalid:
            user_target = (
                f"<p><a href='tg://user?id={fban_user_id}'>{fban_user_name}</a></p>"
            )
        else:
            user_target = fban_user_name

        fban, fbanreason, fbantime = sql.get_fban_user(fed_id, fban_user_id)
        if fban is False:
            await event.reply("This user is not fbanned!")
            return

        chat_list = sql.all_fed_chats(fed_id)
        # Will send to current chat
        await adminbot.send_message(
            chat,
            "<b>Un-FedBan</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>Federation Admin:</b> {}"
            "\n<b>User:</b> {}"
            "\n<b>User ID:</b> <code>{}</code>".format(
                info["fname"],
                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                user_target,
                fban_user_id,
            ),
            parse_mode="HTML",
        )
        # Send message to owner if fednotif is enabled
        if getfednotif:
            try:
                await adminbot.send_message(
                    int(info["owner"]),
                    "<b>Un-FedBan</b>"
                    "\n<b>Federation:</b> {}"
                    "\n<b>Federation Admin:</b> {}"
                    "\n<b>User:</b> {}"
                    "\n<b>User ID:</b> <code>{}</code>".format(
                        info["fname"],
                        f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                        user_target,
                        fban_user_id,
                    ),
                    parse_mode="HTML",
                )
            except Exception as e:
                print(e)
                pass
        # If fedlog is set, then send message, except fedlog is current chat
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if int(get_fedlog) != int(chat):
                try:
                    await adminbot.send_message(
                        int(get_fedlog),
                        "<b>Un-FedBan</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>".format(
                            info["fname"],
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                        ),
                        parse_mode="HTML",
                    )
                except Exception as e:
                    print(e)
                    pass
        unfbanned_in_chats = 0
        for fedchats in chat_list:
            unfbanned_in_chats += 1

        try:
            x = sql.un_fban_user(fed_id, user_id)
            if not x:
                await event.reply(
                    "Un-fban failed, this user may already be un-fedbanned!"
                )
                return
        except:
            pass

        if unfbanned_in_chats == 0:
            await event.reply("This person has been un-fbanned in 0 chats.")
        if unfbanned_in_chats > 0:
            await event.reply(
                "This person has been un-fbanned in {} chats.".format(
                    unfbanned_in_chats
                )
            )
    except Exception as e:
        print(e)
        pass


@admin_cmd("setfedlog",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fedinfo = sql.get_fed_info(args)
            if not fedinfo:
                await event.reply("This Federation does not exist!")
                return
            isowner = is_user_fed_owner(args, user.id)
            if not isowner:
                await event.reply("Only federation creator can set federation logs.")
                return
            setlog = sql.set_fed_log(args, chat)
            if setlog:
                await event.reply(
                    "Federation log `{}` has been set to {}".format(
                        fedinfo["fname"], event.chat.title
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@admin_cmd("unsetfedlog",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fedinfo = sql.get_fed_info(args)
            if not fedinfo:
                await event.reply("This Federation does not exist!")
                return
            isowner = is_user_fed_owner(args, user.id)
            if not isowner:
                await event.reply("Only federation creator can set federation logs.")
                return
            setlog = sql.set_fed_log(args, None)
            if setlog:
                await event.reply(
                    "Federation log `{}` has been revoked on {}".format(
                        fedinfo["fname"], event.chat.title
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@admin_cmd("fedsubs",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        try:
            getmy = sql.get_mysubs(fed_id)
        except:
            getmy = []

        if len(getmy) == 0:
            await event.reply(
                "Federation `{}` is not subscribing any federation.".format(
                    fedinfo["fname"]
                ),
                parse_mode="markdown",
            )
            return
        else:
            listfed = "Federation `{}` is subscribing federation:\n".format(
                fedinfo["fname"]
            )
            for x in getmy:
                listfed += "- `{}`\n".format(x)
            listfed += "\nTo get fed info `/fedinfo <fedid>`. To unsubscribe `/unsubfed <fedid>`."
            await event.reply(listfed, parse_mode="markdown")
    except Exception as e:
        print(e)
        pass


@admin_cmd("myfeds",is_args=False)
async def _(event):
    try:
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        fedowner = sql.get_user_owner_fed_full(user.id)
        if fedowner:
            text = "**You are owner of feds:\n\n**"
            for f in fedowner:
                text += "- **{}**: `{}`\n".format(f["fed"]["fname"], f["fed_id"])
        else:
            text = "**You don't have any feds !**"
        await event.reply(text, parse_mode="markdown")

    except Exception as e:
        print(e)
        pass


@admin_cmd("fbanlist",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return

        getfban = sql.get_all_fban_users(fed_id)
        if len(getfban) == 0:
            await event.reply(
                "The federation ban list of {} is empty".format(info["fname"]),
                parse_mode="html",
            )
            return

        text = "<b>{} users have been banned from the federation {}:</b>\n".format(
            len(getfban), info["fname"]
        )
        for users in getfban:
            getuserinfo = sql.get_all_fban_users_target(fed_id, users)
            if getuserinfo is False:
                text = "There are no users banned from the federation {}".format(
                    info["fname"]
                )
                break
            user_name = getuserinfo["first_name"]
            if not getuserinfo["last_name"] is None:
                user_name += " " + getuserinfo["last_name"]
            text += " • {} (<code>{}</code>)\n".format(
                f"<p><a href='tg://user?id={users}'>{user_name}</a></p>", users
            )
        try:
            await event.reply(text, parse_mode="html")
        except:
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can back up data once every 30 minutes!\nYou can back up data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            cleanr = re.compile("<.*?>")
            cleantext = re.sub(cleanr, "", text)
            with BytesIO(str.encode(cleantext)) as output:
                output.name = "fbanlist.txt"
                await adminbot.send_file(
                    event.chat_id,
                    file=output,
                    filename="fbanlist.txt",
                    caption="The following is a list of users who are currently fbanned in the Federation {}.".format(
                        info["fname"]
                    ),
                )
    except Exception as e:
        print(e)
        pass


@admin_cmd("exportfbans",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        chat_data = {}
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return
        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return
        getfban = sql.get_all_fban_users(fed_id)
        if len(getfban) == 0:
            await event.reply(
                "The federation ban list of {} is empty".format(info["fname"]),
                parse_mode="html",
            )
            return
        args = True
        if args:
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can backup your data once every 30 minutes!\nYou can back up data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            backups = ""
            for users in getfban:
                getuserinfo = sql.get_all_fban_users_target(fed_id, users)
                json_parser = {
                    "user_id": users,
                    "first_name": getuserinfo["first_name"],
                    "last_name": getuserinfo["last_name"],
                    "user_name": getuserinfo["user_name"],
                    "reason": getuserinfo["reason"],
                }
                backups += json.dumps(json_parser)
                backups += "\n"
            with BytesIO(str.encode(backups)) as output:
                output.name = "julia_fbanned_users.json"
                await adminbot.send_file(
                    event.chat_id,
                    file=output,
                    filename="julia_fbanned_users.json",
                    caption="Total {} users are blocked by the Federation {}.".format(
                        len(getfban), info["fname"]
                    ),
                )
            return
    except Exception as e:
        print(e)
        pass


@admin_cmd("subfed",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)
        if args == fed_id:
            await event.reply("You cannot subscribe a federation to it's own")
            return

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        if args:
            getfed = sql.search_fed_by_id(args)
            if getfed is False:
                await event.reply("Please enter a valid federation id.")
                return
            subfed = sql.subs_fed(args, fed_id)
            if subfed:
                await event.reply(
                    "Federation `{}` has subscribed the federation `{}`. Every time there is a Fedban from that federation, this federation will also ban that user.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
                get_fedlog = sql.get_fed_log(args)
                if get_fedlog:
                    if int(get_fedlog) != int(chat):
                        try:
                            await adminbot.send_message(
                                int(get_fedlog),
                                "Federation `{}` has subscribed the federation `{}`".format(
                                    fedinfo["fname"], getfed["fname"]
                                ),
                                parse_mode="markdown",
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply(
                    "Federation `{}` already subscribed the federation `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@admin_cmd("unsubfed",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)
        if args == fed_id:
            await event.reply("You cannot unsubscribe a federation to it's own")
            return

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        if args:
            getfed = sql.search_fed_by_id(args)
            if getfed is False:
                await event.reply("Please enter a valid federation id.")
                return
            subfed = sql.unsubs_fed(args, fed_id)
            if subfed:
                await event.reply(
                    "Federation `{}` now unsubscribe fed `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
                get_fedlog = sql.get_fed_log(args)
                if get_fedlog:
                    if int(get_fedlog) != int(chat):
                        try:
                            await adminbot.send_message(
                                int(get_fedlog),
                                "Federation `{}` has unsubscribed fed `{}`.".format(
                                    fedinfo["fname"], getfed["fname"]
                                ),
                                parse_mode="markdown",
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply(
                    "Federation `{}` is not subscribed to `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@admin_cmd("fbroadcast", is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fed_id = sql.get_fed_id(chat)
            fedinfo = sql.get_fed_info(fed_id)
            if is_user_fed_owner(fed_id, user.id) is False:
                await event.reply("Only federation owners can do this!")
                return
            text = args
            try:
                broadcaster = user.first_name + " " + user.last_name
            except:
                broadcaster = user.first_name
            text += f"\n\n- [{broadcaster}](tg://user?id={user.id})"
            chat_list = sql.all_fed_chats(fed_id)
            failed = 0
            for chat in chat_list:
                title = "**New broadcast from Fed {}**\n\n".format(fedinfo["fname"])
                try:
                    await adminbot.send_message(
                        int(chat), title + text, parse_mode="markdown"
                    )
                except Exception as e:
                    sql.chat_leave_fed(chat)
                    failed += 1
                    print(e)
                    pass

            send_text = "The federation broadcast is complete\n"
            if failed >= 1:
                send_text += "{} groups failed to receive the message.".format(failed)
            await event.reply(send_text)
    except Exception as e:
        print(e)
        pass


@admin_cmd("fednotif",is_args="simple")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if args:
            if args == "on":
                sql.set_feds_setting(user.id, True)
                await event.reply(
                    "Reporting Federation back up! Every user who is fban / unfban you will be notified via PM."
                )
            elif args == "off":
                sql.set_feds_setting(user.id, False)
                await event.reply(
                    "Reporting Federation has stopped! Every user who is fban / unfban you will not be notified via PM."
                )
            else:
                await event.reply("Please enter `on`/`off`", parse_mode="markdown")
        else:
            getreport = sql.user_feds_report(user.id)
            await event.reply(
                "Your current Federation report preferences: `{}`".format(getreport),
                parse_mode="markdown",
            )
    except Exception as e:
        print(e)


@admin_cmd("fedchats",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        getlist = sql.all_fed_chats(fed_id)
        if len(getlist) == 0:
            await event.reply(
                "No chats are joined to the federation **{}**".format(info["fname"]),
                parse_mode="html",
            )
            return

        text = "<b>Here is the list of chats connected to {}:</b>\n\n".format(
            info["fname"]
        )
        for chats in getlist:
            text += " • <code>{}</code>\n".format(chats)
        try:
            await event.reply(text, parse_mode="html")
        except:
            cleanr = re.compile("<.*?>")
            cleantext = re.sub(cleanr, "", text)
            with BytesIO(str.encode(cleantext)) as output:
                output.name = "fedchats.txt"
                await adminbot.send_file(
                    file=output,
                    filename="fedchats.txt",
                    caption="Here is a list of all the chats that joined the federation **{}**".format(
                        info["fname"]
                    ),
                )
    except Exception as e:
        print(e)


@admin_cmd("importfbans",is_args=False)
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        chat_data = {}
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)
        getfed = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return

        if event.reply_to_msg_id:
            op = await event.get_reply_message()
            try:
                op.media.document
            except Exception:
                await event.reply("Thats not a file.")
                return
            h = op.media
            try:
                k = h.document.attributes
            except Exception:
                await event.reply("Thats not a file.")
                return
            if not isinstance(h, MessageMediaDocument):
                await event.reply("Thats not a file.")
                return
            if not isinstance(k[0], DocumentAttributeFilename):
                await event.reply("Thats not a file.")
                return
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can import your data once every 30 minutes!\nYou can get data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            success = 0
            failed = 0
            fileformat = op.file.name.split(".")[-1]
            if fileformat == "json":
                try:
                    file_info = await adminbot.download_file(op, op.file.name)
                except Exception:
                    await event.reply(
                        "Try downloading and re-uploading the file, this one seems broken!"
                    )
                    return
                multi_fed_id = []
                multi_import_userid = []
                multi_import_firstname = []
                multi_import_lastname = []
                multi_import_username = []
                multi_import_reason = []
                with open(op.file.name) as file:
                    file.seek(0)
                    reading = file.read()
                    splitting = reading.split("\n")
                    for x in splitting:
                        if x == "":
                            continue
                        try:
                            data = json.loads(x)
                        except json.decoder.JSONDecodeError as err:
                            failed += 1
                            continue
                        try:
                            import_userid = int(data["user_id"])  # Make sure it int
                            import_firstname = str(data["first_name"])
                            import_lastname = str(data["last_name"])
                            import_username = str(data["user_name"])
                            import_reason = str(data["reason"])
                        except ValueError:
                            failed += 1
                            continue
                        # Checking user
                        if int(import_userid) == BOT_ID:
                            failed += 1
                            continue
                        if is_user_fed_owner(fed_id, import_userid) is True:
                            failed += 1
                            continue
                        if is_user_fed_admin(fed_id, import_userid) is True:
                            failed += 1
                            continue
                        if str(import_userid) == str(OWNER_ID):
                            failed += 1
                            continue
                        multi_fed_id.append(fed_id)
                        multi_import_userid.append(str(import_userid))
                        multi_import_firstname.append(import_firstname)
                        multi_import_lastname.append(import_lastname)
                        multi_import_username.append(import_username)
                        multi_import_reason.append(import_reason)
                        success += 1
                    sql.multi_fban_user(
                        multi_fed_id,
                        multi_import_userid,
                        multi_import_firstname,
                        multi_import_lastname,
                        multi_import_username,
                        multi_import_reason,
                    )
                text = "Blocks were successfully imported.\n`{}` people are blocked.".format(
                    success
                )
                if failed >= 1:
                    text += " {} Failed to import.".format(failed)
                get_fedlog = sql.get_fed_log(fed_id)
                if get_fedlog:
                    if eval(get_fedlog):
                        teks = "Fed **{}** has successfully imported data.\n{} banned.".format(
                            getfed["fname"], success
                        )
                        if failed >= 1:
                            teks += " {} Failed to import.".format(failed)
                        try:
                            await adminbot.send_message(
                                int(get_fedlog), teks, parse_mode="markdown"
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply("This file is not supported.")
                return
            await event.reply(text)
            os.remove(op.file.name)
        else:
            await event.reply("Reply to the backup(export) file to import it.")
            return
    except Exception as e:
        print(e)


@admin_cmd("fbanstat",is_args="simple")
async def _(event):
    try:
        # chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        args = event.pattern_match.group(1)
        if args:
            userid = args
            if args.isdigit():
                user_idd = args
                user_iddd = await adminbot.get_input_entity(int(user_idd))
                user_id = user_iddd.user_id
            else:
                user_idd = args
                user_iddd = await adminbot.get_input_entity(user_idd)
                user_id = user_iddd.user_id
            if not user_id:
                await event.reply("Please enter a valid user id.")
                return
            if user_id:
                user_name, fbanlist = sql.get_user_fbanlist(str(user_id))
                if user_name == "":
                    try:
                        user_namee = await adminbot.get_entity(int(user_id))
                        user_name = user_namee.first_name
                    except Exception:
                        user_name = "He/she"
                    if user_name == "" or user_name is None:
                        user_name = "He/she"
                if len(fbanlist) == 0:
                    await event.reply(
                        "**{}** is not banned in any federation!".format(user_name),
                    )
                    return
                else:
                    teks = "**{}** has been banned in these federations:\n\n".format(
                        user_name
                    )
                    for x in fbanlist:
                        teks += "- `{}`: {}\n".format(x[0], x[1][:20])
                    await event.reply(teks, parse_mode="markdown")
        else:
            await event.reply("Syntax: `/fbanstat <userid/entity>`")
            return
    except Exception as e:
        print(e)


@adminbot.on(events.NewMessage(pattern=None))
async def _(event):
    if event.is_private:
        return
    chat = event.chat_id
    if chat == int(-1001237141420):
        return
    if chat == int(-1001442336182):
        return
    user = event.sender_id
    fed_id = sql.get_fed_id(chat)
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user)
    if fban:
        await event.reply(
            "This user is banned in the current federation!\nI will remove him."
        )
        await adminbot.kick_participant(chat, user)
    else:
        return


@adminbot.on(events.ChatAction())
async def join_ban(event):
    if event.is_private:
        return
    chat = event.chat_id
    if chat == int(-1001237141420):
        return
    if chat == int(-1001442336182):
        return
    user = event.user_id
    fed_id = sql.get_fed_id(chat)
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user)
    if fban:
        await event.reply(
            "This user is banned in the current federation!\nI will remove him."
        )
        await adminbot.kick_participant(chat, user)
    else:
        return


# Temporary data
def put_chat(chat_id, value, chat_data):
    # print(chat_data)
    if value is False:
        status = False
    else:
        status = True
    chat_data[chat_id] = {"federation": {"status": status, "value": value}}


def get_chat(chat_id, chat_data):
    # print(chat_data)
    try:
        value = chat_data[chat_id]["federation"]
        return value
    except KeyError:
        return {"status": False, "value": False}

#======================================================================================
print("Admin Bot Started !!")


def startbot():
    adminbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
