from nonebot import on_notice, NoticeSession, on_request, RequestSession, MessageSegment, get_bot

bot = get_bot()

#自动同意入群申请
@on_request('group')
async def _(session: RequestSession):
    if(session.ctx['group_id'] == 646077259):
        await session.approve()
    return

#欢迎新群友
@on_notice('group_increase')
async def _(session: NoticeSession):
    user_id = session.ctx.get('user_id')
    msg = MessageSegment.at(session.ctx['user_id']) + ' ' + MessageSegment.text(
        '欢迎新进群的小伙伴：\n并仔细阅读本群【所有公告】和【帮助文档】，进群先看【群文件和群相册】，看完有问题再问，为了让你安心看群文件，先禁言三分钟哈~请见谅')
    msg = f'[CQ:at, qq = {user_id}]' +'\n'+msg
    await session.send(msg)
    await bot.set_group_ban(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'], duration=180)

#群友退群
@on_notice('group_decrease')
async def _(session: NoticeSession):
    user_id = session.ctx.get('user_id')
    msg = '/(ㄒoㄒ)/~~又一位群友离我们而去'
    msg = f'[CQ:at, qq = {user_id}]' + '\n' + msg
    await session.send(msg)
