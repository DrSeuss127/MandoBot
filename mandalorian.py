import discord
import random
import os
import json
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle

greet = ["hello", "Hi", "Hello", 'HELLO']
the_way = ["way", "Way", "WAY"]
the_child = ["child", "Child", "The Child"]
activity = ['Activity', 'activity', 'task', 'Task', 'PT']
TOKEN = "YOUR BOT'S TOKEN HERE"
owner_id = 'YOUR ID HERE'
# Hi!! This is a personal project by Clint#0764, you may use this freely.
# I made this bot with the inspiration from The Mandalorian series on Disney+.

intents = discord.Intents(messages = True, 
                          guilds = True, 
                          reactions = True, 
                          members = True
                         )


def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents = intents)
client.remove_command('help')
commandPrefix = client.command_prefix
changeStatus = cycle([f"{len(client.guilds)} servers", "you"])


@client.event
async def on_guild_join( guild):
    guildID = str(guild.id)
    # creates two roles, "Mandalore" for an admin permission, "Mando" for a role with regular perms
    """await guild.create_role( name = "Student",
                                permissions = mando,
                                color = discord.Color.blue(),
                                hoist = True,
                                mentionable = True
                              )
            
    await guild.create_role( name = "Professor/Teacher",
                             permissions = discord.Permissions(administrator = True),
                             color = discord.Color.orange(),
                             hoist = True,
                             mentionable = True
                           )"""
            
    # opens prefixes dictionary, adds the guild id of a server, then writes to the file
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[guildID] = '/'

    with open('prefixes.json', 'w') as file:
        prefixes = json.dump(prefixes, file, indent = 4)

    with open('serverraisehand.json', 'r') as a:
        serverRaiseHandDict = json.load(a)
            
    serverRaiseHandDict[guildID] = list()
            
    with open('serverraisehand.json', 'w') as a:
        serverRaiseHandDict = json.dump(serverRaiseHandDict, a, indent = 4)
            
    with open('serverquestions.json', 'r') as q:
        serverQDict = json.load(q)
            
    serverQDict[guildID] = list()

    with open('serverquestions.json', 'w') as q:
        json.dump(serverQDict, q, indent = 4)
        

@client.event
async def on_guild_remove( guild):

    guildID = str(guild.id)
    # opens prefixes dictionary, removes guild id of a server, then writes to the file
    with open('prefixes.json', 'r') as file:
                prefixes = json.load(file)
            
    prefixes.pop(guildID)

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent = 4)

    # opens serverraisehand dictionary, removes guild id of a server, then writes to the file
    with open('serverraisehand.json', 'r') as a:
        serverRaiseHandDict = json.load(a)
            
    serverRaiseHandDict.pop(guildID)

    with open('serverraisehand.json' ,'w') as a:
        json.dump(serverRaiseHandDict, a, indent = 4)
            
    with open('serverquestions.json', 'r') as q:
        serverQDict = json.load(q)
            
    serverQDict.pop(guildID)

    with open('serverquestions.json', 'w') as q:
        json.dump(serverQDict, q, indent = 4)

        

@tasks.loop(seconds = 20)
async def change_status():
    if len(client.guilds) > 1:
        await client.change_presence(activity = discord.Game(next(cycle([f"{len(client.guilds)} servers", "you"]))))
  
    if len(client.guilds) == 1:
        await client.change_presence(activity = discord.Game(next(cycle([f"{len(client.guilds)}servers", "you"]))))

    # displays the message "I'm ready. Logged in as <bot name>" in the command prompt/terminal.
@client.event
async def on_ready():
    print(f"I'm ready. Logged in as {client.user}")
    change_status.start()

@client.event
async def on_member_join( member):
    embed = discord.Embed( title = "A user has entered the server.",
                           description = f"Welcome, {member.mention}.",
                           color = member.author.color
                         )
    await discord.utils.get(client.get_all_channels(), name = 'general').send(embed = embed)
    print(f'{member} has joined the server {member.guild}.')

    if member.guild_permissions.administrator:
        theMandalore = get(member.guild.roles, name = "Mandalore")
        await member.add_roles(theMandalore)
    else:
        Mando = get(member.guild.roles, name = "Mando")
        regPotato = get(member.guild.roles, name = 'Regular Potatoes')
        await member.add_roles(regPotato)
        
@client.event
async def on_member_remove( member):
    embed = discord.Embed( title = "A user has left the server.",
                           description = f"Goodbye, {member.mention}.",
                           color = discord.Color(0xfcba03)
                        )
    await get(member.guild.get_all_channels(), name = 'general').send(embed = embed)
    print(f'{member} has left the server {member.guild}.')

# allows the bot to respond to certain keywords listed above.
@client.event
async def on_message(message): 

    for greeting in greet:
        if greeting in message.content:
            responses = ["Hi there!", "Hello.", "Greetings.", "Good day!"]
            if message.author == client.user:
                return
            await message.channel.send(f'{message.author.mention} {random.choice(responses)}')
            break

    for way in the_way:
        if way in message.content:
            if message.author == client.user:
                return
            await message.channel.send(f'{message.author.mention} This is the way.')
            break
            
    for child in the_child:
        if child in message.content:
            res = [
                    "Where is the Child?", 
                    "Where have you taken the Child?!", 
                    "I'm not leaving without the kid.",
                    "Travelling with me, that's no life for a kid."
                  ]
            if message.author == client.user:
                return
            await message.channel.send(f'{message.author.mention} {random.choice(res)}')
            
    for act in activity:
        if act in message.content:
            if message.author == client.user:
                return
                    
            await message.channel.send(f"@everyone, your Professor/Teacher has posted a new task!")
            await message.pin()
            break
            

@client.event
async def on_command_error(ctx, error):
            
    key = str(ctx.guild.id)
    with open('prefixes.json', 'r') as file:
        itemPairs = json.load(file)

    value = str(itemPairs[key])
        
   
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Error",
                              description = f"Command not found. Type {value}help for more information.",
                              color = discord.Color.red()
                             )


    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "Error",
                              description = f"A required argument is missing. Type {value}help for more information.",
                              color = discord.Color.red()
                             )
                       
                        
    if isinstance(error, commands.UserInputError):
        embed = discord.Embed(title = "Error",
                              description = f"User input is invalid. Type {value}help for more information.",
                              color = discord.Color.red()
                             )

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Error",
                              description = f"You do not have permission to use this command. Type {value}help for more information.",
                              color = discord.Color.red()
                             )
    await ctx.send(embed = embed)

# Kick command - removes the user from the discord guild/server
@client.command(aliases = ["Kick", "k"])
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
        
        embed = discord.Embed(
            title = "Kick",
            description = f'Kicked user {member.mention}',
            color = ctx.author.color
        )

        await member.kick(reason = reason)
        await ctx.send(embed = embed)
    
    # Ban command - removes the user and blocks future attempts to enter the discord guild/server
@client.command(aliases = ["Ban", "b"])
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):

    embed = discord.Embed(title = "Ban",
                          description = f'Banned user {member.mention}',
                          color = ctx.author.color
                         )

    await member.ban(reason = reason)
    await ctx.send(embed = embed)

    # Unban command - removes the user from the discord server's banned user list, and allows entry into the guild/server
@client.command(aliases = ["Unban", "ub"])
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    if ctx.author.guild_permissions.administrator or ctx.author.id == owner_id:
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                embed = discord.Embed(title = "",
                                      description = f'Unbanned user {member.mention}',
                                      color = ctx.author.color
                                     )

            await ctx.send(embed = embed)
            return

    # Clear command - removes messages in bulk, default value of removed messages is 10
@client.command(aliases = ["Clear", "cl"])
@commands.has_permissions(administrator = True)
async def clear( ctx, amount = 10):

    if ctx.author.guild_permissions.administrator or ctx.author.id == owner_id:
        await ctx.channel.purge(limit = amount)

        embed = discord.Embed(title = "Clear",
                              description = f'Removed {amount} messages.',
                              color = ctx.author.color
                             )

    await ctx.send(embed = embed)

@client.command(aliases = ['sd', 'off'])
@commands.has_permissions(administrator = True)
async def shutdown(ctx, *, message = None):
    embed = discord.Embed(title = "Shutdown",
                          description = 'Shutting down...',
                          color = ctx.author.color
                         )
                             
    id = str(ctx.author.id)
    if id == owner_id:
        await ctx.send(embed = embed)
        await ctx.message.delete()
        print(f'{client.user} is offline.')
        await ctx.bot.logout()

@client.command()
async def test(ctx, arg = None, arg2 = None):
    await ctx.send('You have sent {} and {}'.format(arg, arg2))

# Ping command - when initiated, the bot sends a message to the current text channel that a person is in and replies with their latency.
@client.command(aliases = ["Ping", "p"])
async def ping(ctx):

    embed = discord.Embed(title = "Ping!",
                          description = f'pong! your latency is {round(client.latency * 1000)}ms.',
                          color = ctx.author.color
                         )
    await ctx.send(embed = embed)

# 8ball command - when initiated, the bot displays your question, and its answer which is pulled from the responses listed below.
# the command is initiated in this format: <command prefix>8ball <question> or <command prefix>ask <question>
@client.command(aliases = ['8ball', 'ask'])
async def _8ball( ctx, *, question):
    responses = [
                'Try again.',
                "I don't know. Try again later.",
                "It is certain.",
                "Outlook good.",
                "You may rely on it.",
                "Ask again later.",
                "Concentrate and ask again.",
                "Reply hazy, try again.",
                "My sources say no.",
                "It is decidedly so",
                "Without a doubt.",
                "Yes, definitely.",
                "As I see it, yes.",
                "Most likely.",
                "Yes.",
                "Signs point to yes.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Better not tell you now",
                "Cannot predict now.",
                "Maybe." 
                ]
    embed = discord.Embed(title = "8ball",
                          description = f'Question: {question} \nAnswer: {random.choice(responses)}',
                          color = ctx.author.color
                         )
    await ctx.send(embed = embed)
    
@client.command(aliases = ['speak', 'talk', 'repeat'])
async def say(ctx, *, message = None):
    await ctx.send(message)
    await ctx.message.delete()
    
@client.command(aliases = ['Changeprefix', 'cp'])
async def changeprefix( ctx, newPrefix):

    key = str(ctx.guild.id) 
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
        
    keyList = str(prefixes.keys())
    value = str(prefixes[key])

    for key in keyList:

        prefixes[str(ctx.guild.id)] = newPrefix 

        if newPrefix in value:
            embed = discord.Embed(title = "Change Prefix - Error",
                                  description = f'The command prefix for this server is already set to "{newPrefix}". Please enter another command prefix.',
                                  color = discord.Color.red()
                                 )  

        elif newPrefix not in value:
            with open('prefixes.json', 'w') as file:
                prefixes = json.dump(prefixes, file, indent = 4)

            embed = discord.Embed(title = "Change Prefix",
                                  description = f'The command prefix for this server has been changed to "{newPrefix}"',
                                  color = ctx.author.color
                                 )
        await ctx.send(embed = embed)
        break
                

@client.command(pass_context = True, aliases = ['Help', 'h'])
async def help( ctx, *, arg = None):
        
    key = str(ctx.guild.id)
    with open('prefixes.json', 'r') as file:
        guildsDict = json.load(file)

    keyList = str(guildsDict.keys())
    value = str(guildsDict[key])

    if arg == None:

        embed = discord.Embed(title = "The Mandalorian - Help", description = "These are my commands.", color = ctx.author.color)

        embed.add_field(name = "\n\nHelp", value = f"Shows this menu, and a specific command's information.\n {value}Help, {value}help, {value}h <command>", inline = False)

        embed.add_field(name = "\n\nBan (Admin Only)", value = f"Removes a user from the server and prevents them from entering, unless unbanned.\n\nType {value}help ban for more information.")
    
        embed.add_field(name = '\n\nUnban (Admin Only)', value = f"Removes the banned status for a certain user that was banned.\n\nType {value}help unban for more information.")

        embed.add_field(name = '\n\nClear (Admin Only)', value = f"Removes messages in the current text channel.\n\nType {value}help clear for more information.")

        embed.add_field(name = '\n\nKick (Admin Only)', value = f"Removes a user from the server but does not prevent them from entering again.\n\nType {value}help kick for more information")
    
        embed.add_field(name = "\n\nShutdown (Bot Owner Only)", value = f"Turns off all bot processes.\n\nType {value}help shutdown for more information.")

        embed.add_field(name = "\n\nPing", value = f"Returns Pong! (user latency).\n\nType {value}help ping for more information." )
    
        embed.add_field(name = "\n\n8ball", value = f"Returns a random response for each question.\n\nType {value}help 8ball for more information.")
    
        embed.add_field(name = "\n\nSay", value = f"Repeats what the user says.\n\nType {value}help say for more information.")
                
        embed.add_field(name = "\n\nChange Prefix", value = f"Changes the command prefix of the bot for this server.\n\nType {value}help changeprefix for more information.")

        embed.add_field(name = "\n\nRaise Hand", value = f"Raises your hand.\n\nType {value}help raisehand for more information.")

        embed.add_field(name = "\n\nMove", value = f"Moves member/s to a voice channel. You can only move members to a voice channel if they are connected to a voice channel.\n\nType {value}help move for more information.")

        embed.add_field(name = "\n\nQuestion", value = f"Asks a question and displays the question/s by you and other users.\n\nType {value}help question for more information." )
        
    if arg == 'mute':
        embed = discord.Embed(title = 'Help - Mute (Admin Only)',
                              description = f' {value}Mute, {value}mute <@user#1234> or {value}Mute, {value}mute <all>',
                              color = ctx.author.color)
    
    if arg == 'unmute':
        embed = discord.Embed(title = 'Help - Unmute (Admin Only)',
                              description = f' {value}Unmute, {value}unmute <@user#1234> or {value}Unmute, {value}unmute <all>',
                              color = ctx.author.color)
    
    if arg == 'kick':
        embed = discord.Embed(title = 'Help - Kick (Admin Only)',
                              description = f' {value}Kick, {value}kick <@user#1234>',
                              color = ctx.author.color)
    
    if arg == 'ban':
        embed = discord.Embed(title = 'Help - Ban (Admin Only)',
                              description = f' {value}Ban, {value}ban <@user#1234>',
                              color = ctx.author.color)
    
    if arg == 'unban':
        embed = discord.Embed(title = 'Help - Unban (Admin Only)',
                              description = f' {value}Unban, {value}unban, {value}ub <@user#1234>',
                              color = ctx.author.color)
    if arg == 'move':
        embed = discord.Embed(title = 'Help - Move (Admin Only)',
                              description = f' {value}Move, {value}move <@user/all> <voice channel name>',
                              color = ctx.author.color)
    if arg == 'clear':
        embed = discord.Embed(title = 'Help - Clear (Admin Only)',
                              description = f' {value}Clear, {value}cl <insert amount of messages>',
                              color = ctx.author.color)

    if arg == 'raisehand':
        embed = discord.Embed(title = 'Help - Raise Hand',
                              description = f' {value}Raisehand, {value}rh (list/remove/remove all)',
                              color = ctx.author.color)
        
    if arg == 'say':
        embed = discord.Embed(title = 'Help - Say',
                              description = f' {value}say, {value}speak, {value}talk, {value}repeat <message>',
                              color = ctx.author.color)
    
    if arg == 'question':
        embed = discord.Embed(title = 'Help - Question',
                              description = f' {value}Question, {value}question (ask/list/next/clear)',
                              color = ctx.author.color)
                             
    if arg == 'changeprefix':
        embed = discord.Embed(title = 'Help - Change Prefix',
                              description = f' {value}Changeprefix, {value}cp <new command prefix>',
                              color = ctx.author.color)
        
    if arg == 'ping':
        embed = discord.Embed(title = 'Help - Ping',
                              description = f' {value}Ping, {value}ping, {value}p',
                              color = ctx.author.color)

    if arg == '8ball':
        embed = discord.Embed(title = 'Help - 8ball',
                              description = f" {value}_8ball, {value}8ball, {value}ask <question here>",
                              color = ctx.author.color)
        

    await ctx.send(embed = embed)
    
@client.command(aliases = ["Raisehand", "rh"])
async def raisehand( ctx, arg = None, arg2 = None):
    profRole = get(ctx.guild.roles, name = "Professor/Teacher")
    user = ctx.message.author.mention
    guildID = ctx.guild.id

    with open('prefixes.json', 'r') as file:
        serverPDict = json.load(file)
        
    value = serverPDict[str(guildID)]

    if arg == None and arg2 == None:

        with open('serverraisehand.json', 'r') as a:
            serverRHDict = json.load(a)

        values = serverRHDict.get(str(guildID))

        if f"{user}" in values:
            await ctx.send(f"{user} Hand already raised.") 
        else:
            serverRHDict[str(guildID)].append(f"{user}")
            with open('serverraisehand.json', 'w') as a:
                json.dump(serverRHDict, a, indent = 4)
            
        listValues = str(serverRHDict.get(str(guildID)))[1:-1]
        listValues = listValues.replace(",", "")
        listValues = listValues.replace("'", "")
        listValues = listValues.replace(" ", "\n")
        embed = discord.Embed( title = "Raised Hand/s",
                               description = str(listValues),
                               color = discord.Color(0xfcba03)
                             )
        await ctx.send(embed = embed)
        await ctx.message.add_reactions(":white_check_mark:")
        
    if arg == 'list' and arg2 == None:

        with open('serverraisehand.json', 'r') as a:
            serverRHDict = json.load(a)
            
        values = serverRHDict.get(str(guildID))
        if not values:
            embed = discord.Embed( title = "Raised Hand/s",
                                   description = "None",
                                   color = discord.Color(0xfcba03)
                                 )
        else:
            listValues = str(serverRHDict.get(str(guildID)))[1:-1]
            listValues = listValues.replace(",", "")
            listValues = listValues.replace("'", "")
            listValues = listValues.replace(" ", "\n")
            embed = discord.Embed( title = "Raised Hand/s",
                                   description = str(listValues),
                                   color = discord.Color(0xfcba03)
                                 )
        await ctx.send(embed = embed)
        
    if arg == 'remove' and arg2 == None:
        with open('serverraisehand.json', 'r') as a:
            serverRHDict = json.load(a)
            
        values = serverRHDict.get(str(guildID))

        serverRHDict[str(guildID)].remove(str(user))
        with open('serverraisehand.json', 'w') as a:
            json.dump(serverRHDict, a, indent = 4)
            
        if not values:
            embed = discord.Embed( title = "Raised Hand/s",
                                   description = "None",
                                   color = discord.Color(0xfcba03)
                                 )
        else:
            listValues = str(serverRHDict.get(str(guildID)))[1:-1]
            listValues = listValues.replace(",", "")
            listValues = listValues.replace("'", "")
            listValues = listValues.replace(" ", "\n")
            embed = discord.Embed( title = "Raised Hand/s",
                                   description = str(listValues),
                                   color = discord.Color(0xfcba03)
                                 )
        await ctx.send(embed = embed)
        
    if arg == 'remove' and arg2 == 'all':

        if ctx.message.author.guild_permissions.administrator:
            with open('serverraisehand.json', 'r') as a:
                serverRHDict = json.load(a)
                
            values = serverRHDict.get(str(guildID))

            if not values:
                embed = discord.Embed(title = "Raised Hand/s",
                                      description = "None",
                                      color = discord.Color(0xfcba03)
                                     )
                embed.set_footer(text = "The list is already empty.")
            else:
                serverRHDict[str(guildID)].clear()

                with open('serverraisehand.json', 'w') as a:
                    json.dump(serverRHDict, a, indent = 4)
                    
                embed = discord.Embed(title = "Raised Hand/s",
                                      description = "None",
                                      color = discord.Color(0xfcba03)
                                     )
            await ctx.send(embed = embed)
        else:
            await ctx.send(embed = discord.Embed(title = "Raise Hand - Error",
                                                 description = f"You do not have permission to use this command. Type {value}help for more information.",
                                                 color = discord.Color.red()
                                                )
                          )
@client.command(aliases = ['Question', 'q'])
async def question(ctx, arg = None, *, arg2 = None):
    user = ctx.message.author
    profRole = get(ctx.guild.roles, name = "Professor/Teacher")
    userpresent = False
    guildID = ctx.guild.id

    with open('serverquestions.json', 'r') as q:
        qDict = json.load(q)
    
    values = qDict[str(guildID)]

    if arg == "ask":
        for v in values:
            if v.startswith(f"{user.name}"):
                userpresent = True
            break
        
        if userpresent == True:
            await ctx.send('```Question/s```' +f'```{"".join(values)}```')
            await ctx.send(f"{user.name} already asked a question, you can only ask one question at a time. Question/s raised {profRole.mention}")
        else:
            values.append(f"{user.name}: {arg2}\n")
            with open('serverquestions.json', 'w') as q:
                json.dump(qDict, q, indent = 4)
            
            await ctx.send('```Question/s```' +f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {profRole.mention}")
    
    elif arg == "list" and arg2 == None:
        if not values:
            await ctx.send("```Question/s```" + "```None```")
        else:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {profRole.mention}")
    
    elif arg == "remove" and arg2 == None:
        for v in values:
            if v.startswith(str(user.name)):
                values.remove(v)
            break

        with open('serverquestions.json', 'w') as q:
            json.dump(qDict, q, indent = 4)
        
        if not values:
            await ctx.send('```Question/s```' + '```None```')
        else:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {profRole.mention}")
    
    elif arg == "remove" and arg2 == "all":
        if ctx.message.author.guild_permissions.administrator:
            if not values:
                await ctx.send('```Question/s```' + f'```None```' + 'The question list is empty.```')
            else:
                values.clear()

                with open('serverquestions.json', 'w') as q:
                    json.dump(qDict, q, indent = 4)
                
                await ctx.send('```Question/s```' + '```None```')
        
    else:
        raise commands.CommandError


@client.command(aliases = ["Move", 'mv'])
async def move( ctx, member: str, *, channel: discord.VoiceChannel):
    user = ctx.author
    guildID = str(ctx.guild.id)
    with open('prefixes.json', 'r') as file:
        serverDict = json.load(file)
    guildList = str(serverDict.keys())
    value = serverDict[guildID]

    if ctx.message.author.guild_permissions.administrator or user.id == owner_id:
        try:
            if member == "all":
                embed = discord.Embed(title = "Move",
                                      description = f"All users in {user.voice.channel.mention} moved to {channel.mention}",
                                      color = discord.Color.green()                
                                     )

                for voiceMember in user.voice.channel.members:
                    await voiceMember.move_to(channel)

                await ctx.send(embed = embed)
        
            else:
                member = member.replace("@","")
                member = member.replace("!","")
                member = member.replace("<","")
                member = member.replace(">","")
                member = ctx.guild.get_member(int(member))
                await member.move_to(channel)

                embed = discord.Embed(title = "Move",
                                      description = f"Moved user {member.mention} to {channel.mention}",
                                      color = discord.Color.green()                
                                     )
                await ctx.send(embed = embed)

        except:
            embed = discord.Embed(title = "Move",
                                  description = f"User {member.mention} is not in a voice channel."
                                                 "\nMoving members to a voice channel is only possible if they are in a voice channel and if the voice channel exists.",
                                  color = discord.Color.red()               
                                 )
            await ctx.send(embed = embed)
    else:
        await ctx.send(f"You do not have permission to use this command. Type {value}help for more information.")


client.run(TOKEN)                                    