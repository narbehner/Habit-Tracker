from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

habits=["test habit", "test habit 2"]

@app.context_processor
def add_date_range():   
#this is how you type check(type require?) in python
    def date_range(start: datetime.date):
        #end number for range is non-inclusive 
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    
    return {"date_range": date_range}

@app.route("/")
def index():
    #here we have already selected a date so we have a query string of '?date=...'
    #using fromisoformat we use this query string to generate the date in the same format of date.today() (same as in the else)
    #that becomes the new selected_date value and gets passed to index.html to create a new set of date links (navbar) based on this current date
    date_str = request.args.get("date") # ?date=...
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    #when on home page which has no date selected 
    #we assign today's date as the current date and pass it(via render_template) to the template (index.html)
    #along with date_range fucntion to be used to generate the 'navigation bar' of dates at the top of the page
    else: 
        selected_date = datetime.date.today()
    return render_template(
        "index.html",
        habits=habits, 
        title="Habit Tracker - Home", 
        #date_range=date_range, 
        selected_date=selected_date
        )

@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))

    print(habits)
    return render_template("add_habit.html", title = "Habit Tracker - Add", selected_date=datetime.date.today()) 
    #try changing selected_date here to add habits to different dates ie '?date=..'