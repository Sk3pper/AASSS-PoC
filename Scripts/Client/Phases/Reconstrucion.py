import socket
from Utils.aesCustomKey import AES_decrypt
from Utils.groups import MODP2048, parametres
from Utils.Utils import sPrime, computeMC, contactActor, pedersenModq, computeEms,split

# load group
g2048 = MODP2048()
par = parametres()

DELIM = par.DELIM
def rec(S, S_PRIME, r,  MC, r_prime, MS, abscissas_vector, k, MC_beforeEnc, ID_USER, p, q, g, h):
    # print "RECONSTRUCTION"

    # compute S''
    S_second, r_second = sPrime(S, p, q, g, h)

    # Compute MC'
    # MC, k, rPr
    MC_prime, k_second, r_third, MC_primeBeforeEnc = computeMC(S_second, p, q, g, h)

    # Compute E_MS: E_MS[k||(g^S' h^r')"
    # (MS, k, MC_beforeEnc):
    Ems = computeEms(MS, k, MC_beforeEnc)

    # prepare the message for the Dealer
    # REC1|||sPrime||x1,x2,..,xn||sSecond||mcPrime||eMS||id_user
    dealer_out_data = par.WHICH_PHASE[2] + par.CHAR_MSG_SPLIT + \
                      str(S_PRIME) + par.CHAR_DATA_SPLIT + \
                      str(abscissas_vector) + par.CHAR_DATA_SPLIT + \
                      str(S_second) + par.CHAR_DATA_SPLIT + \
                      str(MC_prime) + par.CHAR_DATA_SPLIT + \
                      str(Ems) + par.CHAR_DATA_SPLIT + \
                      ID_USER + par.CHAR_DATA_SPLIT + DELIM



    # send the data to the Dealer
    dealer_in_data = contactActor(par.DEALER, par.PORT_DEALER, dealer_out_data)

    if "200" in dealer_in_data:
        abscissas_vector = split(dealer_in_data, par.CHAR_DATA_SPLIT)[1]

        # prepare the message for the External Server
        # REC2|||eMS||id_user
        es_out_data = par.WHICH_PHASE[3] + par.CHAR_MSG_SPLIT + \
                      str(Ems) + par.CHAR_DATA_SPLIT + \
                      ID_USER + par.CHAR_DATA_SPLIT+ DELIM

        # send the data to the External Server
        print "          1-Send to " + par.EXTERNAL_SERVER  # + ": " + " out_data = " + es_out_data
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((par.EXTERNAL_SERVER, par.PORT_EXTERNAL_SERVER))
        client.sendall(bytes(es_out_data).encode("utf-8"))
        es_in_data = client.recv(16096)
        print "          1-From " + par.EXTERNAL_SERVER  # + ": " + str(es_in_data.decode())

        if "200" in es_in_data:
            eMS = split(es_in_data, par.CHAR_DATA_SPLIT)[1]

            # decrypt the message
            k_prime = AES_decrypt(MS, eMS)
            # decrypt the message
            MC_from_MS = AES_decrypt(k_prime,MS)

            # D_k'[MS] = MC = MC
            if MC == MC_from_MS:
                # send MC' to the External server
                print "             2-Send to " + par.EXTERNAL_SERVER  #  + ": " + " MC' = " + MC_prime
                client.sendall(bytes(MC_prime).encode("utf-8"))
                es_in_data = client.recv(16096)
                print "             2-From " + par.EXTERNAL_SERVER # + str(es_in_data.decode())

                if "200" in es_in_data:
                    MS_prime = es_in_data
                    return True
                else:
                    print "ERROR SOMETHING IS WENT WRONG: MC != MC_from_MS"
                    return "ERROR SOMETHING IS WENT WRONG: "+str(es_in_data)
            else:
                print "ERROR SOMETHING IS WENT WRONG: MC != MC_from_MS"
                return "ERROR SOMETHING IS WENT WRONG: MC != MC_from_MS"
        else:
            print  "ERROR SOMETHING IS WENT WRONG:" + str(es_in_data)
            return "ERROR SOMETHING IS WENT WRONG:" + str(es_in_data)
    else:
        print  "ERROR SOMETHING IS WENT WRONG:" + str(dealer_in_data)
        return "ERROR SOMETHING IS WENT WRONG:" + str(dealer_in_data)