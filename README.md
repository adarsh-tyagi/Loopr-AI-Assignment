### Loopr LMS Assignment

This assignment solution consists of APIs related to small Library Management System (LMS).

1. Register: POST {host}/main/register
   Provide username and password, if users already exists then it will give that result otherwise create the new user with unique user id and provide that user id in response also.

2. Login: POST {host}/main/login
   Provide username and password, it will authenticate the user and give back the authentication token.

3. Create Book: POST {host}/main/newbook
   Provide the book details like name, price, author and it will create the new book entry in database.

4. Search Books: GET {host}/main/searchbook
   Provide the basic search key related to book name and it will search the books maching the name with search key and return the list of books with all details like name, price, author, status (id available or checked out).

5. Issue Book: POST {host}/main/issuebook
   Provide the book id and number of days and it will issue that book (if available) to the current logged in user for that number of days.

6. Return Book: POST {host}/main/returnbook
   Priovide the book id and it will return the book as available back in database, change back the return date and remove the user to whom book was earlier issued and book again show as available.

7. Delete User: DELETE {host}/main/deleteuser
   Delete the current logged in user.

8. Delete Book: DELETE {host}/main/deletebook
   Provide the book id and it will delete that book from database if that book is available and not already issued to any user.


## Steps to run:
1. Install all the dependencies mentioned in requirements.txt file using command
    `pip install -r requirements.txt`

2. Enter the loopr outer folder and run the project using command:
    `python manage.py runserver 0.0.0.0:<port>`

3. Start using using the api using your own host and port with the urls mentioned in above APIs.

### NOTE: 
- Login first and get the token value and pass that token to the all other APIs authorization header as "Token <token_key>"
- Pass the POST request data in form data format and GET/DELETE request data in request params.
