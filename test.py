import boto3
import mysql.connector as ms
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename



def open_database_connection():
    return ms.connect(user='admin', password='adminadmin',
                     host='pennapps.ccd5u6srhchk.us-east-2.rds.amazonaws.com',
                     database='innodb')


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def update_parent_db(name, age, gender, location, phone, image):
    cnx = open_database_connection()
    mycursor = cnx.cursor()
    query = "INSERT INTO innodb.parents (child_name, age, gender, location, phone, image) VALUES ('" + name + "', " + str(age) + ", '" + gender + "', '" + location + "', " + str(phone) + ", '" + image + "')"
    mycursor.execute(query)
    cnx.commit()
    # result = mycursor.fetchall()
    cnx.close()


def update_concerned_citicen_db(name, age, gender, location, phone, image):
    cnx = open_database_connection()
    mycursor = cnx.cursor()
    query = "INSERT INTO innodb.concerned_citizen (child_name, age, gender, location, phone, image) VALUES ('" + name + "', " + str(age) + ", '" + gender + "', '" + location + "', " + str(phone) + ", '" + image + "')"
    mycursor.execute(query)
    cnx.commit()
    # result = mycursor.fetchall()
    cnx.close()


def compare(img1, img2):
    sourceFile = img1
    targetFile = img2
    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    if response['FaceMatches'] == []:
        return None
    faceMatch = response['FaceMatches'][0]
    similarity = str(faceMatch['Similarity'])
    imageSource.close()
    imageTarget.close()
    return similarity


def compare_all_parent(img):
    cnx = open_database_connection()
    mycursor = cnx.cursor()
    query = "Select image from innodb.parents"
    mycursor.execute(query)
    images = mycursor.fetchall()
    possible_images = []
    for image in images:
        similarity = compare(img, "static/imagesP/" + image[0])
        if similarity == None or int(float(similarity)) <= 90:
            continue
        else:
            if int(float(similarity)) >= 95:
                cnx.close()
                return image[0]
            else:
                possible_images.append(image)
    if len(possible_images) == 0:
        return None
    cnx.close()
    return possible_images


def compare_all_concerned_citizen(img):
    cnx = open_database_connection()
    mycursor = cnx.cursor()
    query = "Select image from innodb.concerned_citizen"
    mycursor.execute(query)
    images = mycursor.fetchall()
    possible_images = []
    print(images)
    for image in images:
        similarity = compare(img, "static/imagesC/" + image[0])
        if similarity == None or int(float(similarity)) <= 90:
            continue
        else:
            if int(float(similarity)) >= 95:
                cnx.close()
                return image[0]
            else:
                possible_images.append(image)
    if len(possible_images) == 0:
        return None
    cnx.close()
    return possible_images

