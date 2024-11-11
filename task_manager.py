# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Storing the components in tasks in a list variable. Giving each of the elements in the list the correct formant.
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]
    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

#====Login Section====
# Creating the user.txt file if it didnt exsit and populating it with 'admin password'
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")


with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

# Asking user to input details to login while not logged in
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    # Checking to see if the username is located in the user dictionary, printing an error message if check fails 
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    # Checking to see if password is the correct one from the user dictionary. printing an error message if check fails. 
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    # If both conditons are met then logged in = true and the user is granted access. 
    else:
        print("Login Successful!")
        logged_in = True

# Creating a function for reg_user 
def reg_user():
    # User to input a new username that is checked agaisnt user dictionary for duplicates. Error message produced if so. 
    new_username = input("Enter new Username: ").strip()
    if new_username in username_password:
        print("That username already exists please enter another one!")    
    else:
        # If username is unique user asked to input password, check to see if passwords match, error message to display if they dont match. Username and password saved into dictionary and added to the user.txt file under the previous entry. 
        if new_username not in username_password:
            while True:
                new_password = input("Enter new Password: ").strip()
                confirm_new_password = input("Re-enter new Password: ").strip()
                if new_password == confirm_new_password:
                    print("New user added")
                    username_password[new_username] = new_password
                    with open("user.txt", "w") as out_file:
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                    return new_username + ", " + new_password
                else:
                    print("Passwords do no match")

# Creating a function for add_task
def add_task():
    # User to input user that is checked agaisnt dictionary to see if it exisits. If not an error message is produced. 
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("Enter a user who exists please.")
    # If correct user is selected user prompted to input follow up information.     
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        # Try used to check that the correct time format is used when entering due date. Error message produced if entered wrong. 
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    # Storing the information entered in a dictionary. then adding the information into tasks.txt. Formatting the information to be displayed in seperate lines split by ;. 
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"{task_username};{task_title};{task_description};{due_date_time.strftime(DATETIME_STRING_FORMAT)};{curr_date.strftime(DATETIME_STRING_FORMAT)};No\n")
    print("Task added successfully")

# Creating a function for View_task
def view_tasks():
    # Checking the current user logged in agaisnt the task list dictionary. 
    user_tasks = [task for task in task_list if task['username'] == curr_user]
    # Printing error message if the user has no task assigned to them. 
    if not user_tasks:
        print("No tasks assigned to you.")
        return
    # Generating numbers to be added to each task starting from 1. 
    for i, task in enumerate(user_tasks, 1):
        # Printing the tasks related to the current user with accending task numbers. 
        print(f"{i}. {task['title']} - {task['description']} - Due: {task['due_date'].strftime(DATETIME_STRING_FORMAT)} - Completed: {'Yes' if task['completed'] else 'No'}")
    while True:
        # Providing a prompt for user to edit the task or leave via input. 
        task_choice = input("Select a task by number to view/edit, or enter '-1' to return to the main menu: ")
        if task_choice == '-1':
            return
        try:
            # Asking user to input a number. user input -1 to account for starting at 0. Error message printited if the numbers dont match the lsit length. 
            task_choice = int(task_choice) - 1
            # Picking the task based on use input and printing out the information in a more readable format. 
            if 0 <= task_choice < len(user_tasks):
                selected_task = user_tasks[task_choice]
                print(f"Title: {selected_task['title']}")
                print(f"Description: {selected_task['description']}")
                print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                print(f"Assigned Date: {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
                print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")
                # Printing options for input from user. 
                action = input("Enter 'c' to mark as complete, 'e' to edit, or any other key to return: ").lower()
                if action == 'c':
                    # Marking the task complete by changing value from false to true. Then updating the task files. 
                    selected_task['completed'] = True
                    update_tasks_file()
                    print("Task marked as complete.")
                    # Checking to see if the task asking to be editted has been completed. If so error message produced. 
                elif action == 'e' and not selected_task['completed']:
                    edit_task(selected_task)
                else:
                    print("Task cannot be edited as it is already completed.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Generating a function for edit_task 
def edit_task(task):
    # Taking the user input username and checking to see if the username is correct. Storing new username. 
    new_username = input(f"Enter new username (current: {task['username']}): ").strip()
    if new_username and new_username in username_password:
        task['username'] = new_username
    # Tasking the user input for date and time. Try used to ensure that correct format has been used. Error message to be displayed if inccorect one used.     
    new_due_date = input(f"Enter new due date (YYYY-MM-DD) (current: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}): ").strip()
    if new_due_date:
        try:
            task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid date format. Due date not changed.")
    update_tasks_file()
    # Print output to inform user. 
    print("Task updated successfully.")

# Generating a function for updating task files. 
def update_tasks_file():
    # Opening tasks.txt and writing the new information over the current information. 
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            task_file.write(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}\n")

# Generating function for view all tasks.
def view_all_tasks():
     '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
     # Printing all of the tasks in the list in a presentable format. 
     for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: {t['description']}\n"
            print(disp_str)

# Generating function for generating reports. 
def generate_reports():
    try:
        # Opening Task.txt and reading how many tasks by lines. Setting the other values to zero for base count. 
        with open("tasks.txt", "r") as f:
            task_list = f.readlines()
            total_tasks = len(task_list)
            completed_tasks = 0
            uncompleted_tasks = 0
            overdue = 0
            per_incomplete = 0
            per_overdue = 0
            # Working out how many task are completed using dictionary key value. adding to create a running value. 
            for line in task_list:
                temp = line.strip().split(";")
                if temp[5].strip().lower() == 'Yes':
                    completed_tasks += 1
                else:
                    # If not complete then checking if overdue. 
                    uncompleted_tasks += 1
                if check_overdue(temp[4]):
                    overdue += 1
            # Working out the % of incomplete and overdue.         
            per_incomplete = round((uncompleted_tasks / total_tasks * 100), 2)
            per_overdue = round((overdue / total_tasks * 100), 2)
        # Creating a new txt file and writing the information to populate file. 
        with open('task_overview.txt', 'w') as f:
            f.write(f"Total tasks:\t\t{total_tasks}\n")
            f.write(f"Completed tasks:\t{completed_tasks}\n")
            f.write(f"Uncompleted tasks:\t{uncompleted_tasks}\n")
            f.write(f"Overdue tasks:\t\t{overdue}\n")
            f.write(f"% Incomplete tasks:\t{per_incomplete}%\n")
            f.write(f"% Overdue tasks:\t{per_overdue}%\n")
    # error message if the files dont exsist to read from. 
    except FileNotFoundError:
        print("The file you are trying to read does not exist.")
    # New try with the user.txt this time. 
    try:
        with open("user.txt", "r") as f:
            user_list = f.readlines()
            # Counting how many users. 
            total_users = len(user_list)
            total_tasks_per_user = []
            # Creating a running count using keys to check tasks for each user. 
            for line in user_list:
                user = line.strip().split(";")
                username = user[0]
                count = 0
                for task in task_list:
                    temp = task.strip().split(";")
                    if temp[0] == username:
                        count += 1
                total_tasks_per_user.append((username, count))
        # opening/creating a new txt file to write the information gathered above in a easy to read way. 
        with open('user_overview.txt', 'w') as f:
            f.write(f"Total users:\t\t{total_users}\n")
            f.write(f"Total tasks:\t\t{total_tasks}\n")
            # Working out the percentage of tasks assigned to each peron. 
            for user, count in total_tasks_per_user:
                f.write(f"Total tasks for {user}:\t{count}\n")
                f.write(f"% of total tasks for {user}:\t{round((count / total_tasks * 100), 2)}%\n")
     # error message if the files dont exsist to read from.
    except FileNotFoundError:
        print("The file you are trying to read does not exist.")

# Creating a function to check overdue date. 
def check_overdue(due_date):
    # Checking the current date system is accessed in same format %Y-%m-%d. 
    due_date = due_date.strip() 
    current_date = datetime.today().strftime("%Y-%m-%d")
    # Comparing the due date and current date. 
    current_date = datetime.today().strptime(current_date, "%Y-%m-%d")
    date_due_gr = datetime.strptime(due_date, '%Y-%m-%d')
    # stating true of false for use earlier in code. 
    if current_date > date_due_gr  :
        return True
    return False

# Creating a function for displaying stats. 
def display_stats():  
    # Printing the information from task_overview.txt in a readable format. 
    try:
        print("-------------------------")
        print("task overview stats")
        with open("task_overview.txt","r") as file:
            for lines in file:
                print(lines)
        print("-------------------------")
        # If not found then error emssage will generate and the reports will be generated. 
    except FileNotFoundError:
            print("The File you are trying to read does not exist, report will be generated automatically.")
            generate_reports()

    try:  
        print("-------------------------")
        print("user overview stats")  
        with open("user_overview.txt","r") as file:
            for lines in file:
                print(lines)
        print("-------------------------")
    except FileNotFoundError:
            print("The File you are trying to read does not exist, report will be generated automatically.")
            generate_reports()

            




# Main menu for maximum display. All tasks displayed with corresponding functions. 
while True:
    print("\nMain Menu")
    print("r - Register User")
    print("a - Add Task")
    print("vm - View My Tasks")
    print("va - View all task")
    print("ds - Display statistics")
    print("gr - Generate reports" )
    print("e - Exit")
    choice = input("Enter your choice by typing the letters on the left: ")
    # Main menu all defined by functions.
    if choice == 'r':
        reg_user()
    elif choice == 'a':
        add_task()
    elif choice == 'va':
         view_all_tasks()
    elif choice == 'vm':
        view_tasks()
    elif choice == 'ds':
        display_stats() 
    elif choice == 'gr':
        generate_reports()
    elif choice == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again.")
              

        
