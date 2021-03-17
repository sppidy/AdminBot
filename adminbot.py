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
from bot import *
admin_cmd = cmd
from telethon import events
from telethon.utils import pack_bot_file_id
import bot.sql.welcomesql
import bot.sql.filtersql

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
                    await jarvis.delete_messages(  # pylint:disable=E0602
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

DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


global last_triggered_filters
last_triggered_filters = {}  # pylint:disable=E0602


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
        await event.reply(f"filter {name} saved successfully. Get it with {name}")
    else:
        await event.reply("Reply to a message with `savefilter keyword` to save the filter")


@admin_cmd("listfilters",is_args=True)
async def on_snip_list(event):
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Available Filters in the Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = "No Filters. Start Saving using `.savefilter`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await jarvis.send_file(
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


@admin_cmd("clearfilter",is_args=True)
@only_groups
@is_bot_admin
@is_admin
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await event.reply(f"filter {name} deleted successfully")


@admin_cmd("clearallfilters",is_args=False)
@only_groups
@is_bot_admin
@is_admin
async def on_all_snip_delete(event):
    remove_all_filters(event.chat_id)
    await event.reply(f"filters **in current chat** deleted successfully")

print("Admin Bot Started !!")


def startbot():
    adminbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
