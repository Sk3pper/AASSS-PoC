import threading
import time

from Phases.Sharing import sharing
from Phases.Reconstrucion import rec

class performTest(threading.Thread):
    # take host_ip, port to contact, and data to send.
    # send the request and wait the respond
    def __init__(self, id_user, password,  phase, p, q, g, h, S_PRIME=None, r=None,  MC=None,  k=None,  r_prime=None,  MC_beforeEnc=None,  MS=None,  abscissas_vector=None):
        """
        :rtype: threading.Thread
        """
        threading.Thread.__init__(self)

        self.id_user = id_user
        self.password = password
        self.phase = phase

        self.p = p
        self.q = q
        self.g = g
        self.h = h

        self.S_PRIME = S_PRIME
        self.r = r
        self.MC = MC
        self.k = k
        self.r_prime = r_prime
        self.MC_beforeEnc = MC_beforeEnc
        self.MS = MS
        self.abscissas_vector = abscissas_vector

        self.time = 0
        self.error = False

    def run(self):
        try:
            if "sharing" in self.phase:
                # call the sharing phase
                startTime = time.time()

                self.S_PRIME,  self.r,  self.MC,  self.k,  self.r_prime,  self.MC_beforeEnc,  self.MS,  self.abscissas_vector = sharing(self.password, self.id_user, self.p, self.q, self.g, self.h)

                # set time
                self.time = time.time() - startTime
            elif "reconstruction" in self.phase:
                # call the reconstruction phase
                startTime = time.time()
                # rec(S, S_PRIME, r, MC, r_prime, MS, abscissas_vector, k, MC_beforeEnc, ID_USER, p, q, g, h):
                ret = rec(self.password, self.S_PRIME, self.r, self.MC, self.r_prime, self.MS, self.abscissas_vector, self.k, self.MC_beforeEnc, self.id_user, self.p, self.q, self.g, self.h)
                if ret is not True:
                    self.error = True
                # set time
                self.time = time.time() - startTime

        except Exception as e:
            print "\n         General Error: " + str(e)

    def getTime(self):
        return self.time

    def getError(self):
        return self.error

    def getValueForReconstruction(self):
        return self.S_PRIME,  self.r,  self.MC,  self.k,  self.r_prime,  self.MC_beforeEnc,  self.MS,  self.abscissas_vector, self.id_user
