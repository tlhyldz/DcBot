import discord
from discord.ext import commands
from utils import *
import os
import interactions


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix='!s ', intents=intents)
ext_file_types = ['png', 'jpg', 'jpeg', 'gif']

@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="Tarkan"))
    print("Ben Hazırım!")


@Bot.command()
async def clear (ctx, amount:int):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Komutun parametreleri eksik!")


@Bot.event
async def on_message(message):
    if len(message.attachments)> 0 and message.channel.name.startswith('sorular') :
        for ext in ext_file_types:
            if message.attachments[0].filename.endswith(ext):
                await message.add_reactions("Ⓐ")
                await message.add_reactions("Ⓑ")
                await message.add_reactions("Ⓒ")
                await message.add_reactions("Ⓓ")
                await message.add_reactions("Ⓔ")
                break


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_chanels, name="hoş-geldiniz")
    await channel.send(f'{member} aramıza katıldı. Hoş geldin!!!')
    print(f'{member} aramıza katıldı. Hoş geldin!!!')


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_chanels, name="gidenler")
    await channel.send(f'{member} aramızdan ayrıldı :( ')
    print(f'{member} aramızdan ayrıldı.')

@Bot.command()
@commands.has_role("admin")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@Bot.command(aliases=["copy"])
async def clone_channel(ctx,amount=1):
    for i in range(amount):
        await ctx.channel.clone()



@Bot.command()
@commands.has_role("admin")
async def kick(ctx, member: discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)

@Bot.command()
async def ban(ctx, member: discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)



@Bot.command()
async def unban(ctx, * , member):
    banned_user= await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for bans in banned_user:
        user = bans.user

        if(user.name,user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned user {user.mention}')
            return



@Bot.command()
async def load(ctx, extensions):
    Bot.load_extension(f'cogs.{extensions}')

@Bot.command()
async def unload(ctx, extensions):
    Bot.unload_extension(f'cogs.{extensions}')

@Bot.command()
async def reload(ctx, extensions):
    Bot.unload_extension(f'cogs.{extensions}')
    Bot.load_extension(f'cogs.{extensions}')

@Bot.command()
async def question(ctx):
    await ctx.message.add_reaction("")



for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        Bot.load_extension(f'cogs.{filename[:-3]}')



Bot.run(TOKEN)
