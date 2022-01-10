// 50-digit
const g = 8;
const h = 10200;
const q = 82654573721126466712343754585912509882438882496343;
const p = 2810255506518299868219687655921025336002922004875663;
const max_random = 2810255506518299868219687655921025336002922004875663;

function sPrime(s,r) {
    var sPr, s_int;
    s_int = strToInt(s);
    console.log("S= "+s+ "-- secret encoded becomes--> S="+s_int);
    sPr = pedersenModq(parseInt(s_int), parseInt(r));
    return sPr;
}

function strToInt(s) {
    var f, n;
    n = s.length;
    f = 0;
    for (var i = 0, _pj_a = n; (i < _pj_a); i += 1) {
        f += (encode(s[i]) * Math.pow(94, ((n - i) - 1)));
    }
    return f;
}

function encode(c) {
    var x;
    x = String.charCodeAt(c);
    console.log(x);
    if (((x > 32) && (x < 127))) {
        return (x - 33);
    }
    console.log("Sorry, I can only handle standard ASCII characters 33-126!");
    exit(1);
}

function pedersenModq(m, r) {
    console.log("m: "+m+" r: "+r);
    var x = bigInt(g).modPow(m, q);
    var y = bigInt(h).modPow(bigInt(r), q);
    return bigInt((bigInt(x).multiply(bigInt(y)))).mod(q);

}


function genRand(max) {
    return bigInt.randBetween("0", max);
    // return Math.floor(Math.random() * Math.floor(max));
}

/*
 *
 *   SHARING FUNCTIONS
 *
 */

// nel primo messaggio verso il dealer invio MC = E_k[g^S' h^r']
function firstMessage(S){
    // compute S'
     console.log("Number.MAX_SAFE_INTEGER= "+genRand(bigInt(max_random)));
    var r = genRand(bigInt(max_random));
    var S_prime = sPrime(S, r);
    console.log("s'="+S_prime);

    // compute pre-MC
    var r_prime = genRand(bigInt(max_random));
    var pre_MC = pedersenModq(S_prime, r_prime).toString();
    console.log("pre_MC="+pre_MC);

    // compute MC = E_k[pre-MC] = E_k[(g^S' g^r') mod q] //CON AES -->
    var key = genRand(Number.MAX_SAFE_INTEGER).toString();
    console.log("key="+ key);
    var ciphertext = AES_encrypt(pre_MC, key);

    // checks that everithing is went well
    var plaintext= AES_decrypt(ciphertext, key);

    if (plaintext !== pre_MC) {
        alert("plaintext !== pre_MC: \nplaintext=" + plaintext + "\npre_MC=" + pre_MC);
        return null;
    }else{
        var Json_data  = JSON.stringify({
            S_prime:S_prime,
            r:r,
            pre_MC:pre_MC,
            r_prime:r_prime,
            MC:ciphertext,
            key:key});
        console.log(Json_data);
        return Json_data;
    }
}
function getSavedData(){
    // var S_prime = localStorage.getItem("S_prime");
    var r = localStorage.getItem("r");
    var preMc = localStorage.getItem("preMc");
    var r_prime = localStorage.getItem("r_prime");
    var MC = localStorage.getItem("MC");
    var key = localStorage.getItem("key");
    var MS = localStorage.getItem("MS");
    var Coordinates = localStorage.getItem("Coordinates");

    var Json_data  = JSON.stringify({
            // S_prime:S_prime,
            r:r,
            preMc:preMc,
            r_prime:r_prime,
            key:key,
            MC:MC,
            MS:MS,
            Coordinates:Coordinates});
    console.log("getSavedData: "+Json_data);

    return Json_data;
}

function saveData(r, preMc, r_prime, MC, key, MS, Coordinates){
    // Store
    //localStorage.setItem("S_prime", S_prime);
    localStorage.setItem("r", r);
    localStorage.setItem("preMc", preMc);
    localStorage.setItem("r_prime", r_prime);
    localStorage.setItem("MC", MC);
    localStorage.setItem("key", key);
    localStorage.setItem("Coordinates", Coordinates);
    localStorage.setItem("MS",MS)
}

/*
 *
 *   RECONSTRUCTION FUNCTIONS
 *
 */

function ricalculateS_prime(S, r) {
    var S_prime = sPrime(S, r);
    console.log("s'="+S_prime);
}


function computeEms(k, preMC, MS) {
    console.log("------------------------------- COMPUTE E_MS ----------------------");
    var data = preMC + "||" + k;

    console.log("data: " + data);
    var Ems = AES_encrypt (data, MS);
    console.log("   eMS: "+Ems);
    console.log("----------------------------END COMPUTE E_MS ----------------------");
    return Ems;

}

// compute new data for the reconstruction
function newData(S){
     console.log(" ------------------------- newData Calculating ------------------------");
    // compute S'
    var r_second = genRand(bigInt(max_random));
    var S_second = sPrime(S, r_second);
    console.log("S_second="+S_second);

    // compute pre-MC
    var r_third = genRand(bigInt(max_random));
    var pre_MC_prime = pedersenModq(S_second, r_third).toString();
    console.log("pre_MC_prime'="+pre_MC_prime);

    // compute MC' = E_k[pre-MC] = E_k[(g^S'' g^r''') mod q] //CON AES -->
    var key_second = genRand(Number.MAX_SAFE_INTEGER).toString();
    console.log("key_second="+ key_second);
    var ciphertext = AES_encrypt(pre_MC_prime, key_second);

    // checks that everithing is went well
    var plaintext= AES_decrypt(ciphertext, key_second);

    if (plaintext !== pre_MC_prime) {
        alert("plaintext !== pre_MC_prime: \nplaintext=" + plaintext + "\npre_MC_prime=" + pre_MC_prime);
        return null;
    }else{
       // save date only in the end
        var Json_data  = JSON.stringify({
            S_second:S_second,
            r_second:r_second,
            pre_MC_prime:pre_MC_prime,
            r_third:r_third,
            MC_prime:ciphertext,
            key_second:key_second});

        console.log(Json_data);
         console.log(" ------------------ end newData Calculating-------------------------------------");

        return Json_data;
    }
}



function saveData2(r_second,pre_MC_prime,r_third,MC_prime,key_second){
    // Store
    //localStorage.setItem("S_second", S_second);
    localStorage.setItem("r_second", r_second);
    localStorage.setItem("pre_MC_prime", pre_MC_prime);
    localStorage.setItem("r_third", r_third);
    localStorage.setItem("MC_prime", MC_prime);
    localStorage.setItem("key_second", key_second);
}

