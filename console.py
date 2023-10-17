#!/usr/bin/python3


"""
module contains the the HBNBCommand class
"""


import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
import models


cls_names = {}
cls_names["BaseModel"] = BaseModel
cls_names["User"] = User
cls_names["State"] = State
cls_names["City"] = City
cls_names["Amenity"] = Amenity
cls_names["Place"] = Place
cls_names["Review"] = Review


def update_inst(instance, attr, attr_value):
    """ add or update attribute of instance """

    value = getattr(instance, attr, None)
    if value is None:
        setattr(
            instance,
            attr, attr_value.replace('"', "")
        )
    else:
        value_type = type(getattr(instance, attr))
        setattr(instance, attr,
                value_type(attr_value.replace('"', "")))


def update_inst_with_dict(command):
    """ add or update multiple attributes with dict """

    command_list = command[
        command.index("{") + 1:command.index("}")
    ].replace(":", "").split(" ")
    arguments = command[
        :command.index("{")
    ].replace('"', '').replace(", ", "").replace(".update(", " ").split(" ")
    if len(arguments) == 0 or arguments[0] == "":
        print("** class name missing **")
    elif arguments[0] not in cls_names:
        print("** class doesn't exist **")
    elif len(arguments) < 2:
        print("** instance id missing **")
    else:
        objects = models.storage.all()
        key = ".".join(arguments)
        if key in objects.keys():
            if len(command_list) == 0:
                print("** attribute name missing **")
            elif len(arguments) % 2 != 0:
                print("** value missing **")
            else:
                instance = objects[key]
                for i in range(0, len(command_list), 2):
                    update_inst(
                        instance,
                        command_list[i].replace("'", "").replace('"', ""),
                        command_list[i + 1]
                    )
                instance.save()
        else:
            print("** no instance found **")


def get_objs(arguments):
    """ get the objects in storage """

    objects = models.storage.all()
    objects_list = []
    for key, value in objects.items():
        if arguments[0] == "":
            objects_list.append(str(value))
            continue
        if arguments[0] == key[:len(arguments[0])]:
            objects_list.append(str(value))
    return objects_list


def get_cmd(command):
    """ reconstruct command """

    if command.find("(") + 1 == command.find(")"):
        return "{}".format(command[:command.find(".")])

    return "{} {}".format(
        command[:command.find(".")],
        command[command.find(
            "(") + 1:-1].replace('"', '').replace(",", "")
        )


class HBNBCommand(cmd.Cmd):
    """ This is a commandline interpreter for AirBnB """

    prompt = "(hbnb) "

    def do_update(self, command):
        """ update command's implementation """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in cls_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                if len(arguments) < 3:
                    print("** attribute name missing **")
                elif len(arguments) < 4:
                    print("** value missing **")
                else:
                    instance = objects[key]
                    update_inst(instance, arguments[2], arguments[3])
                    instance.save()
            else:
                print("** no instance found **")

    def onecmd(self, command):
        """ handle commands such as <Model>.all(), <Model>.show(), etc """

        c = command.split(".")
        if len(c) > 1:
            func = command[command.index(".") + 1:command.index("(")]
            if func == "all":
                return self.do_all(command[:command.index(".")])
            elif func == "show":
                return self.do_show(get_cmd(command))
            elif func == "destroy":
                return self.do_destroy(get_cmd(command))
            elif func == "update":
                if command.find("{") >= 0:
                    update_inst_with_dict(command)
                    return
                else:
                    return self.do_update(get_cmd(command))
            elif func == "count":
                print(len(get_objs(get_cmd(command))))
                return
        return super(HBNBCommand, self).onecmd(command)

    def do_all(self, command):
        """ all command's implementation """

        arguments = command.split(" ")

        if arguments[0] != "" and arguments[0] not in cls_names:
            print("** class doesn't exist **")
            return
        print(get_objs(arguments))

    def do_destroy(self, command):
        """ destroy command's implementation """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in cls_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                instance = objects[key]
                models.storage.remove(key)
                models.storage.save()
                del instance
                return

            print("** no instance found **")

    def do_show(self, command):
        """ implementation of show """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in cls_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                print(objects[key])
                return

            print("** no instance found **")

    def do_create(self, command):
        """ implementation of create """

        if command == "":
            print("** class name missing **")
        elif command not in cls_names.keys():
            print("** class doesn't exist **")
        else:
            instance = (cls_names[command])()
            print(command, instance)
            instance.save()
            print(instance.id)

    def do_quit(self, command):
        """ quit command's implementation """

        return True

    def help_quit(self):
        """ quit command's help """

        print('Quit command to exit the program\n')

    def do_EOF(self, command):
        """ EOF command's implementation """

        print()
        return True

    def emptyline(self):
        """ implementation of emptyline """

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
