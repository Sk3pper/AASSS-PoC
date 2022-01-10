# modp2048 group and h
class MODP2048:
    p = int(1299743)
    # p = int(563)
    # p = int(23)
    # p = int(11)

    q = int(649871)
    # q = int(281)
    # q = int(11)
    #  q = int(5)

    g = int(2)
    # g = int(3)
    # g = int(2)
    # g = int(3)

    h = int(10309)
    # h = int(529)
    # h = int(13)
    # h = int(9)

    t = int(3)
    n = int(5)

    MAX_COORDINATE = 1000
    MAX_RANDOM = 50000


# questi valori sono stati ottenuti dallo script PrimeNumbers

class parametres:
    CHAR_DATA_SPLIT = "|-|"
    CHAR_MSG_SPLIT = "-|-"
    CHAR_REPORT_SPLIT = "\t"
    DELIM_LOG = ".-."
    # local MAC
    # inside container
    PATH_DATA_USERS = "/home-user/data_users"

    FILE_NAME_REPORT_MSG = "report_msg"
    FILE_NAME_ERROR = "errors"

    WHICH_LOG = ['MSG', 'ERROR']

    # INTERFACE = 'lo0'  # local MAC
    INTERFACE1 = 'ethwe0'  # 10.0.0.0/24
    INTERFACE2 = 'eth1'    # 99.0.0.0/24
    PORT_TO_LISTEN = 5000


    BUFFER_SIZE_REQUEST_MESSAGES = 16384  # byte
    TIMEOUT_CONNECTIONS = 3  # secondi

    END_MESSAGES = "end"


    # SHARING CODES
    COD200 = "200"  # Everything is went well

    COD100 = "100"  # User already signed-up [DEALER]
    COD100_desc = "User already signed-up [DEALER]"

    COD300 = "300"  # Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]
    COD150 = "150"  # User already signed-up [External Server]
    COD170 = "170"  # User_id is not present -> Dealer did not contact me or client is anticipating the steps
    COD400 = "400"  # MC_from_client != MC_from_Dealer
    COD500 = "500"  # Problem while Shareholder was saving the share

    COD550 = "550"  # Problem with SHA2, user_id dir is not present. Send MC before
    COD550_desc = "Problem with SHA2, user_id dir is not present. Send MC before"

    COD444 = "444"  # Generale error
    COD444_desc = "General error,try again later"

    # RECONSTRUCTION CODES
    COD600 = "600"  # user_id is not presetn --> you have to pass to signup before
    COD600_desc = "user_id is not present --> you have to pass to signup before"

    COD700 = "700"  # x_i given to the SHAREHOLDER is not right --> deaelr compromised? (1)
    COD750 = "750"  # (s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)
    COD760 = "760"  # user_id is not presetn --> you have to pass to signup before

    COD800 = "800"  # Insufficient shares from shareholders --> check shareholders and xi given from client
    COD800_desc = "Insufficient shares from shareholders --> check shareholders and xi given from client."

    COD830 = "830"  # Some SHAREHOLDERS give to the dealer INCORRECT shares (3)
    COD830_desc = "Some SHAREHOLDERS give to the dealer INCORRECT shares (3)"

    COD850 = "850"  # Insufficient correct shares -> too much shareholder that cheated (4)
    COD850_desc = "Insufficient correct shares -> too much shareholder that cheated (4)"

    COD860 = "860"  # Client is cheating, S' != S' rec
    COD860_desc = "Client is cheating, S' != S' rec"

    COD880 = "880"  # Less than n-coordinates
    COD880_desc = "Less than n-coordinates"

    COD900 = "900"  # user_id is not presetn --> you have to pass to signup before
    COD930 = "930"  # E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)
    COD960 = "960"  # D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)
    COD1000 = "1000"  # D_k'[MS] != MC External Server is cheating (6)

    COD2000 = "2000"  # D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)
    COD2000_desc = "D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)"

    COD2400 = "2400"  # MC != D_k[MS] --> ExternalServer is cheating (8)
    COD2400_desc = " MC != D_k[MS] --> ExternalServer is cheating (8)"

    COD2600 = "2600"  # MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)
    COD2600_desc = "MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)"

    COD3000 = "3000"  # Unrecognized phase
    COD3000_desc = "Unrecognized phase"

