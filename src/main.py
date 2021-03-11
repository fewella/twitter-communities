import requests
import os
import json

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

    ids = []
    for u in r['data']:
        ids.append(u['id'])
    
    return ids


def compare_followers(u1, u2):
    bearer_token = auth()
    url1 = create_uid_url(u1)
    url2 = create_uid_url(u2)
    headers = create_headers(bearer_token)
    params = get_params()
    r1 = connect_to_endpoint(url1, headers, params)
    r2 = connect_to_endpoint(url2, headers, params)

    u1_followers = set()
    u2_followers = set()
    for user in r1['data']:
        u1_followers.add(user['id'])
    for user in r2['data']:
        u2_followers.add(user['id'])
    intersection = u1_followers & u2_followers

    print(len(intersection))
    print(len(u1_followers))
    print(len(u2_followers))
    degree_of_similarity = 0
    if len(u1_followers) < len(u2_followers):
        degree_of_similarity = len(intersection) / len(u1_followers)
    else:
        degree_of_similarity = len(intersection) / len(u2_followers)

    return degree_of_similarity


def main():
    username_1 = "LilyPichu"
    username_2 = "michaelreeves"

    user1_id, user2_id = get_uids([username_1, username_2])

    s = compare_followers(user1_id, user2_id)
    print("degree of similarity between", username_1, "and", username_2, "is", s)

if __name__ == "__main__":
    main()
