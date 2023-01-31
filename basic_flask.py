from flask import Flask, jsonify, make_response
from flask import request
import psycopg2.extras
from helper import *


app = Flask(__name__)


# create_table()

@app.route("/employee", methods=["GET"])
def get_all_employees():
    response, employees = 200, []
    try:
        cur = psql_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("Select * from accounts")
        employees = cur.fetchall()
        cur.close()
    except Exception as e:
        response = 500
    return make_response(jsonify({"data": employees, "response":ERROR_CODES[response]}), response)

@app.route("/employee/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    response, employees = 200, []
    try:
        cur = psql_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("Select * from accounts where id = {}".format(emp_id))
        employees.append(cur.fetchone())
    except Exception as e:
        response = 500
    return make_response(jsonify({"data": employees, "response":ERROR_CODES[response]}), response)

@app.route("/employee/add", methods=["POST"])
def add_employee():
    response, employee = 200, []
    try:
        emp = request.json
        if emp.get("name"): 
            cur = psql_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = "insert into accounts (name, age) values ('%s', '%s') RETURNING *" % (emp.get("name"), emp.get("age"))
            cur.execute(query)
            employee.append(cur.fetchone())
            cur.close()
        else:
            response = 400
    except Exception as e:
        response = 403
    return make_response(jsonify({"data":employee, "response":ERROR_CODES[response]}), response)

@app.route("/employee/update", methods=["PATCH", "PUT"])
def update_employee():
    response = 200
    try:
        emp = request.json
        query_builder, emp_id = "", ""
        for key, value in emp.items():
            if key == "id":
                emp_id = value
            else:
                query_builder += key + "=" + "'"+value+"'"+","
        cur = psql_connection.cursor()
        query = "update accounts set {fields} where id = {id}".format(fields=query_builder[:-1],id=emp_id)
        cur.execute(query)
        cur.close()
    except Exception as e:
        response = 403
    return make_response(jsonify({"data":[], "response":ERROR_CODES[response]}), response)

@app.route("/employee/delete/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    response = 200
    try:
        cur = psql_connection.cursor()
        query = "Delete from accounts where id = {} RETURNING *".format(emp_id)
        cur.execute(query)
        cur.close()
    except Exception as e:
        response = 500
    return make_response(jsonify({"data":[], "response":ERROR_CODES[response]}), response)

# 204

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)




# /employee POST (add employee)
#           GET
#           UPDATE
#           DELETE