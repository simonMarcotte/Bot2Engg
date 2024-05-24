import discord
import random
import math
import asyncio
#from discord import app_commands
from discord.ext import commands
from discord import app_commands

with open('token.txt') as f:
    TOKEN = f.readline()


intents = discord.Intents.default()
intents.message_content = True
MY_SERVER = discord.Object(id=1105192418661380166)

COMMAND_PREFIX = 'b2e '

client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

client.countToggle = False
client.previousNum = 0

COUNTING_CHANNELS = [1105239862631735316]


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
    """Once a message is sent"""

    await client.process_commands(message)
 
    ###############COUNTING GAME###############
    if message.channel.id in COUNTING_CHANNELS and message.content.isnumeric():
        
        #initialize previousID to something random if on the first count
        if client.previousNum == 0: 
            client.prevUserID = message.author.id + 1

        #make sure current and previous ID dont match, if it does, error
        if message.author.id != client.prevUserID:
           
            #make sure that the number sent is the one we are looking for, if not, error
            if int(message.content) == (client.previousNum + 1):
                await message.add_reaction("✅")
                client.previousNum = int(message.content)
                
                #set a new previous user if the current user is not the bot
                if message.author.id != client.user.id:
                    client.prevUserID = message.author.id

                    #Have the bot send the next message if toggled on
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


@client.event
async def on_ready():
    """The bot is ready to recieve commands"""
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
###############GUESSING GAME###############
async def guess(ctx, *args):
    """
    GUESSING GAME
    Give the bot a range from a low to high number, and see if you can
    guess the number within the specified guesses!
    """

    low, high =[int(i) for i in args]
                    
    #Check format
    if low > high:
        await ctx.send("Oops, wrong format. Make sure there are 2 numbers separated by a space.")
    else:
        await ctx.send(f'Guess a number between {low} and {high}')

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(low, high)

    numGuesses = max(math.ceil(math.log2(high - low + 1)), 1)
    
    await ctx.send(f'You have {numGuesses} guesses. Please make your first guess, and good luck.')
    
    guessesUsed = 1

    while True:
        if numGuesses == 0:
            await ctx.send(f':sob: You ran out of guesses. The correct answer was **{answer}**.')
            break
        try:
            guess = await client.wait_for('message', check=is_correct, timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.send(f':hourglass: Sorry, you took too long, the answer was **{answer}**.')
        
        if int(guess.content) == answer:
            await guess.add_reaction("✅")
            return await ctx.send(f':partying_face: Correct! You guessed it in {guessesUsed} guess(es)!')
        else:
            if int(guess.content) > answer:
                guessStatus = "high"
            elif int(guess.content) < answer:
                guessStatus = "low"
            await guess.add_reaction("❌")
            numGuesses = numGuesses - 1
            await ctx.send(f':exclamation: Wrong! That guess was too {guessStatus}. You have {numGuesses} guesses remaining.')
            guessesUsed = guessesUsed + 1


@client.command()
async def gpa(ctx, *args):
    """Calculates GPA based off course units and letter grades"""
    
    course_info = " ".join(args)
    coursearr = course_info.split(",")
   
    gradepoints = []
    total_units = 0
    grades = {"F": 1.0, "D": 1.0, "C": 2.0, "B": 3.0, "A": 4.0, "-": -0.3, "+": 0.3}

    for course in coursearr:
        units, letter_grade = course.split()
        for letter in letter_grade:
            gradepoints.append(grades[letter]*float(units))
        total_units += float(units)
    overallGPA = round(sum(gradepoints)/total_units, 2)
        
    await ctx.send("Your GPA is: "+ str(overallGPA))


@client.command()
async def joined(ctx, member: discord.Member):
    """See when a user joins discord"""
    created_at = member.created_at.strftime("%b %d, %Y")
    await ctx.send(f'{member} joined at {created_at}.')

@client.command()
#generate random response
async def eightball(ctx, *args):
    """
    Generates random response for a given questions
    Upholds CompE vs EE battle within responses
    """

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
async def countforus(ctx):
    """toggle the countforus option on in counting game"""
    countToggleWord = ''
    if client.countToggle:
        client.countToggle = False
        countToggleWord = 'not '
    else:
        client.countToggle = True
        countToggleWord = ''
    await ctx.send('I will now ' + countToggleWord + 'count.')

@client.command()
async def info(ctx):
    """display commands"""
    info = f'''So far, here are my main commands that can be used:
- {COMMAND_PREFIX}guess (num1) (num2), where num1 is lower than num2, and they are space-separated.
          - With this command, you can play a guessing game. Use the command a try it out!
- {COMMAND_PREFIX}gpa (Course Units) (Letter Grade), (Course Units 2) (Letter Grade 2), ...
          - Calculates your GPA with as many course as you like (ex formatting: '?gpa 3.5 A+, 4.0 B+, 3.8 C+' etc)
- {COMMAND_PREFIX}joined @user
          - Find out when a user joined the server! Please be mindful of pinging them...
- {COMMAND_PREFIX}countforus
          - toggles on or off. If on, I will count one extra number after you
- {COMMAND_PREFIX}eightball (your question here)
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
async def display(ctx):
    """display rules to server"""
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
    else:
        ctx.send("Not so fast! This command is for Admin only.")

     
client.run(TOKEN)