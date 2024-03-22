import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import asyncio
import random
import re


TOKEN = 'MTIxOTIyNDk1NzgzNDQ5ODA1OQ.GRTKIg.lex081EQdVZamQLKDp6qTyPNwc-FsTSSC7EW8w'

intents = discord.Intents.default()
intents.voice_states = True
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


afk_users = {}
music_queue = []

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for member in bot.get_all_members():
        if member.id not in warnings:
            warnings[member.id] = 3


# -------------------------- Music functions Start here --------------------------- #


# -------------------------- Music functions end here --------------------------- #


# -------------------------- Misc commands starts here --------------------------- #
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.command()
async def botinvite(ctx):
    """Generates an invite link for the bot."""
    invite_url = discord.utils.oauth_url(ctx.me.id, permissions=discord.Permissions(8))
    await ctx.send(f'Invite me to your server with this link: {invite_url}')

@bot.command()
async def invite(ctx):
    """Sends a never-expiring server invite link."""
    invite = await ctx.channel.create_invite(max_age=0, max_uses=0)
    await ctx.send(invite.url)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked.')

@bot.command()
async def memberstatus(ctx):
    """Displays the count of members based on their statuses."""
    guild = ctx.guild
    members = []
    async for member in guild.fetch_members(limit=None):
        members.append(member)

    # Count members based on their statuses
    online_members = sum(1 for m in members if m.status == discord.Status.online)
    idle_members = sum(1 for m in members if m.status == discord.Status.idle)
    dnd_members = sum(1 for m in members if m.status == discord.Status.do_not_disturb)
    offline_members = sum(1 for m in members if m.status == discord.Status.offline)

    # Count members who are streaming
    streaming_members = sum(1 for m in members if m.activities and any(a.type == discord.ActivityType.streaming for a in m.activities))

    # Create an embed to display the member counts
    embed = discord.Embed(title="Member Status", color=discord.Color.blue())
    embed.add_field(name="Online", value=online_members, inline=True)
    embed.add_field(name="Idle", value=idle_members, inline=True)
    embed.add_field(name="Do Not Disturb", value=dnd_members, inline=True)
    embed.add_field(name="Offline", value=offline_members, inline=True)
    embed.add_field(name="Streaming", value=streaming_members, inline=True)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def rgive(ctx, member: discord.Member, role: discord.Role, *, reason=None):
    """Gives a role to a member."""
    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member} has been given the {role} role.')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def rrm(ctx, member: discord.Member, role: discord.Role, *, reason=None):
    """Removes a role from a member."""
    await member.remove_roles(role, reason=reason)
    await ctx.send(f'{member} has been removed from the {role} role.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member from the server."""
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int, *, reason=None):
    """Unbans a user from the server."""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'{user} has been unbanned.')
    except discord.NotFound:
        await ctx.send('User not found.')

warnings = {}

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    """Warns a member for breaking a rule."""
    if ctx.author.id not in warnings:
        warnings[ctx.author.id] = []
    warnings[ctx.author.id].append((member.id, reason))
    await ctx.send(f"{member.mention} has been warned by {ctx.author.mention} for '{reason}'.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Deletes a specified number of messages from the channel."""
    if amount > 100:
        await ctx.send("You can only delete up to 100 messages at a time.")
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} messages have been deleted.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, new_nick: str):
    """Changes the nickname of a member."""
    try:
        await member.edit(nick=new_nick)
        await ctx.send(f"{member.mention}'s nickname has been changed to {new_nick}.")
    except Exception as e:
        await ctx.send(f"An error occurred while changing the nickname: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
    """Mutes a member for a specified amount of time."""
    muted_role = discord.utils.get(member.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await member.guild.create_role(name="Muted")
        for channel in member.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {duration} minutes.")
    await asyncio.sleep(duration * 60)
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")

@bot.command()
async def botinvite(ctx):
    """Generates an invite link for the bot."""
    await ctx.send(f'https://discord.com/oauth2/authorize?client_id=1219224957834498059&permissions=8&scope=bot')

@bot.command()
async def serverinfo(ctx):
    """Displays information about the server."""
    server = ctx.guild
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=server.name, inline=False)
    embed.add_field(name="Server ID", value=server.id, inline=False)
    embed.add_field(name="Owner", value=server.owner, inline=False)
    embed.add_field(name="Member Count", value=server.member_count, inline=False)
    embed.add_field(name="Creation Date", value=server.created_at.strftime("%B %d, %Y"), inline=False)
    await ctx.send(embed=embed)

    # Echo command
@bot.command()
async def echo(ctx, *, message: str):
    """Repeats the message sent by the user."""
    await ctx.send(message)

    # Roll command
@bot.command()
async def roll(ctx, start: int, end: int):
    """Generates a random number between two integers."""
    await ctx.send(f'{random.randint(start, end)}')


# -------------------------- Misc commands end here --------------------------- #



# -------------------------- AFK Commands starts here --------------------------- #
afk_users = {}

@bot.command()
async def afk(ctx, *, message=None):
    """Sets the AFK status with an optional message."""
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        await ctx.send('AFK status cleared.')
    else:
        if message is None:
            message = 'AFK'
        afk_users[ctx.author.id] = message
        if not any(user.mention in ctx.message.content for user in ctx.message.mentions):
            await ctx.send(f'AFK status set: {message}')

@bot.command()
async def unafk(ctx):
    """Clears the AFK status and sets the user's nickname to their default username."""
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        default_username = ctx.author.name
        try:
            await ctx.author.edit(nick=default_username)
            await ctx.send(f'{ctx.author.mention} is no longer AFK.')
        except discord.HTTPException:
            await ctx.send(f'{ctx.author.mention} is no longer AFK, but I was unable to change their nickname.')
    else:
        await ctx.send(f'{ctx.author.mention} is not currently AFK.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    afk_msg = get_afk_message(message.author)
    if afk_msg and not any(user.mention in message.content for user in message.mentions):
        await message.channel.send(f'{message.author.mention} is currently AFK. {afk_msg}')

def get_afk_message(user):
    if user.id in afk_users:
        return afk_users[user.id]
    else:
        return None

@bot.event
async def on_member_update(before, after):
    if before.nick and before.nick != after.nick:
        if after.id in afk_users:
            default_username = after.name
            await after.edit(nick=default_username)
            if before.guild.me.guild_permissions.manage_nicknames:
                await after.edit(nick=default_username)
                await before.guild.me.edit(nick=f"{bot.user.name} (AFK)")
        elif before.guild.me.guild_permissions.manage_nicknames:
            await before.guild.me.edit(nick=f"{bot.user.name} (AFK)")


# -------------------------- AFK Commands ends here --------------------------- #

# -------------------------- Userinfo Commands starts here --------------------------- #

@bot.command()
async def userinfo(ctx, user: discord.Member = None):
    """Displays information about the user who invoked the command."""
    if user is None:
        user = ctx.author
    embed = discord.Embed(title=f'{user.name}#{user.discriminator}', color=discord.Color.blue())
    embed.add_field(name='ID', value=user.id, inline=True)
    embed.add_field(name='Created At', value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    embed.add_field(name='Joined At', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    embed.add_field(name='Bot', value=user.bot, inline=True)
    await ctx.send(embed=embed)


# -------------------------- Userinfo Commands ends here --------------------------- #

# -------------------------- Ticket commands starts here --------------------------- #

async def notify_admin(channel, user, message_content):
    # Find an admin role or user to notify
    admin_role = discord.utils.get(channel.guild.roles, name="Admin")
    if admin_role:
        mention = admin_role.mention
    else:
        # If there's no admin role, mention the guild owner
        mention = channel.guild.owner.mention
    
    # Send a notification message to the admin
    notification_message = f"Hey {mention}, {user.mention} has created a {channel.mention}. The message by {user.mention}: {message_content}"
    await channel.send(notification_message)

@bot.command()
async def ticket(ctx, *, message: str):
    """Opens a ticket."""
    # Find or create the ticket channel
    ticket_channel = discord.utils.get(ctx.guild.channels, name="tickets")
    if not ticket_channel:
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True),  # User who created the ticket
        }
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True)  # Admin role
        else:
            # If there's no admin role, give read permissions to the guild owner
            overwrites[ctx.guild.owner] = discord.PermissionOverwrite(read_messages=True)
        
        ticket_channel = await ctx.guild.create_text_channel("tickets", overwrites=overwrites)
        await notify_admin(ticket_channel, ctx.author, message)  # Notify admin when channel is created
    
    # Send the ticket message to the ticket channel
    ticket_embed = discord.Embed(title="Ticket", description=message, color=discord.Color.gold())
    ticket_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    ticket_message = await ticket_channel.send(embed=ticket_embed)
    
    await ctx.send("Your ticket has been submitted. Staff will assist you shortly.")

# -------------------------- Ticket commands ends here --------------------------- #

# -------------------------- AutoMod commands starts here --------------------------- #

warnings = {}
keywords = []




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(keyword in message.content for keyword in keywords):
        if message.author.id in warnings:
            warnings[message.author.id] -= 1
            if warnings[message.author.id] == 0:
                embed = discord.Embed(title="Ban Notice", description=f"You have been banned from {message.guild.name} for 24 hours due to excessive use of restricted keywords.", color=0xFF0000)
                try:
                    await message.author.send(embed=embed)
                except discord.errors.Forbidden:
                    await message.channel.send(f'{message.author.mention}, you have been banned for 24 hours due to excessive use of restricted keywords. You will not receive a direct message notification.')
                await message.guild.ban(message.author, reason='Excessive use of restricted keywords', delete_message_days=0)
                del warnings[message.author.id]
                await message.channel.send(f'{message.author.mention} has been banned for 24 hours due to excessive use of restricted keywords.')
            else:
                await message.delete()
                await message.channel.send(f'{message.author.mention}, you have {warnings[message.author.id]} warnings left.')
        else:
            warnings[message.author.id] = 3
            await message.delete()
    else:
        if message.author.id in warnings:
            warnings[message.author.id] = 3

@bot.command()
@commands.has_permissions(manage_messages=True)
async def addkeyword(ctx, keyword: str):
    """Adds a keyword to the list of keywords to watch for."""
    if keyword not in keywords:
        keywords.append(keyword)
        await ctx.send(f"{keyword} has been added to the list of keywords to watch for.")
    else:
        await ctx.send(f"{keyword} is already in the list of keywords to watch for.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Keyword filtering
    if any(keyword in message.content for keyword in keywords):
        if message.author.id in warnings:
            warnings[message.author.id] -= 1
            if warnings[message.author.id] == 0:
                embed = discord.Embed(title="Ban Notice", description=f"You have been banned from {message.guild.name} for 24 hours due to excessive use of restricted keywords.", color=0xFF0000)
                try:
                    await message.author.send(embed=embed)
                except discord.errors.Forbidden:
                    await message.channel.send(f'{message.author.mention}, you have been banned for 24 hours due to excessive use of restricted keywords. You will not receive a direct message notification.')
                await message.guild.ban(message.author, reason='Excessive use of restricted keywords', delete_message_days=0)
                del warnings[message.author.id]
                await message.channel.send(f'{message.author.mention} has been banned for 24 hours due to excessive use of restricted keywords.')
            else:
                await message.delete()
                await message.channel.send(f'{message.author.mention}, you have {warnings[message.author.id]} warnings left.')
        else:
            warnings[message.author.id] = 3
            await message.delete()
    else:
        if message.author.id in warnings:
            warnings[message.author.id] = 3

    # Uppercase filtering
    if message.content.isupper():
        if message.author.id in warnings:
            warnings[message.author.id] -= 1
            if warnings[message.author.id] == 0:
                embed = discord.Embed(title="Ban Notice", description=f"You have been banned from {message.guild.name} for 24 hours due to excessive use of all capital letters.", color=0xFF0000)
                try:
                    await message.author.send(embed=embed)
                except discord.errors.Forbidden:
                    await message.channel.send(f'{message.author.mention}, you have been banned for 24 hours due to excessive use of all capital letters. You will not receive a direct message notification.')
                await message.guild.ban(message.author, reason='Excessive use of all capital letters', delete_message_days=0)
                del warnings[message.author.id]
                await message.channel.send(f'{message.author.mention} has been banned for 24 hours due to excessive use of all capital letters.')
            else:
                await message.channel.send(f'{message.author.mention}, you have {warnings[message.author.id]} warnings left.')
                await message.delete()
        else:
            warnings[message.author.id] = 3
    else:
        if message.author.id in warnings:
            warnings[message.author.id] = 3

    await bot.process_commands(message)



@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx, user: discord.Member):
    if user.id in warnings:
        del warnings[user.id]
        await ctx.send(f'{user.mention}\'s warnings have been reset.')
    else:
        await ctx.send(f'{user.mention} does not have any warnings.')


# -------------------------- AutoMod commands ends here --------------------------- #


bot.run(TOKEN)