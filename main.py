import mysql.connector

db = mysql.connector.connect(user='root', password='Berhed=1_2_3',
                             host='localhost', database='teacherdb')
mycursor = db.cursor()


# Below is a list of initial table and column setups that I used to start the project mycursor.execute('CREATE TABLE
# teacher (teacherID int NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120));') mycursor.execute('ALTER TABLE
# teacher ADD COLUMN overall DECIMAL(9,1)') mycursor.execute('CREATE TABLE comments (commentID int NOT NULL PRIMARY
# KEY, comment TEXT);') mycursor.execute('CREATE TABLE ratings (ratingID int NOT NULL PRIMARY KEY, rating DECIMAL(9,
# 1))') mycursor.execute('CREATE TABLE schools (teacherID int NOT NULL PRIMARY KEY, school_name VARCHAR(50));')
# mycursor.execute('ALTER TABLE comments ADD COLUMN date_added VARCHAR(50);')
# While testing the project and for an initial set of information, I manually added teachers and all of their relevant
# information into my SQL tables


def run_app():
    done = False
    menu = '\n1. Add a teacher\n2. Add a rating to an existing teacher\n3. Add a comment to an existing teacher\n4. ' \
           'View a Teacher\n5. Exit\n '
    while not done:
        print(menu)
        menu_choice = int(input('Select a menu option (1-5): '))
        print()

        if menu_choice == 1:
            teacher_name = str(input('Enter the name of the teacher: '))
            mycursor.execute(f'INSERT INTO teacher (name) VALUES ("{teacher_name}")')
            mycursor.execute(f'SELECT teacherID FROM teacher WHERE name = "{teacher_name}"')
            for i in mycursor:
                num = i[0]
            teacher_rating = int(input(f'\nEnter a rating for {teacher_name} (0.0 - 5.0): '))
            mycursor.execute(f'INSERT INTO ratings (ratingID, rating) VALUES ({num}, {teacher_rating})')
            mycursor.execute(f'UPDATE teacher SET overall = {teacher_rating} WHERE teacherID = {num}')
            teacher_schools = str(input(f'\nEnter the school that {teacher_name} works for: '))
            mycursor.execute(f'INSERT INTO schools (teacherID, school_name) VALUES ({num}, "{teacher_schools}")')
            teacher_comment = str(input(f'\nEnter a short comment to explain your rating for {teacher_name}: '))
            comment_date = str(input('Enter the date that the comment was made (MM/DD/YYYY): '))
            mycursor.execute(f'INSERT INTO comments (commentID, comment, date_added) VALUES '
                             f'({num}, "{teacher_comment}", "{comment_date}")')
            db.commit()
            print(f'\n{teacher_name} has been successfully added!')

        if menu_choice == 2:
            teacher_name = str(input('\nEnter the name of the teacher you would like to rate: '))
            mycursor.execute(f'SELECT teacherID FROM teacher WHERE name = "{teacher_name}"')
            for i in mycursor:
                num = i[0]
            new_teacher_rating = int(input(f'\nEnter a new rating for {teacher_name} (0.0 - 5.0): '))
            mycursor.execute(f'INSERT INTO ratings (ratingID, rating) VALUES ({num}, {new_teacher_rating})')
            mycursor.execute(f'SELECT rating FROM ratings WHERE ratingID = {num}')
            ratings = []
            total = 0
            for i in mycursor:
                ratings.append(i[0])
            for i in ratings:
                total += i
            average = total / len(ratings)
            mycursor.execute(f'UPDATE teacher set overall = {average} WHERE teacherID = {num}')
            db.commit()
            print(f'\nYou have added a rating of {new_teacher_rating} to {teacher_name}\'s file.')

        if menu_choice == 3:
            teacher_name = str(input('\nEnter the name of the teacher you would like to comment on: '))
            mycursor.execute(f'SELECT teacherID FROM teacher WHERE name = "{teacher_name}"')
            for i in mycursor:
                num = i[0]
            new_teacher_comment = str(input('\nEnter the comment you would like to make: '))
            comment_date = str(input('Enter the date that the comment was made (MM/DD/YYYY): '))
            mycursor.execute(f'INSERT INTO comments (commentID, comment, date_added) VALUES '
                             f'({num}, "{new_teacher_comment}", {comment_date})')
            db.commit()
            print(f'\nYou have added a new comment to {teacher_name}\'s file.')

        if menu_choice == 4:
            teacher_name = str(input('Enter the name of the teacher you would like to view: '))
            mycursor.execute(f'SELECT * FROM teacher WHERE name = "{teacher_name}"')
            for i in mycursor:
                num = i[0]
                rating = i[2]
            print(f'\nName: {teacher_name}\n\nRating: {rating}\n')
            mycursor.execute(f'SELECT school_name FROM schools WHERE teacherID = {num}')
            print(f'Schools:')
            school_list = []
            for x in mycursor:
                school_list.append(x[0])
            for y in school_list:
                print(y)
            mycursor.execute(f'SELECT comment FROM comments WHERE commentID = {num}')
            print(f'\nComments:')
            comment_list = []
            for z in mycursor:
                comment_list.append(z[0])
            for w in comment_list:
                print(w)
                print()
            db.commit()

        if menu_choice == 5:
            db.commit()
            done = True
            break
    db.commit()


run_app()
