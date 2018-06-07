import discord, os, urllib.request, json, calendar, sys, psutil, platform, asyncio

TOKEN = 'NDUxMzUwNzg2ODQxMTE2Njcy.DfAihg.MW25ysefWkbGK0Vv6RQc1gQ2Z_Q'

client = discord.Client()

def readFromFile(filename):
    file = open(str(filename), "r")
    data = file.read()
    file.close()
    return data

def removeUnnecessaryItems(data):
    count=0
    for everyData in data:
        if "\n" in everyData:
            data[count]=everyData[:-1]
        count=count+1
        return data
    
def readFile(filename):
    file = open(str(filename), "r")
    data = file.readlines()
    file.close()
    return data

@client.event
async def sendReplyAndWait(contentToSend):
    await client.send_message(discord.Object(id='443350352008577027'), content=(str(contentToSend)))
    messageName = await client.wait_for_message(timeout=300)
    return messageName

async def checkIfReplyReceived(messageName):
    try:
        editedMessage = ((messageName.content).lower()).replace(" ","")
        if "okay" in editedMessage:
            conditionAccepted=True
            await client.send_message(discord.Object(id='443350352008577027'), content=("Usage has been confirmed by " + (str(await client.get_user_info(messageName.author.id))[:-5])))
    except:
        await client.send_message(discord.Object(id='443350352008577027'), content=("Error hasn't been accepted!"))
        conditionAccepted=False
    return conditionAccepted

conditionAccepted=False
                              
async def checkUsageFile():
    global conditionAccepted
    data = removeUnnecessaryItems(readFile("OSStatus.txt"))
                              
    if conditionAccepted==False:
        checkWord=["CPU Usage", "RAM Usage", "Disk Usage"]
        word=0
        for everyTask in data:
            if (int(everyTask)>=75):
                messageName = await sendReplyAndWait(str(checkWord[word]) + " is " + str(data[word])+ "%. Send 'Okay' to confirm that you have seen this message")
                conditionAccepted = await checkIfReplyReceived(messageName)    
            word=word+1
    if conditionAccepted == True:
        await asyncio.sleep(1800)
        conditionAccepted=False

@client.event
async def on_message(message):
    async def determineUser():
        await client.send_message(message.channel, content="whose task? Please @ the user")
        msg = await client.wait_for_message(author=message.author)
        userToEdit = str(((msg.content)[2:])[:-1])
        try:
            userInfo = str(await client.get_user_info(int(userToEdit)))[:-5]
            return userToEdit
        except:
            await client.send_message(message.channel, content="User doesn't exist.")
    
    async def compileTaskAndSend(userToEdit, taskList):
        image=[]
        embed = discord.Embed(title=("List of current task for " + str(str(await client.get_user_info(int(userToEdit)))[:-5] + ":")), color=0xff0000)
        count=0
        for everyTask in taskList:
            count=count+1
            embed.add_field(name="Task " + str(count) + ":", value=(str(everyTask)) , inline=False)
            imageFormats = [".jpg",".png",".jpeg"]
            for everyFormat in imageFormats:
                if str(everyFormat) in everyTask:
                    imageLink = (everyTask.split(str(everyFormat))[0]).split(" ")[-1]
                    image.append(str(imageLink)+str(everyFormat))
        await client.send_message(message.channel, embed=embed)
        return image

    async def addTask(taskList, dictionary):
        await client.send_message(message.channel, content="What task will you like to add?")
        msgTask = await client.wait_for_message(author=message.author)
        taskList.append(msgTask.content)
        dictionary[userToEdit]=taskList
        await saveData()

    async def deleteTask(taskList):
        embed = discord.Embed(title=("List of current task for " + str(str(await client.get_user_info(int(userToEdit)))[:-5]) + ":"), color=0xff0000)
        count=0
        for everyTask in taskList:
            count=count+1
            embed.add_field(name="Task " + str(count) + ":", value=(str(everyTask) + "   - type " + str(count-1) + " to delete.") , inline=False)
        await client.send_message(message.channel, embed=embed)
        deleteNumber = await client.wait_for_message(author=message.author)
        del taskList[int(deleteNumber.content)]
        await saveData()

    async def saveData():
        with open('Name.txt', 'w') as outfile:
            json.dump(dictionary, outfile)
        await client.send_message(message.channel, content="Thank you, your command has been successfully completed.")

    async def embedData(title, arrayListName, arrayListValue):
        embed = discord.Embed(title=str(title), color=0xff0000)
        count=0
        for everyName in arrayListName:
            embed.add_field(name=str(everyName), value=str(arrayListValue[count]), inline=False)
            count=count+1
        await client.send_message(message.channel, embed=embed)

    async def NumberChecker(variableName, MinRange, MaxRange):
        try:
            variableName = int(variableName)
        except ValueError:
            conditionDefined="False"
            while (conditionDefined=="False"):
                try:
                    variableName = int(variableName)
                    conditionDefined = "True"
                except ValueError:
                    await client.send_message(message.channel, content="Only enter numbers between " + str(MinRange) + " to " + str(MaxRange))
                    await client.send_message(message.channel, content="Enter your number that you choose: ")
                    variableName = await client.wait_for_message(author=message.author)
        
        while ((variableName>MaxRange) or (variableName<MinRange)):
            await client.send_message(message.channel, content="Enter a number between " + str(MinRange) + " to " + str(MaxRange));
            await client.send_message(message.channel, content="Enter your number that you choose: ")
            variableName = await client.wait_for_message(author=message.author)
            while not(variableName.isnumeric()):
                await client.send_message(message.channel, content="Only enter numbers between " + str(MinRange) + " to " + str(MaxRange));
                await client.send_message(message.channel, content="Enter your number that you choose: ")
                variableName = await client.wait_for_message(author=message.author)
            variableName = int(variableName);
        return variableName;

    async def removeCommas():
        for x in range(0,len(dataFromFile)):
            newData = dataFromFile[x].replace(",","")
            for y in newData:
                withoutCommasArray.append(y)
        return withoutCommasArray

    async def splitIfMonthOrDays():
        blockOfData = []
        monthlyData = []
        for x in withoutCommasArray:
            try:
                blockOfData.append(int(x))
            except ValueError:
                if x == "!":
                    monthlyData.append(blockOfData)
                    blockOfData=[]
                if x == "\n":
                    dataInYear.append(monthlyData)
                    monthlyData=[]
        return dataInYear

    async def removeUnnecessaryItems():
        for everyMonth in dataInYear:
            for everyDay in everyMonth:
                for item in everyDay:
                    if item == "!":
                        del everyDay[everyDay.index("!")]
                    if item == "\n":
                        del everyDay[everyDay.index("\n")]
        return dataInYear

    
    dataFromFile=""
    withoutCommasArray = []
    dataInYear = []
    monthlyData = []
    
    if message.content.startswith("<@451350786841116672>"):
        actualMessage = (((message.content)[22:]).lower()).replace(" ","")
        
        if actualMessage=="viewtasks":
            userToEdit = await determineUser()
            dictionary = json.loads(str(readFromFile("Name.txt")))
            if userToEdit not in dictionary:
                await client.send_message(message.channel, content="Not in task member list hence no task for " + str(str(await client.get_user_info(int(userToEdit)))[:-5]) + ".")
            else:
                await client.send_message(message.channel, content="Member has been located in task list")
                image = await compileTaskAndSend(userToEdit, dictionary[userToEdit])
                for everyImage in image:
                    await client.send_message(message.channel, str(everyImage))

        if actualMessage == "edittasks":
            if (str(message.author.id)=="440477130837721088") or (str(message.author.id)=="336170734776877056"):
                userToEdit = await determineUser()
                dictionary = json.loads(str(readFromFile("Name.txt")))

                if userToEdit not in dictionary:
                    dictionary[userToEdit]=[]
                    await client.send_message(message.channel, content="Not in task member list. Creating a new list for " + str(str(await client.get_user_info(int(userToEdit)))[:-5]) + "... done.")
                else:
                    await client.send_message(message.channel, content="Member has been located in task list")
                    image = await compileTaskAndSend(userToEdit, dictionary[userToEdit])
                    for everyImage in image:
                        await client.send_message(message.channel, str(everyImage))

                await client.send_message(message.channel, content="would you like to add a new task or delete task?")

                arrayNameList = ["add a task", "delete a task"]
                arrayValueList = ["type 'add'", "type 'delete'"]
                await embedData("Choose an option: ", arrayNameList, arrayValueList)

                msgCommand = await client.wait_for_message(author=message.author)

                if str(msgCommand.content) == "add":
                    await addTask(dictionary[userToEdit], dictionary)

                if str(msgCommand.content) == "delete":
                    await deleteTask(dictionary[userToEdit])
            else:
                await client.send_message(message.channel, content="Access denied. Only for the big guys")

        if actualMessage=="btcprice":
            jsonBitcoinData = json.loads((urllib.request.urlopen(urllib.request.Request(str("https://api.coindesk.com/v1/bpi/currentprice.json"), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'})).read()))
            
            arrayNameList = ["Updated Time: ", "Data Produced by: ", ("BTC to " + str(jsonBitcoinData['bpi']['USD']['code']) + ": "), ("BTC to " + str(jsonBitcoinData['bpi']['EUR']['code']) + ": "), ("BTC to " + str(jsonBitcoinData['bpi']['GBP']['code']) + ": ")]
            arrayValueList = [("Updated  in UTC: " + str(jsonBitcoinData['time']['updated']) +  "\n" + "Updated in BST: " + str(jsonBitcoinData['time']['updateduk'])), jsonBitcoinData['disclaimer'],("1 BTC = $" + str(jsonBitcoinData['bpi']['USD']['rate_float'])), (jsonBitcoinData['bpi']['EUR']['rate_float']), ("1 BTC = £" + str(jsonBitcoinData['bpi']['GBP']['rate_float']))]
            await embedData(("Current " + jsonBitcoinData['chartName'] + " Price"), arrayNameList, arrayValueList)

        if actualMessage=="filelog":
            await client.send_message(message.channel, content="What year would you like to check? Enter in format (yyyy). ")
            yearToCheck = await NumberChecker((await client.wait_for_message(author=message.author)).content, 2017, 2018)
            file = open("checkYear.txt", "w")
            file.write(str(yearToCheck))
            file.close()
            await client.send_message(message.channel, content="Wait a few sec... Updating file...")
            os.system("python countFiles.py")
            await client.send_message(message.channel, content="Done :)")
            dataFromFile = readFile("storedData_2017.txt")
            withoutCommasArray = await removeCommas()
            dataInYear = await splitIfMonthOrDays()
            dataInYear = await removeUnnecessaryItems()
            await client.send_message(message.channel, content="What month would you like to check? Enter month number. ")
            monthToCheck = await NumberChecker((await client.wait_for_message(author=message.author)).content, 1, 12)
            await client.send_message(message.channel, content="What day would you like to check? Enter day number. ")
            dayToCheck = await NumberChecker((await client.wait_for_message(author=message.author)).content, 1, int(len(calendar.monthrange(yearToCheck, monthToCheck))))
            if str(0) in str(dataInYear[(int(monthToCheck)-1)][(int(dayToCheck)-1)]):
                await client.send_message(message.channel, content=("Not all files on " + str(dayToCheck) + " " + str(calendar.month_name[int(monthToCheck)]) + " " + str(yearToCheck)))
                embed = discord.Embed(title=str("List of Time of Missing Files: "), color=0x0000ff)
                count=0
                for everyFile in dataInYear[(int(monthToCheck)-1)][(int(dayToCheck)-1)]:
                    if str(0) == str(everyFile):
                        print(count%2)
                        if count%2 == 0:
                            hour = int(count/2)
                            minute = "00"
                        else:
                            hour = int((count-1)/2)
                            minute = "30"
                        embed.add_field(name=str(str(hour) + ":" + str(minute)) , value="Not Found", inline=False)        
                    count = count + 1
                    if count==24 or count==48:
                        await client.send_message(message.channel, embed=embed)
                        embed = discord.Embed(title=str("List of Time of Missing Files: "), color=0x0000ff)
            else:
                await client.send_message(message.channel, content="All files there")
                await client.send_message(message.channel, content="All files received on " + str(dayToCheck) + " " + str(calendar.month_name[int(monthToCheck)]) + " " + str(yearToCheck))

        if actualMessage=="computerstats":
            BytesPerGB = 1024 * 1024 * 1024
            system = str(platform.system())
            if system == "Windows":
                diskS = psutil.disk_usage('C:')
                diskSpace = psutil.disk_usage('E:')
                arrayNameList = ["Operating System:", "Operating System Architecture:", "CPU Name:", "Number of cores:", "CPU Usage Percent:", "Total Disk Space:", "Total Space Used:", "Total Available Space:", "Total Space Used (percent):", "Total memory:", "Available memory:", "Used memory:", "Used memory (percent):"]
                arrayValueList = [(str(platform.system())+"("+str(sys.platform)+")"), (str((platform.architecture())[0])), (str(platform.processor())), (str(psutil.cpu_count())), (str(psutil.cpu_percent())+"%"), ("%.2fGB" % float(((diskS.total)+(diskSpace.total))/BytesPerGB)), ("%.2fGB" % float(((diskS.used)+(diskSpace.used))/BytesPerGB)), ("%.2fGB" % float(((diskS.free)+(diskSpace.free))/BytesPerGB)), (str("%.2f" % float(((diskS.used)+(diskSpace.used))/((diskS.total)+(diskSpace.total))*100))+"%"), (str("%.2fGB" % float(psutil.virtual_memory()[0]/BytesPerGB))), ("%.2fGB" % float(psutil.virtual_memory()[1]/BytesPerGB)), (str("%.2fGB" % float(psutil.virtual_memory()[3]/BytesPerGB))), ("%.2f" % float(psutil.virtual_memory()[2])+"%")]
                await embedData("Current Computer Stats: ", arrayNameList, arrayValueList)
            elif (system == "Linux"):
                diskS = psutil.disk_usage('/')
                arrayNameList = ["Operating System:", "Operating System Architecture:", "CPU Name:", "Number of cores:", "CPU Usage Percent:", "Total Disk Space:", "Total Space Used:", "Total Available Space:", "Total Space Used (percent):", "Total memory:", "Available memory:", "Used memory:", "Used memory (percent):"]
                arrayValueList = [(str(platform.system())+"("+str(sys.platform)+")"), (str((platform.architecture())[0])), (str(platform.processor())), (str(psutil.cpu_count())), (str(psutil.cpu_percent())+"%"), ("%.2fGB" % float(((diskS.total))/BytesPerGB)), ("%.2fGB" % float(((diskS.used))/BytesPerGB)), ("%.2fGB" % float(((diskS.free))/BytesPerGB)), (str("%.2f" % float(((diskS.used))/((diskS.total))*100))+"%"), (str("%.2fGB" % float(psutil.virtual_memory()[0]/BytesPerGB))), ("%.2fGB" % float(psutil.virtual_memory()[1]/BytesPerGB)), (str("%.2fGB" % float(psutil.virtual_memory()[3]/BytesPerGB))), ("%.2f" % float(psutil.virtual_memory()[2])+"%")]
                await embedData("Current Computer Stats: ", arrayNameList, arrayValueList)
            else:
                await client.send_message(message.channel, content="Unable to determine stats due to unidentified operating system")

        if actualMessage=="help":
            arrayNameList = ["Bitcoin Rates in Euros, Pounds and dollars", "View tasks of members", "edit tasks of members (only accessible to admin and developer)", "Check if all file has been received", "Computer stats on which bot is running on"]
            arrayValueList = ["@Prime BTC Price", "@Prime view tasks", "@Prime edit tasks", "@Prime File Log", "@Prime computerstats"]
            await embedData("Choose an option: ", arrayNameList, arrayValueList)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='proto_lab'))
    print('Logged in as')
    print(client.user.name)
    print('------')
    #await client.send_message(discord.Object(id='443350352008577027'), content="Optimus Prime is online, at your service.")
    #await client.send_message(discord.Object(id='443350352008577027'), content="Going down for an hour for maintenance! Services will be unavailable")
    await checkUsageFile()
    while True:
        await asyncio.sleep(1)
        await checkUsageFile()
client.run(TOKEN)
