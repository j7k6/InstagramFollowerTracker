from instagrapi import Client
import json
import time


login = False
session_id = None

while login is False:
    try:
        with open("config.json", "r") as c:
            cl = Client(json.load(c))
    except:
        pass

    if session_id is not None:
        try:
            cl = Client()
            cl.login_by_sessionid(session_id)
        except Exception as e:
            print(e)
            pass

    try:
        user_id = cl.account_info().dict()["pk"]
        login = True
    except:
        print("---")
        
        session_id = input("session_id: ") or None

try:
    with open("config.json", "w") as c:
        json.dump(cl.get_settings(), c)
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

    try:
        followers = cl.user_followers(user_id, False)
        followers_new = list(followers.keys())
    except Exception as e:
        print(e)
        continue

    try:
        with open("followers.txt") as f:
            followers_old = f.read().split("\n")
    except FileNotFoundError:
        followers_old = []
    except Exception as e:
        print(e)
        break

    followers_added = list(set(followers_new) - set(followers_old))
    followers_removed = list(set(followers_old) - set(followers_new))

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {len(followers_new)} (\033[01m\033[92m{len(followers_added):+d}\033[00m/\033[01m\033[91m-{len(followers_removed)}\033[00m)")

    if len(followers_added) > 0:
        for user_id in followers_added:
            try:
                user_name = cl.username_from_user_id(user_id)
            except Exception as e:
                print(e)
                continue

            print(f"\033[01m\033[92mhttps://instagram.com/{user_name}/\033[00m")

    if len(followers_removed) > 0:
        for user_id in followers_removed:
            try:
                user_name = cl.username_from_user_id(user_id)
            except Exception as e:
                print(e)
                continue

            try:
                with open("unfollowers.txt", "a+") as f:
                    f.write(f"{user_id}\n")
            except Exception as e:
                print(e)
                pass

            print(f"\033[01m\033[91mhttps://instagram.com/{user_name}/\033[00m")

    try:
        with open("followers.txt", "w") as f:
            f.write("\n".join(followers_new))
    except Exception as e:
        print(e)
        break
