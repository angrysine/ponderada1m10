import jwt


jwtToDecode = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEifQ.m7PfmznOzVM_99aKLPdkxx35CUs2uux6DYgR1MDlLzA"

print(jwt.decode(jwtToDecode,"secret",algorithms=["HS256"]))