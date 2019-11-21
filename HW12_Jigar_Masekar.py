"""
@author- Jigar Masekar

   HW12 Code for the fourth and final iteration of project

"""

import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/inst")
def instructor_summary():
    """ function which renders manually entered data into the designed web page template"""
    data = [
        {
            'cwid': '98762',
            'name': 'Hawking, S',
            'dept': 'CS',
            'course': 'CS 501',
            'nos': 1
        },
        {
            'cwid': '98762',
            'name': 'Hawking, S',
            'dept': 'CS',
            'course': 'CS 546',
            'nos': 1
        }
    ]

    return render_template("inst_table.html",
                           title="Stevens Repository",
                           table_title="Instructor Summary",
                           instructors=data)


@app.route("/dbi")
def inst_summary():
    """ function which renders data retrieved from a database into the designed web page template"""

    db_file = "/Users/jigar/sqlite/startup.db"

    try:
        db = sqlite3.connect(db_file)
    except sqlite3.OperationalError:
        return f"Error! Unable to open database."
    else:
        query = """select instructors.CWID, instructors.Name, instructors.Dept, grades.Course, count(*) as 
                   Number_of_Student from instructors join grades on instructors.CWID = grades.InstructorCWID 
                   group by Course, InstructorCWID"""

        data = [{"cwid": CWID, "name": Name, "dept": Dept, "course": Course, "students": Number_of_Student}
                for CWID, Name, Dept, Course, Number_of_Student in db.execute(query)]

        db.close()

        return render_template('inst_table.html',
                               title="Stevens Repository",
                               table_title="Instructor Summary",
                               instructors=data)


app.run(debug=True)
