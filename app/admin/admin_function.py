# 管理功能
from telegram import ChatPermissions, ChatMember
from telegram.ext import CallbackContext

from app.model.models import init_session,BanUserLogo
from telegram import Update

#是否存在违禁词
def delete_txt(txt, str):
    for x in txt:
        if x in str:
            return x
    return None

#获取违禁词
def get_ban_word(ban_word_object):  # 获取
    lis = []
    words = ban_word_object.select()
    for x in words:
        lis.append(x[0])
    return lis

#写入违禁词
def write_ban_word(ban_word_object, str):
    ban_word_object.insert(str)

#封禁用户
#在调用词方法之前请检查 机器人是否有相关权限
def block_person(update:Update, context: CallbackContext, ban_word):
    session=init_session()
    existing_user: BanUserLogo | None = session.get(BanUserLogo, update.effective_user.id)
    if not existing_user:
         session.add(BanUserLogo(uid=update.effective_user.id,
                            usr_name=update.effective_user.name,
                            word=update.message.text,
                            ban_word=ban_word
                            ))
    session.commit()
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                     user_id=update.effective_user.id,
                                     permissions=ChatPermissions(can_send_messages=False,
                                                                 can_send_media_messages=False))

#判断是否有删除消息的权限
def bot_delete_permission(update: Update, context: CallbackContext):
    # 机器人id
    bot_user_id = context.bot.get_me().id

    # 群组的 Chat ID
    chat_id = update.message.chat_id

    chat_memeber: ChatMember = context.bot.get_chat_member(chat_id, bot_user_id)

    if not chat_memeber.can_delete_messages:
        return 0

    return 1
#判断是否有封锁用户的权限
def bot_restrict_permission(update: Update, context: CallbackContext):
    # 机器人id
    bot_user_id = context.bot.get_me().id

    # 群组的 Chat ID
    chat_id = update.message.chat_id

    chat_memeber: ChatMember = context.bot.get_chat_member(chat_id, bot_user_id)

    if not chat_memeber.can_restrict_members:
        return 0

    return 1