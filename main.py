from flask import Flask, render_template
import util

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='tippettez22'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/

# Route to insert 'Cherry' into basket_a
@app.route('/api/update_basket_a')
def update_basket_a():
    try:
        # Connect to DB
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        # Insert new row into basket_a
        cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
        connection.commit()
        # Disconnect from DB
        util.disconnect_from_db(connection, cursor)
        return "Success!"
    except Exception as e:
        return f"Error: {e}"
        
@app.route('/api/unique')
# this is how you define a function in Python
def index():
    # this is your index page
    # connect to DB
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "SELECT a, fruit_a, b, fruit_b FROM basket_a FULL JOIN basket_b ON fruit_a = fruit_b WHERE a IS NULL OR b IS NULL;")
    if record == -1:
        # you can replace this part with a 404 page
        print('Something is wrong with the SQL command')
    else:
        # this will return all column names of the select result table
        # ['customer_id','store_id','first_name','last_name','email','address_id','activebool','create_date','last_update','active']
        col_names = [desc[0] for desc in cursor.description]
        # only use the first four rows
        log = record[:4]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('index.html', sql_table = log, table_title=col_names)



if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)

