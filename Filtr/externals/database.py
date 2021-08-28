import sqlite3
import pathlib

# create a database table
# add data to the table
# get data from the table
# update database
# add more tables

class Database():
    ''' this is a database object that when instanciated 
        should be the name of the database its representing.

        For example:
        audiodata = Database("audiodata")

        now the audiodata object is permenantly a reference for the audiodata database

        A Database object has:
            - a name (the name of the database)
            - a location (where on the disc/cloud the database is stored)
            - data 
            - functions to access data from the database
            - functions to save the database object
            - functions to interact with other database objects
    '''
    