import sys
from twocaptcha import TwoCaptcha

def solve(url: str, sitekey, iv, cp_context):
    API_KEY = "XXXXXXXXXXXXXXX"  # Substitua pelo seu API_KEY da 2Captcha

    solver = TwoCaptcha(API_KEY)

    try:
        result = solver.amazon_waf(
            sitekey='0x1AAAAAAAAkg0s2VIOD34y5',
            iv=iv,
            context=cp_context,
            url=url
        )
    except Exception as e:
        sys.exit(e)

    else:
        sys.exit('solved: ' + str(result))