import requests
import os
import json
import time

def auth():
    return os.environ.get("BEARER_TOKEN")


def create_username_url(usernames=""):
    usernames = "usernames=" + usernames
    user_fields = "user.fields=description,created_at,id,location,name,verified"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def create_uid_url(user_id=2244994945):
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def get_params():
    return {"user.fields": "created_at"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params=None):
    if params:
        response = requests.request("GET", url, headers=headers, params=params)
    else:
        response = requests.request("GET", url, headers=headers)

    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_uids(usernames_as_list):
    usernames_as_str = ""
    for s in usernames_as_list:
        usernames_as_str += s + ","
    usernames_as_str = usernames_as_str[:-1]
    
    bearer_token = auth()
    url = create_username_url(usernames_as_str)
    headers = create_headers(bearer_token)
    r = connect_to_endpoint(url, headers)
    
    print(r)
    if 'errors' in r:
        return -1

    ids = []
    for u in r['data']:
        ids.append(u['id'])
    if len(ids) == 1:
        ids = ids[0]

    return ids


def retrieve_sample_followers(uid):
    bearer_token = auth()
    url = create_uid_url(uid)
    headers = create_headers(bearer_token)
    params = get_params()
    params['max_results'] = 1000
    
    followers = set()

    for i in range(15):
        try:
            r = connect_to_endpoint(url, headers, params)
        except:
            time.sleep(16 * 60)
            r = connect_to_endpoint(url, headers, params)

        for u in r['data']:
            followers.add(u['id'])
        
        if 'next_token' in r['meta']:
            params['pagination_token'] = r['meta']['next_token']
        else:
            break
    
    return followers
    

def retrieve_input_followers(filename):
    f = open(filename, "r")
    usernames = []
    for line in f:
        usernames.append(line.rstrip())
    f.close()

    for username in usernames:
        print("retrieving", username)
        uid = get_uids([username])
        if uid == -1:
            print("ERROR: could not find uid for", username, ". Skipping...")
            continue
        followers = retrieve_sample_followers(uid)
        
        user_output_file = "data/" + username + ".txt"
        f = open(user_output_file, "w") 
        for u in followers:
            f.write(u + "\n")
        f.close()


def main():
    input_filename = "data/input_usernames.txt"
    retrieve_input_followers(input_filename)


if __name__ == "__main__":
    main()
