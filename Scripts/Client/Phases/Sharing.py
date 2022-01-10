import socket

# UNICAST = "127.0.0.1"
from Utils.Utils import split
from Utils.groups import MODP2048, parametres
from Utils.Utils import sPrime, computeMC, contactActor, pedersenModq, computeEms

# load group
g2048 = MODP2048()
par = parametres()

DELIM = par.DELIM

def sharing(S, ID_USER, p, q, g, h):
    # print "SHARING"

    # compute S_prime
    S_PRIME, r = sPrime(S, p, q, g, h)

    # compute MC
    # MC, k, rPr
    MC, k, r_prime, MC_beforeEnc = computeMC(S_PRIME, p, q, g, h)

    # prepare the message for the Dealer
    dealer_out_data = par.WHICH_PHASE[0] + par.CHAR_MSG_SPLIT + str(MC) + par.CHAR_DATA_SPLIT + ID_USER + par.CHAR_DATA_SPLIT+ DELIM

    # send the request to the Dealer and wait the response
    dealer_in_data = contactActor(par.DEALER, par.PORT_DEALER, dealer_out_data)

    # if everything is went well
    if "200" in dealer_in_data:
        # prepare the message for the External Server
        es_out_data = par.WHICH_PHASE[1] + par.CHAR_MSG_SPLIT + str(MC) + par.CHAR_DATA_SPLIT + ID_USER + par.CHAR_DATA_SPLIT + DELIM

        # send the request to the External Server and wait the response
        es_in_data = contactActor(par.EXTERNAL_SERVER, par.PORT_EXTERNAL_SERVER, es_out_data)

        if "200" in es_in_data:
            # retrieve MS
            MS = split(es_in_data, par.CHAR_DATA_SPLIT)[1]

            # prepare the message for the Dealer
            dealer_out_data2 = par.WHICH_PHASE[1] + par.CHAR_MSG_SPLIT + str(S_PRIME) + par.CHAR_DATA_SPLIT + ID_USER + par.CHAR_DATA_SPLIT+ DELIM

            # send the request to the Dealer and wait the response
            dealer_in_data2 = contactActor(par.DEALER, par.PORT_DEALER, dealer_out_data2)

            if "200" in dealer_in_data2:
                abscissas_vector = split(dealer_in_data2, par.CHAR_DATA_SPLIT)[1]
                return S_PRIME, r, MC, k, r_prime, MC_beforeEnc, MS, abscissas_vector
            else:
                print "ERROR SOMETHING IS WENT WRONG:" + str(dealer_in_data2)
                return "ERROR SOMETHING IS WENT WRONG:" + str(dealer_in_data2)

        else:
            print "ERROR SOMETHING IS WENT WRONG:" + str(es_in_data)
            return "ERROR SOMETHING IS WENT WRONG:"+str(es_in_data)
    else:
        print "ERROR SOMETHING IS WENT WRONG:" + str(dealer_in_data)
        return "ERROR SOMETHING IS WENT WRONG:"+str(dealer_in_data)
