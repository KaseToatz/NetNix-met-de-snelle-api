from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"])

yes = ctx.hash("bestebaas")

print(yes)