import json
import random

import requests

BASE_URL = "http://localhost:8000/api/"

with open('config.json', 'r') as f:
    config = json.load(f)


def signup(email, password):
    """Sign up a new user."""
    response = requests.post(BASE_URL + 'user/signup/', data={
        'email': email,
        'password': password
    })
    return None


def login(email, password):
    """Login and get the access token."""
    response = requests.post(BASE_URL + 'user/login/', data={
        'email': email,
        'password': password
    })

    if response.status_code == 200:
        response_json = json.loads(response.content)
        token = response_json.get('access')
        return token

    response.raise_for_status()


def create_post(token, title, content):
    """Create a new post with the given title and content."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(BASE_URL + 'posts/', headers=headers, data={
        'title': title,
        'content': content,
    })

    if response.status_code == 201:
        return json.loads(response.content)['id']

    return None


def like_post(token, post_id:int):
    """Like a post with the given ID."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.patch(BASE_URL + f'posts/{post_id}/like/', headers=headers)

    return response.status_code == 200


if __name__ == '__main__':
    all_posts_id = []

    for user in range(config['number_of_users']):
        email = f'user_{random.randint(1, 10000)}@example.com'
        password = "password"
        signup(email, password)
        token = login(email, password)

        for post in range(random.randint(1, config['max_posts_per_user'])):
            title = f'Post {random.randint(1, 10000)}'
            content = f'Content {random.randint(1, 10000)}'
            post_id = create_post(token, title, content)
            all_posts_id.append(post_id)

            num_likes = random.randint(1, config['max_likes_per_user'])
            for like in range(num_likes):
                post_id = random.choice(all_posts_id)
                like_post(token, post_id)
