#!/usr/bin/env python3
# This Python file uses the following encoding:utf-8

# ===== #
#
# ▀█████████▄     ▄████████         Websites: HackingPassion.com | Bullseye0.com
#   ███    ███   ███    ███         Author: Jolanda de Koff | Bulls Eye
#   ███    ███   ███    █▀          GitHub: https://github.com/BullsEye0
#  ▄███▄▄▄██▀   ▄███▄▄▄             linkedin: https://www.linkedin.com/in/jolandadekoff
# ▀▀███▀▀▀██▄  ▀▀███▀▀▀             Facebook Group: https://www.facebook.com/groups/hack.passion/
#   ███    ██▄   ███    █▄          Facebook: https://www.facebook.com/profile.php?id=100069546190609
#   ███    ███   ███    ███         Twitter: https://twitter.com/bulls__eye
# ▄█████████▀    ██████████         LBRY: https://lbry.tv/$/invite/@hackingpassion:9
#
#          Bulls Eye..!
# ===== #

# Shodan Eye v1.2.0 Created April - August 2019
# Shodan Eye v1.3.0 December 2019
# Copyright (c) 2019 - 2025 Jolanda de Koff.

# Your Shodan API Key can be found here: https://account.shodan.io

########################################################################

# A notice to all nerds and n00bs...
# If you will copy the developer's work it will not make you a hacker..!
# Respect all developers, we doing this because it's fun...

########################################################################


import getpass
import os
import random
import re
import shodan
import sys

# Shodan Eye v1.3.0

banner1 = ("""

\033[1;31m

  ██████ ██░ ██ ▒█████ ▓█████▄ ▄▄▄      ███▄    █    ▓████▓██   ██▓█████
▒██    ▒▓██░ ██▒██▒  ██▒██▀ ██▒████▄    ██ ▀█   █    ▓█   ▀▒██  ██▓█   ▀
░ ▓██▄  ▒██▀▀██▒██░  ██░██   █▒██  ▀█▄ ▓██  ▀█ ██▒   ▒███   ▒██ ██▒███
  ▒   ██░▓█ ░██▒██   ██░▓█▄  █░██▄▄▄▄██▓██▒  ▐▌██▒   ▒▓█  ▄ ░ ▐██▓▒▓█  ▄
▒██████▒░▓█▒░██░ ████▓▒░▒████▓ ▓█   ▓██▒██░   ▓██░   ░▒████▒░ ██▒▓░▒████▒
▒ ▒▓▒ ▒ ░▒ ░░▒░░ ▒░▒░▒░ ▒▒▓  ▒ ▒▒   ▓▒█░ ▒░   ▒ ▒    ░░ ▒░ ░ ██▒▒▒░░ ▒░ ░
░ ░▒  ░ ░▒ ░▒░ ░ ░ ▒ ▒░ ░ ▒  ▒  ▒   ▒▒ ░ ░░   ░ ▒░    ░ ░  ▓██ ░▒░ ░ ░  ░
░  ░  ░  ░  ░░ ░ ░ ░ ▒  ░ ░  ░  ░   ▒     ░   ░ ░       ░  ▒ ▒ ░░    ░
      ░  ░  ░  ░   ░ ░    ░         ░  ░        ░       ░  ░ ░       ░  ░
                        ░                                  ░ ░  v1.3.0

\033[1;m
            \033[1;31mShodan Eye v1.3.0\033[0m

    ✓ The author is not responsible for any damage, misuse of the information.
    ✓ Shodan Eye shall only be used to expand knowledge and not for
      causing malicious or damaging attacks.
    ✓ Just remember, Performing any hacks without written permission is illegal ..!

            Author:  Jolanda de Koff Bulls Eye
            Github:  https://github.com/BullsEye0
            Website: https://HackingPassion.com
            Patreon: https://www.patreon.com/jolandadekoff

            \033[1;31mHi there, Shall we play a game..?\033[0m 😃
        """)

banner2 = ("""

\033[1;31m


   ▄▄▄▄▄    ▄  █ ████▄ ██▄   ██      ▄       ▄███▄ ▀▄    ▄ ▄███▄
  █     ▀▄ █   █ █   █ █  █  █ █      █      █▀   ▀  █  █  █▀   ▀
▄  ▀▀▀▀▄   ██▀▀█ █   █ █   █ █▄▄█ ██   █     ██▄▄     ▀█   ██▄▄
 ▀▄▄▄▄▀    █   █ ▀████ █  █  █  █ █ █  █     █▄   ▄▀  █    █▄   ▄▀
              █        ███▀     █ █  █ █     ▀███▀  ▄▀     ▀███▀
             ▀                 █  █   ██                       v1.3.0

                              ▀
\033[1;m
        \033[1;31mShodan Eye v1.3.0\033[0m

    ✓ The author is not responsible for any damage, misuse of the information.
    ✓ Shodan Eye shall only be used to expand knowledge and not for
      causing malicious or damaging attacks.
    ✓ Just remember, Performing any hacks without written permission is illegal ..!

            Author:  Jolanda de Koff Bulls Eye
            Github:  https://github.com/BullsEye0
            Website: https://HackingPassion.com
            Patreon: https://www.patreon.com/jolandadekoff

            \033[1;31mHi there, Shall we play a game..?\033[0m 😃
        """)

banners = (banner1, banner2)


def get_api_key():
    shodan_api_key = os.environ.get("SHODAN_API_KEY")
    if shodan_api_key:
        return shodan_api_key

    if os.path.exists("./api.txt") and os.path.getsize("./api.txt") > 0:
        with open("api.txt", "r") as f:
            return f.readline().rstrip("\n")

    shodan_api_key = getpass.getpass("[!] \033[34mPlease enter a valid Shodan API Key: \033[0m")
    with open("api.txt", "w") as f:
        f.write(shodan_api_key)
    print("\n[~] \033[34mFile written: ./api.txt \033[0m")
    return shodan_api_key


def run():
    print(random.choice(banners))

    save_choice = input("\n[+] \033[34mDo you like to save the output in a file? \033[0m(Y/N) ").strip()
    save_enabled = save_choice.lower().startswith("y")
    log_filename = ""
    log_file = None

    if save_enabled:
        log_filename = input("\n[~] \033[34mGive the file a name: \033[0m ").strip()
        if not re.match(r'^[a-zA-Z0-9_\-]+$', log_filename):
            print("[!] \033[1;31mInvalid filename. Use only letters, numbers, underscores, hyphens.\033[0m")
            sys.exit(1)
        print("\n" + "  " + "»" * 78 + "\n")
    else:
        print("[!] \033[34mSaving is skipped\033[0m")
        print("\n" + "  " + "»" * 78 + "\n")

    while True:
        shodan_api_key = get_api_key()
        api = shodan.Shodan(shodan_api_key)

        limit = 888
        counter = 1

        try:
            print("[~] \033[34mChecking Shodan.io API Key... \033[0m")
            api.search("b00m")
            print("[✓] \033[34mAPI Key Authentication:\033[0m SUCCESS..!")
            search_query = input("\n[+] \033[34mEnter your keyword(s):\033[0m ")

            if save_enabled:
                log_file = open(f"{log_filename}.txt", "a")

            try:
                for banner in api.search_cursor(search_query):
                    print(f"[+] \033[1;31mIP: \033[1;m{banner['ip_str']}")
                    print(f"[+] \033[1;31mPort: \033[1;m{banner['port']}")
                    print(f"[+] \033[1;31mOrganization: \033[1;m{banner['org']}")
                    print(f"[+] \033[1;31mLocation: \033[1;m{banner['location']}")
                    print(f"[+] \033[1;31mLayer: \033[1;m{banner['transport']}")
                    print(f"[+] \033[1;31mDomains: \033[1;m{banner['domains']}")
                    print(f"[+] \033[1;31mHostnames: \033[1;m{banner['hostnames']}")
                    print(f"[+] \033[1;31mThe banner information for the service: \033[1;m\n\n{banner['data']}")
                    print(f"\n[✓] Result: {counter}. Search query: {search_query}")

                    if log_file:
                        result_data = (
                            f"\nIP: {banner['ip_str']}"
                            f"\nPort: {banner['port']}"
                            f"\nOrganisation: {banner['org']}"
                            f"\nLocation: {banner['location']}"
                            f"\nLayer: {banner['transport']}"
                            f"\nDomains: {banner['domains']}"
                            f"\nHostnames: {banner['hostnames']}"
                            f"\nData\n{banner['data']}"
                        )
                        log_file.write(result_data)

                    print("\n" + "  " + "»" * 78 + "\n")

                    counter += 1
                    if counter >= limit:
                        break
            finally:
                if log_file:
                    log_file.close()

            break

        except KeyboardInterrupt:
            print("\n")
            print("\033[1;91m[!] User Interruption Detected..!\033[0m")
            print("\n\n\t\033[1;91m[!] I like to See Ya, Hacking \033[0m😃\n\n")
            sys.exit(1)

        except shodan.APIError as api_error:
            print(f"[✘] \033[1;31mError: {api_error} \033[0m")
            change_key = input("[*] \033[34mWould you like to change the API Key? <Y/N>:\033[0m ").strip()
            if change_key.lower().startswith("y"):
                shodan_api_key = getpass.getpass("[✓] \033[34mPlease enter valid Shodan.io API Key:\033[0m ")
                with open("api.txt", "w") as f:
                    f.write(shodan_api_key)
                print("\n[~] \033[34mFile written: ./api.txt\033[0m")
                print("[~] \033[34mRestarting the Platform, Please wait...\033[0m \n")
                continue
            else:
                print("")
                print("[•] Exiting Platform... \033[1;91m[!] I like to See Ya, Hacking \033[0m😃\n\n")
                sys.exit()

    print("\n\n\tShodan Eye \033[1;91mI like to See Ya, Hacking \033[0m😃\n\n")


# =====# Main #===== #
if __name__ == "__main__":
    run()
