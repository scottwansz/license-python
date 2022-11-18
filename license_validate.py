import uuid

import jwt
from jwt import ExpiredSignatureError, ImmatureSignatureError, InvalidAudienceError

public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0aoMwp3VX0atakvuqF+I\nQP7ElZ40IHUnrh9EA+NN7+1C6SsK+Wu2tmr3o/I06h8Fh1V/XLveEX70aXTJNZpX\nvxvO7OXcn6BVsrL87zbYK0vriR8ALcefhrpPpmtqNSlNoqTpLI/VAr++Xo/IdGoj\nwflXU3h3d8BXUQ3EOB2iSjqNHXcaaa5Us6DpQvotkQDfTcaxnfV30DlxLgT9G+/a\nNKjHM8CKmuhcKiS+OHJ0UvxGJsXHw9GT/KhDm8OGTO56Ua2+1teHMaZKK7FDZOOq\nluMAoSUmcqiiKdqK4EfptmBvNXLULTp1bz/8CRJkGFKojXshFlowBeWhIus8k84o\nnQIDAQAB\n-----END PUBLIC KEY-----\n'

'''
校验网卡物理地址
检验License文件有效期，包括生效期与失效期
返回授权的用户信息，包括机构名称
'''


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def license_validate(license_file_path):
    with open(license_file_path, 'r') as f:
        try:
            decoded = jwt.decode(f.read(), public_key, algorithms=["RS256"], audience="win-client")
            if decoded.get('mac') == get_mac_address():
                return True, decoded
            else:
                print(get_mac_address())
                return False, {'err': 'mac-error'}
        except ExpiredSignatureError:
            print('Signature has expired')
            return False, {'err': 'expired'}
        except ImmatureSignatureError:
            print('The token is not yet valid (nbf)')
            return False, {'err': 'not-yet'}
        except InvalidAudienceError:
            print("Invalid audience")
            return False, {'err': 'wrong-audience'}
        except Exception as err:
            print('error:', err)
            return False, {'err': 'unknown-error'}


if __name__ == '__main__':
    print(license_validate('license.dat'))
