# © Designed and Developed by Mehmet Güdük.
# © Licensed with GPL-3.0 License, Author is Mehmet Güdük.



from datetime import datetime
import sqlite3
import os
users_documents_location = os.path.expanduser('~\Documents')
location = users_documents_location + "\LearnQuick"

# Creating LearnQuick folder into user's Documents Folder for adding all databases.
try:
    os.makedirs(location)
except:
    pass


###################################################################################################################################
# A function that converts labels to seconds for other database functions.
def label_to_seconds(txt: str):
    items = [int(x) if x.isnumeric() else x for x in txt.split() ]
    seconds = 0
    for i in range(0,len(items),2):
        a = items[i+1]
        if a.lower()=="hours" or a.lower()=="hour":
            seconds += 3600*items[i]
        elif a.lower()=="minutes" or a.lower()=="minute":
            seconds += 60*items[i]
        elif a.lower()=="seconds" or a.lower()=="second":
            seconds += items[i]
    return seconds
###################################################################################################################################






###################################################################################################################################
# The main goal of this function is that, connecting main database of application.
def DATABASE_CONNECT(): 
    global connection
    label = location+ "\learnquick_database.db"
    connection = sqlite3.connect(label)
    global cursor
    cursor = connection.cursor()
###################################################################################################################################
# The main goal of this function is that, disconnecting from main database of application.
def DATABASE_DISCONNECT():
    connection.commit()
    connection.close()
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, getting all decks(tables) from main database.
table_list = []
def DATABASE_get_decks(): 
    table_list.clear()
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(sql)
    tables = cursor.fetchall()
    for table in tables:
        table_list.append(table[0])
###################################################################################################################################
# The main goal of this function is that, getting all cards(items) from main database tables.
card_list = [] 
def DATABASE_get_cards(deckname): 
    try:
        card_list.clear()
        sql = "SELECT * FROM '{}'".format(deckname)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            card_list.append(row)
    except sqlite3.OperationalError:
        pass
###################################################################################################################################
# The main goal of this function is that, getting all card(item) fronts and backs from main database.
fronts_list = []
backs_list = []
def DATABASE_get_fronts_and_backs(deckname):
    fronts_list.clear()
    backs_list.clear()
    sql = "SELECT * FROM '{}'".format(deckname)
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        fronts_list.append(result[1])
        backs_list.append(result[2])
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, creating new deck(table) into main database.
def DATABASE_create_deck(new_deckname):
    sql = f'CREATE TABLE IF NOT EXISTS "{new_deckname}" ("card_id"	INTEGER NOT NULL UNIQUE,"card_front"	TEXT NOT NULL,"card_back"	TEXT NOT NULL,"red" INTEGER NOT NULL,"orange" INTEGER NOT NULL,"yellow" INTEGER NOT NULL,"green" INTEGER NOT NULL,"blue" INTEGER NOT NULL,PRIMARY KEY("card_id" AUTOINCREMENT))'
    cursor.execute(sql)
    connection.commit()
    DATABASE_get_decks()
###################################################################################################################################
# The main goal of this function is that, renaming a deck(table) in main database.
def DATABASE_rename_deck(old_deckname, new_deckname):
    try:
        sql = f"ALTER TABLE '{old_deckname}' RENAME TO '{new_deckname}'"
        cursor.execute(sql)
    except:
        pass
    connection.commit()
###################################################################################################################################
# The main goal of this function is that, deleting a deck(table) from main database.
def DATABASE_delete_deck(deckname):
    sql = f'DROP TABLE "{deckname}"'
    cursor.execute(sql)
    connection.commit()
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, creating cards(items) into decks(tables).
def DATABASE_create_card(deckname, new_front, new_back):
    sql = f"INSERT INTO '{deckname}' (card_front, card_back, red, orange, yellow, green, blue) VALUES(?, ?, ?, ?, ?, ?, ?)"
    values = (new_front, new_back, 1, 0, 0, 0, 0)
    cursor.execute(sql, values)
    connection.commit()
###################################################################################################################################
# The main goal of this function is that, deleting cards(items) from decks(tables).
def DATABASE_delete_card(deckname, front, back): 
    sql = 'DELETE FROM "{}" WHERE card_front="{}" AND card_back="{}"'.format(deckname,front,back)
    cursor.execute(sql)
    connection.commit()
###################################################################################################################################
# The main goal of this function is that, renaming cards(items) in decks(tables).
def DATABASE_update_card(deckname, front, back, new_front, new_back):
    sql = 'UPDATE "{}" SET card_front="{}", card_back="{}" WHERE card_front="{}" AND card_back="{}"'.format(deckname,new_front,new_back,front,back)
    cursor.execute(sql)
    connection.commit()
###################################################################################################################################


###################################################################################################################################
# The main goals of this functions is that, adding cards to lists by colors.
red_list = []
orange_list = []
yellow_list = []
green_list = []
blue_list = []
def DATABASE_get_all_reds_into_list(deckname):
    red_list.clear()
    sql = "SELECT * FROM '{}' WHERE red=1 AND orange=0 AND yellow=0 AND green=0 AND blue=0".format(deckname)
    cursor.execute(sql)
    reds = cursor.fetchall()
    for red in reds:
        red_list.append(red) 
def DATABASE_get_all_oranges_into_list(deckname):
    orange_list.clear()
    sql = "SELECT * FROM '{}' WHERE red=0 AND orange=1 AND yellow=0 AND green=0 AND blue=0".format(deckname)
    cursor.execute(sql)
    oranges = cursor.fetchall()
    for orange in oranges:
        orange_list.append(orange)
def DATABASE_get_all_yellows_into_list(deckname):
    yellow_list.clear()
    sql = "SELECT * FROM '{}' WHERE red=0 AND orange=0 AND yellow=1 AND green=0 AND blue=0".format(deckname)
    cursor.execute(sql)
    yellows = cursor.fetchall()
    for yellow in yellows:
        yellow_list.append(yellow)
def DATABASE_get_all_greens_into_list(deckname):
    green_list.clear()
    sql = "SELECT * FROM '{}' WHERE red=0 AND orange=0 AND yellow=0 AND green=1 AND blue=0".format(deckname)
    cursor.execute(sql)
    greens = cursor.fetchall()
    for green in greens:
        green_list.append(green)
def DATABASE_get_all_blues_into_list(deckname):
    blue_list.clear()
    sql = "SELECT * FROM '{}' WHERE red=0 AND orange=0 AND yellow=0 AND green=0 AND blue=1".format(deckname)
    cursor.execute(sql)
    blues = cursor.fetchall()
    for blue in blues:
        blue_list.append(blue)
###################################################################################################################################
# The main goals of this functions is that, setting card's color property to None.
def DATABASE_reset_colors_for_card(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=0, orange=0, yellow=0, green=0, blue=0 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
###################################################################################################################################
# The main goals of this functions is that, setting card property to related color.
def DATABASE_setting_red(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=1, orange=0, yellow=0, green=0, blue=0 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
def DATABASE_setting_orange(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=0, orange=1, yellow=0, green=0, blue=0 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
def DATABASE_setting_yellow(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=0, orange=0, yellow=1, green=0, blue=0 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
def DATABASE_setting_green(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=0, orange=0, yellow=0, green=1, blue=0 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
def DATABASE_setting_blue(deckname, card_front, card_back):
    sql = 'UPDATE "{}" Set red=0, orange=0, yellow=0, green=0, blue=1 WHERE card_front="{}" AND card_back="{}"'.format(deckname, card_front, card_back)
    cursor.execute(sql)
    connection.commit()
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, connecting logs database of application.
def DATABASE_CONNECT_for_logs():
    global connection_logs
    label = location+ "\learnquick_database_logs.db"
    connection_logs = sqlite3.connect(label)
    global cursor_logs
    cursor_logs = connection_logs.cursor()
###################################################################################################################################
# The main goal of this function is that, disconnecting from logs database of application.
def DATABASE_DISCONNECT_for_logs():
    connection_logs.commit()
    connection_logs.close()
###################################################################################################################################
# The main goal of this function is that, creating day(table) in logs database.
def DATABASE_creating_table_for_day(date):
    sql = f'CREATE TABLE IF NOT EXISTS "{date}" ("id" INTEGER NOT NULL UNIQUE, "deckname" TEXT, "studytime" TEXT, PRIMARY KEY("id"))'
    cursor_logs.execute(sql)
    connection_logs.commit()
###################################################################################################################################
# The main goal of this function is that, inserting user's log info into days(tables).
def DATABASE_insert_log_inside_table(logname, deckname, studytime):
    decknames = []
    studytimes = []
    sql = f"SELECT * FROM '{logname}'"
    cursor_logs.execute(sql)
    result = cursor_logs.fetchall()
    for row in result:
        decknames.append(row[1])
        studytimes.append(row[2])
    if deckname in decknames:
        index_no_of_deckname = decknames.index(deckname)
        new_study_time = label_to_seconds(studytime)
        old_studytime = label_to_seconds(studytimes[index_no_of_deckname])
        seconds = new_study_time + old_studytime
        hours = divmod(seconds,3600)[0]
        minutes = divmod(seconds-(hours*3600),60)[0]
        remaining_seconds = seconds-((hours*3600)+(minutes*60))
        if remaining_seconds == 0 and hours == 0 and minutes == 0:
            time_label = "No info"
        elif hours > 1: 
            time_label = f"{hours} Hours {minutes} Minutes {remaining_seconds} Seconds"
        elif hours == 1:
            time_label = f"{hours} Hour {minutes} Minutes {remaining_seconds} Seconds"
        elif hours == 0 and minutes > 1:
            time_label = f"{minutes} Minutes {remaining_seconds} Seconds"
        elif hours == 0 and minutes == 1:
            time_label = f"{minutes} Minute {remaining_seconds} Seconds"
        elif hours == 0 and minutes == 0:
            time_label = f"{remaining_seconds} Seconds"
        sql = f'UPDATE "{logname}" SET studytime="{time_label}" WHERE deckname="{deckname}"'
        cursor_logs.execute(sql)
        connection_logs.commit()
    else:
        sql = f"INSERT INTO '{logname}' (deckname, studytime) VALUES('{deckname}', '{studytime}')"
        cursor_logs.execute(sql)
        connection_logs.commit()
###################################################################################################################################
# The main goal of this function is that, getting all log info from logs database.
def DATABASE_get_logs_from_db(date):
    try:
        sql = f"SELECT * FROM '{date}'"
        cursor_logs.execute(sql)
        logs = cursor_logs.fetchall()
        return logs
    except sqlite3.OperationalError:
        pass
###################################################################################################################################
# # The main goal of this function is that, clearing all info inside of day(table).
def DATABASE_clear_day_log(date):
    try:
        sql = f'DROP TABLE "{date}"'
        cursor_logs.execute(sql)
        connection_logs.commit()
    except sqlite3.OperationalError:
        pass
###################################################################################################################################
# The main goal of this function is that, removing a info inside of day(table).
def DATABASE_remove_record_from_db(date, index_no):
    try:
        sql = f'DELETE FROM "{date}" WHERE id="{index_no}"'
        cursor_logs.execute(sql)
        connection_logs.commit()
    except sqlite3.OperationalError:
        pass
###################################################################################################################################
# The main goal of this function is that, changing deckname in logs database when user change deckname.
def DATABASE_change_decknames_from_db(oldname, newname):
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor_logs.execute(sql)
    tables = cursor_logs.fetchall()
    for table in tables:
        sql = f'UPDATE "{table[0]}" SET deckname="{newname}" WHERE deckname="{oldname}"'
        cursor_logs.execute(sql)
        connection_logs.commit()
###################################################################################################################################
# The main goal of this function is that, deleting deck in logs database when user delete deck.
def DATABASE_delete_logs_when_a_deck_deleted(deckname):
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor_logs.execute(sql)
    tables = cursor_logs.fetchall()
    for table in tables:
        sql = f'DELETE FROM "{table[0]}" WHERE "deckname"="{deckname}"'
        cursor_logs.execute(sql)
        connection_logs.commit()
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, getting deck's last studied time from logs database.
def DATABASE_getting_last_studied_time(deckname):
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor_logs.execute(sql)
    tables = cursor_logs.fetchall()
    date_list = []
    for table in tables:
        date_list.append(table[0])
    date_list = sorted(date_list, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    date_list.reverse()
    kk = 1
    for date in date_list:
        sql = f'SELECT * FROM "{date}"'
        cursor_logs.execute(sql)
        logs = cursor_logs.fetchall()
        if kk == 0:
            break
        for log in logs:
            if log[1] == deckname:
                kk = 0
                return date
                break
###################################################################################################################################
# The main goal of this function is that, getting deck's total studied time from logs database.
def DATABASE_getting_total_studied_time(deckname):
    try:
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor_logs.execute(sql)
        tables = cursor_logs.fetchall()
        i = 0
        all_logs = []
        for table in tables:     
            try:
                sql = f"SELECT * FROM '{table[0]}'"
                cursor_logs.execute(sql)
                logs = cursor_logs.fetchall()
                for log in logs:
                    all_logs.append(log)
            except sqlite3.OperationalError:
                pass
        for log in all_logs:   
            if log[1] == deckname:
                i += label_to_seconds(log[2])
        return i 
    except sqlite3.OperationalError:
        pass
###################################################################################################################################


###################################################################################################################################
# The main goal of this function is that, adding default list(deck, table) into main database of application.
def DATABASE_inserting_default_list(front, back):
    sql = f"INSERT INTO 'German Top200 Words (Default Deck)' (card_front, card_back, red, orange, yellow, green, blue) VALUES(?, ?, ?, ?, ?, ?, ?)"
    values = (front, back, 1, 0, 0, 0, 0)
    cursor.execute(sql, values)
    connection.commit()
###################################################################################################################################
# The main goal of this function is that, inserting a value that shows is user deleted default deck or renamed.
def DATABASE_user_deleted_default():
    label = location+ "\learnquick_database_default.db"
    connection_default = sqlite3.connect(label)
    cursor_default = connection_default.cursor()

    sql = f'CREATE TABLE IF NOT EXISTS "defaultdeck" ("id" INTEGER NOT NULL, "status" TEXT, PRIMARY KEY("id"))'
    cursor_default.execute(sql)
    connection_default.commit()

    try:
        sql = f'INSERT INTO "defaultdeck" (id) VALUES(0)'
        cursor_default.execute(sql)
        connection_default.commit()
    except:
        pass
    
    sql = f'UPDATE "defaultdeck" SET "status"="DELETED" WHERE "id"=0'
    cursor_default.execute(sql)
    connection_default.commit()

    connection_default.close()
###################################################################################################################################
# The main goal of this function is that, returning the value that DATABASE_user_deleted_default function has created.
def DATABASE_user_deleted_default_tool():
    try:
        label = location+ "\learnquick_database_default.db"
        connection_default = sqlite3.connect(label)
        cursor_default = connection_default.cursor()
        sql = f'SELECT * FROM "defaultdeck"'
        cursor_default.execute(sql)
        result = cursor_default.fetchall() 
        connection_default.close()
        return result[0][1]
    except sqlite3.OperationalError:
        pass
###################################################################################################################################
# The main goal of this function is that, inserting a value that shows is application has created default deck.
def DATABASE_is_default_created():
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(sql)
    tables = cursor.fetchall()
    for table in tables:
        if table[0] == "German Top200 Words (Default Deck)":
            return True
###################################################################################################################################