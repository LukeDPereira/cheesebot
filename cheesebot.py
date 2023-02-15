import asyncio
import random
import discord
import datetime
import humanfriendly
from discord import app_commands
from discord import Embed
from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps
from itertools import cycle


# INTENTS (NEED TO LIST ALL MEMBERS)
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.


bot = commands.Bot(command_prefix = ';', intents=intents, help_command = None)



@bot.event			# Tells Discord that it's a event
async def on_ready():	# Important that the 
  						# name of the event is 
    					# "on_ready"
    print("Ready! MAKE SURE TO REMOVE CHEESERS ;removecheesers!!!!!!!!!!!!!!")		# Prints ready to the console
    status_swap.start() # starts swapping the status from the function status_swap
    #await guild.get_member(int(117666445529186307)).timeout(None)
    print(discord.__version__)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)



status = cycle(["Try the new Slash commands!", "/timeout"])
@tasks.loop(seconds=30)
async def status_swap():
    await bot.change_presence(activity=discord.Game(next(status)))

#test command to see if bots working
@bot.command()
async def hello (ctx):
    await ctx.send("Hello!") # .reply to reply to it


#starts loop to remove role from people who dont have the role and also give people who are supposed to have the role
#i couldve used an event listener to the audit log instead of a loop but i made this before the fact that i knew about it and the project is now over
@bot.command()
@commands.is_owner()
async def removecheesers(ctx, enabled = "start"):
    await ctx.message.delete()
    if enabled.lower() == "stop":
        removeallrole.stop()
    elif enabled.lower() == "start":
        print("STARTED")
        removeallrole.start(ctx)

#996160704216301680 is the role for cheese touch
@tasks.loop(seconds=2)
async def removeallrole (ctx): # loop through each person and loop through their roles to find a role and remove it
    with open ('cheesetouchowners.txt', 'r') as file: 
       currentcheesetoucher = int(file.readline().rsplit(':')[1].rsplit('\n')[0]) # the text file has their discord IDs because they cant change that while they can change their nickname/name
    await ctx.message.guild.get_member(int(currentcheesetoucher)).add_roles(discord.Object(996160704216301680), reason = "U CANT ESCAPE THE CHEESE  ", atomic = True) # ADDS CHEESE ROLE TO PERSON
    for i in ctx.message.guild.members: # i is the member 
        for role in i.roles: #check each role for each member
            if role.id == 996160704216301680 and i.id != currentcheesetoucher: # role id is the role of cheese to make sure its not assigned to the wrong person, if so remove it
                await i.remove_roles(discord.Object(996160704216301680), reason = "Not supposed to have cheese role", atomic = True) 



#command to give someone else the cheese touch, possible once every 5 mins per user
@bot.command()
@commands.cooldown(1,300, commands.BucketType.user)
async def transfercheese (ctx):
    with open ('cheesetouchowners.txt', 'r') as file: # get current cheese toucher id
                cheesetouchers =[]
                for line in file:
                    cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))
    cheeseholder = False
    if ctx.message.author.id == cheesetouchers[0] or ctx.message.author.id == 117666445529186307: # the or 117666445529186307 is if the owner of the bot does it to force it
    
        select = Select(options =[]) #creates an empty drop down selection bar
        members = []

        with open ('cheesetouchowners.txt', 'r') as file: # get cheese touch owner
            cheesetouchers =[]
            for line in file:
                cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))

        #get everyone whos playing (called players)
        with open ('players.txt', 'r') as file:
            players = []
            for line in file:
                players.append(int(line.rsplit('\n')[0]))

        # FOR SELECT DROPDOWN MEMBER LIST
        for i in ctx.message.guild.members: # i is the member
            if i.id not in cheesetouchers and i.id in players:
                select.add_option(label = str(i.display_name), value = str(i.id), description = str(i)) #if they arent apart of players (because dropdowns have a 25 selection limit we had to limit players, i just think dropdowns look cool so i added it)
                members.append(i)                                                                       #add their display name(nickname) and their actual discord name and add it to the members list we made 

        #this runs when they click on a selection in the drop down
        #this block of code is meant to have a 50/50 chance to actually transfer it but if the owner does it they will have a 100% chance ONLY when they dont have the cheese touch as
        #a way to force it to someone else incase they are annoyed or doing something.
        async def my_callback(interaction): # runs when they click a dropdown
            # IF LUKE DOES IT
            if interaction.user == ctx.message.guild.get_member(int(117666445529186307)) and interaction.user != ctx.message.guild.get_member(int(cheesetouchers[0])):
                print("ADMIN TRANSFER CHEESE") #prints to console so i can see
                print(interaction.user, " tried transferring it - ADMIN COMMAND")
                with open ('cheesetouchowners.txt', 'w') as file: #updates the latest three cheesetouchers in the file
                        file.write(f"Current cheese toucher:{select.values[0]}\n")
                        file.write(f"Previous cheese toucher:{cheesetouchers[0]}\n")
                        file.write(f"Second Previous cheese toucher:{cheesetouchers[1]}")

                await ctx.message.guild.get_member(int(select.values[0])).add_roles(discord.Object(996160704216301680), reason = "CHOSEN FOR CHEESE ROLE", atomic = True) # ADDS CHEESE ROLE TO NEW PERSON
                await ctx.message.guild.get_member(int(cheesetouchers[0])).remove_roles(discord.Object(996160704216301680), reason = "RELEASED FROM CHEESE ROLE", atomic = True) # REMOVES CHEESE ROLE TO NEW PERSON
                await interaction.response.send_message(f"You chose: {ctx.message.guild.get_member(int(select.values[0])).mention}, it worked!")

            #CHECK IF MESSAGE AUTHOR IS THE PERSON WHO DID THE INTERACTION
            #This is because people when the person who had cheesetouch used the command other people could still select the dropdown so check if it is the same person who called the command
            elif ctx.message.author == interaction.user:
                print(f"{interaction.user} tried transferring it to {ctx.message.guild.get_member(int(select.values[0]))} - NORMAL COMMAND")
                x = random.randint(1,2)
                print(x)
                if x >= 2:# 50/50 chance for it to work, if 2 it does if 1 it doesnt
                    with open ('cheesetouchowners.txt', 'w') as file: #update cheesetouch owners
                        file.write(f"Current cheese toucher:{select.values[0]}\n")
                        file.write(f"Previous cheese toucher:{cheesetouchers[0]}\n")
                        file.write(f"Second Previous cheese toucher:{cheesetouchers[1]}")

                    await ctx.message.guild.get_member(int(select.values[0])).add_roles(discord.Object(996160704216301680), reason = "CHOSEN FOR CHEESE ROLE", atomic = True) # ADDS CHEESE ROLE TO NEW PERSON
                    await ctx.message.guild.get_member(int(cheesetouchers[0])).remove_roles(discord.Object(996160704216301680), reason = "RELEASED FROM CHEESE ROLE", atomic = True) # REMOVES CHEESE ROLE TO NEW PERSON
                    await interaction.response.send_message(f"You chose: {ctx.message.guild.get_member(int(select.values[0])).mention}, it worked!")
                elif x <= 1:
                    await interaction.response.send_message(f"You chose: {ctx.message.guild.get_member(int(select.values[0])).mention}, it failed RIP")
                else:
                    await interaction.response.send_message(f"this code was never supposed to run")

                await message.delete() #deletes interaction message so no one can click on it again
           
            else:
                print(interaction.user, " tried transferring it - WHEN NOT CHEESE HOLDER") #console logs
                await interaction.response.send_message(f"You arent the cheeseholder!", ephemeral = True)


        #this is for the select dropdown to add all its properties
        #this happens before they select the dropdown, this is jsut to send the message
        select.callback = my_callback
        view = View()
        view.add_item(select)
        cheeseholder = True
        message = await ctx.send("Choose the person to transfer to, note that the previous 2 people cannot be chosen", view=view)
        message_id = message.id 

    #if they arent the actual cheese holder reset their cooldown, because it goes on a 5 min cooldown after using it
    if cheeseholder == False:
        await ctx.send("You arent the current cheese holder!")
        transfercheese.reset_cooldown(ctx)


#displays the last three cheese touch owners
@bot.command()
async def owners (ctx):
    with open ('cheesetouchowners.txt', 'r') as file:
        cheesetouchers =[]
        for line in file:
            cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))
    embed = discord.Embed(title = "CHEESE OWNERS")
    embed.add_field(name= "CURRENT CHEESE OWNER", value = ctx.message.guild.get_member(int(cheesetouchers[0])), inline = True)
    embed.add_field(name= "PREVIOUS CHEESE OWNER", value = ctx.message.guild.get_member(int(cheesetouchers[1])), inline = True)
    embed.add_field(name= "SECOND PREVIOUS CHEESE OWNER", value = ctx.message.guild.get_member(int(cheesetouchers[2])), inline = True)
    await ctx.send(embed=embed)

    
#this command was the incentive to give it away but also let people interact with the bot
#it let you "troll" people and annoy them, there was mute, deafen, disconnect, and change their nickname
@bot.command()
@commands.cooldown(1,300, commands.BucketType.guild)
async def trollcheese (ctx,*, arg = ""):
    count = []
    with open ('cheesetouchowners.txt', 'r') as file:
        cheesetouchers =[]
        for line in file:
            cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))
                
    await ctx.message.delete()

    if arg == "":
        print("no arguments, resetting cooldown")
        await ctx.send("refer to ;help trollcheese to see the proper syntax")
        trollcheese.reset_cooldown(ctx)
    elif arg == "mute":
        await ctx.message.guild.get_member(int(cheesetouchers[0])).edit(mute = True)
        print(ctx.message.author, " muted cheese holder")
    elif arg == "deafen":
        await ctx.message.guild.get_member(int(cheesetouchers[0])).edit(deafen = True)
        print(ctx.message.author, " deafened cheese holder")
    elif arg == "disconnect":
        await ctx.message.guild.get_member(int(cheesetouchers[0])).move_to(None)
        print(ctx.message.author, " disconnected cheese holder")
    elif arg.rsplit(' ')[0] == "nick":

        name = arg.split(' ', 1)[1]
        await ctx.message.guild.get_member(int(cheesetouchers[0])).edit(nick = name)
        print(f"{ctx.message.author} changed nick of cheese holder to {name}")


    #timeout had a vote system where 3 people needed to vote for it because otherwise it would be too annoying
    #it would just be once 3 people have voted for it time them out
    elif arg == "timeout": 
        print(ctx.message.author, " time out cheese holder") #the votes were written in a document incase i needed to update the code or it went offline it would be saved
        with open ('trollcheesecount.txt', 'r') as file:
                for line in file:
                    count.append(int(line.rsplit('\n')[0]))
        count[0] += 1
        # IF THEY HAVE ENOUGH VOTES
        if count[0] >= 3: 
            count[0] = 0
            with open ('cheesetouchowners.txt', 'r') as file:
                cheesetouchers =[]
                for line in file:
                    cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))
            with open ('trollcheesecount.txt', 'w') as file:
                file.write(str(count[0]))
            await ctx.message.guild.get_member(int(cheesetouchers[0])).timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds=60)) #times out user for 60 seconds
            await ctx.send("CHEESE HOLDER JUST GOT TIMED OUT FOR 5 MINS")

        #IF THEY DONT HAVE ENOUGH VOTES
        elif count[0] < 3:
            print("counting up")
            with open ('trollcheesecount.txt', 'w') as file:
                file.write(str(count[0]))
    else:
        print("invalid arguments, resetting cooldown")
        await ctx.send("refer to ;help trollcheese to see the proper syntax")
        trollcheese.reset_cooldown(ctx)
        
#checks how much votes till cheese holder is timed out        
@bot.command()
async def timeoutvotes(ctx):
    count = []
    await ctx.message.delete()
    with open ('trollcheesecount.txt', 'r') as file:
                for line in file:
                    count.append(int(line.rsplit('\n')[0]))
    await ctx.send(f"the vote to timeout the cheeseholder is {count[0]}/3")

#every 12 hours anyone in the server could "impeach" the cheeseholder incase they were never online or didnt want to give it away, to stop it from only being on one person
@bot.command()
@commands.cooldown(1,43200, commands.BucketType.guild)
async def impeach (ctx):
    if isinstance(ctx.message.channel, discord.Thread) == False: #checks if its not a thread but an actual channel
        members = []

        #GETS CHEESETOUCH OWNERS FROM TEXT FILE AND ADD IT INTO LIST (IDS ONLY)
        with open ('cheesetouchowners.txt', 'r') as file:
            cheesetouchers =[]
            for line in file:
                cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))

        #GETS PLAYERS FROM TEXT FILE (IDS) AND ADDS TO LIST (IDS ONLY)
        if ctx.message.author.id != cheesetouchers[0]:
            with open ('players.txt', 'r') as file:
                players = []
                for line in file:
                    players.append(int(line.rsplit('\n')[0]))

            # ADD TO ALL MEMBERS WHO ARE IN players TEXT FILE TO A LIST
            #the last 3 cheese touch owners cannot be chosen for impeach
            for i in ctx.message.guild.members: # i is the member
                if i.id not in cheesetouchers and i.id in players:
                    members.append(i.id)


            #picks a random person to give the cheese touch to
            x = random.randint(0,len(members) - 1)

            print(f"{ctx.author} transferred it to  {ctx.message.guild.get_member(int(members[x]))} - IMPEACH")
            with open ('cheesetouchowners.txt', 'w') as file:
                file.write(f"Current cheese toucher:{members[x]}\n")
                file.write(f"Previous cheese toucher:{cheesetouchers[0]}\n")
                file.write(f"Second Previous cheese toucher:{cheesetouchers[1]}")

            await ctx.message.guild.get_member(int(members[x])).add_roles(discord.Object(996160704216301680), reason = "CHOSEN FOR CHEESE ROLE", atomic = True) # ADDS CHEESE ROLE TO NEW PERSON
            await ctx.message.guild.get_member(int(cheesetouchers[0])).remove_roles(discord.Object(996160704216301680), reason = "IMPEACHED FROM CHEESE ROLE", atomic = True) # REMOVES CHEESE ROLE TO NEW PERSON
            await ctx.send(f"You impeached {ctx.message.guild.get_member(int(cheesetouchers[0])).mention} and {ctx.message.guild.get_member(int(members[x])).mention} got chosen!")
    
        else: #incase the current cheese toucher tries impeaching himself because he failed the 50/50 to transfercheese
            await ctx.send("You cant impeach yourself, that would be cheating")
            impeach.reset_cooldown(ctx)
    else:
        await ctx.send("This command is disabled in threads!")
        impeach.reset_cooldown(ctx)


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
# ADMIN COMMANDS
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

##############################################################################################################
#TIMEOUT SOMEONE
##############################################################################################################

#the checks for user.id in perms is to see if they have perms to use the admin commands if not, something bad will happen to them
@bot.tree.command(name="timeout", description = "for the worthy")
@app_commands.describe(member = "User to timeout", time_in_seconds = "The time to time them out for(in seconds)")
async def timeout(interaction, member: discord.Member, time_in_seconds: int):
    with open ('perms.txt', 'r') as file:
        perms =[]
        for line in file:
            perms.append(int(line))

    if  interaction.user.id in perms:
        await interaction.response.send_message(f"Successfully timed out `{member}` for `{time_in_seconds}` seconds", ephemeral = True)
        await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=int(time_in_seconds)), reason = "forcefully timed out by admins")
        await bot.get_channel(996155642492497961).send(f"`{interaction.user}` has forcetimed out `{member}` for `{time_in_seconds}` seconds")
        print(f"FORCE TIMEOUT HAPPENED FROM {interaction.user.name}")
    else:
        await interaction.response.send_message(f"You dont have access to this command! (btw you are timed out for as long as you tried to time out someone else if it is too long msg luke to remove it", ephemeral = True)
        await interaction.user.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=int(time_in_seconds)), reason = "timed out himself because he was not worthy")
        await bot.get_channel(996155642492497961).send(f" `{interaction.user}` timed out himself for `{time_in_seconds}`seconds rip bozo, he also tried to timeout {member}") #this is logs that get sent to a channel so everyone
                                                                                                                                                                              # in that channel gets to see who timed themselves out



##############################################################################################################
# UNTIMEOUT SOMEONE
##############################################################################################################
@bot.tree.command(name="untimeout", description = "for the worthy")
@app_commands.describe(member = "User to timeout")
async def untimeout(interaction, member: discord.Member):
    with open ('perms.txt', 'r') as file:
        perms =[]
        for line in file:
            perms.append(int(line))

    if  interaction.user.id in perms:
        await interaction.response.send_message(f"untimed out {member}", ephemeral = True)
        await member.timeout(None)
        await bot.get_channel(996155642492497961).send(f"untimed  out {member}")
    else:
        await interaction.response.send_message(f"You dont have access to this command!", ephemeral = True) # ephemeral = True means to send it to them in a message where only they can see


##############################################################################################################
#GIVE PERMS TO SOMEONE
##############################################################################################################
@bot.command(aliases = ['giveperms'])
@commands.is_owner()
async def addperms(ctx, member: discord.Member):
    with open ('perms.txt', 'a') as file:
         file.write(f"{str(member.id)}\n")
    await bot.get_channel(996155642492497961).send(f"given timeout perms to {member}")
##############################################################################################################
#REMOVE PERMS FROM SOMEONE
##############################################################################################################
@bot.command(aliases = ['ripperms', 'byeperms'])
@commands.is_owner()
async def removeperms(ctx, member: discord.Member):
    with open ('perms.txt', 'r') as file:
        perms =[]
        for line in file:
            perms.append(line)
    with open ('perms.txt', 'w') as file:
        for element in perms:
            if int(element) != member.id:
                file.write(element)
    await bot.get_channel(996155642492497961).send(f"taken timeout perms from {member}")

##############################################################################################################
#CHECK WHO HAS PERMS
##############################################################################################################
@bot.command(aliases = ['checkperms', 'whohasperms'])
@commands.is_owner()
async def perms(ctx):
    names = []
    with open ('perms.txt', 'r') as file:
        perms =[]
        for line in file:
            names.append(f'<@{int(line)}>')
    message = ""
    for name in names:
        message += name + "\n"

    embed = Embed(title = "Perms list", description = "The people who have perms to timeout are: ")
    embed.add_field(name = "Names", value = message, inline = False)
    await bot.get_channel(996155642492497961).send(embed=embed)





        



#########################################
# RESET COOLDOWN ON ANY COMMAND
#########################################
@bot.command(aliases = ['reset'])
@commands.is_owner()
async def reset_cooldown(ctx, member: discord.Member, command):
    ctx.author = member
    ctx.message.author = member
    
    bot.get_command(command).reset_cooldown(ctx)
    await bot.get_channel(996155642492497961).send(f"Reset cooldown {command} for {member}")
    print(f"Reset cooldown {command} for {member}")
    await ctx.message.delete()




#########################################
# HELP COMMAND
#########################################
@bot.command(name = "help", aliases = ['helpme'])
async def helpme (ctx, arg = ""):
    embed = discord.Embed(title = "HELP MENU")
    if arg == "":
        embed.add_field(name= "transfercheese", value = "transfers the cheese(only works if u have the cheese) \n(5 min cooldown)", inline = True)
        embed.add_field(name= "owners", value = "shows the 3 previous cheese owners", inline = True)
        embed.add_field(name = "trollcheese", value = "able to mess with cheese holder, \n ;help trollcheese for more info\n(5 min cooldown guild wide)", inline = True)
        embed.add_field(name= "timeoutvotes", value = "shows the amount of votes needed to timeout cheeseholder for 5 mins", inline = True)
        embed.add_field(name= "impeach", value = "transfers cheese without fail, the cheeseholder cannot impeach \n (12 hour cooldown guild wide)", inline = True)
    elif arg == "trollcheese":
        embed.add_field(name="trollcheese", value = "able to mess with cheese holder, the command can only be used once every 5 mins and there are 5 possible things to do:\n Mute, Deafen, Disconnect, Nick, Timeout\n to use nick use ;trollcheese nick (name you want)\n timeout is a bit different, it needs 5 votes to mute the holder for 5 mins \n for the rest use ;trollcheese mute/deafen/disconnect\n this command is done in secret (deletes your message automatically)", inline = True)

    await ctx.send(embed=embed)




#this command scrapes all the peoples messages in a channel that it was sent it to scrape all the data of messages that have emojis on it, to determine who has the highest emojis given and received, and for each emoji
#data was later sorted out in excel for convenience and it was easier
#the excel file already had the players names in the top row of excel sheet because i made code to put it there one time and deleted it after, probably should have commented it out but oh well
#this whole code block would make more sense while looking at the excel sheet given

@bot.command()
@commands.is_owner()
async def scrape(ctx):


    
    members = []
    wb = openpyxl.load_workbook("emotes.xlsx")
    sh1 = wb['Sheet1']
    with open ('cheesetouchowners.txt', 'r') as file:
                cheesetouchers =[]
                for line in file:
                    cheesetouchers.append(int(line.rsplit(':')[1].rsplit('\n')[0]))

#GETS PLAYERS FROM TEXT FILE (IDS) AND ADDS TO LIST (IDS ONLY)
    with open ('allplayers.txt', 'r') as file:
        allplayers = []
        for line in file:
            allplayers.append(int(line.rsplit('\n')[0]))

    # ADD TO ALL MEMBERS WHO ARE IN players TEXT FILE TO A LIST
    for i in ctx.message.guild.members: # i is the member
        if i.id in allplayers:
            members.append(i.name)
            #print(i.name)
            #print(type(i.name))
    rows = 0
    for max_row, row in enumerate(sh1, 1):            #this code is here because with openpyxl even if you clicked on an empty cell in like row 100,
        if not all(col.value is None for col in row): #it would count as that being the max row used, so we check the all the rows to see if they have None and if they dont add 1 to rows
            rows += 1

    #add all the row values and column values to an array
    rowvalues = []
    for i in range(1, rows + 1):
        rowvalues.append(sh1.cell(i,1).value)
    columnvalues = []
    for i in range(1, 25):
        columnvalues.append(sh1.cell(1,i).value)

    
    async for message in ctx.message.channel.history(limit=None): # get all messages in the channel ADD (limit=50) next to history if u want to limit it
        if message.author.bot == False and message.author.id in allplayers: #if the message isnt from a bot and they are apart of players
            #print(f"{message.content} ----- {message.reactions} ----- SENT BY {message.author}") #testing logs
            reactiontotal = 0
            for reaction in message.reactions: # go through all the reactions (incase there are multiple)
                users = [user async for user in reaction.users()] # add all reaction users to a list called users
                userlist = [i.name for i in users] # convert all users into users.name
                reactiontotal += reaction.count
                if(isinstance(reaction.emoji, str)): #this if and else statement is because some emojis were returned as strings (nmot emoji object) because they are deleted emojis and so 
                    emojiname = reaction.emoji       #you cant call emoji.name to a string object so that had to be done. otherwise just call emoji.name and assign it to emojiname variable
                else:
                    emojiname = reaction.emoji.name

                #print(reaction.emoji)
                #print(emojiname)
                #print(f"THE REACTION IS = {emojiname} AND THE COUNT IS = {reaction.count} THE MESSAGE AUTHOR IS {message.author} AND THE EMOJI GIVER IS {userlist} AND THE MESSAGE URL IS {message.jump_url} ") #reaction.emoji shows the emoji you type to send it in disc (dev version)
                #testing logs
                
                if emojiname + " given" not in rowvalues: #couldnt find so add a new row with emojiname + "received" and "given" and add one to the author and user
                    #print(f"{emojiname} ISNT IN THE ROW SO NOW ADDING IT TO EXCEL FILE CURRENTLY !!!!!!!!")
                    rows += 1
                    sh1.cell(row=rows, column=1, value = emojiname + " received") #add new row at the bottom called emojiname + received 
                    rowvalues.append(sh1.cell(rows,1).value)
                    rows += 1
                    sh1.cell(row=rows, column=1, value = emojiname + " given")
                    rowvalues.append(sh1.cell(rows,1).value)
                    for i in range(2,25): # FILL REST OF CELLS WITH 0's
                        sh1.cell(row=rows, column=i, value = 0) 
                        sh1.cell(row=rows - 1, column=i, value = 0)#since rows is at the given row which is the second row added go back a row and do the same for the received row

                
                rowcount = 1 # the row 
                for row in rowvalues: #for each row in the list check if the name equals the one we are on to find the row #
                    if emojiname + " received" == row:
                        columncount = 1
                        for column in columnvalues: #check if the author of the message is the same as the column we are checking
                            if str(message.author.name) == column: 

                                #these two if statements were for some stats i had pre placed, like highest singular emoji on a message 
                                #or highest emojis in total on a single message etc

                                if sh1.cell(row= 4,column= columncount).value < reaction.count: # CHECK FOR HIGHEST SINGULAR EMOJI COUNT
                                    sh1.cell(row = 4,column = columncount, value = reaction.count) # row 4 is highest emoji singular
                                    sh1.cell(row = 5,column = columncount, value = message.jump_url) # row 5 is message link for highest emoji singlular

                                if sh1.cell(row= 6,column= columncount).value < reactiontotal: # CHECK FOR HIGHEST MULTI EMOJI COUNT
                                    sh1.cell(row = 6,column = columncount, value = reactiontotal) # row 6 is highest emoji multple
                                    sh1.cell(row = 7,column = columncount, value = message.jump_url) # row 7 is message link for highest emoji multiple

                                    
                                sh1.cell(row = rowcount, column = columncount, value = sh1.cell(row = rowcount, column = columncount).value + reaction.count) #adds emoji count to whatever emoji they reacted with
                                sh1.cell(row = 2, column = columncount, value = sh1.cell(row = 2, column = columncount).value + reaction.count) #adds emoji count to the total emojis received stat


                            if column in userlist: #userlist is list of users that have reacted to it
                                #adds emoji count to whatever emoji they received in excel
                                sh1.cell(row = rowcount + 1, column = columncount, value = sh1.cell(row = rowcount + 1, column = columncount).value + 1)
                                #adds emoji count to total emoji count given (row 3)
                                sh1.cell(row = 3, column = columncount, value = sh1.cell(row = 3, column = columncount).value + 1)
                                    
                            columncount += 1
                    rowcount += 1
                    #updates column count and row count after

    wb.save("emotes.xlsx") #save excel sheet otherwise nothing would update
    print("saved")
    


#if they are on cooldown, send this message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Your on cooldown, wait {:.2f} seconds".format(error.retry_after)
        await ctx.send(msg)




    
bot.run('TOKEN HIDDEN')
