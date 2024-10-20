import pandas as pd
import os

user_file_name = "users.csv"
task_file_name = "tasks.csv"

def create_files_if_not_exists():
    # for user authentications and all
    if not os.path.exists(user_file_name):
        df = pd.DataFrame({"user_name":[], "password": []})
        df.to_csv(user_file_name, index=False)

    # for storing tasks
    if not os.path.exists(task_file_name):
        df = pd.DataFrame({"task_id": [], "user_name":[], "task": [], "status": []})
        df.set_index("task_id", inplace=True)
        df.to_csv(task_file_name)

create_files_if_not_exists()

def get_next_task_id():
    """Retrieve the next available task_id."""
    if not os.path.exists(task_file_name):
        return 1 
    df = pd.read_csv(task_file_name, index_col="task_id")
    if df.empty:
        return 1
    return df.index.max() + 1  # Increment from the highest task_id

def register(user_name: str, password: str) -> bool:
    try:
        df = pd.read_csv(user_file_name)
        row = df[df['user_name'] == user_name]
        if user_name in df['user_name'].values and row['password'][1] == password:
            print("User already Registered")
            return True

        new_user = {"user_name": user_name, "password": password}
        new_row_df = pd.DataFrame([new_user])
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_csv(user_file_name, index=False)
        print("User Registered")
        return True
    except Exception as e:
        print(f"Cannot register User: {e}")
        return False

def login(user_name: str, password: str)->bool:
    df = pd.read_csv(user_file_name)
    get_rows = df.iterrows()
    for item in get_rows:
        if item[1]['user_name'] == user_name and item[1]['password'] == password:
            print("Valid User")
            return True
    
    print("Either Password or username is incorrect")
    return False

def add_task(user_name: str, task_desc: str, status = "todo") -> bool:
    try:
        df = pd.read_csv(task_file_name)
        new_row = {"task_id": get_next_task_id(),"user_name": user_name, "task": task_desc, "status": status}
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(task_file_name, index=False)
        print(f"Task Added for {user_name}")
    except Exception as e:
        print(f"error occured: {e}")
        return False
    
    return True

def view_tasks(user_name: str):
    df = pd.read_csv(task_file_name)
    list_of_tasks = []
    for row in df.iterrows():
        row = row[1]
        if row['user_name'] == user_name:
            list_of_tasks.append({'task_id': row['task_id'], "task": row['task'], "status": row['status']})

    print(f"List of Tasks for {user_name} : {list_of_tasks}")
    return list_of_tasks

def mark_task_complete(task_id: int) -> bool:
    df = pd.read_csv(task_file_name)
    try:
        df.loc[df['task_id'] == task_id, 'status'] = 'done'
        df.to_csv(task_file_name, index=False)        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def delete_task(task_id: int)->bool:
    df = pd.read_csv(task_file_name)
    try:
        intial_len = df.shape[0]
        df = df[df['task_id'] != task_id]
        df.to_csv(task_file_name, index=False)
        if intial_len == df.shape[0]:
            print("Task did not exist")
            return False
        print(f"Task Deleted with id: {task_id}")
        return True
    except Exception as e:
        print(e)
        return False
    
def action():
    while True:
        is_registered = input("Are you registered? - 'y' for yes and 'n' for no : ")
        user_name = input("Enter username : ")
        password = input("Enter Password : ")
        is_valid = False
        if is_registered == 'y':
            if login(user_name=user_name, password=password):
                print(f"Welcome Back, {user_name}")
                is_valid = True
            else:
                print("Try Again")
        else:
            register_user = register(user_name=user_name, password=password)
            if register_user:
                print(f"Welcome, {user_name}")
                is_valid = True
            else:
                print("Something Went Wrong Or User Already Exists")

        if not is_valid:
            continue

        while True:        
            choice = input("Options: 1. Add Task, 2. View Tasks, 3. Mark a Task as Complete, 4. Delete a Task, 5.Logout : ")

            if choice == '1':
                task = input("Enter task details : ")
                add_task(user_name=user_name, task_desc=task)
            elif choice == '2':
                view_tasks(user_name=user_name)
            elif choice == '3':
                view_tasks(user_name=user_name)
                task_id = input('Enter task id to be marked as done : ')
                mark_task_complete(task_id=int(task_id))
            elif choice == '4':
                view_tasks(user_name=user_name)
                task_id = input('Enter task id to be deleted : ')
                delete_task(task_id=int(task_id))
            elif choice == '5':
                print("logout")
                break
        
        exit_ = input("Exit Application? y for yes any other key for no : ")
        if exit_ == 'y':
            break

action()