from config import MAP_API_KEY

print("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=phare&inputtype=textquery&fields=formatted_address,name,geometry&locationbias=circle:2000000@47.0359,2.7868&key=" + MAP_API_KEY)
