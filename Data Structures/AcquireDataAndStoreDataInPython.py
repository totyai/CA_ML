#!/usr/bin/env python
# coding: utf-8

# # Acquiring And Storing Data In Python

# This lab is targeted at students who are familiar with Python who are looking to query an API and store data into a database.

# ## Querying APIs Using Python

# Python is a very powerful language that can quickly be used to ingest data from an Application Program Interface (API) and make it available for consumption later by storing it in a database. APIs specify how software components interact. 
# 
# There are different methods that are used to interact with HTTP APIs.
# 
# | Method | Type   |            Description                |
# |--------|--------|---------------------------------------|
# | POST   | Create |  Used to create data                  |
# | GET    | Read   |  Used to retrieve data                |
# | PUT    | Update/Modify | Updates the entity if it exists / creates a new one if it doesnt | 
# | PATCH  | Update/Replace | Applies a partial update to data |
# | DELETE | Remove |  Deletes data |

# ## **Lab:** Querying an API Using Python

# In this lab we will query an API in Python, and extract specific fields to print.  Data can be exchanged in any format but we will receive data in [Java Script Object Notation (JSON)](https://www.json.org/json-en.html) which allows for ease of understanding.

# Let's take a look at a quick example of how to query an API using python. We'll be querying a cat fact API, which will return a random fact about cats (along with other some other data). Take a look at the example below and try to understand how program works. We'll go over the inner workings of it aftewards.
# 
# **NOTE**: Because we're querying a random fact, the results commented in the code will be different when actually ran.

# In[6]:


get_ipython().system('pip install requests')
import requests #1

response = requests.get('https://cat-fact.herokuapp.com/facts/random') #2

print(response) #3
# <Response [200]>

data = response.json() #4

print(data) #5
# {'used': False, 'source': 'api', 'type': 'cat', 'deleted': False, '_id': '591f98803b90f7150a19c23f', '__v': 0, 'text': "Cats can't taste sweets.", 'updatedAt': '2020-05-10T20:20:11.457Z', 'createdAt': '2018-01-04T01:10:54.673Z', 'status': {'verified': True, 'sentCount': 1}, 'user': '5a9ac18c7478810ea6c06381'}

print(data['text']) #6
# Cats can't taste sweets.


# Diving into our code, let's go over how this all works.
# - Notice that line `#1` imports the `requests` library. This is a very common python library used HTTP requests, and is the backbone of our API consumer.
# - At line `#2` is where the actual quering of the API occurs. The `requests` package will connect to the URL, retreive the data and store it in an easy-to-use python object. This data is then store in a variable called `response`
# - Line `#3` prints the result of our `request` call. The varible `response` if of type `Response` and shows us one value, 200. This is the status code from the HTTP server. A status of 200 means that everything went smoothly.
# - Now we need to actually work with the data that we received from the cat fact web API. This is done on line `#4`. The `requests` package makes working with JSON data extremly easy, by simply invoking the `.json()` method. This will in return, provide a JSON object of the result (if the result was written in JSON format, otherwise raise an error). Since we know JSON objects are key/value based, this becomes a dictonary type in python, which makes retreiving information a piece of cake.
# - The raw JSON (dictonary) data is printed on line `#5`. This shows all the data we have to work with.
# - From the API, the `text` field contains the fact. The other fields, such as `status`, `_id`, etc, provide extra information about the fact. Line `#6` prints out the fact to the console.
# 
# This can be simplified into a Bash one-line that you can run:
# ```bash
# python -c "import requests; print(requests.get('https://cat-fact.herokuapp.com/facts/random').json()['text'])"
# ```

# ## Storing Data from an API

# Now that we have the basic understanding of how to query an API, let's expand our knowledge to query an API to build a database.
# We're going to build a rudimentary book catalog.
# To build the database, we will query the [Open Books Library API](https://openlibrary.org/dev/docs/api/books), which contains a lot of information about a book based on the books ISBN number. 

# ### The Database Model

# The database will have a very simple design, with the main entites being _Books_, _Authors_, and _Themes_.
# A _book_ will consist of an ISBN, title, subtitle, and number of pages.
# Remember it is proper to have a primary key that is unique to identify the row.
# Fortuantely, an ISBN is a unique identifier for a book, so we'll use that as our primary key.
# If you're thinking, _"But isn't there an ISBN 10 and an ISBN 13 that can reference the same book?"_, you're not wrong
# However, for the sake of brevity, only the ISBN queried will be used.
# An _author_ will consist of the author's name and an `id` that will incriment every time a new author is inserted into the table.
# Finally, a _theme_ has a similar schema as an author, it has the name of the theme, and an automatically incrementing `id`.
# 
# The last part is tying our data together.
# A book may have one to many authors, and as well, an author may have one to many books.
# This type of relationship is called a [many-to-many relationship](https://en.wikipedia.org/wiki/Many-to-many_(data_model)).
# To map the _book_ and _author_ entities together, we use a [link table](https://en.wikipedia.org/wiki/Associative_entity).
# Using a link table helps reduce duplicate data within a table.
# For example, let's look at the book: [Design Patterns: Elements of Reusable Object Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns).
# This book has four authors associated with it.
# If we had included an `author` column in the _book_ table, there would be multiple rows with the same title, isbn, subtitle, etc.
# The only difference would be the author's name was changed.
# Ignoring the fact that the ISBN in our table must be unique, you can see how adding in many books can result in mounds of duplicate data, and this is not desirablable.
# The same principle is applied to a _book_ and _theme_ relationship.
# 
# For a graphical represnetation, refer to the entitiy-relationship diagram below.

# ![image of our data models](./assets/lab6/erd.png)

# ## **Lab:** Putting it together by reading data from an API and Storing it into a database.

# Now to build a new Python notebook that will automate the process. The script will execute the following:
# - Connecting to the database
# - Creating the database
# - Creating the tables for database
# - For each ISBN in a list of ISBNs:
#  - Query the OpenLibrary API to retreive the book data
#  - Manipulate the returned JSON data into python variables
#  - Insert the data into the database

# ### Connect to the database
# 
# Start to create the Python notebook by clicking File > New notebook > conda_python3:
# 
# ![image of our data models](./assets/lab6/new_notebook.png)
# 
# Name the notebook `book-catalog`. Next, fill in the empty code block by adding in the required libraries, and the connection to the database in RDS.
# 
# ```python
# ! pip install requests mysql-connector
# 
# # import the required libraries
# import re
# import requests
# import mysql.connector
# import boto3
# 
# # Use AWS boto3 sdk to retreive RDS MySQL database endpoint
# rds_client = boto3.client('rds')
# response = rds_client.describe_db_instances()
# endpoint = response['DBInstances'][0]['Endpoint']['Address']
# 
# db = mysql.connector.connect(
#   host=endpoint,
#   user="admin",
#   passwd="demotest123"
# )
# ```

# ### Create the database
# 
# Similar to previous labs, we'll get a `cursor` from the database object and execute some raw SQL queries to build our database.
# 
# ```python
# cursor = db.cursor()
# 
# # create database
# cursor.execute('DROP DATABASE IF EXISTS book_catalog')
# cursor.execute('CREATE DATABASE IF NOT EXISTS book_catalog')
# cursor.execute('USE book_catalog')
# ```

# In[ ]:





# ### Create the Tables for the Database
# 
# Below is the code for creating the tables in the MySQL database.
# If you're not sure what everything means, don't fret.
# Just make sure you can see how the fields in the diagram above match the fields within the `CREATE TABLE` queries.
# 
# ```python
# # create tables
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS books (
#     isbn VARCHAR(13) PRIMARY KEY,
#     title TEXT NOT NULL,
#     subtitle TEXT DEFAULT NULL,
#     no_pages INT DEFAULT 0
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# ''')
# 
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS authors (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name TEXT NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# ''')
# 
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS themes(
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name TEXT NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# ''')
# 
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS authors_books (
#     isbn VARCHAR(13),
#     author_id INT,
#     PRIMARY KEY (isbn, author_id),
#     FOREIGN KEY (isbn) REFERENCES books(isbn),
#     FOREIGN KEY (author_id) REFERENCES authors(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# ''')
# 
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS books_themes (
#     isbn VARCHAR(13),
#     theme_id INT,
#     PRIMARY KEY (isbn, theme_id),
#     FOREIGN KEY (isbn) REFERENCES books(isbn),
#     FOREIGN KEY (theme_id) REFERENCES themes(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# ''')
# db.commit()
# cursor.close()
# ```

# ### Setup the Data for the API
# 
# Next, create a list of ISBNs to be queried against the API. The `API_URL` variable is the base URL for the OpenLibrary API, and afterwards, the parameters can be added in.
# 
# ```python
# # the base URL to query the books API
# API_URL = 'http://openlibrary.org/api/books'
# 
# # a list of ISBNs to be added to the catalog
# isbn_list = [
#     '978-0201853926',
#     '0201558025',
#     '978-1-93435-645-6',
#     '9780199218462',
#     '978-4915512377',
#     '1593278551',
#     '0811862151',
#     '9780761174707',
#     '1844834115',
#     '9781408845646',
#     '9780201896831',
#     '0321534964',
#     '1408855895',
#     '0590353403',
# ]
# ```

# ### Query the OpenLibrary API
# 
# For each ISBN in the list, we build an `isbn_payload`.
# This is the format in which the OpenLibrary API requires the `bibkeys` parameter to be formatted.
# For example, using the book from before, the `isbn_payload` would be set to `ISBN:0201633612`.
# Next, set up the parameters required for the API to retreive the book's data.
# We set the `format` to return JSON, and the `jscmd` to _data_.
# With all the parameters set, use the `requests` package to make the call to the API.
# 
# ```python
# # cycle through the list and query the API
# for isbn in isbn_list:
#     # grab a fresh cursor
#     cursor = db.cursor()
# 
#     # set up proper search parameters for the API
#     isbn_payload = 'ISBN:%s' % isbn
# 
#     # set all parameters needed to make the request
#     params = {
#         'bibkeys':isbn_payload,
#         'format':'json',
#         'jscmd':'data'
#     }
# 
#     # send the request
#     r = requests.get(API_URL, params)
# ```
# 
# Go to http://openlibrary.org/api/books?bibkeys=ISBN:0201633612&format=json&jscmd=data in your web browser to view the raw JSON output from the API.

# ### Retreiving the Book and Manipulating the Data
# 
# To retreive the book data, we convert the reponse from the API into JSON, and access the object data for the key `isbn_payload`.
# Which if you recall is ISBN:0201633612 for our example book.
# From there we can obtain all the information we need from the JSON data.
# For each piece of information we need, check that it is in the response and then assign it to a variable.
# For the `authors` and `themes`, the python code creates a list of strings containing only the text data from the JSON.
# Finally, the `isbn_clean` variable removes any extra characters and leaves only digits to meet the ISBN VARCHAR(13) requirement.
# 
# ```python
#     # retreive the book from the JSON data
#     book = r.json()[isbn_payload]
# 
#     # obtain all information we require to put into our database
#     title = book['title']
#     subtitle = book['subtitle'] if 'subtitle' in book else ''
#     no_pages = book['number_of_pages'] if 'number_of_pages' in book else 0
#     authors = [auth['name'] for auth in book['authors']]
#     themes = [subj['name'] for subj in book['subjects']] if 'subjects' in book else []
# 
#     # clean up ISBN from input (numbers only to fit the VARCHAR(13) limit)
#     isbn_clean = re.sub('[^0-9]', '', isbn)
# ```

# ### Insert Data into the Database
# Inserting the book datay is very straight forward.
# Take the data from earlier and execute an `INSERT` statement.
# 
# ```python
#     # insert data into database
# 
#     # insert book
#     insert_book_stmt = 'INSERT INTO books(isbn, title, subtitle, no_pages) VALUES( %s, %s, %s, %s )'
#     cursor.execute(insert_book_stmt, (isbn_clean, title, subtitle, no_pages))
# ```
# 
# To insert the authors into the database is a bit more complex.
# Each author of the book needs to be inserted in the database, and then it needs to be added into the `authors_books` table as well.
# However, we can't blindly insert each author into the database, otherwise we would have duplicate author names with different ids, rendering our link table useless.
# To solve this issue, query the `authors` table first and check if the author already exists.
# If it doesn't, insert the new author and use `cursor.lastrowid` to get the newly inserted author's id.
# However, if the author does exist, retreive the `id` from the SELECT statement.
# Now that the hard part is out of the way, the link table data can be inserted as simply as the book.
# 
# ```python
#     # insert authors
#     # check if author exists in DB otherwise create and retreive the ID
#     insert_author_stmt = 'INSERT INTO authors(name) VALUES(%(name)s)'
#     insert_authors_books_stmt = 'INSERT INTO authors_books VALUES (%s, %s)'
#     for author in authors:
#         select_author_id_stmt = 'SELECT id FROM authors WHERE name = "{}"'.format(author)
#         cursor.execute(select_author_id_stmt)
#         result = cursor.fetchone()
# 
#         if result is None:
#             cursor.execute(insert_author_stmt, {'name':author})
#             author_id = cursor.lastrowid
#         else:
#             author_id = result[0]
# 
#         # insert author_id into authors_books
#         cursor.execute(insert_authors_books_stmt, (isbn_clean, author_id))
# ```
# 
# **NOTE**: The line `select_author_id_stmt = 'SELECT id FROM authors WHERE name = "{}"'.format(author)` is prone to SQL injection and shouldn't be used in a production environment. It is only for demonstration purposes.
# 
# To add themes into the database, follow the same procedure as the authors.
# 
# ```python
#     # insert themes
#     # check if theme exists in DB otherwise create and retreive the ID
#     insert_theme_stmt = 'INSERT INTO themes(name) VALUES(%(name)s)'
#     insert_books_themes_stmt = 'INSERT INTO books_themes VALUES (%s, %s)'
#     for theme in themes:
#         select_theme_id_stmt = 'SELECT id FROM themes WHERE name = "{}"'.format(theme)
#         cursor.execute(select_theme_id_stmt)
#         result = cursor.fetchone()
# 
#         if result is None:
#             cursor.execute(insert_theme_stmt, {'name':theme})
#             theme_id = cursor.lastrowid
#         else:
#             theme_id = result[0]
# 
#         # insert theme_id into books_themes
#         cursor.execute(insert_books_themes_stmt, (isbn_clean, theme_id))
# ```
# 
# Finally, before moving on to the next ISBN in the list, commit the changes to the database and close the cursor.
# 
# ```python
#     db.commit()
#     cursor.close()
# ```

# ### **Solution**: Python Code in its Entirety

# In[21]:


get_ipython().system(' pip install requests mysql-connector')

# import the required libraries
import re
import requests
import mysql.connector
import boto3

# Use AWS boto3 sdk to retreive RDS MySQL database endpoint
rds_client = boto3.client('rds')
response = rds_client.describe_db_instances()
endpoint = response['DBInstances'][0]['Endpoint']['Address']

db = mysql.connector.connect(
  host=endpoint,
  user="admin",
  passwd="demotest123"
)

cursor = db.cursor()

# create database
cursor.execute('DROP DATABASE IF EXISTS book_catalog')
cursor.execute('CREATE DATABASE IF NOT EXISTS book_catalog')
cursor.execute('USE book_catalog')

# create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    isbn VARCHAR(13) PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT DEFAULT NULL,
    no_pages INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS authors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS themes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS authors_books (
    isbn VARCHAR(13),
    author_id INT,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn),
    FOREIGN KEY (author_id) REFERENCES authors(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS books_themes (
    isbn VARCHAR(13),
    theme_id INT,
    PRIMARY KEY (isbn, theme_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn),
    FOREIGN KEY (theme_id) REFERENCES themes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
''')
db.commit()
cursor.close()

# the base URL to query the books API
API_URL = 'http://openlibrary.org/api/books'

# a list of ISBNs to be added to the catalog
isbn_list = [
    '978-0201853926',
    '0201558025',
    '978-1-93435-645-6',
    '9780199218462',
    '978-4915512377',
    '1593278551',
    '0811862151',
    '9780761174707',
    '1844834115',
    '9781408845646',
    '9780201896831',
    '0321534964',
    '1408855895',
    '0590353403',
]

# cycle through the list and query the API
for isbn in isbn_list:
    # grab a fresh cursor
    cursor = db.cursor()

    # set up proper search parameters for the API
    isbn_payload = 'ISBN:%s' % isbn

    # set all parameters needed to make the request
    params = {
        'bibkeys':isbn_payload,
        'format':'json',
        'jscmd':'data'
    }

    # send the request
    r = requests.get(API_URL, params)

    # retreive the book from the JSON data
    book = r.json()[isbn_payload]

    # obtain all information we require to put into our database
    title = book['title']
    subtitle = book['subtitle'] if 'subtitle' in book else ''
    no_pages = book['number_of_pages'] if 'number_of_pages' in book else 0
    authors = [auth['name'] for auth in book['authors']]
    themes = [subj['name'] for subj in book['subjects']] if 'subjects' in book else []

    # clean up ISBN from input (numbers only to fit the VARCHAR(13) limit)
    isbn_clean = re.sub('[^0-9]', '', isbn)

    # insert data into database

    # insert book
    insert_book_stmt = 'INSERT INTO books(isbn, title, subtitle, no_pages) VALUES( %s, %s, %s, %s )'
    cursor.execute(insert_book_stmt, (isbn_clean, title, subtitle, no_pages))

    # insert authors
    # check if author exists in DB otherwise create and retreive the ID
    insert_author_stmt = 'INSERT INTO authors(name) VALUES(%(name)s)'
    insert_authors_books_stmt = 'INSERT INTO authors_books VALUES (%s, %s)'
    for author in authors:
        select_author_id_stmt = 'SELECT id FROM authors WHERE name = "{}"'.format(author)
        cursor.execute(select_author_id_stmt)
        result = cursor.fetchone()

        if result is None:
            cursor.execute(insert_author_stmt, {'name':author})
            author_id = cursor.lastrowid
        else:
            author_id = result[0]

        # insert author_id into authors_books
        cursor.execute(insert_authors_books_stmt, (isbn_clean, author_id))

    # insert themes
    # check if theme exists in DB otherwise create and retreive the ID
    insert_theme_stmt = 'INSERT INTO themes(name) VALUES(%(name)s)'
    insert_books_themes_stmt = 'INSERT INTO books_themes VALUES (%s, %s)'
    for theme in themes:
        select_theme_id_stmt = 'SELECT id FROM themes WHERE name = "{}"'.format(theme)
        cursor.execute(select_theme_id_stmt)
        result = cursor.fetchone()

        if result is None:
            cursor.execute(insert_theme_stmt, {'name':theme})
            theme_id = cursor.lastrowid
        else:
            theme_id = result[0]

        # insert theme_id into books_themes
        cursor.execute(insert_books_themes_stmt, (isbn_clean, theme_id))

    db.commit()
    cursor.close()


# **BONUS**: Using the book-catalog python notebook, add in your own ISBN to be inserted into the database. Also you can confirm the data is stored by using SELECT SQL statements.
