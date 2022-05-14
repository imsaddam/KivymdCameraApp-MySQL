import mysql.connector
import os


def digital_to_binary(image_name):
    # Convert digital data to binary format
    with open(image_name, 'rb') as file:
        binaryData = file.read()
    return binaryData


my_db = mysql.connector.connect(host="localhost", user="root", passwd="")
db_create = my_db.cursor()

# Create a database
db_create.execute("CREATE DATABASE IF NOT EXISTS user_registration")
my_db.database = "user_registration"
# Create a Table
db_create.execute("""CREATE TABLE IF NOT EXISTS images(
    image_id int(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    image_path varchar(1000) CHARACTER SET utf8 NOT NULL,
    image_name BLOB ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)


def localImageDelete(images):
    for image in images:
        try:
            os.remove(image)
        except OSError as e:
            print("Error: %s : %s" % (image, e.strerror))


def save_images(images):
    binary_pictures = []
    for image in images:
        picture = digital_to_binary(image)
        binary_pictures.append(picture)

    try:
        cursor = my_db.cursor()
        insert_query = "INSERT INTO images(image_path,image_name) VALUES(%s,%s)"
        parameters = list(zip(images, binary_pictures))
        cursor.executemany(insert_query, parameters)
        my_db.commit()
        # deletion code
        localImageDelete(images)
    except Exception as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        my_db.close()

    return 1


def login_user(image_id, image_name):
    cursor = my_db.cursor()
    user_query = "SELECT image_id, image_name FROM  images"
    # parameters = (email, password)
    cursor.execute(user_query)
    cursor.fetchall()
    my_db.commit()
    my_db.close()
    return 1
