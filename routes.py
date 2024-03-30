from flask import Blueprint, render_template, request, redirect, url_for, current_app
import datetime
import uuid

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")

#defaultdict has the ability to create default values for entries that did not exist prior

def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.context_processor
def add_date_range():   
#this is how you type check(type require?) in python
    def date_range(start: datetime.datetime):
        #end number for range is non-inclusive 
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    
    return {"date_range": date_range}


@pages.route("/")
def index():
    #here we have already selected a date so we have a query string of '?date=...'
    #using fromisoformat we use this query string to generate the date in the same format of date.today() (same as in the else)
    #that becomes the new selected_date value and gets passed to index.html to create a new set of date links (navbar) based on this current date
    date_str = request.args.get("date") # ?date=...
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    #when on home page which has no date selected 
    #we assign today's date as the current date and pass it(via render_template) to the template (index.html)
    #along with date_range fucntion to be used to generate the 'navigation bar' of dates at the top of the page
    else: 
        selected_date = today_at_midnight()

    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    #what the fuck is going on here
    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})

    return render_template(
        "index.html",
        habits=habits_on_date, 
        title="Habit Tracker - Home", 
        selected_date=selected_date,
        completions=completions
        )


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = today_at_midnight()
    data_to_insert = {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
    if request.form:
        current_app.db.habits.insert_one(data_to_insert) ##<----------
    print(data_to_insert)
    return render_template("add_habit.html", title = "Habit Tracker - Add", selected_date=today) 
    #try changing selected_date here to add habits to different dates ie '?date=..'


@pages.route("/complete", methods=["POST"])
def complete():
    date_completed = request.form.get("date")
    #this gets the data from the form "habitName"
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_completed)
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for("habits.index", date=date_completed))