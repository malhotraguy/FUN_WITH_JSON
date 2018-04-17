import json
import requests
response = requests.get('https://jsonplaceholder.typicode.com/todos')
todos = json.loads(response.text)
# Map of userId to number of complete TODOs for that user
todos_by_user = {}
print("todos[:5]=",todos[:5])
# Increment complete TODOs count for each user.
for todo in todos:
    if todo["completed"]:
        try:
            # Increment the existing user's count.
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            # This user has not been seen. Set their count to 1.
            todos_by_user[todo["userId"]] = 1

# Create a sorted list of (userId, num_complete) pairs.
print("todos_by_user=",todos_by_user)

top_users = sorted(todos_by_user.items(),key=lambda x: x[1], reverse=True)
#sorted() have a key parameter to specify a function to be called on each list element prior to making comparisons.
print("top_users=",top_users,type(top_users))
# Get the maximum number of complete TODOs.
max_complete = top_users[0][1]

# Create a list of all users who have completed
# the maximum number of TODOs.
users = []
for user, num_complete in top_users:
    if num_complete < max_complete:
        break
    users.append(str(user))

max_users = ' and '.join(users)
print("max_users =",max_users )

# Define a function to filter out completed TODOs 
# of users with max completed TODOS.
def keep(todo):
    is_complete = todo["completed"]
    has_max_count = todo["userId"] in users
    return is_complete and has_max_count

# Write filtered TODOs to file.
with open("filtered_data_file.json", 'w') as data_file:
    filtered_todos = list(filter(keep, todos))#filter creates a list of elements for which a function returns true
    json.dump(filtered_todos, data_file, indent=2)
