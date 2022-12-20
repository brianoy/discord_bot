import discord
from discord.ext import commands,tasks
import json
import random

from auto_roll_call.qr_code import qr_code_decode
from auto_roll_call.translate import AI
from auto_roll_call.roll_call import auto_roll_call

from mod.addlog import addlog#不要用print()，而是用addlog.debug()或addlog.info()等等
from mod.emoji_role import know_emoji_find_id,know_emoji_find_name,know_id_find_emoji,know_id_find_name,know_name_find_emoji,know_name_find_id#我就一次引入全部了
from mod.message_process import message_process
from mod.voice_chat_log import voice_chat_log
from mod.japan_ticket import japan

counter_for_MOTD = 0

with open('.\setting.json',mode='r',encoding='utf-8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = ',', intents = intents)

print("TOKEN : "+jdata['TOKEN'])
print("ID : "+jdata['ID'])

@bot.event
async def on_ready():
    addlog.info(">>>>>>>>>已上線<<<<<<<<<")
    print('目前登入身份：'+ str(bot.user))
    game = discord.Game('ohohoh')
    await bot.change_presence(status=discord.Status.online, activity=game)
    presence_loop.start()
    #check_japan_airline_loop.start()


@tasks.loop(seconds=3)
async def presence_loop():
    total_members = []
    global counter_for_MOTD
    for guild in bot.guilds:
        total_members.extend(guild.members)
    total_members_count = len(set(total_members))
    presence = [
        "ohohoh",
        str(total_members_count) + "個二逼卵子在看我",
        "hihihi"
    ]
    if (counter_for_MOTD >= len(presence)):
        counter_for_MOTD = 0
    game = discord.Game(presence[counter_for_MOTD])
    counter_for_MOTD += 1
    await bot.change_presence(status=discord.Status.online, activity=game)

@tasks.loop(minutes=20)
async def check_japan_airline_loop():
    japan.check_airline_price()


@bot.event
async def on_member_join(member):
    addlog.info(f'{member} 加入了伺服器!') #=print(member + "join!")
    channel = bot.get_channel(int(jdata['ID']))
    await channel.send(f'{member} 一支一支棒棒')

@bot.event
async def on_member_remove(member):
    addlog.info(f'{member} 離開了伺服器!')
    channel = bot.get_channel(int(jdata['ID']))
    await channel.send(f'{member} 真假:(')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} ms') 

@bot.command()
async def morning(ctx):
    random_pic = random.choice(jdata['Morning_pic'])
    pic = discord.File(random_pic)
    addlog.debug(f'Good morning 指令已偵測 {ctx},')
    addlog.debug(f'送出{random_pic} !')
    await ctx.send(file = pic)

@bot.command()
async def em(ctx):
    embed=discord.Embed(title="身分組", description="自己選擇需要的身分組，如果無法運作就找離九八八踹共", color=0xbdf7ff)
    embed.set_image(url="https://obs.line-scdn.net/0hzmZ4fmppJUJnTTKByc5aFV8bKTNUKz9LRSlqdBFPLiIYYWBEWyp2IRJKfG4adWITR35qJBZOfnsadGNHWw/w644")
    embed.add_field(name="#礦工", value="按下這個標籤【⛏️】", inline=True)
    embed.add_field(name="#啞巴", value="按下這個標籤【🫢】", inline=True)
    embed.add_field(name="#我們缺DJ", value="按下這個標籤【💿】", inline=True)
    embed.add_field(name="#開車車", value="按下這個標籤【🤵‍♂】", inline=True)
    embed.add_field(name="美女", value="按下這個標籤【💃】", inline=True)
    embed.add_field(name="帥哥", value="按下這個標籤【🕺】", inline=True)
    embed.add_field(name="處男", value="按下這個標籤【🤮】", inline=True)
    embed.add_field(name="大GG", value="按下這個標籤【👃】", inline=True)
    embed.set_footer(text="\n\n嗯哼嗯哼嗯亨嗯亨")
    await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if (payload.channel_id == 1026408101752090665 and payload.message_id == 1027410329833066576):
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reactions = str(payload.emoji)
        user_object = payload.member
        addlog.debug(message)
        role_id = know_emoji_find_id(reactions)
        if role_id != 0:
            role = user_object.guild.get_role(role_id)
            await user_object.add_roles(role, atomic=True)
            name = know_id_find_name(role_id)
            addlog.info("已幫" + str(user_object) + "加入身分組 >" + name + "< (" + str(role_id) + ")") 

#payload.member only works with on_raw_reaction_add()
@bot.event
async def on_raw_reaction_remove(payload):
    if (payload.channel_id == 1026408101752090665 and payload.message_id == 1027410329833066576):
        guild = await bot.fetch_guild(payload.guild_id)
        user_object = await guild.fetch_member(payload.user_id)
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reactions = str(payload.emoji)
        #guild_id = payload.guild_id
        addlog.debug(message)
        role_id = know_emoji_find_id(reactions)
        if role_id != 0:
            role = user_object.guild.get_role(role_id)
            await user_object.remove_roles(role, atomic=True)
            name = know_id_find_name(role_id)
            addlog.info("已幫" + str(user_object) + "移除身分組 >" + name + "< (" + str(role_id) + ")") 
    
@bot.event
async def on_message(message):
    if str(message.author) == "大洋遊俠#0000" or str(message.author) == "lijiubot#5772" or str(message.author) == "Mine Bot#8530": #排除掉機器人、自己還有webhook傳的訊息
        pass
    else: #排除掉雜魚訊息後進入處理訊息模組
        msg_pros_object = message_process.message_process(message) #訊息處理，在mod/message_process裡面
        try:
            #print(message.attachments[0]['url'])
            pass
        except IndexError:
            pass
        if msg_pros_object != False: #msg_pros_object內部有東西才channel.send，否則將會raise error
            await message.channel.send(msg_pros_object)
        await bot.process_commands(message) #加了這行才可以監聽on_message順便還有指令的功能，要不然一開始on_message會override bot的command權限

@bot.event
async def on_voice_state_update(member, before, after):
    print(before)
    print(after)
    print(member)
    voice_chat_log(member, before, after)



bot.run(jdata['TOKEN'])

