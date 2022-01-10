/*
    SHARING CODE
 */

const COD200 = "200"; // Everything is went well

const COD100 = "100"; // User already signed-up [DEALER]
const COD100_desc = "User already signed-up [DEALER]";

const COD300 = "300"; // Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]
const COD300_desc = "Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]";

const COD150 = "150"; // User already signed-up [External Server]
const COD150_desc = "User already signed-up [External Server]";

const COD170 = "170"; // User_id is not present -> Dealer did not contact me or client is anticipating the steps
const COD170_desc = " User_id is not present -> Dealer did not contact me or client is anticipating the steps";

const COD400 = "400"; // MC_from_client != MC_from_Dealer
const COD400_desc = "MC_from_client != MC_from_Dealer";

const COD500 = "500"; // Problem while Shareholder was saving the share
const COD500_desc = "Problem while Shareholder was saving the share";

const COD530 = "530"; // User already signed-up  [Shareholder]
const COD530_desc = "User already signed-up  [Shareholder]";

const COD550 = "550"; // Problem with SHA2, user_id dir is not present. Send MC before
const COD550_desc = "Problem with SHA2, user_id dir is not present. Send MC before";

const COD444 = "444"; // General error
const COD444_desc = "General error";

const COD5 = "5";
const COD5_desc = "Error in REC1, maybe client has sent malformed json";

const COD15 = "15";  // Error in SHA1, maybe client has sent malforme json
const COD15_desc = "Error in SHA1, maybe client has sent malforme json"

const COD30 = "30";  // Error in SHA2, maybe client has sent malforme json
const COD30_desc = "Error in SHA2, maybe client has sent malforme json"

const COD45 = "45";
const COD45_desc = "Error in SHA2, maybe client has sent a malformed json";

function checkError(error) {
    var msg = '';
    if (error === COD100)
        msg = COD100_desc;
    else if (error === COD300)
        msg = COD300_desc;
    else if (error === COD150)
        msg = COD150_desc;
    else if (error === COD170)
        msg = COD170_desc;
    else if (error === COD400)
        msg = COD400_desc;
    else if (error === COD500)
        msg = COD500_desc;
    else if (error === COD300)
        msg = COD100_desc;
    else if (error === COD550)
        msg = COD550_desc;
    else if (error === COD530)
        msg = COD530_desc;
    else if (error === COD444)
        msg = COD444_desc;
    else if (error === COD5)
        msg = COD5_desc;
    else if (error === COD15)
        msg = COD15_desc;
    else if (error === COD30)
        msg = COD30_desc;
    else if (error === COD45)
        msg = COD45_desc;
    else
        msg = "Error not found: "+error;

    alert(msg)
}


/*
    RECONSTRUCTION CODE
 */

const COD600 = "600"; // user_id is not present --> you have to pass to signup before
const COD600_desc = "user_id is not present --> you have to pass to signup before";

const COD700 = "700"; // x_i given to the SHAREHOLDER is not right --> deaelr compromised? (1)
const COD700_desc ="x_i given to the SHAREHOLDER is not right --> deaelr compromised? (1)";

const COD750 = "750"; //  (s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)
const COD750_desc = "(s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)";

const COD760 = "760"; // user_id is not presetn --> you have to pass to signup before
const COD760_desc = "user_id is not presetn --> you have to pass to signup before";

const COD800 = "800"; // Insufficient shares from shareholders --> check shareholders and xi given from client
const COD800_desc = "Insufficient shares from shareholders --> check shareholders and xi given from client";

const COD830 = "830"; // Some SHAREHOLDERS give to the dealer INCORRECT shares (3)
const COD830_desc = "Some SHAREHOLDERS give to the dealer INCORRECT shares (3)";

const COD850 = "850"; // Insufficient correct shares -> too much shareholder that cheated (4)
const COD850_desc = "Insufficient correct shares -> too much shareholder that cheated (4)";

const COD860 = "860"; // Client is cheating, S' != S'_rebuilt
const COD860_desc = "Client is cheating, S' != S'_rebuilt";

const COD880 = "880"; // Less than n-coordinates
const COD880_desc ="Less than n-coordinates";

const COD900 = "900"; // user_id is not present --> you have to pass to signup before
const COD900_desc = "user_id is not present --> you have to pass to signup before";

const COD930 = "930"; // E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)
const COD930_desc = "E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)";

const COD960 = "960"; // D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)
const COD960_desc = "D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)";

const COD1000 = "1000"; // D_k'[MS] != MC External Server is cheating (6)
const COD1000_desc = "D_k'[MS] != MC External Server is cheating (6)";

const COD2000 = "2000"; // D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)
const COD2000_desc = "D_k[MC_given in SHA from client] != preMC --> Client is cheating (7)";

const COD2400 = "2400"; // MC != D_k[MS] --> ExternalServer is cheating (8)
const COD2400_desc = "MC != D_k[MS] --> ExternalServer is cheating (8)";

const COD2600 = "2600"; // MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)
const COD2600_desc = "MC'_from_Client != MC'_from_ExternalServer --> Es or client is cheating (9)";


function checkErrorRec(error) {
    var msg = '';
    if (error === COD600)
        msg = COD600_desc;
    else if (error === COD700)
        msg = COD700_desc;
    else if (error === COD750)
        msg = COD750_desc;
    else if (error === COD760)
        msg = COD760_desc;
    else if (error === COD800)
        msg = COD800_desc;
    else if (error === COD830)
        msg = COD830_desc;
    else if (error === COD850)
        msg = COD850_desc;
    else if (error === COD860)
        msg = COD860_desc;
    else if (error === COD880)
        msg = COD880_desc;
    else if (error === COD900)
        msg = COD900_desc;
    else if (error === COD930)
        msg = COD930_desc;
    else if (error === COD960)
        msg = COD960_desc;
    else if (error === COD1000)
        msg = COD1000_desc;
    else if (error === COD2000)
        msg = COD2000_desc;
    else if (error === COD2400)
        msg = COD2400_desc;
    else if (error === COD2600)
        msg = COD2600_desc;
    else if (error === COD444)
        msg = COD444_desc;
    else
        msg = "Error not found: "+error;

    alert(msg)
}