from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode, json_decode

# https://jwcrypto.readthedocs.io/en/latest/jws.html#examples

prk = {
    "d": "ISMf7sYys5cN3yj0e6YDWh93A1pd6HFtoTsYw6x4gIUV4PrHqTsOPIaeEo1ObVK77jFtNaYc1RWC3TvqJzoMGjEHhomoKW29LU6HI8VUTb6_TzWUO-gXfxB2QaJzeTPKfoDe4vu3N0qZHkbFVTwHYIMCbhzqTcgB1t17KoqLGMWWG8lugZ8lMbsN7GvKZ5rVCTIbKy7ODvJ6mUkVLKI45A8etjlHS63-oczCwyhMeW-ge4Gjn2L16NAJeRfyUOXq5Zz859WK75ZZ73W6zY_A_CmwGanD3G7pdNgN1v0fVBFIhop4PfobZlL3U5b-iyWsnSDuAIBbE8gRaJGDFuoStQ",
    "dp": "Z1Ypi-T0jWOOK3QENOA0vnywOmPyTn0huvDwPPA1F20AXDlZsicgrlrsq71Cu-fs5gbqpvxxY9TyR5vHW_k9zbVF4DtIQlorwVIYv1siuHqS8wCw3U4eeO1gvTmMGFZvyv5FdCnjNQW3TsyFdgD9j4DynMj0FlKg5ymkTJZBWZ0",
    "dq": "lTOuN_gAeoeoEjRl0fI18lVAS_wkXT_HodDO6-IJPmCSLNsh1mvWs7pRqN-UjHG03F3gQHpLz_U23iXTJvERVW5DbSmOTu9Vd0Mx0MaUPdcmypfYlPvx-ngs2FK2tM-ZGxGmXOHUNZhFnChKIcgAv3OVW3p0Q0Cjw_PSGhm9IpU",
    "e": "AQAB", "kty": "RSA",
    "n": "rcSw3-OuSUZ_uvymEthMKUAZ8vhMYTjzhgjWr1B_1qfM38G-Ioo5JrIgzt9dKua5I-ubQ0UYoWsiPQbQSpCSAzqXyRZDxaPTWLQkh03qlfjsi3NeOtNZRBeQFECblkTEjAixbTyJ2vjQQUy6oIHhDMt7132HBwG1LkOLrHDrTXbWB3GVYujRaNjeIkpdplJAT7b11xiJgzbawCjRRlnHbd-PgMTTzWcM1VMa8Q6SekjC01iXs6YUMl6Cz0DZ3v6-l0pzjMRfUtjtcMZ_0IYFCJn9QPysZx3Twsj-cp7HnC_UEvKWpJKUq24Sg7WFLhGRW_vzg7vfQnBBEoCAWbheIQ",
    "p": "tUcyKsM6lXPIUvTx15ZRtpDBc5hJT2-3eW_ALPR7NEcgdGS3bChW0RennzO7dM3hRfuM8m7OcDC4t8vcEGwrxCF96PhV4si_5Fs00ldo_0aRvBABoX98647kN69QlzWbgxSiv4xhp0Rv_-qmTGTdZEnwQ9YKq88fhs_Gl4ZXbCU",
    "q": "9WUMZAgzXIi0uO2OIhAzu_IdNsxKdPd68ckF8nnbD7T26xv4evokPqIgacg7IcaPUeLMQJifwU2BQ8b73G9aPIEJYfLt0_n9OnlrJHZFJNqYAPfAgT14V2NWuoCm_AZv1-CAylmAVwsQfqCxfFk3DHWZwNhgw9o-Lkr2V-ZmS00",
    "qi": "qWvqEUVHMuysNk7HsxfLhk6irhkbZVbkZ2AkqcgdxtebuikN9Eh_i78QxxQaLA-y7BUkMKTx0uP4VT7zfFpRVagDOOowWBSWkhsSi78qS4irD6ZLoJal5slj4aIKwzX3H7th3w78_TljVWYSTyxWCaz4_D22HiixQHI1zoYmDEg"}


puk = {"e": "AQAB", "kty": "RSA",
       "n": "rcSw3-OuSUZ_uvymEthMKUAZ8vhMYTjzhgjWr1B_1qfM38G-Ioo5JrIgzt9dKua5I-ubQ0UYoWsiPQbQSpCSAzqXyRZDxaPTWLQkh03qlfjsi3NeOtNZRBeQFECblkTEjAixbTyJ2vjQQUy6oIHhDMt7132HBwG1LkOLrHDrTXbWB3GVYujRaNjeIkpdplJAT7b11xiJgzbawCjRRlnHbd-PgMTTzWcM1VMa8Q6SekjC01iXs6YUMl6Cz0DZ3v6-l0pzjMRfUtjtcMZ_0IYFCJn9QPysZx3Twsj-cp7HnC_UEvKWpJKUq24Sg7WFLhGRW_vzg7vfQnBBEoCAWbheIQ"}

public_key = jwk.JWK(**puk)
private_key = jwk.JWK(**prk)
# private_key = jwk.JWK.generate(kty='RSA', size=2048)

# f = open("d:/license.dat", "w")
# f.write()

# public_key.import_key(**puk)
# private_key.import_key(**prk)

print(private_key.export_private())
print(private_key.export_public())

# public_key.import_key(**json_decode(private_key.export_public()))

payload = "My Encrypted message"

protected_header = {
    "alg": "RSA-OAEP-256",
    "enc": "A256CBC-HS512",
    "typ": "JWE",
    "kid": public_key.thumbprint(),
}

jwetoken = jwe.JWE(payload.encode('utf-8'),
                   recipient=public_key,
                   protected=protected_header)
enc = jwetoken.serialize()

jwetoken = jwe.JWE()
jwetoken.deserialize(enc, key=private_key)
payload = jwetoken.payload
