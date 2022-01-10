function AES_encrypt(plaintext, key){
    console.log ("\n\n-------------- ENCRYPTION-------------------------------------------");

    console.log ("PLAINTEXT: "+plaintext);
    console.log ("KEY: "+key);


    var ciphertext = CryptoJS.AES.encrypt(plaintext, key);

    var key_base64 = ciphertext.key.toString(CryptoJS.enc.Base64);
    var iv_base64 = ciphertext.iv.toString(CryptoJS.enc.Base64);
    var ciphertext_base64 = ciphertext.ciphertext.toString(CryptoJS.enc.Base64);

    console.log("data to use for decryption:\n"+
            "key_base64:       "+key_base64+
            "\niv_base64:      "+iv_base64+
            "\nciphertext_base64:      "+ ciphertext_base64);

   var Json_data  = JSON.stringify({
            key:key_base64,
            iv:iv_base64,
            ciphertext:ciphertext_base64})
    console.log(Json_data);

    return Json_data
}

// the data has to be base64 encoded
/**
 * @return {string}
 */
function AES_dencrypt(ciphertext_base64, key_base64, iv_base64){
    console.log ("\n\n-------------- DENCRYPTION-------------------------------------------");
    // translate from bas64 to bin
    var ciphertext_bin = CryptoJS.enc.Base64.parse(ciphertext_base64);
    var key_bin = CryptoJS.enc.Base64.parse(key_base64);
    var iv_bin = CryptoJS.enc.Base64.parse(iv_base64);

    // we have to pass the binary!
    var decrypted = CryptoJS.AES.decrypt({ciphertext: ciphertext_bin}, key_bin, {
      iv: iv_bin,
      mode: CryptoJS.mode.CBC
    });

    console.log("data to use for decryption:\n"+
            "key_base64:       "+key_base64+
            "\niv_base64:      "+iv_base64+
            "\nciphertext_base64:      "+ ciphertext_base64);

    console.log ("PLAINTEXT: "+decrypted.toString(CryptoJS.enc.Utf8));

    return decrypted.toString(CryptoJS.enc.Utf8)
}