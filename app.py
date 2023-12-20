from instagrapi import Client
import json
import time
import getpass


login = False
session_id = None
username = None
password = None
totp = None

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

    if username is not None:
        try:
            cl = Client()
            cl.login(username, password, verification_code=totp)
        except Exception as e:
            print(e)
            pass

    try:
        user_id = cl.account_info().dict()["pk"]
        login = True
    except:
        print("---")
        
        session_id = input("session_id: ") or None

        if session_id is not None:
            continue

        username = input("username: ")
        password = getpass.getpass("password: ")
        totp = input("totp: ")

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

    unfollowers = list(set(followers_old) - set(followers_new))

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {len(followers_new)} ({-len(unfollowers)})")

    if len(unfollowers) > 0:
        for unfollower_id in unfollowers:
            try:
                unfollower_username = cl.username_from_user_id(unfollower_id)
            except Exception as e:
                print(e)
                continue

            try:
                """cl.user_unfollow(unfollower_id)"""
                unfollowed = True
            except Exception as e:
                print(e)
                unfollowed = False

            try:
                with open("unfollowers.txt", "a+") as f:
                    f.write(f"{unfollower_id}\n")
            except Exception as e:
                print(e)
                pass

            unfollower_url = f"https://instagram.com/{unfollower_username}/"

            if unfollowed:
                print(f"\033[01m\033[91m{unfollower_url}\033[00m")
            else:
                print(f"{unfollower_url}")

    try:
        with open("followers.txt", "w") as f:
            f.write("\n".join(followers_new))
    except Exception as e:
        print(e)
        break
