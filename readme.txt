Required Library -
    flask, flask-socketio, psutil, signal, inspect

NOTE - Refer functions_lookup.py file to import functions to be exposed as a service

HOW TO RUN -
1. Run "python utility.py"
2. Head to localhost:5000
3. Click on 'Use Service' Button.
4. A new server will automatically start on a new port to expose the available functions as service.
5. Use postman to issue services on the listed endpoints.
6. Refer examples at the end of this file to understand how to issue service through postman.


About Utility -
1. Functions are defined in functions.py

2. All functions can be imported in function_lookup.py which generated a lookup dictionary and exports it.
    To import new functions from other files simply add this line in function_lookup.py - 
        #functions_list += [o for o in getmembers(functions) if isfunction(o[1])]
            -where functions is name of the file imported containing functions

3. utility.py file is the main file where, socket connection and main server is coded.
    Upon starting this file a server on port 5000 is available to all users. It has a button to start services.
    On click the available functions are exposed as a service to the user through unique port number (aka unique server for each user is started)
    
    Note - Service is available as long as the user remains on the page, as soon as disconnected, the port is free and server is closed.
            The free port is now available for any new user when he requests a service.

4. service.py file is where a dynamic route is defined
    This dynamic route takes function_name as input from the user in route request,
    and if the function_name matches a function in function_lookup dictionary and has been exposed as a service it calls it and returns the result 
    given right parameters are passed by the user.



EXAMPLES - 

#1. Number Multiplication

URL - http://127.0.0.1:5000/dynamic/multiply
Data - 
{
    "a": 5,
    "b": 3,
    "c": 7
}

Output - 
{
    "result": 105
}



#2. Number Addition

URL - http://127.0.0.1:5000/dynamic/addition
Data - 
{
    "a": 5,
    "b": 3,
    "c": 7.7,
    "d": 10
}

Output - 
{
    "result": 25.7
}



#3. String Addition/Concatenation

URL - http://127.0.0.1:5000/dynamic/addition
Data - 
{
    "a": "Ron",
    "b": 3,
    "c": "Harry",
    "d": 10
}

Output - 
{
    "result": "Ron3Harry10"
}



#4. User registeration with right paramater names as keys

URL - http://127.0.0.1:5000/dynamic/register_user
Data -
{
    "name": "Harry",
    "age": 18,
    "contact": 12512521,
    "email": "harry@ss.co",
    "password": "harry12345"
}

Output -
{
    "result": "User has been registered"
}



#5. User registeration with wrong/missing paramater names as keys

URL - http://127.0.0.1:5000/dynamic/register_user
Data - 
{
    "name": "Harry",
    "age": 18,
    "contact": 12512521
}

Output - 
{
    "result": "email,password required!"
}



#6. Create new post with right parameter names as keys

URL - http://127.0.0.1:5000/dynamic/create_post
Data - 
{
    "title": "Dynamic Utility",
    "author": "Tushar",
    "description": "Dynamically calls a function using user given function name and data"
}

Output -
{
    "result": "Dynamic Utility - By Tushar --> Dynamically calls a function using user given function name and data"
}



#7. Create post with wrong/missing parameter names as keys

URL - http://127.0.0.1:5000/dynamic/create_post
Data - 
{
    "topic": "Dynamic Utility",
    "by": "Tushar",
    "description": "Dynamically calls a function using user given function name and data"
}

Output -
{
    "reason": "title,description,author parameters required! Some are missing!",
    "result": "unknown"
}
