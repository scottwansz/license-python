"""
https://pyjwt.readthedocs.io/en/latest/usage.html
https://www.jianshu.com/p/35c264a55826
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa


# cryptography 生成证书言式
def crypto_certificate_rsa():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Private Key serialization
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.PKCS8,
                                            encryption_algorithm=serialization.NoEncryption()
                                            )

    # Public Key serialization
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return {"key_private": pem_private, "key_public": pem_public}


# 自带证书方式
def self_certificate_rsa():
    with open("rsa/rsa_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Private Key serialization
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.PKCS8,
                                            encryption_algorithm=serialization.NoEncryption()
                                            )

    # Public Key serialization
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return {"key_private": pem_private, "key_public": pem_public}


def rsa_256_encoded(data_dict, key_private):
    encoded = jwt.encode(data_dict, key_private, algorithm='RS256')
    return encoded


def rsa_256_decoded(data_bytes, key_public):
    encoded = jwt.decode(data_bytes, key_public, algorithms=["RS256"])
    return encoded


if __name__ == "__main__":
    key = crypto_certificate_rsa()

    print(key.get("key_private"))
    print(key.get("key_public"))

    data_encoded = rsa_256_encoded({"hello": "test"}, key.get("key_private"))
    data_decoded = rsa_256_decoded(data_encoded, key.get("key_public"))
    print(data_encoded)
    print(data_decoded)
