import tweepy

consumer_key = "vpKETAsmeeFPr0HqYdwQEGsSM";
#eg: consumer_key = "YisfFjiodKtojtUvW4MSEcPm";


consumer_secret = "QCXRMjpWV9HNzM4BPgiMdFovNDwouUDFEccNm6yni25sZ2KR8I";
#eg: consumer_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token = "405109277-U28FwefgUhZRtPUTB4vqVnxrog2LRNYa9ASTZBiO";
#eg: access_token = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token_secret = "mxqM7w3IsjRYgEiMbbYu7pv5BOSwWhZLtmbxRWEkjUKoD";
#eg: access_token_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
