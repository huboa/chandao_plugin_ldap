import jwt
payload = {'test': '123'}
token = jwt.encode(payload, 'key123', algorithm='HS256')

print(token)
decode_token=jwt.decode(token, 'key123', algorithms='HS256')
print(decode_token)