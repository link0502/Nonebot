from nonebot import on_command, CommandSession, permission as perm
from  nonebot import get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import requests
bot=get_bot()

#查询群信息
@on_command('send_group_list', aliases=('群',),permission=perm.SUPERUSER)
async def send_group_list(session: CommandSession):
    #获取qq群的信息
    group_list = await session.bot.get_group_list()
    msg='共有{}个群：'.format(len(group_list))
    for group in group_list:
        msg+='\n-----------------\n'+'群名:' + group['group_name'] + '\n' +'群号:' + str(group['group_id'])
    await session.send(msg)


@on_command('delete_Group', aliases=('退群',),permission=perm.SUPERUSER)
async def delete_Group(session: CommandSession):
    GroupID= session.get('tuiqun', prompt='你想退出哪个群呢？（请输入群号）')
    try:
        await bot.set_group_leave(group_id=GroupID)
        await session.send('退出成功')
    except:
        await session.send('操作失败')


@delete_Group.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将群名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：退群 12323
            session.state['tuiqun'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的群号（而是发送了空白字符），则提示重新输入
        QQ=session.ctx['user_id']
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('[CQ:at,qq='+str(QQ)+']\n输入的群号不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的输入的群号），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

@on_natural_language(keywords={'退群'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    #获取群ID
    GroupID=''
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'm':
            # ns 词性表示地名
            GroupID= int(word.word)
    # 如果没有找到群ID就直接忽略
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'delete_Group', current_arg=GroupID or '')

