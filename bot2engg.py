import discord
import random
import asyncio
#from discord import app_commands
from discord.ext import commands
from discord import app_commands

with open('token.txt') as f:
    TOKEN = f.readline()


intents = discord.Intents.default()
intents.message_content = True
MY_SERVER = discord.Object(id=1105192418661380166)

client = commands.Bot(command_prefix='?', intents=intents)

client.countToggle = False
client.previousNum = 0


@app_commands.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 1081379977087426741:
        print("Waiting for sync...")
        await client.tree.sync()
        await interaction.response.send_message('Synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@app_commands.command(name='guessinggame', description='Guess what number I am thinking of')
async def guessinggame(interaction: discord.Interaction, arg1: int, arg2: int):
    await interaction.response.send_message(f'You wrote {arg1} and {arg2}')
     

@client.event 
async def on_message(message):

    await client.process_commands(message)

    #initialize previousID to something random if on the first count
    #make sure current and previous ID dont match, if it does, error
    #make sure that the number sent is the one we are looking for, if not, error
    #set a new previous user if the current user is not the bot
    #Have the bot send the next message if toggled on
       
    ###############COUNTING GAME###############
    if message.channel.id == 1105239862631735316 and message.content.isnumeric():
        
        if client.previousNum == 0: 
            client.prevUserID = message.author.id + 1
       
        if message.author.id != client.prevUserID:
           
            if int(message.content) == (client.previousNum + 1):
                await message.add_reaction("✅")
                client.previousNum = int(message.content)
                
                if message.author.id != client.user.id:
                    client.prevUserID = message.author.id

                    if client.countToggle:
                            nextNum = int(message.content) + 1
                            await message.channel.send(nextNum)
            else:
                await message.add_reaction("❌")
                await message.channel.send("NOOO! <@" + str(message.author.id) + "> RUINED IT AT **" + str(client.previousNum) + "**!!! 😭😭")
                await message.channel.send("Oh well, the next number is 1.")
                client.previousNum = 0
        else:
            await message.add_reaction("❌")
            await message.channel.send("NOOO! <@" + str(message.author.id) + "> RUINED IT AT **" + str(client.previousNum) + "**!!! 😭😭 **You can't count 2 numbers in a row**.")
            await message.channel.send("Oh well, the next number is 1.")
            client.previousNum = 0

    ###############GUESSING GAME###############
    if message.content.startswith('?guess'):

        endMessage = message.content.split(" ", 1)[1]
        guessNum =[int(i) for i in endMessage.split()]
                        

        if guessNum[0] > guessNum[1]:
            await message.channel.send("Oops, wrong format. Make sure there are 2 numbers separated by a space.")
        else:
            await message.channel.send(f'Guess a number between {guessNum[0]} and {guessNum[1]}')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(guessNum[0], guessNum[1])

        if guessNum[1] < 10:
                numGuesses = 3
        elif guessNum[1] < 50:
                numGuesses = 5
        elif guessNum[1] < 100:
                numGuesses = 7
        else:
            numGuesses = 10
        
        await message.channel.send(f'You have {numGuesses} guesses. Please make your first guess, and good luck.')
        
        guessesUsed = 1

        while True:
            if numGuesses == 0:
                await message.channel.send(f':sob: You ran out of guesses. The correct answer was {answer}.')
                break
            try:
                guess = await client.wait_for('message', check=is_correct, timeout=20.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')
            
            if int(guess.content) == answer:
                await guess.add_reaction("✅")
                return await message.channel.send(f'You are right! You guessed it in {guessesUsed} guess(es)!')
            else:
                if int(guess.content) > answer:
                    guessStatus = "high"
                elif int(guess.content) < answer:
                    guessStatus = "low"
                await guess.add_reaction("❌")
                numGuesses = numGuesses - 1
                await message.channel.send(f'Wrong. That guess was too {guessStatus}. You have {numGuesses} guesses remaining.')
                guessesUsed = guessesUsed + 1

@client.event
async def on_ready():
    print(f'Logged in as {client.user.display_name}')
    
'''@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(1107747501391482880)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "✅":
      Role = discord.utils.get(user.guild.roles, name="Foundations")
      if user.id != client.user.id:
        await user.add_roles(Role)'''

"""CLIENT COMMANDS BEGIN HERE"""
@client.command()
async def gpa(ctx, *args):
    ###############CALCULATES GPA###############
    message = args.join(" ")
    courseinfo = message.split(" ", 1)[1]
    gradepoints = []
    coursecred = 0
    coursearr = courseinfo.split(",")
    for course in coursearr:
        letterToGPA = 0
        specific = course.split()
        for letter in specific[1]:
            if letter == "D":
                    letterToGPA = 1.0
            elif letter == "C":
                    letterToGPA = 2.0
            elif letter == "B":
                    letterToGPA = 3.0
            elif letter == "A":
                    letterToGPA = 4.0
            elif letter == "+" and letterToGPA != 4.0:
                    letterToGPA += 0.3
            elif letter == "-":
                    letterToGPA -= 0.3
        gradepoints.append(letterToGPA*float(specific[0]))
        coursecred += float(specific[0])
    overallGPA = round(sum(gradepoints)/coursecred, 1)
        
    await message.channel.send("Your GPA is: "+ str(overallGPA))


@client.command()
#See when a user joins
async def joined(ctx, member: discord.Member):
    created_at = member.created_at.strftime("%b %d, %Y")
    await ctx.send(f'{member} joined at {created_at}.')

@client.command()
#generate random response
async def eightball(ctx, *args):
    for x in args:
        x.lower() 

    choice = random.randint(0,4)
    responses = ["I would say no", "Absolutely without a doubt", "I dunno why are you asking me", "Probably, yeah", "No please no"]
    blacklisted = ["ee", "electrical"]
    if ctx.author.id == 690668757068284004 and (blacklisted[0] in args or blacklisted[1] in args):
        await ctx.send("CompE > EE")
    else:
        await ctx.send(responses[choice])

@client.command()
#toggle the countforus option on in counting game
async def countforus(ctx):
    countToggleWord = ''
    if client.countToggle:
        client.countToggle = False
        countToggleWord = 'not '
    else:
        client.countToggle = True
        countToggleWord = ''
    await ctx.send('I will now ' + countToggleWord + 'count.')

@client.command()
#display commands
async def info(ctx):
    info = '''So far, here are my main commands that can be used:
- ?guess (num1) (num2), where num1 is lower than num2, and they are space-separated.
          - With this command, you can play a guessing game. Use the command a try it out!
- ?gpa (Course Units) (Letter Grade), (Course Units 2) (Letter Grade 2), ...
          - Calculates your GPA with as many course as you like (ex formatting: '?gpa 3.5 A+, 4.0 B+, 3.8 C+' etc)
- ?joined @user
          - Find out when a user joined the server! Please be mindful of pinging them...
- ?countforus
          - toggles on or off. If on, I will count one extra number after you
- ?eightball (your question here)
          - I am all knowing. I will answer every question you provide to me'''
    await ctx.send(info)

@client.command()
#sync client tree
async def sync(ctx):
    if ctx.message.author.id == 1081379977087426741:
        await client.tree.sync()
        await ctx.send("Client tree synced")
        print('synced')
    else:
        await ctx.send('Must be owner to use this command')


@client.command()
#display rules to server
async def display(ctx):
     if ctx.message.author.id == 1081379977087426741:
            descDisp = '''**Welcome to the B2E Discord! This is a place anyone can use to discuss the B2E program, ask questions, and get involved with student life! During your time in this discord, we ask you to follow a few rules to make sure everyone has a safe space and stays happy!**
    
    If you’re new to Discord, you might find this guide helpful: https://support.discord.com/hc/en-us/articles/360045138571-Beginner-s-Guide-to-Discord
    
    And if you don't know how to change your nickname, follow this handy guide here:  https://support.discord.com/hc/en-us/articles/219070107-Server-Nicknames

    __RULES__
    1) **Change your nickname on the server to your full name and pronouns**
    If your **preferred name differs from the name in our documents** - use your preferred name here and send either @afify (he/him) or @Simon M a message letting us know :)
    2) Be polite and mindful of other's feelings
    3) Respect pronouns and diversity
    4) Don't bully, harass or be toxic in general
    5) Keep the chat SFW (including profile pictures)
    6) Do not spam text or advertise
    7) Personal attacks will result in banning from server for a period of time or permanently, based on the situation

    __Academic Integrity Rules__
    Don't share exam materials, solutions to assignments, or any other materials that would give some students an unfair advantage. The university is very strict with these rules, and some will find it is much better just to receive the lower grade than to be faced with academic misconduct.

    Please react :white_check_mark: once you read the server rules AND changed your nickname to your real name & pronouns to access the other channels!

    If you've changed your nickname and you've paid for some B2E services - let us know by reacting :pencil: if you're in Academic Essentials and :camping: if you're in Engg Camp. We will then verify this and add you to your specific channels :)

    To enroll in academic essentials or engg camp: https://estore.engineering.ualberta.ca/b2e/'''
            embe = discord.Embed(title="RULES", description = descDisp, color=0x808080) 
            new_msg = await ctx.send(embed=embe)
            await new_msg.add_reaction("✅")
            await new_msg.add_reaction("📝")
            await new_msg.add_reaction("🏕️")

     
client.run(TOKEN)