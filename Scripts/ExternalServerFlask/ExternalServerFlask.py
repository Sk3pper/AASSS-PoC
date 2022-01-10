import socket

import time

import netifaces as ni
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_cors import CORS, cross_origin
from Utils import logError

app = Flask(__name__)
app.secret_key = 'random string'
base_ip = "https://192.168.99.104:3000"
cors = CORS(app, resources={r"/ExternalServerSha2/*": {"origins": base_ip},
                            r"/Rec2/*" : {"origins": base_ip},
                            r"/Rec1": {"origins": base_ip}}, supports_credentials=True)
# cors = CORS(app, resources={r"/Rec1": {"origins": "https://127.0.0.1:3000"}})

IP_ES = "ExternalServer"
PORT_ES = 6000
session_dictionary = {}

COD45 = "45"
COD45_desc = "Error in SHA2, maybe client has sent a malformed json"

COD10 = "10"
COD10_desc = "Error in REC2, maybe client has sent a malformed json"

COD200 = "200"

COD444 = "444"
COD444_desc = "General error"

DELIM = "---"
#################################
#             SHARING           #
#################################
@cross_origin()
@app.route('/ExternalServerSha2', methods=['POST'])
def ExternalServerSha2():
    try:
        print "          [SHAII-ExternalServerFlask] Contatto il dealer socket..."

        print "[SHAII-ExternalServerFlask] phase: " + request.form['phase']
        print "[SHAII-ExternalServerFlask] MC: " + request.form['MC']
        print "[SHAII-ExternalServerFlask] user_id: " + request.form['user_id']

        out_data = "SHA2|||" + request.form['MC'] + "||" + request.form['user_id']+ "||" + DELIM
        print out_data

        in_data = send_data(IP_ES, PORT_ES, out_data)

        print in_data
        return in_data

    except Exception as e:
        print "\n         [SHAII-ExternalServerFlask] General Error: " + str(e)
        msg = COD45 + "||" + COD45_desc

        user_id = request.form['user_id']
        if user_id == '':
            user_id = "None"

        logError("SHARING", "ExternalServer", COD45, COD45_desc, user_id)
        return msg


#################################
#      RECONSTRUCTION           #
#################################
# oss: il login lo mettiamo sull' ES cosi il dealer non puo fare MIMA. Avendo https il client sa con chi sta parlando.
# perche e' certificato --> non pupi farlo perche' il local sotage e' per dominio

@app.route('/Rec2', methods=['POST'])
def Rec2():
    try:
        print "         [REC2] session var:" + str(session)

        if 'username' in session:
            print "username in session"
            # Second call, the ExternalServer-socker will replay with MS'

            print "     [REC2-username in session] MC_prime: " + request.form['MC_prime']
            client = session_dictionary[session['username']]
            client.sendall(bytes(str(request.form['MC_prime'])).encode("utf-8"))
            es_in_data = client.recv(4096)

            # toDO: check es_in_data if everything is went well
            if COD200 in es_in_data:
                # set session
                session['login'] = session['username']
                # delete username
                session.pop('username', None)
                session.modified = True
                print "     [REC2-username in session] session var:" + str(session)
                return es_in_data
            else:
                msg = COD444 + "||" + COD444_desc

                user_id = request.form['user_id']
                if user_id == '':
                    user_id = "None"

                logError("RECONSTRUCTION", "ExternalServer", COD444, COD444_desc, user_id)
                return msg
        else:
            print "username IS NOT IN session"
            # First call
            print "     [REC2-username IS NOT IN session] phase: " + request.form['phase']
            print "     [REC2-username IS NOT IN session]eMS: " + request.form['eMS']
            print "     [REC2-username IS NOT IN session]id_user: " + request.form['id_user']

            # model: REC2|||eMS||id_user
            out_data = "REC2|||" + request.form['eMS'] + "||" + request.form['id_user']+ "||" + DELIM
            print out_data

            # contact the ExternalServer server, and save the connection in order to replay for the second step
            print "          [REC2-username IS NOT IN session]Send to " + IP_ES + ": " + " out_data = " + out_data
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP_ES, PORT_ES))
            client.sendall(bytes(out_data).encode("utf-8"))
            es_in_data = client.recv(4096) # here there is the MS' information
            print "          [REC2-username IS NOT IN session]From " + IP_ES + ": " + str(es_in_data.decode())
            print "es_in_data: "+str(es_in_data)

            # check
            if COD200 in es_in_data:
                session['username'] = request.form['id_user']
                session_dictionary[request.form['id_user']] = client


            print "     [REC2-username IS NOT IN session]session_dictionary: "+str(session_dictionary)
            print "     [REC2-username IS NOT IN session]session var:" + str(session)
            # return E_ms[k']
            return es_in_data

    except Exception as e:
        print "\n         [REC2-username IS NOT IN session] General Error: " + str(e)
        msg = COD10 + "||" + COD10_desc

        user_id = request.form['user_id']
        if user_id == '':
            user_id = "None"

        logError("RECONSTRUCTION", "ExternalServer", COD10, COD10_desc, user_id)
        return msg


@app.route('/checkSession')
def checkSession():
    if 'username' in session:
        return "Session is active"
    else:
        return "Session IS NOT active"


@app.route('/Homepage')
def Homepage():
    if 'login' in session:
        print "login in session"
        return render_template('home.html')
    else:
        print "login IS NOT in session"
        return render_template('Error.html')


@app.route('/ErrorPage')
def ErrorPage():
    return render_template('Error.html')


def send_data(IP, PORT, out_data):
    print "          [ExternalServerFlask]For " + IP + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.sendall(bytes(out_data).encode("utf-8"))
    in_data = client.recv(4096)
    print "          [ExternalServerFlask]From " + IP + ": " + str(in_data.decode())
    return in_data


if __name__ == "__main__":
    IP_HOST = '0.0.0.0'
    PORT = 4000
    app.run(host=IP_HOST, port=PORT, ssl_context=('cert.pem', 'key.pem'), threaded=True, debug=False)
    # app.run(port=4000, threaded=True)

