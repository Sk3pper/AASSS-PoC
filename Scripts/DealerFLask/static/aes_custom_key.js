var keySize = 256;
var ivSize = 128;
var iterations = 100;

/**
 * @return {string}
 */
function AES_encrypt (msg, pass) {
  console.log("         --------------------------- AES_encrypt ----------------------------------------------------------------");
  var salt = CryptoJS.lib.WordArray.random(128/8);

    var key = CryptoJS.PBKDF2(pass, salt, {
      keySize: keySize/32,
      iterations: iterations
    });

  console.log("         key: "+key);

  var iv = CryptoJS.lib.WordArray.random(128/8);

  var encrypted = CryptoJS.AES.encrypt(msg, key, {
    iv: iv,
    padding: CryptoJS.pad.Pkcs7,
    mode: CryptoJS.mode.CBC

  });

  // salt, iv will be hex 32 in length
  // append them to the ciphertext for use  in decryption
  console.log("         salt: "+salt.toString());
  console.log("         iv: "+iv.toString());
  console.log("         encrypted: "+encrypted.toString());

  var transitmessage = salt.toString()+ iv.toString() + encrypted.toString();
  console.log("         transitmessage: "+transitmessage.toString());

   console.log("        ----------------------------------END AES_encrypt--------------------------------------------------------------------------------");
  return transitmessage;
}


function AES_decrypt (transitmessage, pass) {
  console.log("           --------------------------- AES_decrypt ----------------------------------------------------------------");
  // CryptoJS.enc.Base64.parse() gives HEX string, which is used in CryptoJS.AES.encrypt()
  var salt = CryptoJS.enc.Hex.parse(transitmessage.substr(0, 32));
  var iv = CryptoJS.enc.Hex.parse(transitmessage.substr(32, 32));
  var encrypted = transitmessage.substring(64);

  var key = CryptoJS.PBKDF2(pass, salt, {
      keySize: keySize/32,
      iterations: iterations
    });

  var decrypted = CryptoJS.AES.decrypt(encrypted, key, {
    iv: iv,
    padding: CryptoJS.pad.Pkcs7,
    mode: CryptoJS.mode.CBC

  });
  console.log("         decrypted: "+decrypted.toString(CryptoJS.enc.Utf8));
  console.log("         --------------------------- END AES_decrypt ----------------------------------------------------------------");
  var dec = decrypted.toString(CryptoJS.enc.Utf8);
  return dec;
}

