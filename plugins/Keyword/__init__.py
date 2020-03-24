# 关键词特定回复
# -*- coding: utf-8 -*-
import random
from .db import *
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand, permission as perm

# 注册一个仅内部使用的命令，不需要 aliases(这里就是不加命令时调用的方法)
@on_command('keyword')
async def keyword(session: CommandSession):
    QQ = session.ctx['user_id']
    message = session.get('message')
    # 这里来简单的替换内容
    message = message.replace("@", "[CQ:at,qq=" + str(QQ) + "]")
    message = message.replace("\\n", "\n")
    await session.send(message)


@on_command('key_search', aliases=('查询', '查询关键词'))
async def key_search(session: CommandSession):
    QQ = session.ctx['user_id']
    sql="SELECT thekey,replay FROM ckeyword"
    result=sql_dql(sql)
    if len(result)>0:
        senddata=""
        for i in range(0,len(result)):
            senddata+=(str(i)+"、" +"   "+result[i][0]+"\n")
        await session.send(senddata)
    else:
        await session.send("[CQ:at,qq=" + str(QQ) + "]      查询结果为空")

#命令入口 添加信任QQ  
@on_command('trustqq',aliases=('信任', '添加信任'),permission=perm.SUPERUSER | perm.GROUP_ADMIN) 
async def _(session: CommandSession):
    QQ = session.ctx['user_id']
    msg = session.current_arg
    if session.is_first_run:
        await session.pause("[CQ:at,qq=" + str(QQ) + "]   回复QQ号即可添加")
    elif msg.isdigit():
        sql = "INSERT INTO believe (QQ) VALUES ('" + msg + "')"
        if sql_dml(sql) is None:
            await session.send("[CQ:at,qq=" + str(QQ) + "]   添加成功!")
            session.finish()
        else:
            await session.send("[CQ:at,qq=" + str(QQ) + "]   添加失败，该用户已存在")
            session.finish()
    else:
        await session.send("[CQ:at,qq=" + str(QQ) + "]   错误回复,已退出!")
        session.finish()

#命令入口 学习模式
@on_command('learning',aliases=('学习', '学习模式')) 
async def _(session: CommandSession):
    QQ = session.ctx['user_id']
    msg = session.current_arg
    if session.is_first_run:
        sql = "SELECT QQ FROM believe WHERE QQ='" + str(QQ) + "'"
        if sql_dql(sql):
            await session.pause("[CQ:at,qq=" + str(QQ) + "]\n回复“关键词-回复内容”即可学习到这个内容（多个回复可以用@@分割）\n小提示：支持表情，换行，还有‘@’表示@这个人")
        else:
            await session.send("[CQ:at,qq=" + str(QQ) + "]，抱歉，你不在信任名单中")
            session.finish()
    elif "-" in msg:
        if await addreplay(msg) is None:
            await session.pause("[CQ:at,qq=" + str(QQ) + "]，添加成功\n继续输入可继续学习，输入其他指令则退出学习模式")
        else:
            await session.send("[CQ:at,qq=" + str(QQ) + "]，添加失败\n已退出学习模式")
            session.finish()
    else:
        await session.send("[CQ:at,qq=" + str(QQ) + "]，输入错误，已退出学习模式!")
        session.finish()


#自然语言入口 添加关键词
@on_natural_language(keywords={'？'})
async def _(session: NLPSession):
    QQ = session.ctx['user_id']
    stripped_msg = session.msg.strip()
    # 快捷添加
    if stripped_msg.startswith("？") and "-" in stripped_msg:
        sql = "SELECT QQ FROM believe WHERE QQ='" + str(QQ) + "'"
        if sql_dql(sql) is not None:
            if  await addreplay(stripped_msg[1:]) is None:
                await session.send("[CQ:at,qq=" + str(QQ) + "]      更新成功！")
            else:
                await session.send("[CQ:at,qq=" + str(QQ) + "]      添加失败")
        else:
            await session.send("[CQ:at,qq=" + str(QQ) + "]      抱歉，你不在信任名单")
    else:
        await session.send("[CQ:at,qq=" + str(QQ) + "]      指令错误！")
    return IntentCommand(65, 'keyword', args={'message': ''})
#函数 添加关键词
async def addreplay(content):
    data = content.split("-")
    # 内容不能为空
    if not data[0] or not data[1]:
        return False
    # 这里提取一下优先级
    weight=50
    # 先找找关键词是否存在
    sql = "SELECT thekey,replay FROM cKeyword WHERE thekey='" + data[0] + "'"
    dta = sql_dql(sql)
    if dta:
        # 关键词存在
        sql = "UPDATE cKeyword SET replay='" + data[1] + "',weight="+str(weight)+" WHERE thekey='" + data[0] + "'"
    else:
        sql = "INSERT INTO cKeyword (thekey,replay,weight) VALUES ('" + data[0] + "','" + data[1] + "',"+str(weight)+")"
    return sql_dml(sql)


@on_command('key_delete', aliases=('删除', '删除关键词'))
async def key_delete(session: CommandSession):
    QQ = session.ctx['user_id']
    key = session.get('key', prompt='你想删除哪个关键词呢？')
    sql = "SELECT QQ FROM believe WHERE QQ='" + str(QQ) + "'"
    if sql_dql(sql):
        sql="SELECT thekey  FROM cKeyword WHERE thekey='"+key+"'"
        if sql_dml(sql) is None:        
            await session.send("[CQ:at,qq=" + str(QQ) + "]      未找到关键词:"+key)
            session.finish()
        else:
            sql="DELETE FROM cKeyword WHERE thekey='"+key+"'"
            sql_dml(sql)
            await session.send("[CQ:at,qq=" + str(QQ) + "]      成功删除关键词:"+key)
            session.finish()
    else:
        await session.send("[CQ:at,qq=" + str(QQ) + "]      抱歉，你不在信任名单")

@key_delete.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['key'] = stripped_arg
        return
    session.state[session.current_key] = stripped_arg



#关键词回复
@on_natural_language
async def _(session: NLPSession):
    QQ = session.ctx['user_id']
    message = session.msg.strip()
    # 先把所有的数据都读出来
    sql = "SELECT thekey,replay,weight FROM ckeyword WHERE thekey LIKE '%" + message + "%'"
    result = sql_dql(sql)
    #这里是优先级的设置
    priority=70
    a=len(result)
    if  a > 0:
        klen = 0
        strg = ""
        # 我们这里匹配最长的
        for data in result:
            tlen = len(data[0])
            #如果完全匹配
            if data[0].strip()==message:
                priority=95
                strg=data[1]
                break
            elif tlen > klen:
                klen = tlen
                strg = data[1]
        content = strg
    else:
        return None
    return IntentCommand(priority, 'keyword', args={'message': content})
