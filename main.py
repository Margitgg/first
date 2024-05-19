from config import token
import discord
from discord import Message, Option, Member, User
from discord.commands.context import ApplicationContext as c
import datetime
import asyncio

bot = discord.Bot(intents=discord.Intents.all())
bad_words = ["дурак", "лох", "балбес"]
good_words = ["блоха", "оглох"]
reps = {}


@bot.event
async def on_ready():
    print("бот запущен")


@bot.event
async def on_message(m: Message):
    global reps
    clean_msg = "".join(letter.lower() for letter in m.content if letter.isalpha())
    bad_word = False
    for word in bad_words:
        if word in clean_msg:
            bad_word = True
            break
    good_word = False
    for word in good_words:
        if word in clean_msg:
            good_word = True
            break
    if m.author.bot:
        return
    if m.author.id not in reps:
        reps[m.author.id] = 0
    if m.reference:
        ref_author = bot.get_message(m.reference.message_id).author.id
        name_author = bot.get_message(m.reference.message_id).author
        if m.content == "+++":
            reps[ref_author] += 1
            await m.channel.send(
                f"{m.author.name} повысил репутацию {name_author}! количество баллов: {reps[ref_author]}")
            if reps[ref_author] > 5:
                Moderator = discord.utils.get(name_author.guild.roles, name="Модератор")
                await name_author.add_roles(Moderator)
    elif m.content == "привет":
        await m.channel.send("привет я бот")
    elif "ку" in m.content:
        await m.reply("ку ку")
    elif m.content == "бот го в лс":
        await m.author.send("я здесь")
    elif bad_word is True and good_word is not True:
        await m.delete()


@bot.event
async def on_member_join(mem: Member):
    channels = mem.guild.channels
    for channel in channels:
        if channel.name == "основной":
            await channel.send(f"к нам присоединился {mem.mention}")
        if channel.name == "spam":
            await channel.send(f"зашёл {mem.name}")


@bot.event
async def on_member_remove(mem: Member):
    channels = mem.guild.channels
    for channel in channels:
        if channel.name == "основной":
            await channel.send(f"от нас ушёл {mem.name}")
        if channel.name == "spam":
            await channel.send(f"вышел {mem.name}")


@bot.event
async def on_member_update(old: Member, new: Member):
    channel = None
    channels = new.guild.channels
    for ch in channels:
        if ch.name == "spam":
            channel = ch
    if old.nick != new.nick:
        await channel.send(
            f"{old.name if not old.nick else old.nick} теперь {'без ника' if not new.nick else new.nick}")
    if old.roles != new.roles:
        await channel.send(f"{new.name} поменял роль")


@bot.event
async def on_user_update(old: User, new: User):
    channel = None
    channels = None
    members = bot.get_all_members()
    for mem in members:
        if new.name == mem.name:
            channels = mem.guild.channels
    for ch in channels:
        if ch.name == "spam":
            channel = ch
    if old.avatar != new.avatar:
        await channel.send(f"У {new.name} изменилась аватарка")
        await channel.send(new.avatar.url)
        msg = await channel.history(limit=1).flatten()
        await msg[0].add_reaction("😕")


@bot.slash_command(description="время в Москве")
async def msc_time(ctx: c):
    msc = datetime.timezone(datetime.timedelta(hours=3))
    data = datetime.datetime.now(msc)
    await ctx.respond(f"текущее время в Москве: {data.strftime('%H:%M:%S')}")


@bot.slash_command(description="Удаление сообщений")
async def clean(ctx: c, messages_for_delete: Option(int) = 10):
    await ctx.channel.purge(limit=messages_for_delete)
    await ctx.respond("начинается удаление")
    await ctx.delete()


@bot.slash_command(description="время в Аргентине")
async def arg_time(ctx: c):
    arg = datetime.timezone(datetime.timedelta(hours=-3))
    data = datetime.datetime.now(arg)
    await ctx.respond(f"текущее время в Аргентине: {data.strftime('%H:%M:%S')}")


@bot.slash_command(description="уравнение")
async def urav(ctx: c, x: Option(int), y: Option(int)):
    result = x ** 2 + y
    await ctx.respond(f'{x} ** 2 + {y} = {result}')


@bot.user_command(name="дата регистрации")
async def reg(ctx: c, member: Member):
    await ctx.respond(f"{member.mention} создал аккаунт {member.created_at}")


@bot.message_command(name="повышение репутации")
async def plus_rep(ctx: c, m: Message):
    await ctx.respond(f"моё уважение {m.author.mention}")


@bot.message_command(name="неуважение")
async def minus_rep(ctx: c, m: Message):
    await ctx.respond(f"диз {m.author.mention}")
    await ctx.delete(delay=2)
    await m.add_reaction("👎🏿")


@bot.message_command(name="нарушение прав.серв")
async def minus_rep(ctx: c, m: Message):
    await ctx.respond(f"это нарушение прав сервера, 1 предупреждение, больше предупреждений не будет{m.author.mention}")
    await ctx.delete(delay=25)
    await m.add_reaction("😡")


@bot.slash_command(description="таймер")
async def timer(ctx: c, sec: Option(int)):
    await ctx.respond(f"{ctx.author.mention} твой таймер запущен")
    await asyncio.sleep(sec)
    await ctx.channel.send(f"{ctx.author.mention} твои {sec} секунд прошли")


bot.run(token)
