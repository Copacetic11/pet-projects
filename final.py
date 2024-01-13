import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

def initialize_database():
    con = sqlite3.connect('time.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS activities(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   activity TEXT, 
                   start_date TEXT, 
                   start_time TEXT, 
                   end_date TEXT, 
                   end_time TEXT, 
                   duration TEXT)''')
    con.commit()
    con.close()

# Call this function at the beginning of your script
initialize_database()

def master_clear():
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS activities')



def view_all():
    con = sqlite3.connect('time.db')
    cur = con.cursor()


    cur.execute("SELECT * FROM activities")
    items = cur.fetchall()
    for item in items:
        print(item)

    con.commit()
    con.close()

def add_one(module, start_date, start_time, end_date, end_time):
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    # Since dates are already in 'YYYY-MM-DD' format, we can use them directly
    formatted_start_date = start_date
    formatted_end_date = end_date

    # Correct the formatting of time from 'HHMM' to 'HH:MM'
    formatted_start_time = f"{start_time[:2]}{start_time[2:]}"
    formatted_end_time = f"{end_time[:2]}{end_time[2:]}"
    #print(formatted_start_time, formatted_end_time)

    # Calculate duration
    start_datetime = datetime.strptime(f"{formatted_start_date} {formatted_start_time}", "%Y-%m-%d %H:%M")
    end_datetime = datetime.strptime(f"{formatted_end_date} {formatted_end_time}", "%Y-%m-%d %H:%M")
    duration_delta = end_datetime - start_datetime
    hours = int(duration_delta.total_seconds() // 3600)
    minutes = int((duration_delta.total_seconds() % 3600) // 60)

    # Insert into the database
    cur.execute("INSERT INTO activities (activity, start_date, start_time, end_date, end_time, duration) VALUES (?, ?, ?, ?, ?, ?)", 
                (module, formatted_start_date, formatted_start_time, formatted_end_date, formatted_end_time, f'{hours}H {minutes}M'))

    con.commit()
    con.close()




def converter(time_in_str):
    # Assuming time_in_str is in the format 'YYYY-MM-DD HH:MM'
    dt_obj = datetime.strptime(time_in_str, "%Y-%m-%d %H:%M")
    return dt_obj


def how_many_entries():

    con = sqlite3.connect('time.db')
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM activities')
    entries = cur.fetchone()[0]
    con.commit()
    con.close()
    return entries




    #convert start_time, end_time into datetime objects or string format

def delete(rowid):
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    cur.execute("DELETE FROM activities WHERE id = ?", (rowid,))
    

    con.commit()
    con.close()    

def update(rowid, t, change, *durationing):

    if durationing == ():
            


        con = sqlite3.connect('time.db')
        cur = con.cursor()

        sql_command = f"UPDATE activities SET {t} = ? where id = ?"
        cur.execute(sql_command, (change, rowid))

        con.commit()
        con.close()   
    
    if durationing != ():
        durationing = durationing[0]
        con = sqlite3.connect('time.db')
        cur = con.cursor()

        sql_command = f"UPDATE activities SET {t} = ?, duration = ? where id = ?"
        cur.execute(sql_command, (change, durationing, rowid))

        con.commit()
        con.close()   

def selector(rowid, column):
    con =sqlite3.connect('time.db')
    cur = con.cursor()

    cur.execute("SELECT " +column + " FROM activities WHERE id = ?", (rowid,))
    return cur.fetchone()[0]

def stopwatch(mod):
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM activities WHERE id = 1")
    watch = cur.fetchone()
    
    if watch:
        
        # Check if the stopwatch is already running
        if watch[2] is not None and watch[3] is not None:
         
            # Stopwatch is running; stop it and log the activity
            end_dt = datetime.now()
            end_date_str = end_dt.strftime("%Y-%m-%d")
            end_time_str = end_dt.strftime("%H:%M")

            # Verify that start date and time are not None
            if watch[2] is None or watch[3] is None:
                print("Invalid start date or time in stopwatch record.")
                con.close()
                return

            start_dt_str = f"{watch[2]} {watch[3]}"  # Format: 'YYYY-MM-DD HH:MM'
            start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
            duration = end_dt - start_dt
            duration_str = f'{duration.seconds // 3600}H {duration.seconds % 3600 // 60}M'

            cur.execute("INSERT INTO activities (activity, start_date, start_time, end_date, end_time, duration) VALUES (?, ?, ?, ?, ?, ?)", 
                        (watch[1], watch[2], watch[3], end_date_str, end_time_str, duration_str))
            con.commit()
            cur.execute("UPDATE activities SET activity = NULL, start_date = NULL, start_time = NULL, end_date = NULL, end_time = NULL, duration = NULL WHERE id = 1")
            con.commit()
        elif watch[2] is None and watch[3] is None:
            # Stopwatch is not running; start it
            
            start_dt = datetime.now()
            start_date_str = start_dt.strftime("%Y-%m-%d")
            start_time_str = start_dt.strftime("%H:%M")
            cur.execute("UPDATE activities SET activity = ?, start_date = ?, start_time = ? WHERE id = 1", 
                        (mod, start_date_str, start_time_str))

        con.commit()
    else:
        print("Stopwatch record not found.")

    con.close()



def update_duration(rowid):
    con = sqlite3.connect('time.db')
    cur = con.cursor()
    try:
        # Retrieve the current start and end date and time
        cur.execute("SELECT start_date, start_time, end_date, end_time FROM activities WHERE id = ?", (rowid,))
        start_date, start_time, end_date, end_time = cur.fetchone()

        # Parse the start and end datetime
        start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

        # Calculate the new duration
        duration = end_datetime - start_datetime
        duration_str = f'{duration.seconds // 3600}H {duration.seconds % 3600 // 60}M'

        # Update the duration in the database
        cur.execute("UPDATE activities SET duration = ? WHERE id = ?", (duration_str, rowid))
        con.commit()
    except Exception as e:
        print(f"Error updating duration: {e}")
    finally:
        con.close()







def get_month_range(month, year):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return start_date, end_date



##### DATA VISUALISATION #####


# Connect to SQLite database
def matplotvis():
    # Connect to SQLite database
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    # Retrieve data from database
    cur.execute("SELECT activity, duration FROM activities")
    data = cur.fetchall()

    # Close the database connection
    con.close()

    # Data Preparation
    activity_duration = {}
    for item in data:
        activity, duration = item
        if duration:
            hours, minutes = 0, 0
            if 'H' in duration:
                hours = int(duration.split('H')[0])
                minutes = int(duration.split('H')[1].split('M')[0]) if 'M' in duration else 0
            elif 'M' in duration:
                minutes = int(duration.split('M')[0])
            
            total_minutes = hours * 60 + minutes

            if activity in activity_duration:
                activity_duration[activity] += total_minutes
            else:
                activity_duration[activity] = total_minutes

    # Sorting the activities for better visualization
    sorted_activities = sorted(activity_duration.items(), key=lambda x: x[1], reverse=True)

    # Unpacking the sorted activities for plotting
    activities, total_durations = zip(*sorted_activities)

    # Plotting
    plt.bar(activities, total_durations)
    plt.xlabel('Activity')
    plt.ylabel('Total Minutes Spent')
    plt.title('Time Spent on Various Activities in Minutes')
    plt.xticks(rotation=45)
    plt.show()





def plotlyvis():
    # Connect to SQLite database
    con = sqlite3.connect('time.db')
    cur = con.cursor()

    # Retrieve data from database
    cur.execute("SELECT activity, duration FROM activities")
    data = cur.fetchall()

    # Close the database connection
    con.close()

    # Data Preparation
    activity_duration = {}
    for item in data:
        activity, duration = item
        if duration:
            hours, minutes = 0, 0
            if 'H' in duration:
                hours = int(duration.split('H')[0])
                minutes = int(duration.split('H')[1].split('M')[0]) if 'M' in duration else 0
            elif 'M' in duration:
                minutes = int(duration.split('M')[0])

            total_minutes = hours * 60 + minutes

            if activity in activity_duration:
                activity_duration[activity] += total_minutes
            else:
                activity_duration[activity] = total_minutes

    # Convert to list of dictionaries for Plotly
    activities_data = [{'Activity': activity, 'Total Minutes': minutes} for activity, minutes in activity_duration.items()]

    # Plotting
    fig = px.bar(activities_data, x='Activity', y='Total Minutes', title='Time Spent on Various Activities in Minutes')
    fig.show()




        

con = sqlite3.connect('time.db')
cur = con.cursor()


# Check if the first row (stopwatch row) exists
cur.execute("SELECT * FROM activities WHERE id = 1")
if not cur.fetchone():
    # Insert the first row for the stopwatch if it doesn't exist
    cur.execute("INSERT INTO activities (id, activity, start_date, start_time, end_date, end_time, duration) VALUES (1, NULL, NULL, NULL, NULL, NULL, NULL)")

con.commit()
con.close()


    

answer = input('What would you like to do? (View, Visualise, Record or Update) ')

while answer not in ['View', 'Visualise', 'Record', 'Update']:
    print("Please pick either 'View', 'Visualise', 'Record' or 'Update'")
    answer = input('What would you like to do? (View, Record, Visualise or Update) ')

if answer == 'View':

    subanswer = input('Which way would you like to view your statistics? (Module or Timeframe) ')

    while subanswer not in ['Module', 'Timeframe']:
        print("Please pick 'Module' or 'Timeframe'")
        subanswer = input('Which way would you like to view your statistics? (Module or Timeframe) ')

    if subanswer == 'Module':
        mod = input('Which module?: ')
        con = sqlite3.connect('time.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM activities WHERE activity = ?", (mod,))
        items = cur.fetchall()
        for item in items:
            print(item)
        con.close()



    if subanswer == 'Timeframe':
        sub2ans = input('Please key in the timeframe you would like to view (Accepted formats: DDMMYYYY, MMYYYY):')

        if len(sub2ans) == 6:  # MMYYYY format
            month = int(sub2ans[:2])
            year = int(sub2ans[2:])
            start_date, end_date = get_month_range(month, year)

            con = sqlite3.connect('time.db')
            cur = con.cursor()

            cur.execute("SELECT * FROM activities WHERE start_date >= ? AND end_date <= ?", (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
            activities = cur.fetchall()
            for activity in activities:
                print(activity)

            con.close()

        elif len(sub2ans) == 8:  # DDMMYYYY format
            specific_date = datetime.strptime(sub2ans, "%d%m%Y").strftime("%Y-%m-%d")
            con = sqlite3.connect('time.db')
            cur = con.cursor()

            cur.execute("SELECT * FROM activities WHERE start_date = ?", (specific_date,))
            items = cur.fetchall()
            for item in items:
                print(item)
            
            con.close()




if answer == 'Record':
    subanswer = input('Module?: ')
    stopwatch(subanswer)

if answer == 'Update':
    
    subanswer = input('Would you like to add a new record (Add), edit an existing record (Edit) or delete an existing record (Delete)? ')

    while subanswer not in ['Add', 'Edit', 'Delete']:
        print("Please pick 'Add', 'Edit' or 'Delete'")
        subanswer = input('Would you like to add a new record (Add), edit an existing record (Edit) or delete an existing record (Delete)? ')

    if subanswer == 'Add':
        while True: 
            mod = input('Module: ')
            start_date = input('Start Date (DDMMYYYY): ')  # Change to DDMMYYYY
            start_time = input('Start Duration (HHMM): ')
            end_date = input('End Date (DDMMYYYY): ')  # Change to DDMMYYYY
            end_time = input('End Duration (HHMM): ')

            # Format the dates and times
            start_date_formatted = datetime.strptime(start_date, "%d%m%Y").strftime("%Y-%m-%d")
            end_date_formatted = datetime.strptime(end_date, "%d%m%Y").strftime("%Y-%m-%d")
            start_time_formatted = f"{start_time[:2]}:{start_time[2:]}"
            end_time_formatted = f"{end_time[:2]}:{end_time[2:]}"

            print(f"Module: {mod}, Start: {start_date_formatted} {start_time_formatted}, End: {end_date_formatted} {end_time_formatted}")
            confirm = input('Is this correct? Y/N: ')
            if confirm == 'Y':
                break

        add_one(mod, start_date_formatted, start_time_formatted, end_date_formatted, end_time_formatted)


            
    if subanswer == 'Delete':
        view_all()
        target = int(input('Please key in the id of the row you would like to delete: '))

        while target < 0 or target > how_many_entries():
            print('Please pick a valid id')
            target = int(input('Please key in the id of the row you would like to delete: '))

        delete(target)
        
    
    if subanswer == 'Edit':
        view_all()
        target = int(input('Please key in the id of the row you would like to edit: '))

        while target < 0 or target > how_many_entries():
            print('Please pick a valid id')
            target = int(input('Please key in the id of the row you would like to edit: '))

        subtarget = input('What would you like to edit? (Module, Start or End): ')

        while subtarget not in ['Module', 'Start', 'End']:
            subtarget = input('What would you like to edit? (Module, Start or End): ')

        if subtarget == 'Start':
            new_date = input('Enter new start date (DDMMYYYY): ')
            new_time = input('Enter new start time (HHMM): ')
            # Format new date and time
            new_date_formatted = datetime.strptime(new_date, "%d%m%Y").strftime("%Y-%m-%d")
            new_time_formatted = f"{new_time[:2]}:{new_time[2:]}"
            update(target, 'start_date', new_date_formatted)
            update(target, 'start_time', new_time_formatted)

            update_duration(target)

        elif subtarget == 'End':
            new_date = input('Enter new end date (DDMMYYYY): ')
            new_time = input('Enter new end time (HHMM): ')
            # Format new date and time
            new_date_formatted = datetime.strptime(new_date, "%d%m%Y").strftime("%Y-%m-%d")
            new_time_formatted = f"{new_time[:2]}:{new_time[2:]}"
            update(target, 'end_date', new_date_formatted)
            update(target, 'end_time', new_time_formatted)

            update_duration(target)

        else:  # Editing Module
            new_module = input('Enter new module name: ')
            update(target, 'activity', new_module)

if answer == 'Visualise':
    
    subanswer = input('Static or Dynamic?: ')

    if subanswer == 'Static':
        matplotvis()

    if subanswer == 'Dynamic':
        plotlyvis()



        



        


        

        



        


    








