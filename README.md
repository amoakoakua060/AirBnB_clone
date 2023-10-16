# HIGH LEVEL PROGRAMMING

## AirBnB Clone

---

### Description
This project is entails the following:
- A _command interpreter__ to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
- A _website_ (the front-end) that shows the final product to everybody: static and dynamic
- A _database_ or _files_ that store data (data = objects)
- An _API_ that provides a communication interface between the front-end and your data (retrieve, create, delete, update them)

---

Command Interpreter
The command interpreter part of the this clone allows us to do the following:
- create your data model
- manage (create, update, destroy, etc) objects via a console / command interpreter
- store and persist objects to a file (JSON file)

Start
You start the program by running the executable _console.py_.
```bash
AirBnB_clone$ ./console.py
(hbnb) 
```

Examples
The following are some examples of the program
```bash
AirBnB_clone$ ./console.py
(hbnb) 
(hbnb) 
(hbnb) all
[]
(hbnb) 
(hbnb) all MyModel
** class doesn't exist **
(hbnb) show BaseModel
** instance id missing **
(hbnb) show BaseModel My_First_Model
** no instance found **
(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c51234
```

---
