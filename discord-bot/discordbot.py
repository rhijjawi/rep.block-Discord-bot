import discord
from discord.ext import commands
from typing import Union, Optional

bot = commands.Bot(command_prefix='!')
token = open("token.txt", "r").readline()  # Looks for Api Client ID
embed_color = 0xff8200
good_color = 0x75F702
bad_color = 0xf80a02

user_id = 234649992357347328

@bot.event
async def on_ready():
    print("The bot is ready! To view available commands, please type !help")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
        name=str(len(bot.guilds)) + " servers | !help")
    )
    
@bot.command()
async def hilfe(ctx):
    embed = discord.Embed(title='RepBlock Help', description='Directions on how to use diffrent commands', color=embed_color, inline=False)
    embed.add_field(name='!whois <UserID>/@mention', value='Gives more information about specific Discord user.', inline=False)
    embed.add_field(name='!rep+ <UserID.', value='Gives a time value for how long until given holiday.', inline=False)
    embed.add_field(name='!unblock <UserID>', value='Returns a wiki link for more information on given holiday.', inline=False)
    embed.add_field(name='!ping', value='Test latency between Discord API and rep.block', inline=False)
    embed.add_field(name='!whois', value='Returns a WhoIS discord of a specific user', inline=False)
    await ctx.send(embed=embed)

@bot.command()#Check latency
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'{round(bot.latency*1000)}ms', color=embed_color)
    await ctx.send(embed=embed)

@bot.command() #reputation
async def rep(ctx, user: discord.Member=None):
    await ctx.send("Hi there! To give someone a negative rep, please paste their ID in the chat")
    
@commands.has_permissions(send_messages=True)
@bot.command() #whois command
async def whois(ctx, user: discord.Member=None):
    user = user or ctx.author
    avatar = user.avatar_url
    if user.bot:
        isbot = 'Yes'
    else:
        isbot = 'No'
    ct = user.created_at.strftime("%a, %d %B %Y , %I %M %p UTC")
    embed = discord.Embed(title=f'Discord Whois Complete', description=f'The user looked up was: {user}', color=good_color, inline=False)
    embed.set_image(url=f'{avatar}')
    embed.add_field(name='Is this user a bot?', value=f'{isbot}')
    embed.add_field(name='Account Creation Date', value=f'{ct}')
    embed.add_field(name='Reputation', value=f'{rep}')
    await ctx.send(embed=embed)

@whois.error
async def whois(ctx,error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title=f'Discord Whois Failed', description=f"**Could not find specified User ID**\n!whois <UserID>\n!whois @mention\n*UserID should be a number and can be copied by right click on a user's profile*", color=embed_color, inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def purge(ctx, limit: int):
        author = format(ctx.author.name)
        await ctx.channel.purge(limit=limit + 1)
        embed=discord.Embed(title="", description=f"**{author}** purged **{limit}** messages!.", colour=bad_color, url="")
        await ctx.send(embed=embed, delete_after=5.0)

@purge.error
async def purge(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f'Message Purge Failure', description=f"No messages left **or** messages are older than 14 days", colour=bad_color)
        await ctx.send(embed=embed, delete_after=10.0)
    
@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, member: Optional[Union[discord.Member, discord.Object]], *, reason=None):
    if member == ctx.message.author:
        embed = discord.Embed(title=f'Discord User Kick', description=f'**Failed!**\n\nIncorrect Syntax:\n!kick <@mention>', color=bad_color, inline=False)
        return await ctx.send(embed=embed)
    if not member:
        return await ctx.send("You need to ping the person whom you would like to kick")
    reason = reason or "No reason provided."
    embed = discord.Embed(title=f"<{member} has been kicked by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
    if isinstance(member, discord.Member):
        try:
            await member.send(embed=embed)
            embed = discord.Embed(title=f"{member} has been kicked by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
        except discord.HTTPException:
            print(f"DEBUG: Failed to dm {member} when kicking them from {ctx.guild.name}")
    else:
        embed = discord.Embed(title=f"<@{member.id}> has been kicked by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
    await ctx.guild.kick(member, reason=reason)        
    await ctx.channel.send(embed=embed)
        

@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, member: Optional[Union[discord.Member, discord.Object]], *, reason=None):
    if member == ctx.message.author:
        embed = discord.Embed(title=f'Discord User Ban', description=f'**Failed!**\n\nIncorrect Syntax:\n!ban <@mention>', color=bad_color, inline=False)
        return await ctx.send(embed=embed)
    if not member:
        return await ctx.send("You need to ping the person whom you would like to ban!")
    reason = reason or "No reason provided."
    embed = discord.Embed(title=f"<{member} has been banned by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
    if isinstance(member, discord.Member):
        try:
            await member.send(embed=embed)
            embed = discord.Embed(title=f"{member} has been banned by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
        except discord.HTTPException:
            print(f"DEBUG: Failed to dm {member} when banning them from {ctx.guild.name}")
    else:
        embed = discord.Embed(title=f"<@{member.id}> has been banned by {ctx.author}.", color=good_color, description=f"Reason: {reason}")
    await ctx.guild.ban(member, reason=reason)        
    await ctx.channel.send(embed=embed)


bot.run(token)