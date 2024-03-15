from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from requests import post
import pyodbc
import requests, json
from flask_sqlalchemy import SQLAlchemy

# Input Parameters
getdatacmd='SELECT * FROM Employee'
connstring='DRIVER={ODBC Driver 17 for SQL Server};SERVER=Aravind;DATABASE=TestDB;ENCRYPT=no;Trusted_Connection=yes;'

# Create the flask app
app = Flask(__name__)
# Create an API object
api = Api(app)

getCountrycmd='select * from CountryMaster'
getCitiesCountcmd='SELECT StateMaster.Name, COUNT(CityMaster.ID) AS NumberOfCities FROM CountryMaster JOIN StateMaster ON CountryMaster.ID = StateMaster.CountryID JOIN CityMaster ON StateMaster.ID = CityMaster.StateID GROUP BY StateMaster.Name;'
getEmpDetailcmd='Select * from Employee emp Join Address ad on emp.EmployeeID = ad.EmployeeID Join EmpRoles emprol on emprol.EmpID=emp.EmployeeID Join Role rl on rl.RoleID = emprol.RoleID'
getTopcmd='Select top 1* From Employee emp Join Address ad on emp.EmployeeID = ad.EmployeeID Order by 1 Asc;'
getRowscmd='Select * From Employee emp Join Address ad on emp.EmployeeID = ad.EmployeeID Where emp.EmployeeID = 2'
GetEmployeeDatacmd='Select * FRom Employee EMP join Address AD on EMP.EmployeeID = AD.EmployeeID join EmpRoles EmR on EmR.EmpID = EMP.EmployeeID join Role Ro on EmR.RoleID = Ro.RoleID'
getCitybyStatecmd='Select * from CityMaster CIM join StateMaster Stm on Stm.id = CIM.StateID join CountryMaster CM on CM.id = Stm.CountryID Where StateID = 1626'
getCityListByStateIdQuery='Select * from CityMaster CIM join StateMaster Stm on Stm.id = CIM.StateID join CountryMaster CM on CM.id = Stm.CountryID Where StateID ='
getTopRecordsQuery='Select top {0} * From CountryMaster Where id = {1}'
UpdateRecordcmd="UPDATE Employee SET EmailID = \'{0}\'   WHERE EmployeeID = {1} "
InsertRecordscmd="INSERT INTO Employee  Values ( \'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')"
DeleteEmployeeRecordcmd="DELETE FROM Employee WHERE EmployeeID= {0};"
	

#@app.route('/Countrylist')
# Class for GetCountryData
# http://127.0.0.1:5000/Countrylist
class GetCountryData(Resource):
	# GET Request
	@app.route('/Countrylist', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getCountrycmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'Countries List'},{'data': results} )
	
# GEt Cities count from data
	# http://127.0.0.1:5000/CitiesCount
class GetCitiesCountData(Resource):
	# GET Request
	@app.route('/CitiesCount', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getCitiesCountcmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'Count of cities in states List'},{'data': results} )
	
# Class for GetData
	# http://127.0.0.1:5000/Employeelist
class GetData(Resource):
	# GET Request
	@app.route('/Employeelist', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getdatacmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		# 	cursor.execute('INSERT INTO Target (id, column1, column2) values(?,?,?)', value['id'],value['column1'],value['column2'])
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'The below specified data added to database'},{'data': results} )

# Class for Empdetails
	# http://127.0.0.1:5000/Empdetails
class GetEmpdetails(Resource):
	# GET Request
	@app.route('/Empdetails', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getEmpDetailcmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'Employee Details'},{'data': results} )
	
# Bringing Top Data From Table
	# http://127.0.0.1:5000/TOP
class GetTOP(Resource):
	# GET Request
	@app.route('/TOP', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getTopcmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'Top 1 list'},{'data': results} )

# getting the Rows from Table
	# http://127.0.0.1:5000/Row
class GetRow(Resource):
	# GET Request
	@app.route('/Row', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(getRowscmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'Row'},{'data': results} )
	
# GetEmployeeData
	# http://127.0.0.1:5000/Three
class GetEmployeeData(Resource):
	# GET Request
	@app.route('/EmployeeData', methods=['GET'])
	def get(self):
		cnxn = pyodbc.connect(connstring)
		cursor = cnxn.cursor()
		cursor.execute(GetEmployeeDatacmd)
		columns = [column[0] for column in cursor.description]
		results = []
		rows = cursor.fetchall()
		for row in rows:
			value=dict(zip(columns, row))
			results.append(value)
		cnxn.commit()
		cursor.close()
		return jsonify({'message': 'GetEmployeeData'},{'data': results} )
	
#GetCityCountByState
	# http://127.0.0.1:5000/CityByState

class GetCityByState(Resource):
	# GET Request
	@app.route('/CityByState', methods=['Get'])
	def CityByState():
		if request.method == 'GET':
			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			cursor.execute(getCitybyStatecmd)
			columns = [column[0] for column in cursor.description]
			results = []
			rows = cursor.fetchall()
			for row in rows:
				value=dict(zip(columns, row))
				results.append(value)
				cnxn.commit()
				cursor.close()
				return jsonify({'message': 'CityCountByState'},{'data': results} )
			
# Api Method to get city list using state Id
# http://127.0.0.1:5000/City/GetCityListByStateID
class GetCityListByStateID(Resource):
	# Post Request
	@app.route('/City/GetCityListByStateID', methods=['POST'])
	def CityListByStateID():
		if request.method == 'POST':
			###declaring a variable to store stateid
			state_id = request.json['stateid']
			###declaring a variable to combine both strings in to one
			cmd_query = getCityListByStateIdQuery + state_id
			###Connect to DB
			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			###Executing the Query
			cursor.execute(cmd_query)
			columns = [column[0] for column in cursor.description]
			results = []
			rows = cursor.fetchall()
			###Displaying all the data fetched from the DB
			for row in rows:
				value=dict(zip(columns, row))
				results.append(value)
				cnxn.commit()
				cursor.close()
				#returning the data using custom message
				return jsonify({'message': 'CityListByStateID'},{'data': results} )			
			
# Api Method to get Top Record from Employee table
# http://127.0.0.1:5000/Emp/topRecord
class GetTopRecord(Resource):
	# Post Request
	@app.route('/Emp/TopRecord', methods=['POST'])
	def TopRecord():
		if request.method == 'POST':
			###declaring a variable to store TopRecord
			numberofrecords = request.json['numberofrecords']
			ID = request.json['ID']
			###declaring a variable to combine both strings in to one
			cmd_query = getTopRecordsQuery.format(numberofrecords, ID)
			###Connect to DB
			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			###Executing the Query
			cursor.execute(cmd_query)
			columns = [column[0] for column in cursor.description]
			results = []
			rows = cursor.fetchall()
			###Displaying all the data fetched from the DB
			for row in rows:
				value=dict(zip(columns, row))
				results.append(value)
			cnxn.commit()
			cursor.close()
				#returning the data using custom message
			return jsonify({'message': 'TopRecord'},{'data': results} ,{'Query': cmd_query} )

# Update Records		
class UpdateRecords(Resource):
	# Put Request
	@app.route('/Emp/UpdateRecords', methods=['PUT'])
	def UpdateRecord():
		if request.method == 'PUT':
			EmailID = request.json['EmailID']
			EmployeeID = request.json['EmployeeID']

			cmd_query = UpdateRecordcmd.format(EmailID, EmployeeID)

			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			cursor.execute(cmd_query)

			# columns = [column[0] for column in cursor.description]
			# results = []
			# rows = cursor.fetchall()
			# ###Displaying all the data fetched from the DB
			# for row in rows:
			# 	value=dict(zip(columns, row))
			# 	results.append(value)
			cnxn.commit()
			cursor.close()
				#returning the data using custom message
			return jsonify({'message': 'UpdateRecords'}, {'Query': cmd_query} )
	
# Class for City
# http://127.0.0.1:5000/City

class TestPost(Resource):
	# GET Request
	@app.route('/Post/create-row-in-gs', methods=['Post'])
	def create_row_in_gs():
		if request.method == 'POST':
			t_id = request.json['id']
			t_name = request.json['name']
			created_on = request.json['created_on']
			modified_on = request.json['modified_on']
			desc = request.json['desc']
			create_row_data = {'id': str(t_id),'name':str(t_name),'created-on':str(created_on),'modified-on':str(modified_on),'desc':str(desc)}
	# response = requests.post(
    #         url, data=json.dumps(create_row_data),
    #         headers={'Content-Type': 'application/json'})
			return jsonify({'message': 'City'},{'data': create_row_data} )
		
# Inserting Employee Records		
class InsertRecords(Resource):
	# Put Request
	@app.route('/InsertRecords', methods=['POST'])
	def InsertRecord():
		if request.method == 'POST':
			FirstName = request.json['FirstName']
			LastName = request.json['LastName']
			EmailID = request.json['EmailID']
			MobileNumber = request.json['MobileNumber']
			Pincode = request.json['Pincode']

			cmd_query = InsertRecordscmd.format(FirstName, LastName, EmailID, MobileNumber, Pincode)

			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			cursor.execute(cmd_query)
			cnxn.commit()
			cursor.close()
				#returning the data using custom message
			return jsonify({'message': 'InsertRecords'}, {'Query': cmd_query} )

#Deleting Employee Records		
class DeleteEmployeeRecord(Resource):
	# Put Request
	@app.route('/DeleteEmployeeRecord', methods=['POST'])
	def DeleteEmployeeRecord():
		if request.method == 'POST':
			EmployeeID = request.json['EmployeeID']
			cmd_query = DeleteEmployeeRecordcmd.format(EmployeeID)
			cnxn = pyodbc.connect(connstring)
			cursor = cnxn.cursor()
			cursor.execute(cmd_query)
			cnxn.commit()
			cursor.close()
			return jsonify({'message': 'DeleteEmployeeRecords'}, {'Query': cmd_query} )

# # Add the defined resources along with their corresponding urls
# api.add_resource(GetData, '/Employeelist')

# Driver function
if __name__ == '__main__':

	app.run(debug = True)