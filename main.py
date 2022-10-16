import requests,json

cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|"

def gettingip(place,game):
    Data = {
    "placeId": place,
    "isTeleport": True,
    "gameId": game,
    "gameJoinAttemptId": game
    }
    Headers = {
        "Referer": f"https://www.roblox.com/games/{place}/",
        "Origin": "https://roblox.com",
        "User-Agent": "Roblox/WinInet",
        "Content-Type": "application/json"
        }
    x = requests.post(
        url="https://gamejoin.roblox.com/v1/join-game-instance",
        json=Data,
        headers=Header,
        cookies={".ROBLOSECURITY": cookie}
        ).json()
    if not x['joinScript']:
        return "Could not be obtained"
    Address = x['joinScript']['ServerConnections'][0]['Address']
    if "128.116" not in Address:
        Address = x['joinScript']['UdmuxEndpoints'][0]['Address']
    try:
        return f"{Address} {x['joinScript']['ServerConnections'][0]['Port']}"
    except:
        return "Could not be obtained"

def gettingservers(place):
    placename = requests.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place}",
                             cookies={".ROBLOSECURITY":cookie}).json()
    if not placename:
        return print("Invalid place id!")
    else:
        name = placename[0]['name']
    print(f"Getting servers for: {name}")
    request = requests.get(f"https://games.roblox.com/v1/games/{place}/servers/Public?limit=10").json()
    for a,i in enumerate(request['data']):
        z = gettingip(place,i['id'])
        try:
            print(f"Server {a+1} | Players: {i['playing']}/{i['maxPlayers']} | IP {z}")
        except:
            print(f"Server {a+1} | Data could not be obtained")
        

def gettinguniverse(place):
    x = requests.get(f"https://api.roblox.com/universes/get-universe-containing-place?placeid={place}").json()
    try:
        UniverseId = x['UniverseId']
    except:
        return print("Invalid place id!")
    zjson = requests.get("https://develop.roblox.com/v1/universes/"+str(UniverseId)+"/places?sortOrder=Asc&limit=100").json()
    print("Found {} places".format(len(zjson['data'])))
    for a,d in enumerate(zjson['data']):
        while True:
            serverlist = requests.get("https://games.roblox.com/v1/games/"+str(d['id'])+"/servers/Public??sortOrder=Asc&limit=10")
            if serverlist.status_code == 200:
              break
        serverlist = serverlist.json()
        if serverlist['data']:
          print("Place {}: ".format(a+1) + d['name']+" ("+str(d['id'])+")")
          for a,i in enumerate(serverlist['data']): 
            z = gettingip(d['id'],i['id'])
            try:
              print(f"Server {a+1} | Players: {i['playing']}/{i['maxPlayers']} | IP {z}")
            except:
              print(f"Server {a+1} | Data could not be obtained\n")

def gettingplayer(user):
    if not user.isdigit():
        data = {"Usernames":[user]}
        x = requests.post("https://users.roblox.com/v1/usernames/users",data=data).json()
        if not x['data']:
            return print("Invalid username")
        else:
            user = x['data'][0]['id']
    z = requests.get(
        f"https://api.roblox.com/users/{user}/onlinestatus/",
        cookies={".ROBLOSECURITY":cookie}).json()
    if "Playing" not in z['LastLocation']:
        return print(f"user is not playing a game!")
    elif z['LastLocation'] == "Playing":
        return print(f"User has their joins off.")
    elif not z['GameId']:
        return print(f"Can't join user's game - it might be grouplocked or a private server?")
    else:
        x =  gettingip(z['PlaceId'],z['GameId'])
        print(f"user is playing {z['LastLocation'][8:]} | IP {x}")
def main():
    while True:
        try:
            type = input("Enter 1 to get IPs for a place\nEnter 2 to get IPs for a universe\nEnter 3 to get IPs from a player's game\n")
            if type == "1":
                gettingservers(input("PlaceID: "))
            elif type == "2":
                gettinguniverse(input("PlaceID: "))
            elif type == "3":
                gettingplayer(input("Username/UserID: "))
            else:
                print("Invalid choice.")
        except Exception as e:
            print("An error occurred - please try again!")
main()
