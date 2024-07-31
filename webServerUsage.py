import re

user_data = {}

with open('access_log.txt', 'r') as file:
    for line in file:
        match = re.search(r'~(\w+)/.*\s(\d+)$', line)
        if match:
            user_id = match.group(1)
            value = int(match.group(2))

            if user_id in user_data:
                user_data[user_id] += value
            else:
                user_data[user_id] = value
print(user_data)