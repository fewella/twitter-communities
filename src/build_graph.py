import os

data_directory = "../data/follower_data"


def get_followers(username):
    filename = data_directory + username + ".txt"
    f = open(filename, "r")
    followers = [line.rstrip() for line in f]
    f.close()
    return followers


def main():
    # build dict: username -> list of follower ids
    
    usernames = [filename.rstrip(".txt") for filename in os.listdir(data_directory)]


if __name__ == "__main__":
    main()
