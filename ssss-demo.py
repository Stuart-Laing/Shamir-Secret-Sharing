import shamir_secret_sharing_system as ssss


print(f"54 base 16 into base 10        : {ssss.conversions.base_converter('54', 16, 10)}")
print(f"ff base 16 into base 16        : {ssss.conversions.base_converter('ff', 16, 16)}")


# shamir_secret_sharing_system.verify.Base("16", True)
# shamir_secret_sharing_system.verify.Secret("wow thats neat ☞")
