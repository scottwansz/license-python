from calendar import timegm
from datetime import timedelta, datetime, timezone

import jwt
from jwt import ExpiredSignatureError, ImmatureSignatureError, InvalidAudienceError, MissingRequiredClaimError


def create_license_file(payload):
    private_key = b'-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDRqgzCndVfRq1q\nS+6oX4hA/sSVnjQgdSeuH0QD403v7ULpKwr5a7a2avej8jTqHwWHVX9cu94RfvRp\ndMk1mle/G87s5dyfoFWysvzvNtgrS+uJHwAtx5+Guk+ma2o1KU2ipOksj9UCv75e\nj8h0aiPB+VdTeHd3wFdRDcQ4HaJKOo0ddxpprlSzoOlC+i2RAN9NxrGd9XfQOXEu\nBP0b79o0qMczwIqa6FwqJL44cnRS/EYmxcfD0ZP8qEObw4ZM7npRrb7W14cxpkor\nsUNk46qW4wChJSZyqKIp2orgR+m2YG81ctQtOnVvP/wJEmQYUqiNeyEWWjAF5aEi\n6zyTziidAgMBAAECggEADZuRT3JJ/nCKYctC1pe4sqs2XBWUAYVJCYKK+gufK9LE\n1HhQMob8qVNA9lmKeKWByNpSNVUWISGRwGRtiLaXOlaWNAbpLk0MMthuFSKEni7D\nvzcNXmtF3csqzzzKfF/NY6B7Z8KACzkhpGaFlpSq9HR35/l6G4IWyLJxiUjXFyUe\ng7tkyTwhQLtLOJuq/DMIZmrTo/aVFHYpnZTTB7Hx4d/dUoD/lGRKxARVfd+7Tg95\ngrM3IiBSBdvS0jVJD0JacMAcnzoFj4LbfODhnCsmJQ9DeiB9DRmAXCI22E1KZX6/\nJZ/7XSJ+RSKEjJZ0qJ6mfp9RrY6Ju0Ou32RqbpNVqwKBgQDUtsnzFKG3idXkhFzR\n+/3y9WdLNnsdrVgSf+CEMUxRfig8KR1gyv+BE58T2IgyCq+cd8QbUU9/DBcQjcXD\n0IKr4F0lNbyhAyl7OZLANy+B0vNjh6d3wLjk19dri+a6Xoo63qGkf85Fb4k643QT\nYETP+qrHI2zww5fh47/8djXbHwKBgQD8VGKsNu5ud6uqJBB8yFGUeh+KG2PHpDwn\nxrOtdSCvg3Mj1LjD1YO7+8N5ytJTBszxxo4/VxD0KGYQxufOT1ExOzRpKNCz9GIW\nAsxrdlzH4kZt66ld1IpE0gXU/89+UdbyvpHPtErZr1GKhaT7KRB1CjvLfy01ChC1\n4iJxnm/AwwKBgFSwtjUm+MAni9ag8IfWSaSrGkYy2c/WDWPIMC7Rpe4oSYKyZ/T6\nvcG5ezOemZM69/JXKOgrdnhB6wj3OU8ePHiMKum+vGxq4uAh6xDGqA6LW8Y742xl\neff7C9TQ7bs0GtsXesoQ7KJupvegSb3RLXSU+9uvehdd+KHCWNT+h7DHAoGAJaG4\nLZLrsFHsqi1CwDln4UrtVT2MfgPCbPQ3a9EiFMr36woYnCxFv01m880J3RQQkKZa\nJJwpjSBRSINBowU1SLBZuq05ovz5e+ri7cvzPmRCuLYCxlmiXW0tLX0RRveRpRZC\nzMVIvHpnIM+ZsVOIfswN6uWGqnhb0aRuGp/Ubt0CgYEAs+dRIjI4oaTPg+StBcy5\nEzTQi57p8daJFfFWX117kahucPXdTpMtWAofjVyFJlcGKgyb95UgseLKVzk87Y+r\nbFAgHUsrcGN4RyV8J3wiVkfPtaNG4ZXL74aOc/rxl7tRkKE9KRU+KxlIxRZmE7JQ\neHMLp1OX6KN+x83CHyEaG+8=\n-----END PRIVATE KEY-----\n'
    public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0aoMwp3VX0atakvuqF+I\nQP7ElZ40IHUnrh9EA+NN7+1C6SsK+Wu2tmr3o/I06h8Fh1V/XLveEX70aXTJNZpX\nvxvO7OXcn6BVsrL87zbYK0vriR8ALcefhrpPpmtqNSlNoqTpLI/VAr++Xo/IdGoj\nwflXU3h3d8BXUQ3EOB2iSjqNHXcaaa5Us6DpQvotkQDfTcaxnfV30DlxLgT9G+/a\nNKjHM8CKmuhcKiS+OHJ0UvxGJsXHw9GT/KhDm8OGTO56Ua2+1teHMaZKK7FDZOOq\nluMAoSUmcqiiKdqK4EfptmBvNXLULTp1bz/8CRJkGFKojXshFlowBeWhIus8k84o\nnQIDAQAB\n-----END PUBLIC KEY-----\n'

    encoded = jwt.encode(payload, private_key, algorithm="RS256")
    # print(encoded)

    f = open('license.dat', 'w')
    f.write(encoded)
    f.close()

    try:
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"], audience="win-client")
        print(decoded)
    except ExpiredSignatureError:
        print('Signature has expired')
    except ImmatureSignatureError:
        print('The token is not yet valid (nbf)')
    except InvalidAudienceError:
        print("Invalid audience")
    except MissingRequiredClaimError:
        print('Token is missing the "aud" claim')
    except Exception as err:
        print('error:', err)


if __name__ == '__main__':
    now = timegm(datetime.now(tz=timezone.utc).utctimetuple())

    nbf = now + timedelta(days=0).total_seconds()
    exp = now + timedelta(days=90).total_seconds()

    payload = {
        "iss": "智眸医疗",
        "aud": ['win-client', 'ai-server'],
        "nbf": nbf,
        "exp": exp,
        "usr": "爱尔眼科",
        "mac": "d8:5e:d3:f9:6e:d2",
    }

    create_license_file(payload)
