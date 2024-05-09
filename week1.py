import requests
from datetime import datetime
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

work_url = 'https://66095c000f324a9a28832d7e.mockapi.io/users'


def get_data(url) -> dict:
    response = requests.get(url)
    return response.json()


def find_user(data: list, name: str):
    for user in data:  # Assuming data is a list of user objects
        if user["name"] == name:  # Replace ID with your search criteria
            user_id = user["id"]
            return user_id  # Stop iterating after finding the user


def state_sum_of_first_n_users(data: list, number: int):
    count = 0
    state_sum = 0
    for user in data:  # Assuming data is a list of user objects
        while count < number:
            state_sum += float(user['state'])
            count += 1
    return state_sum


def post_user(file: str, url: str):
    with open(file, 'r') as f:
        json_data = f.read()
    headers = {"Content-Type": "application/json"}  # Set appropriate content type
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code


def parse_data(date: str):
    # Parse the string into a datetime object
    datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Extract individual components as a list of numbers
    date_time_list = [
        datetime_obj.year,
        datetime_obj.month,
        datetime_obj.day,
        datetime_obj.hour,
        datetime_obj.minute,
        datetime_obj.second,
        int(datetime_obj.microsecond / 1000),  # Extract milliseconds (avoid microseconds)
    ]

    return date_time_list  # Output: [2036, 10, 25, 11, 44, 6, 223]


def oldest_user(data: dict):
    us = data[0]
    name = us['name']
    birthday = us['birth']
    for user in data:
        try:
            if all(a > b for a, b in zip(parse_data(birthday), parse_data(user['birth']))):
                continue
            else:
                name = user['name']
                birthday = user['birth']
        except ValueError:
            continue
    return name, birthday


def poorest_user(data: list):
    us = data[0]
    name = us['name']
    state = us['state']
    for user in data:  # Assuming data is a list of user objects
        if float(user['state']) < float(state):  # Replace ID with your search criteria
            name = user['name']
            state = user['state']
        else:
            continue
    return name, state


def users_born_in_april(data: list):
    count = 0
    for user in data:
        try:
            if parse_data(user['birth'])[1] == 4:
                count += 1
            else:
                continue
        except ValueError:
            continue
    return count


if __name__ == "__main__":
    user_data = get_data(work_url)
    "post_status = post_user('user_with_state_1B.json', work_url)"
    with Pool() as process_pool:
        found_user_id = process_pool.apply_async(find_user, args=(user_data, 'Wilson VonRueden'))
        state_sum_of_first_76_users = process_pool.apply_async(state_sum_of_first_n_users, args=(user_data, 76))
        found_oldest_user = process_pool.apply_async(oldest_user, args=(user_data,))
        found_poorest_user = process_pool.apply_async(poorest_user, args=(user_data,))
        found_users_born_in_april = process_pool.apply_async(users_born_in_april, args=(user_data,))
        print(found_user_id.get())
        print(state_sum_of_first_76_users.get())
        print(found_oldest_user.get())
        print(found_poorest_user.get())
        print(found_users_born_in_april.get())
