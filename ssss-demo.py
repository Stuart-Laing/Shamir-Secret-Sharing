import shamir_secret_sharing_system as ssss
from shamir_secret_sharing_system.fraction import Fraction


# print(f"54 base 16 into base 10        : {ssss.conversions.base_converter('54', 16, 10)}")
# print(f"ff base 16 into base 16        : {ssss.conversions.base_converter('ff', 16, 16)}")


# Fraction(10, 20) / Fraction(20, 10), Fraction(1, 4)
print(Fraction(10, 20))
print(Fraction(20, 10))
print(Fraction(1, 4))

print(Fraction(10, 20) / Fraction(20, 10))

# shamir_secret_sharing_system.verify.Base("16", True)
# shamir_secret_sharing_system.verify.Secret("wow thats neat ☞")
