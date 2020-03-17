from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

help_text = " 1. 发送【报修】，获取报修入口\n 2. 发送【教程】，获取上网教程。\n 3. 发送【投诉】，获取投诉链接。 \n 4. 发送【其他】，获取其他功能！"


@on_natural_language(keywords={'帮助'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    return IntentCommand(90.0, '帮助', current_arg='')

@on_command('帮助', aliases=('帮助','000' ))
async def address(session: CommandSession):
    try:
        await session.send("命令说明：\n"+help_text, ignore_failure=False)
    except:
        print("send error!")
