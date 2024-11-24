A demo of Cosmos chains returning 0 power validators from CometBFT's `/validators` RPC endpoint.

For that purpose we connect to any chain from [Cosmos Directory](https://cosmos.directory/). 

For example to test the Cosmos Hub chain, run `python3 validators.py cosmoshub`. The script, [validators.py](./validators.py), 
repeatedly queries CometBFT's `/validators` endpoint for the (last 10) validators, keeps track of the first/last queried block in [cosmoshub.toml](./cosmoshub.toml),
and will accumulate reported 0-power validators with respective block numbers in [_cosmoshub_found.txt](./_cosmoshub_found.txt). The script will restart the process on any failures, or when manually restarted.
