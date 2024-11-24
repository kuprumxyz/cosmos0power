import requests
import toml
import sys

net = sys.argv[1]
print("Starting for chain: " + net)
req = requests.get('https://rpc.cosmos.directory/'+net+'/validators?page=1&per_page=1')
height = int(req.json()['result']['block_height'])
total = int(req.json()['result']['total'])
page = int((total-1) / 10 + 1)
print("Latest height: " + str(height))
print("Total validators: " + str(total))
print("Will request page: " + str(page))


config = "./" + net + ".toml"
found = "./_" + net + "_found.txt"

def process(height):
    res = requests.get('https://rpc.cosmos.directory/'+net+'/validators?height=' 
            + str(height) + '&page=' + str(page) + '&per_page=10').json()
    for v in res["result"]["validators"]:
        if int(v["voting_power"]) == 0:
            print(v)
            with open(found, 'a+') as f:
                print(height, "\n", v, file = f)

def read_config():
    try:
        with open(config, 'r') as f:
            data = toml.load(f)
    except FileNotFoundError:
        # first run
        data = {
            'first_block': height,
            'last_block': height-1
        }
    return data


while True:
    try:
        data = read_config()
        first = data['first_block']
        last = data['last_block']
        while last < height:
            last += 1
            print(last)
            process(last)
            data["last_block"] = last
            with open(config, 'w') as f:
                toml.dump(data, f)
            
        while True:
            first -= 1
            print(first)
            process(first)
            data["first_block"] = first
            with open(config, 'w') as f:
                toml.dump(data, f)
    except Exception:
        print("An error occurred; restarting...")
