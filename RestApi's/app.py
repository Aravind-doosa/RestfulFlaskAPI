from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# SQL Server connection setup
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-7E4JG5I;"
    "DATABASE=tbl_EmployeeMaster;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Routes

@app.route('/api/employees', methods=['GET'])
def get_employees():
    cursor.execute("SELECT * FROM tbl_Employee")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)

@app.route('/api/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    cursor.execute("SELECT * FROM tbl_Employee WHERE EmployeeID = ?", emp_id)
    row = cursor.fetchone()
    if row:
        columns = [column[0] for column in cursor.description]
        return jsonify(dict(zip(columns, row)))
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/api/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    cursor.execute(
        "INSERT INTO tbl_Employee (EmployeeName, Age, Department) VALUES (?, ?, ?)",
        data['EmployeeName'], data['Age'], data['Department']
    )
    conn.commit()
    return jsonify({'message': 'Employee added successfully'}), 201

@app.route('/api/employee/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()
    cursor.execute(
        "UPDATE tbl_Employee SET EmployeeName = ?, Age = ?, Department = ? WHERE EmployeeID = ?",
        data['EmployeeName'], data['Age'], data['Department'], emp_id
    )
    conn.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/api/employee/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    cursor.execute("DELETE FROM tbl_Employee WHERE EmployeeID = ?", emp_id)
    conn.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.route('/api/locations', methods=['GET'])
def get_locations():
    cursor.execute("SELECT * FROM tbl_Location")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)

@app.route('/api/location', methods=['POST'])
def add_location():
    data = request.get_json()
    cursor.execute(
        "INSERT INTO tbl_Location (LocationName, Address) VALUES (?, ?)",
        data['LocationName'], data['Address']
    )
    conn.commit()
    return jsonify({'message': 'Location added successfully'}), 201

@app.route('/api/location/<int:loc_id>', methods=['PUT'])
def update_location(loc_id):
    data = request.get_json()
    cursor.execute(
        "UPDATE tbl_Location SET LocationName = ?, Address = ? WHERE LocationID = ?",
        data['LocationName'], data['Address'], loc_id
    )
    conn.commit()
    return jsonify({'message': 'Location updated successfully'})

@app.route('/api/location/<int:loc_id>', methods=['DELETE'])
def delete_location(loc_id):
    cursor.execute("DELETE FROM tbl_Location WHERE LocationID = ?", loc_id)
    conn.commit()
    return jsonify({'message': 'Location deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
