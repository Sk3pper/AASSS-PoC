const g = 2;
const h= 10309;
const q= 649871;
const p = 1299743;

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
    return (x.multiply(y)).mod(q);
}


function genRand(max) {
    return Math.floor(Math.random() * Math.floor(max));
}


// nel primo messaggio verso il dealer invio MC = E_k[g^S' h^r']
function firstMessage(S){
    // compute S'
    var r =genRand(Number.MAX_SAFE_INTEGER);
    var S_prime = sPrime(S, r);
    console.log("s'="+S_prime);

    // compute pre-MC
    var r_prime =genRand(Number.MAX_SAFE_INTEGER);
    var pre_MC = pedersenModq(S_prime, r_prime).toString();
    console.log("pre_MC="+pre_MC);

    // compute MC = E_k[pre-MC] = E_k[(g^S' g^r') mod q] //CON AES -->
    var key = genRand(Number.MAX_SAFE_INTEGER).toString();
    var result = AES_encrypt(pre_MC,key);

    result = JSON.parse(result);

    var ciphertext_base64 = result['ciphertext']; //MC
    var key_base64 = result['key'];
    var iv_base64 = result['iv'];

    // checks that everithing is went well
    var plaintext= AES_dencrypt(ciphertext_base64,key_base64, iv_base64);
    if (plaintext !== pre_MC) {
        alter("plaintext !== pre_MC: \nplaintext=" + plaintext + "\npre_MC=" + pre_MC);
        return null;
    }else{
        // save everything
        saveData(S_prime,r,pre_MC,r_prime,ciphertext_base64,key_base64,iv_base64);

        var Json_data  = JSON.stringify({
            S_prime:S_prime,
            r:r,
            pre_MC:pre_MC,
            r_prime:r_prime,
            MC:ciphertext_base64,
            key_base64:key_base64,
            iv_base64:iv_base64});

        console.log(Json_data);


        return Json_data;
    }
}












function getSavedData(){
    var S_prime = localStorage.getItem("S_prime");
    var r = localStorage.getItem("r");
    var preMc = localStorage.getItem("preMc");
    var r_prime = localStorage.getItem("r_prime");
    var MC = localStorage.getItem("MC");
    var key_base64 = localStorage.getItem("key_base64");
    var iv_base64 = localStorage.getItem("iv_base64");

    var Json_data  = JSON.stringify({
            S_prime:S_prime,
            r:r,
            preMc:preMc,
            r_prime:r_prime,
            MC:MC,
            key_base64:key_base64,
            iv_base64:iv_base64});

    return Json_data;
}

function saveData(S_prime,r,preMc,r_prime,MC,key_base64,iv_base64){
    // Store
    localStorage.setItem("S_prime", S_prime);
    localStorage.setItem("r", r);
    localStorage.setItem("preMc", preMc);
    localStorage.setItem("r_prime", r_prime);
    localStorage.setItem("MC", MC);
    localStorage.setItem("key_base64", key_base64);
    localStorage.setItem("iv_base64", iv_base64);
}


