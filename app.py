import test
import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import datetime


class S:
    sess = ""
    inf = ["", "", 0, "", "", 0]
    result = ""

UPLOAD_FOLDER = 'static/imagesC'
UPLOAD_FOLDERP = 'static/imagesP'

ALLOWED_EXTENSIONS = ['jpg']
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDERP'] = UPLOAD_FOLDERP


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/citizen', methods=['GET', 'POST'])
def citizen():
    S.sess = "citizen"
    return render_template('uploadCitizen.html')


@app.route('/family', methods=['GET', 'POST'])
def family():
    S.sess = "family"
    return render_template('uploadFamily.html')


@app.route('/submitInf', methods=['GET', 'POST'])
def submitInf():
    S.inf[1] = request.form['name']
    S.inf[2] = int(request.form['age'])
    S.inf[3] = request.form['gender']
    S.inf[4] = request.form['location']
    S.inf[5] = int(request.form['contact'])
    print("S.inf[0")
    print(S.inf[0])
    result = test.compare_all_concerned_citizen("static/imagesP/" + S.inf[0])
    print(S.inf[0])
    print(result)
    if result == None:
        return render_template('familyNoResults.html')
    if isinstance(result, str):
        S.result = result
        os.remove("static/imagesP/" + S.inf[0])

        cnx = test.open_database_connection()
        mycursor = cnx.cursor()

        name = "SELECT child_name FROM innodb.concerned_citizen where image = '" + S.result + "'"
        age = "SELECT age FROM innodb.concerned_citizen where image = '" + S.result + "'"
        gender = "SELECT gender FROM innodb.concerned_citizen where image = '" + S.result + "'"
        location = "SELECT location FROM innodb.concerned_citizen where image = '" + S.result + "'"
        phone = "SELECT phone FROM innodb.concerned_citizen where image = '" + S.result + "'"

        mycursor.execute(name)
        namee = mycursor.fetchall()[0][0]

        mycursor.execute(age)
        agee = mycursor.fetchall()[0][0]

        mycursor.execute(gender)
        genderr = mycursor.fetchall()[0][0]

        mycursor.execute(location)
        locationn = mycursor.fetchall()[0][0]

        mycursor.execute(phone)
        phonee = mycursor.fetchall()[0][0]

        cnx.commit()
        cnx.close()
        image = "static/imagesC/" + result + "?" + str(datetime.datetime.now())
        print("res")
        print(result)
        print(image)
        return render_template('oneResult.html', img=image,  name=namee, age=agee, gender=genderr, location=locationn, phone=phonee )
    return "Try Again"


@app.route('/submitInfC', methods=['GET', 'POST'])
def submitInfC():
    S.inf[1] = request.form['name']
    S.inf[2] = int(request.form['age'])
    S.inf[3] = request.form['gender']
    S.inf[4] = request.form['location']
    S.inf[5] = int(request.form['contact'])
    print("s.inf")
    print(S.inf)
    result = test.compare_all_parent("static/imagesC/" + S.inf[0])
    print("result")
    print(result)
    if result == None:
        return render_template('citizenNoResults.html')
    if isinstance(result, str):
        S.result = result
        print("result")
        print(result)
        os.remove("static/imagesC/" + S.inf[0])

        cnx = test.open_database_connection()
        mycursor = cnx.cursor()

        name = "SELECT child_name FROM innodb.parents where image = '" + S.result + "'"
        age = "SELECT age FROM innodb.parents where image = '" + S.result + "'"
        gender = "SELECT gender FROM innodb.parents where image = '" + S.result + "'"
        location = "SELECT location FROM innodb.parents where image = '" + S.result + "'"
        phone = "SELECT phone FROM innodb.parents where image = '" + S.result + "'"


        mycursor.execute(name)
        namee = mycursor.fetchall()[0][0]

        mycursor.execute(age)
        agee = mycursor.fetchall()[0][0]

        mycursor.execute(gender)
        genderr = mycursor.fetchall()[0][0]

        mycursor.execute(location)
        locationn = mycursor.fetchall()[0][0]

        mycursor.execute(phone)
        phonee = mycursor.fetchall()[0][0]


        cnx.commit()
        cnx.close()
        image = "static/imagesP/" + result + "?" + str(datetime.datetime.now())
        print("res")
        print(result)
        print(image)

        return render_template('oneResult.html', img=image, name=namee, age=agee, gender=genderr, location=locationn, phone=phonee )
    return "Try Again"


@app.route('/delete', methods=['POST'])
def delete():
    if S.sess == "citizen":
        os.remove("static/imagesP/" + S.result)

        cnx = test.open_database_connection()
        mycursor = cnx.cursor()
        query = "DELETE FROM innodb.parents where image = '" + S.result + "'"
        mycursor.execute(query)
        cnx.commit()
        cnx.close()

    else:
        os.remove("static/imagesC/" + S.result)
        cnx = test.open_database_connection()
        mycursor = cnx.cursor()
        query = "DELETE FROM innodb.concerned_citizen where image = '" + S.result + "'"
        mycursor.execute(query)

        cnx.commit()
        cnx.close()
    return "Thank You And Congratulations"


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Please select file"
        if file and allowed_file(file.filename):
            cnx = test.open_database_connection()
            mycursor = cnx.cursor()
            query = "Select Max(citizen_id) from innodb.concerned_citizen"
            mycursor.execute(query)
            count = mycursor.fetchall()

            if count[0][0] == None:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str("1" + ".jpg")))
                S.inf[0] = ("1.jpg")
                cnx.close()
                return render_template('uploadCitizen2.html')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(int(count[0][0])+1)+".jpg"))
                S.inf[0] = (str(int(count[0][0]) + 1) + ".jpg")
                cnx.close()
                return render_template('uploadCitizen2.html')
    return "Only accepts JPG files, Go back and Try again"


@app.route('/upload_fileF', methods=['GET', 'POST'])
def upload_fileF():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Please select file"
        if file and allowed_file(file.filename):
            cnx = test.open_database_connection()
            mycursor = cnx.cursor()
            query = "Select Max(parent_id) from innodb.parents"
            mycursor.execute(query)
            count = mycursor.fetchall()

            if count[0][0] == None:
                file.save(os.path.join(app.config['UPLOAD_FOLDERP'], str("1" + ".jpg")))
                S.inf[0] = ("1.jpg")

                cnx.close()
                return render_template('uploadFamily2.html')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDERP'], str(int(count[0][0]) + 1) + ".jpg"))
                S.inf[0] = (str(int(count[0][0]) + 1) + ".jpg")
                cnx.close()
            return render_template('uploadFamily2.html')
    return "Only accepts JPG files, Go back and Try again"


@app.route('/homeF', methods=['GET', 'POST'])
def homeF():
    os.remove("static/imagesP/" + S.inf[0])
    return render_template('homeF.html')


@app.route('/homeC', methods=['GET', 'POST'])
def homeC():
    os.remove("static/imagesC/"+ S.inf[0])
    return render_template('homeC.html')


@app.route('/saveC', methods=['GET', 'POST'])
def saveC():
    test.update_concerned_citicen_db(S.inf[1], S.inf[2], S.inf[3], S.inf[4], S.inf[5], S.inf[0])
    return "Your information has been saved"


@app.route('/saveF', methods=['GET', 'POST'])
def saveF():
    test.update_parent_db(S.inf[1], S.inf[2], S.inf[3], S.inf[4], S.inf[5], S.inf[0])
    return "Your information has been saved"


if __name__ == '__main__':
    app.run()
