# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                       #
#					Code Bye Trappi						# 
#														# 
#														# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import discord
import random
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio
import datetime

bot = commands.Bot(command_prefix = "?", description = "Bot de Trappi")

#démarage
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Streaming(name='In development | ?help', url = "https://www.twitch.tv/ytrappi"))
	print("---------------------------")
	currentDT = datetime.datetime.now()
	print(currentDT)
	print("Ready !")
	print("--------------------------")

#test say
@bot.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))

#Traduction
@bot.command()
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

#clear
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
	message = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in message:
		await message.delete()

#mute
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

#unmute
@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

#kick
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
	await ctx.guild.kick(user, reason = reason)
	embed = discord.Embed(title = "**Expulsion**", description = "Un modérateur a frappé !", color=0xfa8072)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url = "https://o1.llb.be/image/thumb/56d959703570e6ca6b0da009.jpg")
	embed.add_field(name = "Membre expulsé", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	await ctx.send(embed = embed)

#Session
@bot.command()
@commands.has_permissions(ban_members = True)
async def session(ctx):
	await ctx.send("Envoyez **l'heure** de votre session")
	def checkMessage(message):
		return message.author == ctx.message.author and ctx.message.channel == message.channel

	try:
		recette = await bot.wait_for("message", timeout = 10, check = checkMessage)
	except:
		await ctx.send("Veuillez réitérer la commande.")
		return
	message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
	await message.add_reaction("✅")
	await message.add_reaction("❌")


	def checkEmoji(reaction, user):
		return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

	try:
		reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
		if reaction.emoji == "✅":
			await message.delete()
			embed = discord.Embed(title = "**Session Programmé**", description = "La session a bien été créé, Coché la réaction qui vous convient pour savoir si vous allez être là oui ou non, puis rendez-vous dans le salon vocal Lobby en attendant les autres joueurs !", color=0xc80e0e)
			embed.set_author(name = ctx.author.name)
			embed.set_thumbnail(url = "https://www.mvps.net/docs/wp-content/uploads/2019/07/go.jpg")
			embed.add_field(name = "✅ si vous serai là", value=".", inline=False)
			embed.add_field(name = "❌ si vous ne serai pas là ", value=". ", inline=False)
			embed.add_field(name = "⏲ si vous serai en retard", value=". ", inline=False)
			await ctx.send(embed = embed)
			message = await ctx.send(f"**__Ici:__**")
			await message.add_reaction("✅")
			await message.add_reaction("❌")
			await message.add_reaction("⏲")
		else:
			await ctx.send("La session a bien été annulé ✅")
	except:
		await ctx.send("La session a bien été annulé ✅")


#unban
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à bien été unban :white_check_mark:")
			return
	await ctx.send(f"L'utilisateur **{user}** ne se trouve pas dans la liste des joeurs bannis :x:")

#ban
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
	await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", color=0xfa8072)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url = "https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif?itemid=12646581")
	embed.add_field(name = "Membre banni", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	await ctx.send(embed = embed)
	await ctx.send ("https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif?itemid=12646581")

#test
@bot.command()
async def test(ctx):
	message3 = f"```Je suis ton père```"
	await ctx.send(message3)

#test2
@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")

@bot.command()
async def bienvenue(ctx):
    message2 = f"**Bonjour mon amis !** \nTe voilà sur le server de Dodo \nIci tu pourras **discuter** avec des personne pour pouvoir faire connaissance, \nSi tu souhaite inviter des personne copie cet invite et envoyer là a tout tes **amis !** \nhttps://discord.gg/fHbEWSSKr9"
    await ctx.send(message2)

#info server
@bot.command()
@commands.has_permissions(administrator = True)
async def serverinfo(ctx):
    server = ctx.guild
    TextChannels = len(server.text_channels)
    VoiceChannels = len(server.voice_channels)
    DescriptionServer = server.description
    NombrePerson = server.member_count
    ServerNom = server.name
    message = f"**Bonjour Mon amis !** \nLe server s'appelle: *{ServerNom}*. \nLe server contient {NombrePerson} personnes. \nLa description du server est: {DescriptionServer}. \nCe server possède {TextChannels} salon textuels. \nCe server possède {VoiceChannels} salon vocaux"
    await ctx.send(message)

bot.run ("Njg3MDE3NTYwNjQ2MjIxODQ1.Xmfo9g.dErARmplURnqvcwoheElsWxNkKY")
