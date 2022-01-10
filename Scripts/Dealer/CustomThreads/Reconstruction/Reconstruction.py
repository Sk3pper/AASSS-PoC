import threading

import os
from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.PedersenUtilities.VSS import pedersenVerify
from CustomThreads.PedersenUtilities.VSS import pedersenRecover
from CustomThreads.PedersenUtilities.VSS import genRand
from CustomThreads.aesCustomKey import AES_encrypt, AES_decrypt
from CustomThreads.Sharing.Sharing import sharing2Dealer
from CustomThreads.Utils.Utils_function import write_data, send_data, readPenultimeLine, readIntPenultimeLine, \
    computeCoordinate, split, strToIntList
from CustomThreads.Utils.Utils_function import logMsg, logError

# load group
g2048 = MODP2048()
par = parametres()

t = g2048.t
n = g2048.n

CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
PATH_DATA_USERS = par.PATH_DATA_USERS
CHAR_COORD_SPLIT = par.CHAR_COORD_SPLIT
WHICH_PHASE = par.WHICH_PHASE

FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
FILE_NAME_NW_INFORMATION = par.FILE_NAME_NW_INFORMATION
FILE_NAME_MC = par.FILE_NAME_MC

IP_SHAREHOLDERS = par.IP_SHAREHOLDERS
PORT_SHAREHOLDERS = par.PORT_SHAREHOLDERS
PORT_EXTERNAL_SERVER = par.PORT_EXTERNAL_SERVER
IP_EXTERNAL_SERVER = par.IP_EXTERNAL_SERVER

COD200 = par.COD200  # every is went well
COD300 = par.COD300  # saved is not went well
COD400 = par.COD400  # xi != h(xi)
COD450 = par.COD450  # (s_i,t_i) given by DEALER TO SHAREHOLDER is not consistent with commitments
COD500 = par.COD500  # (s_i,t_i) given by SHAREHOLDER TO DEALER is not consistent with commitments
COD550 = par.COD550  # S' != \overline(S')

COD650 = par.COD650  # error in REC-Client MC!=D_k'[MS]
COD700 = par.COD700  # error in REC2-Dealer MC_dec != D_k[MC]
COD750 = par.COD750  # error in REC2-Dealer D_k'[MS] != MC

COD999 = par.COD999  # error in SHA1-ExternalServer
COD888 = par.COD888  # error in REC1 ES

# NEW CODES
COD600 = par.COD600  # user_id is not presetn --> you have to pass to signup before
COD600_desc = par.COD600_desc

COD800 = par.COD800  # Insufficient shares from shareholders --> check shareholders and xi given from client
COD800_desc = par.COD800_desc

COD830 = par.COD830  # Some SHAREHOLDERS give to the dealer INCORRECT shares (3)
COD830_desc = par.COD830_desc

COD850 = par.COD850  # Insufficient correct shares -> too much shareholder that cheated (4)
COD850_desc = par.COD850_desc

COD860 = par.COD860  # Client is cheating, S' != S' rec
COD860_desc = par.COD860_desc

COD880 = par.COD880  # Less than n-coordinates from Client
COD880_desc = par.COD880_desc

COD2000 = par.COD2000  # D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)
COD2000_desc = par.COD2000_desc

COD2400 = par.COD2400  # MC != D_k[MS] --> ExternalServer is cheating (8)
COD2400_desc = par.COD2400_desc

COD2600 = par.COD2600  # MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)
COD2600_desc = par.COD2600_desc

COD444 = par.COD444  # Generale error
COD444_desc = par.COD444_desc

DELIM = par.DELIM


#################################
#             REC1              #
#################################
# send the x_i to shareholders and retrive the (s_i,t_i)
def request_Shares(abscissa_vect, id_user):
    # cycling on abscissa_vec
    # Dealer sends the request to each Shareholder in order to give to it the couple (s_i,t_i)
    # the request is made with n-thread that wait the data.
    # The main_th wait that every Shareholder replay and then put togheter the information
    i = 0
    j = 1
    th_list = []
    for IP in IP_SHAREHOLDERS:
        # start thread listener connections unicast
        out_data = "REC" + CHAR_MSG_SPLIT + str(abscissa_vect[i]) + CHAR_DATA_SPLIT + id_user + par.CHAR_DATA_SPLIT + DELIM
        th = RequestSharesThread(IP, PORT_SHAREHOLDERS, out_data, id_user, j, abscissa_vect[i])
        # unicast_conn.setDaemon(True)
        th.start()
        th_list.append(th)
        i += 1
        j += 1

    for th in th_list:
        th.join()

    # At this point we have the replays of each shareholder.
    # check if we have at least t-shares
    # (we don't know if are also correct but for the first step we check if there are)
    shares = []
    t_shares = []
    error = 0
    ip_shareholders = []
    coordinates = []

    for th in th_list:
        info = th.getIn_data()
        ip_shareholders.append(th.getIp())

        # info should be CODX||Desc 0r COD200||s_i||t_i
        data = split(info, CHAR_DATA_SPLIT)

        if data[0] == COD200:
            shares.append(data[1])
            t_shares.append(data[2])
            coordinates.append(th.getCoordinate())
        else:
            shares.append(None)
            t_shares.append(None)
            coordinates.append(None)
            error += 1

    print "         shares: " + str(shares)
    print "         t_shares: " + str(t_shares)
    print "         ip_shareholders: " + str(ip_shareholders)
    print "         error: " + str(error)

    return shares, t_shares, coordinates, ip_shareholders, error


class RequestSharesThread(threading.Thread):
    # take host_ip, port to contact, and data to send.
    # send the request and wait the respond
    def __init__(self, host_ip, port, out_data, id_user, id, xi):
        """
        :rtype: threading.Thread
        """
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.port = port
        self.out_data = out_data
        self.in_data = ''
        self.id_user = id_user
        self.id = id
        self.xi = xi

    def run(self):
        try:
            # perform the request and wait the respond
            sh = "Shareholder-" + str(self.id)
            # From, To, Payload, Phase, id_user
            logMsg("Dealer", sh, self.out_data, "RECONSTRUCTION", self.id_user)

            self.in_data = send_data(self.host_ip, self.port, self.out_data)
        except Exception as e:
            print "\n         General Error: " + str(e)
            self.in_data = COD444 + CHAR_DATA_SPLIT + COD444_desc

            # Log error Phase, Actor, CODError, Payload,  id_user
            payload = COD444_desc + str(e) + " IP: "+str(self.host_ip)
            logError("SHARING", "Dealer", COD444, payload, self.id_user)

    def getIn_data(self):
        return self.in_data

    def getIp(self):
        return self.host_ip

    def getCoordinate(self):
        return self.xi


# delete the None information inside these lists
def deleteNone(shares, t_shares, coordinates, ip_shareholders):
    s = []
    ts = []
    c = []
    ips = []

    for i in range(0, len(shares)):
        if (shares[i] is not None) and (t_shares[i] is not None) and (coordinates[i] is not None):
            s.append(int(shares[i]))
            ts.append(int(t_shares[i]))
            c.append(int(coordinates[i]))
            ips.append(ip_shareholders[i])

    print "\n        shares: " + str(s)
    print "         t_shares: " + str(ts)
    print "         coordinates: " + str(c)
    print "         ip_shareholders: "+str(ip_shareholders)

    return s, ts, c, ips


def deleteIncorrectShares(check_list_shares, shares, t_shares, coordinates, ip_shareholders):
    # we have to pass only the correct info
    c_shares = []
    c_coordinates = []
    c_t_shares = []
    ips = []
    for i in range(0, len(shares)):
        if check_list_shares[i] == True:
            c_shares.append(shares[i])
            c_t_shares.append(t_shares[i])
            c_coordinates.append(coordinates[i])
            ips.append(ip_shareholders[i])

    print "\n       c_shares: " + str(c_shares)
    print "         c_t_shares: " + str(c_t_shares)
    print "         c_coordinates: " + str(c_coordinates)
    print "         c_ips: " + str(ips)

    return c_shares, c_t_shares, c_coordinates, ips


def reconstructionDealer1(self, sPrime, abscissa_vect, sSecond, mcPrime, eMS, id_user):
    print "     reconstructionDealer1"
    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_comm = path_user + "/" + FILE_NAME_COMM
    path_file_name = path_user + "/" + FILE_NAME_NW_INFORMATION
    msg = ''

    try:
        # check if the user is already signed-up
        if os.path.isdir(path_user):
            if len(abscissa_vect) != n:
                print "     Less than n-coordinates from Client"
                msg = COD880 + CHAR_DATA_SPLIT + COD880_desc
                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("RECONSTRUCTION", "Dealer", COD880, COD880_desc, id_user)

            else:
                # request (si,ti) to SHAREHOLDERS!
                shares, t_shares, coordinates,  ip_shareholders, error = request_Shares(abscissa_vect, id_user)

                if error != 0 and (n-error) >= t:
                    print " report the error: we can continue but something is went bad --> deeply understand"
                    m = "someone did not replay:  "

                    for i in range(0, len(shares)):
                        if shares[i] is None:
                            m = m +  " | " + str(ip_shareholders[i])

                    # Log error Phase, Actor, CODError, Payload,  id_user
                    logError("RECONSTRUCTION", "Dealer", "None", m, id_user)

                if (n-error) >= t:
                    # read files and extract the informations, take the last penultimate-line,
                    # because the last-line is the \n char
                    Commitments = readIntPenultimeLine(path_file_comm)
                    print "         Commitments:" + str(Commitments)

                    # now we have commits and shares we can CHECK if the shares and t-shares are correct through commits
                    check_list_shares = []

                    shares, t_shares, coordinates, ip_shareholders = deleteNone(shares, t_shares, coordinates, ip_shareholders)
                    Commitments = strToIntList(Commitments)

                    # check the given shares
                    correct_shares = 0
                    for i in range(0, len(shares)):
                        check_result = pedersenVerify(coordinates[i], shares[i], t_shares[i], Commitments)
                        check_list_shares.append(check_result)

                        if check_result:
                            correct_shares += 1

                    print "     check_list_shares: "+str(check_list_shares)

                    # report the error because some shareholder is compromised
                    if correct_shares != (n-error):
                        # some of the given shares are incorrect
                        print "     Log the error for the admin system"
                        msg = COD830 + CHAR_DATA_SPLIT + COD830_desc

                        m = 'who is cheating: '
                        for i in range(0, len(check_list_shares)):
                            if check_list_shares[i] == False:
                                print "     who is cheating: " + str(ip_shareholders[i])
                                m = m + " | " + str(ip_shareholders[i])

                        # Log error Phase, Actor, CODError, Payload,  id_user
                        payload = COD830_desc + " " + m
                        logError("RECONSTRUCTION", "Dealer", COD830, payload, id_user)

                    # with at least t correct shares we can reconstruct the secret
                    if correct_shares >= t:
                        # reconstruct the secret
                        # take only the CORRECT SHARES in order do rebuild the secret
                        c_shares,  c_t_shares, c_coordinates, c_ip_shareholder = deleteIncorrectShares(check_list_shares, shares, t_shares, coordinates, ip_shareholders)

                        recoveredK = pedersenRecover(c_coordinates, c_shares, c_t_shares, Commitments)
                        print "\n     recoveredK: " + str(recoveredK)

                        if recoveredK == sPrime:
                            print "     secret: " + str(sPrime) + " recoveredK: " + str(recoveredK) + "        True"
                            # since the secret given to the user is equal to the reconstructed one we can save the
                            # temporary data like: sSecond, mcPrime, eMS, id_user,
                            # Precalculating also x1',..,xn'
                            coordinate = computeCoordinate()

                            # sSecond||coordinate||mcPrime||eMS
                            data = str(sSecond) + CHAR_DATA_SPLIT + \
                                   coordinate + CHAR_DATA_SPLIT + \
                                   str(mcPrime) + CHAR_DATA_SPLIT + \
                                   eMS + "\n"

                            # flush data
                            write_data(path_file_name, data)

                            # now we have to contact ExternarlServer and send to it: REC1|||eMS||id_user
                            out_data_es = WHICH_PHASE[2] + CHAR_MSG_SPLIT + \
                                          str(eMS) + CHAR_DATA_SPLIT + id_user + par.CHAR_DATA_SPLIT + DELIM

                            # Log the message (From, To, Payload, Phase, id_user)
                            logMsg("Dealer", IP_EXTERNAL_SERVER, out_data_es, "RECONSTRUCTION", id_user)

                            # ExternalServer's replay
                            in_data_es = send_data(IP_EXTERNAL_SERVER, PORT_EXTERNAL_SERVER, out_data_es)

                            if COD200 in in_data_es:
                                print "          Now the client can contact the ES"
                                msg = COD200 + CHAR_DATA_SPLIT + str(coordinate)
                            else:
                                print "          Something was went wrong in the ES"
                                msg = in_data_es
                        else:
                            print "    ERROR, something is went wrong in the pedersenRecover secret: " + str(sPrime) + \
                                  " recoveredK: " + str(recoveredK) + "        False"
                            msg = COD860 + CHAR_DATA_SPLIT + COD860_desc

                    else:
                        print "     ERROR: less than t CORRECT shares"
                        m = '  who is cheating: '
                        for i in range(0, len(check_list_shares)):
                            if check_list_shares[i] == False:
                                print "     who is cheating: "+str(ip_shareholders[i])
                                m = m +" | "+ str(ip_shareholders[i])
                        payload = COD850_desc + m
                        msg = COD850 + CHAR_DATA_SPLIT + COD850_desc

                        # Log error Phase, Actor, CODError, Payload,  id_user
                        logError("RECONSTRUCTION", "Dealer", COD850, payload, id_user)
                else:
                    # less than t-shareholders give us the coordinates
                    print "     ERROR: less than t-shareholders give us the coordinates"
                    print "     Someone of the SHAREHOLDERS does not reply, discover why: " \
                          "Client give us the incorrect coordiante?"

                    print "     The Shareholder that did not reply are: "
                    m = " The Shareholder that did not reply are: "
                    for i in range(0, len(shares)):
                        if shares[i] is None:
                            print ip_shareholders[i]
                            m = m +" | "+ str(ip_shareholders[i])
                    payload = COD800_desc + m
                    # Log error Phase, Actor, CODError, Payload,  id_user
                    logError("SHARING", "Dealer", COD800, payload, id_user)
                    msg = COD800 + CHAR_DATA_SPLIT + COD800_desc

        else:
            print "     ERROR: user_id is NOT present. It has to signed-up before"
            msg = COD600 + CHAR_DATA_SPLIT + COD600_desc
            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "Dealer", COD600, COD600_desc, self.id_user)


    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc

        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "Dealer", COD444, payload, id_user)

    # Log message (From, To, Payload, Phase, id_user)
    logMsg("Dealer", "Client", msg, "RECONSTRUCTION", id_user)

    # send back to the Client
    self.csocket.send((bytes(msg).encode("utf-8")))

    print "     Client at " + str(self.clientAddress) + " disconnected..."


#################################
#             REC2              #
#################################

def retrieve_info(path_user):
    # prendo l'informazione di MC dal file MC_information
    path_file_MC = path_user + "/" + FILE_NAME_MC
    MC = readPenultimeLine(path_file_MC)[:-len("\n")]
    print "     MC: " + str(MC)

    # prendo le informazioni nuove dal file new_informations
    path_file_NW_INFORMATION = path_user + "/" + FILE_NAME_NW_INFORMATION
    info = split(readPenultimeLine(path_file_NW_INFORMATION), CHAR_DATA_SPLIT)
    print "     info: " + str(info)
    # model: sSecond||coordinate||mcPrime||eMS
    sSecond = info[0]
    coordinate = info[1]
    mcPrime_fromClient = info[2]
    eMS = info[3]

    return MC, sSecond, coordinate, mcPrime_fromClient, eMS


def reconstructionDealer2(self, k, kPrime, MS, MC_dec, MC_prime_fromES, id_user):
    print "\n     reconstructionDealer2"
    path_user = PATH_DATA_USERS + "/" + id_user
    msg = ''
    try:
        if not os.path.isdir(path_user):
            print "     ERROR: user_id is NOT present. It has to signed-up before"
            msg = COD600 + CHAR_DATA_SPLIT + COD600_desc
            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("RECONSTRUCTION", "Dealer", COD600, COD600_desc, self.id_user)
        else:
            # retrieve the information from the two files: FILE_NAME_MC e FILE_NAME_NW_INFORMATION
            MC, sSecond, coordinate, mcPrime_fromClient, eMS = retrieve_info(path_user)

            # compute the 3 checks
            # check3: mcPrime_fromClient =?= MC_prime_fromES
            print "\n     mcPrime_fromClient: " + mcPrime_fromClient
            print "     MC_prime_fromES: " + MC_prime_fromES

            if mcPrime_fromClient == MC_prime_fromES:
                print "     mcPrime_fromClient == MC_prime_fromES"

                # check2: D_k'[MS] =?= MC
                decrypted_MS = AES_decrypt(kPrime, MS)

                print "\n     decrypted MS: " + decrypted_MS
                print "     MC: " + MC

                if decrypted_MS == MC:
                    print "     decrypted_MS == MC"

                    # check1: MC_dec =?= D_k[MC]
                    decrypted_MC = AES_decrypt(k, MC)

                    print "\n     decrypted MC: " + decrypted_MC
                    print "     MC_dec: " + MC_dec

                    if decrypted_MC == MC_dec:
                        print "     decrypted_MC == MC_dec"
                        print "\n        ricostruiamo il segreto!!"

                        # All 3 checks are passed

                        # Save the new value of MC that is MC'
                        path_file_name = path_user + "/" + FILE_NAME_MC
                        data = str(mcPrime_fromClient) + "\n"

                        # flush data
                        write_data(path_file_name, data)

                        # Replace S' with S'' but this time the coordinates are fixed

                        # set the information and call sharing SHA2
                        coordinate = split(coordinate, CHAR_COORD_SPLIT)
                        print "      informations passed to sharing2Dealer:" + \
                              "\n      sSecond: " + str(sSecond) + \
                              "\n      id_user: " + str(id_user) + \
                              "\n      coordinate: " + str(coordinate)

                        coordinate = strToIntList(coordinate)

                        # Start the sharing phase SHA2
                        sharing2Dealer(None, int(sSecond), id_user, abscissa_vector=coordinate)

                        msg = COD200
                    else:
                        print "     decrypted_MC != MC_dec"
                        msg = COD2000 + CHAR_DATA_SPLIT + COD2000_desc
                        # Log error Phase, Actor, CODError, Payload,  id_user
                        logError("RECONSTRUCTION", "Dealer", COD2000, COD2000_desc, id_user)

                else:# error 8
                    print "     decrypted_kPrime_MS != MC"
                    msg = "decrypted_kPrime_MS != MC"
                    msg = COD2400 + CHAR_DATA_SPLIT + COD2400_desc
                    # Log error Phase, Actor, CODError, Payload,  id_user
                    logError("RECONSTRUCTION", "Dealer", COD2400, COD2400_desc, self.id_user)

            else:
                # error 9
                print "     mcPrime_fromClient != MC_prime_fromES"
                msg = COD2600 + CHAR_DATA_SPLIT + COD2600_desc
                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("RECONSTRUCTION", "Dealer", COD2600, COD2600_desc, self.id_user)


    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc
        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("RECONSTRUCTION", "Dealer", COD444, payload, id_user)

    self.csocket.send((bytes(msg).encode("utf-8")))
    print "     Client at " + str(self.clientAddress) + " disconnected..."
