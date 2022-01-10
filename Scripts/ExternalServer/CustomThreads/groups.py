# modp2048 group and h
class MODP2048:
    # 50-digit
    p = int(2810255506518299868219687655921025336002922004875663)
    q = int(82654573721126466712343754585912509882438882496343)
    g = int(8)
    h = int(10200)

    # 250-digit
    # p = int(5554053263402624785673387123401890600422195865746459511213572804465388888673782810180238504823775733345501561201936684986963667080842979342023391333068308225584964785575876917135170750062489154407210832944461799040516295312260671396312891883324978444209)
    # q = int(4508160116398234403955671366397638474368665475443554798062964938689439033014434099172271513655662121221998020456117439112795184318866054660733272185932068364922861027253146848324002232193578859096762039727647564156263226714497298211292931723478066919)
    # g = int(939)
    # h = int(2381)

    # 700-digit
    # p = int(43541296145345379426170554180353055727191440646523138191278605133104043501069900637178068451850606698411911485342148022147355705107838524243636850891185413502399523850157398804062945667319354045255849182960668983815150659740281717722477110392351095854735899708492172956051119618057860321500212138549501371187196597552572635312301159251199958169676040680109293061695464169017481134411121279452609027687687198948998116523640131689706661612636436792306748526202691151208303114245920433933826094978515705357656419896335497655149086955592799824878597905138897642230913329944260680880698934449447023017285691302331403670981902334678579988147035305187250018758718790570525477359846226751954604142777127419100863)
    # q = int(8114292982733018901634467793580517280505300157756827840342639793720470276010044844796509215775364647486379330104761092461303709487111167395385175343120651044055073397345769437954332028945090205973881696414586094635697103939672329057487348190896588865958982427970960297437778534859832337215842739200428880206335556755977009935203346860081989968258673253840718051005490899928714337385598449394820914589580171254006357906008224317873026763443242041056047060417944679688464985882579283252669790342623128094978833376134084542517533908981140481714237403119436757776912659326176049362783998220172758668894090812957771835814741396697461794287557828025950432120521578563273476958599744083480172221911503432557)
    # g = int(20125)
    # h = int(26551)

    # ---------------- OLD VALUES -----------
    # p = int(563)
    # p = int(23)
    # p = int(11)

    # q = int(281)
    # q = int(11)
    #  q = int(5)

    # g = int(3)
    # g = int(2)
    # g = int(3)

    # h = int(529)
    # h = int(13)
    # h = int(9)

    #  p = int(1299743) q = int(649871) g = int(2) h = int(10309)
    t = int(3)
    n = int(5)

    MAX_COORDINATE = 100000
    MAX_RANDOM = 5000000
# questi valori sono stati ottenuti dallo script PrimeNumbers


class parametres:
    CHAR_DATA_SPLIT = "||"
    CHAR_MSG_SPLIT = "|||"
    CHAR_LOG_DATA_SPLIT = "|-|"
    CHAR_LOG_MSG_SPLIT = "-|-"
    DELIM_LOG = ".-."
    # local MAC
    # inside container
    PATH_DATA_USERS = "/home-user/data_users"

    # in questo file ogni ES si salva MC,k',EMS, tutte le info per quell'utente.
    # per ogni riga ho MC||k'||MS
    FILE_NAME_INFORMATION = "information"
    FILE_NAME_EMS = "ems"

    WHICH_PHASE = ['SHA1', 'SHA2', 'REC1', 'REC2']
    WHICH_LOG = ['MSG', 'ERROR']
    DEBUG = True

    # INTERFACE = 'lo0'  # local MAC
    INTERFACE = 'eth2'  # containter
    PORT_TO_LISTEN = 6000


    IP_DEALER = "MasterJarvis"
    PORT_DEALER = 8000

    IP_LOG = "LOG"
    PORT_LOG = 5000
    END_MESSAGES = "end"

    BUFFER_SIZE_REQUEST_MESSAGES = 16384  # byte
    TIMEOUT_CONNECTIONS = 3  # secondi
    DELIM = "---"

    # SHARING CODES
    COD200 = "200"  # Everything is went well
    COD100 = "100"  # User already signed-up [DEALER]

    COD300 = "300"  # Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]
    COD300_desc = "Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]"

    COD150 = "150"  # User already signed-up [External Server]
    COD150_desc = " User already signed-up [External Server]"

    COD170 = "170"  # User_id is not present -> Dealer did not contact me or client is anticipating the steps
    COD170_desc = "User_id is not present -> Dealer did not contact me or client is anticipating the steps"

    COD400 = "400"  # MC_from_client != MC_from_Dealer
    COD400_desc = "MC_from_client != MC_from_Dealer"

    COD444 = "444"  # Generale error
    COD444_desc = "General error,try again later"

    COD500 = "500"  # Problem while Shareholder was saving the share



    # RECONSTRUCTION CODES
    COD600 = "600"  # user_id is not presetn --> you have to pass to signup before

    COD700 = "700"  # x_i given to the SHAREHOLDER is not right --> deaelr compromised? (1)
    COD700_desc = "x_i given to the SHAREHOLDER is not right --> dealer compromised? (1)"
    COD750 = "750"  # (s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)
    COD750_desc = "(s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)"
    COD760 = "760"  # user_id is not present --> you have to pass to signup before
    COD760_desc = "user_id is not present --> you have to pass to signup before"

    COD800 = "800"  # Insufficient shares from shareholders --> check shareholders and xi given from client
    COD830 = "830"  # Some SHAREHOLDERS give to the dealer INCORRECT shares (3)
    COD850 = "850"  # Insufficient correct shares -> too much shareholder that cheated (4)
    COD860 = "860"  # Client is cheating

    COD900 = "900"  # user_id is not presetn --> you have to pass to signup before
    COD900_desc = " user_id is not present --> you have to pass to signup before"

    COD930 = "930"  # E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)
    COD930_desc = "E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)"

    COD960 = "960"  # D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)
    COD960_desc = "D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)"


    COD1000 = "1000"  # D_k'[MS] != MC External Server is cheating (6)
    COD2000 = "2000"  # D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)
    COD2400 = "2400"  # MC != D_k[MS] --> ExternalServer is cheating (8)
    COD2600 = "2600"  # MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)
    COD3000 = "3000"  # Unrecognized phase
    COD3000_desc = "Unrecognized phase"

    # OLD
    COD450 = "450"  # (s_i,t_i) given by DEALER TO SHAREHOLDER is not consistent with commitments
    COD550 = "550"  # S' != \overline(S')
    COD650 = "650"  # error in REC-Client MC!=D_k'[MS]
    COD222 = "222"  # error in ES-REC2 --> D_k[MC] != g^S' h^r'
    COD333 = "333"  # error in ES-REC2 --> E_ms_fromDealer !=E_ms_fromClient
    COD555 = "555"  # error in ES-SHA2 --> MC_client != MC Dealer
    COD777 = "777"  # error in ES-SHA1 --> E_k'[MC] != D_k'[MC]
    COD999 = "999"  # error in SHA1 ES
    COD888 = "888"  # error in REC1 ES