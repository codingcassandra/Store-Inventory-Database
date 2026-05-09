For my project, I built a command-line app using Python that connects to a MySQL database to handle a basic e-commerce system. 
The main goal was to focus on security, so instead of writing SQL queries directly in my Python code, I used stored procedures 
for everything. The database was already set up with tables for users, products, and sales, and I had to make sure my script 
worked with that specific schema without changing it.

I implemented a menu driven interface where users first log in through a "Users" table that defines if they are an Admin or a 
Customer. If you're an admin, the Python script lets you add or edit products and check out the total sales. If you're a 
customer, you can create an account, sign in, place new orders, and view or cancel your existing ones. Basically, I used the 
mysql-connector-python library to bridge the gap between my Python code and the database, making sure every CRUD operation was 
handled safely through the backend procedures.
