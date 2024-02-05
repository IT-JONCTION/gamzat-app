from datetime import date
from datetime import datetime
from flask import Flask, render_template
import pandas as pd
import sqlite3

# create a database in sqlite3
db_connection = sqlite3.connect("/workspaces/gamzat-app/db/support_tickets_daily_stats.db")
cursor = db_connection.cursor()

# create daily stats table in sql
db_creation = """CREATE TABLE IF NOT EXISTS daily_stats (
id INTEGER PRIMARY KEY NOT NULL,
date_of_creation DATE NOT NULL, 
tickets_qty INT NOT NULL
)"""

cursor.execute(db_creation)
db_connection.commit()

#  the code below is used once to feed sql db with past data and is should not be used only once, during app deployment
# ---------------------------------------------------------------------------------------------------------------------
# # Function to extract date from datetime string
# def extract_date(datetime_str):
#     return pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S')

# # Read CSV file into a pandas DataFrame
# csv_file = "/workspaces/gamzat-app/db/evening.csv"
# df = pd.read_csv(csv_file, parse_dates=['creation_date'], date_parser=extract_date)

# # Group by date and count the number of rows for each date
# daily_counts = df.groupby(df['creation_date'].dt.date).size().reset_index(name='tickets_qty')

# # Insert data into daily_stats table
# for index, row in daily_counts.iterrows():
#     cursor.execute("INSERT INTO daily_stats (date_of_creation, tickets_qty) VALUES (?, ?)",
#                 (str(row['creation_date']), row['tickets_qty']))

# # Commit changes and close connection
# db_connection.commit()
# -------------------------------------------------------------------------------------------------------------------
db_connection.close()


# Configure application
app = Flask(__name__)

# create index route
@app.route("/")
def index():

    # read the morning file
    dfMorning = pd.read_csv("/workspaces/gamzat-app/db/morning.csv", sep=",")

    # read the evening file
    dfEvening = pd.read_csv("/workspaces/gamzat-app/db/evening.csv", sep=",")
    
    # show all tickets that are not admin closure and not removed
    total_tickets_morning = len(dfMorning)
    total_tickets_evening = len(dfEvening)
    total_tickets_difference = total_tickets_morning - total_tickets_evening

    # agents verif
    verif_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="03 - Agent Vérification SWAP") 
                          & (dfMorning["marque"] == "FEIDER")])
    
    verif_all_morning = len(dfMorning[(dfMorning["pseudo"]=="03 - Agent Vérification SWAP")])
    
    verif_others_morning = verif_all_morning - verif_feider_morning

    verif_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="03 - Agent Vérification SWAP") 
                          & (dfEvening["marque"] == "FEIDER")])
    
    verif_all_evening = len(dfEvening[(dfEvening["pseudo"]=="03 - Agent Vérification SWAP")])
    
    verif_others_evening = verif_all_evening - verif_feider_evening

    verif_feider_difference = verif_feider_morning - verif_feider_evening
    verif_others_difference = verif_others_morning - verif_others_evening


    # agents admin
    admin_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="02 - Agent Administratif SWAP") 
                          & (dfMorning["marque"] == "FEIDER")])
    
    admin_all_morning = len(dfMorning[(dfMorning["pseudo"]=="02 - Agent Administratif SWAP")])
    
    admin_others_morning = admin_all_morning - admin_feider_morning

    admin_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="02 - Agent Administratif SWAP") 
                          & (dfEvening["marque"] == "FEIDER")])
    
    admin_all_evening = len(dfEvening[(dfEvening["pseudo"]=="02 - Agent Administratif SWAP")])
    
    admin_others_evening = admin_all_evening - admin_feider_evening

    admin_feider_difference = admin_feider_morning - admin_feider_evening
    admin_others_difference = admin_others_morning - admin_others_evening

    # agents tech
    tech_feider_morning  = len(dfMorning[(dfMorning["pseudo"]=="01 - Agent Technique SWAP") 
                         & (dfMorning["marque"] == "FEIDER")])
    
    tech_all_morning = len(dfMorning[(dfMorning["pseudo"]=="01 - Agent Technique SWAP")])
    
    tech_others_morning = tech_all_morning - tech_feider_morning

    tech_feider_evening  = len(dfEvening[(dfEvening["pseudo"]=="01 - Agent Technique SWAP") 
                         & (dfEvening["marque"] == "FEIDER")])
    
    tech_all_evening = len(dfEvening[(dfEvening["pseudo"]=="01 - Agent Technique SWAP")])
    
    tech_others_evening = tech_all_evening - tech_feider_evening

    tech_feider_difference = tech_feider_morning - tech_feider_evening
    tech_others_difference = tech_others_morning - tech_others_evening


    # agent pieces
    pieces_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="04 - Agent Pièces SWAP") 
                           & (dfMorning["marque"] == "FEIDER")])
    
    pieces_all_morning = len(dfMorning[(dfMorning["pseudo"]=="04 - Agent Pièces SWAP")])
    
    pieces_others_morning = pieces_all_morning - pieces_feider_morning

    pieces_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="04 - Agent Pièces SWAP") 
                           & (dfEvening["marque"] == "FEIDER")])
    
    pieces_all_evening = len(dfEvening[(dfEvening["pseudo"]=="04 - Agent Pièces SWAP")])
    
    pieces_others_evening = pieces_all_evening - pieces_feider_evening

    pieces_feider_difference = pieces_feider_morning - pieces_feider_evening
    pieces_others_difference = pieces_others_morning - pieces_others_evening 


    # connect to the db
    db_connection = sqlite3.connect('/workspaces/gamzat-app/db/support_tickets_daily_stats.db')
    cursor = db_connection.cursor()

    # get current date 
    current_date = date.today()
    current_date = current_date.strftime('%Y-%m-%d')
    temp_list = []
    temp_list.append(current_date)
    current_date = temp_list

    # get today's ticket qty
    cursor.execute("SELECT tickets_qty FROM daily_stats WHERE date_of_creation = ?", (current_date))
    tickets_created_today = cursor.fetchone()[0]  # Fetch the result and get the count value
    db_connection.close()


    return render_template("index.html", 
                           pieces_others_morning=pieces_others_morning, pieces_feider_morning=pieces_feider_morning, 
                           pieces_others_evening=pieces_others_evening, pieces_feider_evening=pieces_feider_evening, 
                           pieces_feider_difference=pieces_feider_difference,pieces_others_difference=pieces_others_difference,
                           tech_feider_morning=tech_feider_morning,tech_others_morning=tech_others_morning, 
                           tech_feider_evening=tech_feider_evening,tech_others_evening=tech_others_evening, 
                           tech_feider_difference = tech_feider_difference, tech_others_difference=tech_others_difference,
                           total_tickets_morning=total_tickets_morning,
                           total_tickets_evening=total_tickets_evening,
                           total_tickets_difference=total_tickets_difference,
                           verif_feider_morning=verif_feider_morning, verif_others_morning=verif_others_morning, 
                           verif_feider_evening=verif_feider_evening, verif_others_evening=verif_others_evening,
                           verif_feider_difference=verif_feider_difference, verif_others_difference=verif_others_difference,
                           admin_others_morning=admin_others_morning, admin_feider_morning=admin_feider_morning, 
                           admin_feider_evening=admin_feider_evening, admin_others_evening=admin_others_evening,
                           admin_feider_difference=admin_feider_difference, admin_others_difference=admin_others_difference, 
                           tickets_created_today=tickets_created_today)

@app.route("/dashboards")
def dashboards():

    # connect to the db
    db_connection = sqlite3.connect('/workspaces/gamzat-app/db/support_tickets_daily_stats.db')
    cursor = db_connection.cursor()

    # get today's ticket qty
    cursor.execute("SELECT date_of_creation FROM daily_stats")
    dates_list = []
    check = cursor.fetchall()  # Fetch the result and get the count value
    for i in check:
        dates_list.append(i[0])

    cursor.execute("SELECT tickets_qty FROM daily_stats")
    tickets_list = []
    check2 = cursor.fetchall()  # Fetch the result and get the count value
    for i in check2:
        tickets_list.append(i[0])

    db_connection.close()

    return render_template("dashboards.html", dates_list=dates_list, tickets_list=tickets_list)

@app.route("/distributor")
def distributor():
    return render_template("distributor.html")

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html")

if __name__=="__main__":
    app.run(debug=True)
