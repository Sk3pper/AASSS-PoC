import socket
import time
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_cors import CORS, cross_origin
from Utils import logError

IP_DEALER = "MasterJarvis"
PORT_DEALER = 8000

COD200 = "200"
COD5 = "5"
COD5_desc = "Error in REC1, maybe client has sent malformed json"
COD15 = "15"  # Error in SHA1, maybe client has sent malforme json
COD15_desc = "Error in SHA1, maybe client has sent malforme json"
COD30 = "30"  # Error in SHA2, maybe client has sent malforme json
COD30_desc = "Error in SHA2, maybe client has sent malforme json"

app = Flask(__name__)
app.secret_key = 'random string'
base_ip = "https://192.168.99.104:4000"
cors = CORS(app, resources={r"/ExternalServerSha2": {"origins": base_ip},
                            r"/Rec2": {"origins": base_ip},
                            r"/Rec1/*": {"origins": base_ip}})

DELIM = "---"


#################################
#             SHARING           #
#################################
@app.route('/')
def index():
    return render_template('register.html')


@cross_origin()
@app.route('/Sha1', methods=['POST'])
def Sha1():
    try:
        print "          [SHAI-DealerFlask] Contatto il dealer through socket..."
        print "          [SHAI-DealerFlask] phase: " + request.form['phase']
        print "          [SHAI-DealerFlask] MC: " + request.form['MC']
        print "          [SHAI-DealerFlask] user_id: " + request.form['user_id']

        out_data = "SHA1|||"+request.form['MC']+"||"+request.form['user_id'] + "||" + DELIM
        print out_data

        in_data = send_data(IP_DEALER, PORT_DEALER, out_data)

        if COD200 in in_data:
            # set the session in order to remember the user. In this way another client cannot call SHA2
            session["username"] = request.form['user_id']
            return in_data
        else:
            return in_data

    except Exception as e:
        print "\n         [SHAI-DealerFlask] General Error: " + str(e)
        msg = COD15 + "||" + COD15_desc
        user_id = request.form['user_id']
        if user_id == '':
            user_id = "None"

        logError("SHARING", "Dealer", COD15, COD15_desc, user_id)
        return msg


@app.route('/DealerSha2', methods=['POST'])
def DealerSha2():
    try:
        if 'username' in session:
            print "          [SHAII-DealerFlask] Contatto il dealer socket..."
            print "          [SHAII-DealerFlask] phase: " + request.form['phase']
            print "          [SHAII-DealerFlask] Sprime: " + request.form['Sprime']
            print "          [SHAII-DealerFlask] user_id: " + request.form['user_id']

            out_data = "SHA2|||"+request.form['Sprime']+"||"+request.form['user_id']+ "||" + DELIM
            print out_data

            in_data = send_data(IP_DEALER, PORT_DEALER, out_data)

            if COD200 in in_data:
                # set tha everything is went well
                session['right'] = session['username']

                # delete username session
                session.pop('username', None)
                return in_data
            else:
                return "Error you have to re-signup"
        else:
            # Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "Dealer", "550", "Problem with SHA2, user_id dir is not present. Send MC before", "None")
            return "550||Problem with SHA2, user_id dir is not present. Send MC before"
    except Exception as e:
        print "\n         [SHAII-DealerFlask] General Error: " + str(e)
        msg = COD30 + "||" + COD30_desc
        user_id = request.form['user_id']
        if user_id == '':
            user_id = "None"

        logError("SHARING", "Dealer", COD30, COD30_desc, user_id)
        return msg


@app.route('/Sha3', methods=['POST'])
def DealerSha3():
    return "200||ciao"

#################################
#      RECONSTRUCTION           #
#################################

@app.route('/Login')
def Login():
    return render_template('login.html')

@app.route('/Rec1', methods=['POST'])
def Rec1():
    try:
        print "     [RECI - DealerFlask] Contatto il dealer socket..."
        print "     [RECI - DealerFlask] phase: " + request.form['phase']
        print "     [RECI - DealerFlask] Sprime: " + request.form['Sprime']
        print "     [RECI - DealerFlask] Coordinate: " + request.form['Coordinate']
        print "     [RECI - DealerFlask] Ssecond: " + request.form['Ssecond']
        print "     [RECI - DealerFlask] MCprime: " + request.form['MCprime']
        print "     [RECI - DealerFlask] eMS: " + request.form['eMS']
        print "     [RECI - DealerFlask] id_user: " + request.form['id_user']

        # REC1|||sPrime||x1,x2,..,xn||sSecond||mcPrime||eMS||id_user
        out_data = "REC1|||" + request.form['Sprime'] + "||" + request.form['Coordinate'] + "||" + \
                   request.form['Ssecond'] +"||"+request.form['MCprime']+"||"+request.form['eMS'] +"||" + \
                   request.form['id_user'] + "||" + DELIM
        print out_data
        in_data = send_data(IP_DEALER, PORT_DEALER, out_data)

        if COD200 in in_data:
            # se cod200 allora set session
            print "     [RECI - DealerFlask] DEALER 200 OK!!"
            return in_data
        else:
            return in_data

    except Exception as e:
        print "\n         [RECI - DealerFlask] General Error: " + str(e)
        msg = COD5 + "||" + COD5_desc
        user_id = request.form['user_id']
        if user_id == '':
            user_id = "None"

        logError("RECONSTRUCTION", "Dealer", COD5, COD5_desc, user_id)
        return msg


@app.route('/checkSession')
def checkSession():
    if 'username' in session:
        return "Session is active"
    else:
        return "Session IS NOT active"


@app.route('/RightPage')
def RightPage():
    if 'right' in session:
        session.pop('right', None)
        return render_template('Right.html')
    else:
        return "Register to the system "


@app.route('/ErrorPage')
def ErrorPage():
    return render_template('Error.html')


def send_data(IP, PORT, out_data):
    print "          [DealerFlask]For " + IP + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.sendall(bytes(out_data).encode("utf-8"))
    in_data = client.recv(4096)
    print "          [DealerFlask]From " + IP + ": " + str(in_data.decode())
    return in_data


if __name__ == "__main__":
    IP_HOST = '0.0.0.0'
    PORT = 3000
    app.run(host=IP_HOST, port=PORT, ssl_context=('cert.pem', 'key.pem'), threaded=True, debug=False)
