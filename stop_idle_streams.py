from time import sleep
import requests
base = "http://localhost:5000"
from collections import defaultdict
def main():
    #timeout = args[1]
    timeout = 300
    max_strikes = 10
    streamstate = defaultdict(lambda: 0) # manages the streamid -> number of strikes mapping
    while True:
        streams = requests.get(base +"/streams/json").json()
        for streamid,stream in streams.items():
            state = stream['status']['state']
            listeners = stream['status'].get('listeners',-1)
            strikes = streamstate[streamid]
            if state == 'play' and listeners == 0:
                strikes = strikes + 1
                print(f"{streamid} is running but has no listeners, increasing strikes to {strikes}")
            else:
                print(f"{streamid} {state} {listeners}")
                strikes = 0

            if strikes >= max_strikes:
                print(f"{streamid} was idle for too long, stopping stream")
                requests.post(base + f"/stream/{streamid}/stop")

            streamstate[streamid] = strikes
        print(f"sleeping for {timeout} seconds")
        sleep(timeout)

if __name__ == "__main__":
    main()
