from instagrapi import Client
import json
import time

cl = Client()

try:
    cl.load_settings('config.json')
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
    cl.dump_settings('config.json')
except Exception as e:
    print(e)


while True:
    print("---")

    try:
        while (time.time() - start_time) < 3600:
            time.sleep(10)
    except NameError:
        pass
    finally:
        start_time = time.time()


    followers_new = []

    try:
        followers = cl.user_followers(user_id, False)

        for follower_id in list(followers.keys()):
            followers_new.append({'id': follower_id, 'username': followers[follower_id].username})

        assert len(followers) > 0
    except Exception as e:
        print(e)
        continue


    followers_old = []

    try:
        with open(f"followers_{user_id}.txt") as f:
            followers_raw = f.read().splitlines()
    except:
        pass

    try:
        for follower in followers_raw:
            (follower_id, follower_username) = follower.split('|')
            followers_old.append({'id': follower_id, 'username': follower_username})
    except:
        followers_old = []


    followers_out = []

    try:
        with open(f"followers_{user_id}.txt", "w") as f:
            for follower in followers_new:
                followers_out.append(f"{follower['id']}|{follower['username']}")

            f.write('\n'.join(followers_out))
    except Exception as e:
        print(e)
        break


    followers_added = list(set([f['id'] for f in followers_new]) - set([f['id'] for f in followers_old]))

    followers_removed = list(set([f['id'] for f in followers_old]) - set([f['id'] for f in followers_new]))

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {len(followers_new)} (\033[01m\033[92m{len(followers_added):+d}\033[00m/\033[01m\033[91m-{len(followers_removed)}\033[00m)")


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

                    with open(f"unfollowers_{user_id}.txt", "a+") as f:
                        f.write(f"{follower_id}|{follower_username}\n")
                except:
                    pass
