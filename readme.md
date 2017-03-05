# Catalog App

This is the project 5 for Full Stack Web Developer Nanodegree Program. This web app lists different categories and items within each category. Logged in users have more authorities with regards to modifying categories or items.

## Functionalities of this web app

- Any user, even not logged in, can view any category and any item.
- The web app uses OAuth, and in order to login, you need to have a google plus or facebook account.
- Only logged-in user can create a new category or create a new item under an existing category.
- Logged-in user can edit or delete the category or item he or she created.
- Any category and item can only be edited or deleted by its creator.
- Please note, if you find that the facebook login button is not displayed correctly, use the google chrome in the incognito mode to open the web app and refresh the login page.

## Code Usage

The web app depends on lots of python packages, and therefore it is highly recommended you install the linux virtual machine in order to run the app successfully. Please see the following steps.

1. Make sure you have vagrant and virtualbox instanlled on your desktop.

2. Download the repository and unzip the folder to your desktop.

3. Open you terminal, move to the folder ```/vagrant``` and type the command to setup the virtual machine.
```
vagrant up
```

4. If everything is fine, you should have a new virtual machine installed, and type the command to log into it.
```
vagrant ssh
```

5. After successfully logged into your virtual machine, type the following command to move to the web app folder.
```
cd /vagrant/catalog
```

6. Now type the following command to create a database for the web app.
```
python database_setup.py
```

7. You should have a file called ```catalog.db``` now. Type the following command to insert some data into the database.
```
python item_insert.py
```

8. Catalog App is good to go, now type the command to finally start it.
```
python index.py
```

9. Open your web browser (Google Chrome Recommended), type ```localhost:5000``` and have fun!

10. If you want to stop the virtual machine, make sure you log out of the virtual machine and type the following command.
```
vagrant halt
```

## JSON Endpoints

This web app support several JSON Endpoints.

1. JSON data enpoint for all the categories.
```
localhost:5000/categories/JSON
```

2. JSON data endpoint for a category and all items of that category. Please note ```category_id``` is a number, and it is the id for a category.
```
localhost:5000/categories/category_id/JSON
```

3. JSON data endpoint for an item, under a certan category. Please note ```item_id``` is a number, and it is the id for an item.
```
localhost:5000/categories/category_id/items/item_id/JSON
```

## License
This project is licensed under the terms of the **MIT** license.