from instagrapi import Client
import datetime
import json
import os
import time


config_file = os.path.join(os.path.dirname(__file__), 'config.json')
cl = Client()

try:
    cl.load_settings(config_file)
except:
    pass

while True:
    try:
        user_id = cl.account_info().dict()['pk']
        user_name = cl.account_info().dict()['username']

        break
    except:
        session_id = input("session_id: ") or None

    try:
        cl.login_by_sessionid(session_id)
    except:
        print("login_failed!")
        print("---")

print(f"logged in as '{user_name}'")

try:
    cl.dump_settings(config_file)
except Exception as e:
    print(e)


followers_file = os.path.join(os.path.dirname(__file__), f"followers_{user_id}.txt")
unfollowers_file = os.path.join(os.path.dirname(__file__), f"unfollowers_{user_id}.txt")

followers_old = []

while True:
    print("---")

    try:
        while (time.time() - start_time) < 3600:
            time.sleep(1)
    except NameError:
        pass
    finally:
        start_time = time.time()


    try:
        followers = cl.user_followers(user_id, False)
        followers_new = [{'id': f, 'username': followers[f].username} for f in list(followers.keys())]
    except Exception as e:
        print(e)
        continue


    if len(followers_old) == 0:
        try:
            with open(followers_file) as f:
                followers_raw = f.read().splitlines()
        except:
            followers_raw = []
    
        if len(followers_raw) > 0:
            for follower in followers_raw:
                try:
                    (follower_id, follower_username) = follower.split('|')
                    followers_old.append({'id': follower_id, 'username': follower_username})
                except:
                    pass


    followers_out = [f"{f['id']}|{f['username']}" for f in followers_new]

    try:
        with open(followers_file, 'w') as f:
            f.write('\n'.join(followers_out))
    except Exception as e:
        print(e)


    followers_added = list(set([f['id'] for f in followers_new]) - set([f['id'] for f in followers_old]))
    followers_removed = list(set([f['id'] for f in followers_old]) - set([f['id'] for f in followers_new]))

    print(f"{datetime.datetime.now()}: {len(followers_new)} (\033[01m\033[92m{len(followers_added):+d}\033[00m/\033[01m\033[91m-{len(followers_removed)}\033[00m)")


    if len(followers_old) > 0:
            for follower_id in followers_added:
                try:
                    follower_username = [f for f in followers_new if f['id'] == follower_id][0]['username']

                    print(f"\033[01m\033[92mhttps://instagram.com/{follower_username}/\033[00m")
                except:
                    pass

            for follower_id in followers_removed:
                try:
                    follower_username = [f for f in followers_old if f['id'] == follower_id][0]['username']

                    print(f"\033[01m\033[91mhttps://instagram.com/{follower_username}/\033[00m")

                    with open(unfollowers_file, 'a+') as f:
                        f.write(f"{follower_id}|{follower_username}\n")
                except:
                    pass

    followers_old = followers_new
