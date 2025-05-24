'''
Special Cases:
SC1: something followed by :
SC2: something followed by : and "
SC3: something followed by =
SC4: something followed by = and "
SC5: something followed by " and :

# special cases
"SC1":r'({})(("|\')?):(\s*?)(("|\')?)([^\s]+)(\5)',
"SC2":r'({})(("|\')?):(\s*?)(("|\'))([^\s]+)(\5)',
"SC3":r'({})((\'|")])?()(\s*?)=(\s*?)(("|\')?)([^\s]+)(\7)',
"SC4":r'({})((\'|")])?()(\s*?)=(\s*?)(("|\'))([^\s]+)(\7)',
"SC5":r'({})([^\s]*?)(\s*?)("|\')([^\s]+)(\4);'


'''


regexes = {

    # hashes 
    "LDB-hashes":r"\$6\$.{103}",
    "Base64 strings >=10":r"[-A-Za-z0-9+/]{10,}={0,3}",

    # emails
    "Email":r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',    

    # tokens
    "SlackToken":r'(xox[pboa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})',
    "GenericPrivateKeyBlock":r'BEGIN.*PRIVATE KEY',
    "UsernamePasswordCombo":r'^[a-z]+://.*:.*@',
    "FacebookOauth":r"[fF][aA][cC][eE][bB][oO][oO][kK].*['|\"][0-9a-f]{32}['|\"]",
    "TwitterOauth":r"[tT][wW][iI][tT][tT][eE][rR].*['|\"][0-9a-zA-Z]{35,44}['|\"]",
    "GitHub":r"[gG][iI][tT][hH][uU][bB].*['|\"][0-9a-zA-Z]{35,40}['|\"]",
    "GoogleOauth":r"(\"client_secret\":\"[a-zA-Z0-9-_]{24}\")",
    "AWSApiKey":r"AKIA[0-9A-Z]{16}",
    "HerokuApiKey":r"[hH][eE][rR][oO][kK][uU].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
    "GenericApiKey":r"[aA][pP][iI]_?[kK][eE][yY].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
    "GenericSecret":r"[sS][eE][cC][rR][eE][tT].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
    "SlackWebhook":r"https://hooks[.]slack[.]com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
    "Google-GCP-ServiceAccount1":r"\"type\": \"service_account\"",
    "TwilioApiKey":r"SK[a-z0-9]{32}",
    "PasswordInURL":r"[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
    "Amazon-MWS-AuthToken":r"(amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    "FacebookAccessToken":r'(EAACEdEose0cBA[0-9A-Za-z]+)',
    "GoogleApiKey":r'(AIza[0-9A-Za-z\\-_]{35})',
    "GoogleCloudPlatformAPIKey":r"(AIza[0-9A-Za-z\\-_]{35})",
    "GoogleCloudPlatformOauth":r"([0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com)",
    "GoogleDriveApiKey":r"(AIza[0-9A-Za-z\\-_]{35})",
    "GoogleDriveOauth":r"([0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com)",
    "Google-GCP-ServiceAccount2":r'("type": "service_account".*)',
    "GoogleGmailApiKey":r"(AIza[0-9A-Za-z\\-_]{35})",
    "GoogleGmailOauth":r"([0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com)",
    "GoogleOauthAccessToken":r"(ya29\\.[0-9A-Za-z\\-_]+)",
    "GoogleYouTubeApiKey":r"(AIza[0-9A-Za-z\\-_]{35})",
    "GoogleYouTubeOauth":r"([0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com)",
    "MailChimpApiKey":r"([0-9a-f]{32}-us[0-9]{1,2})",
    "MailgunApiKey":r"(key-[0-9a-zA-Z]{32})",
    "PaypalBraintreeAccessToken":r"(access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32})",
    "PicaticApiKey":r"(sk_live_[0-9a-z]{32})",
    "StripeApiKey":r"(sk_live_[0-9a-zA-Z]{24})",
    "StripeRestrictedApiKey":r"(rk_live_[0-9a-zA-Z]{24})",
    "SquareAccessToken":r"(sq0atp-[0-9A-Za-z\\-_]{22})",
    "SquareOAuthSecret":r"(sq0csp-[0-9A-Za-z\\-_]{43})",
    "TwitterAccessToken":r"[tT][wW][iI][tT][tT][eE][rR].*[1-9][0-9]+-[0-9a-zA-Z]{40}",
    "Kubernetes Token":r'[a-z0-9]{6}\.[a-z0-9]{16}',
    "JWT":r"e[yw][A-Za-z0-9-_]+\.(?:e[yw][A-Za-z0-9-_]+)?\.[A-Za-z0-9-_]{2,}(?:(?:\.[A-Za-z0-9-_]{2,}){2})?",
    "JSESSIONID":r"\b([A-F0-9]+)((\.[A-Za-z0-9]+)*)\b",
    "PHPSESSID":r'\b([a-z0-9]{26})\b',
    "Jenkins Breadcrumb":r'[a-z0-9]{32}|[a-z0-9]{64}',
    "Jenkins API Token":r'11[a-z0-9]{32}',
    "XOR encoded passwords":r'\b(password="{xor}.*")\b',

    # ip addresses
    "IPv4 Address":r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
    "IPv6 Address":r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))',

    # credentials in commands
    "Creds in curl command":r'\b(curl .*(?:-u|--user) .*:.*)\b',
    "Usernames in ftp command":r'\b(ftp .*@.*)\b',
    "Creds in xml structure":r'(?:(name=".*".*value=".*")|(value=".*".*name=".*"))',
    "Creds in netcool command":r'\b(netcool .*-password .*)\b',
    "Creds in keytool command":r'\b(keytool .*-srcstorepass .*)\b',
    "Creds in openssl command":r'\b(openssl .*-passout pass:.*)\b',
    "Creds in ldapsearch":r'\b(ldapsearch .*(?:-w|-W).*)\b',    

    # credentials in urls
    "Creds in url":r'\b((?:http|https|ftp|sftp)://.*:.*@.*)\b',
    "Creds in url (no pw)":r'\b((?:http|https|ftp|sftp)://.*@.*)\b',
    "Creds in JDBC conn string":r'\b((?:jdbc|JDBC):.*/.*@.*)\b',

    # common hash types
    "MD5 hash":r"[a-f0-9]{32}",
    "SHA1 hash":r"[a-f0-9]{40}"
}