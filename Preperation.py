import random

import text_conversion


class Polynomial:
    def __init__(self, *values):
        # TODO Find a better name than 'values'
        self.values = values

    def __repr__(self):
        # output_string = f"{self.values[0]} + "

        output_string = " + ".join([f"{num}x^{index}" for index, num in enumerate(self.values)])

        return output_string

    def find_x(self, y):
        pass

    def find_y(self, x):
        y = 0
        for index, value in enumerate(self.values):
            y += value * (x ** index)
        return y


s = "WoW"
total_parts = 5
min_parts_required = 3

secret = text_conversion.encode(s)

random_field_limit = random.randint(max(secret, total_parts) * 2, max(secret, total_parts) * 4)
poly_numbers = []

while len(poly_numbers) != (min_parts_required - 1):
    random_number = random.randint(2, random_field_limit - 1)
    if random_number not in poly_numbers:
        poly_numbers.append(random_number)

secret_poly = Polynomial(secret, *poly_numbers)

parts = []
for x_coord in range(1, total_parts + 1):
    parts.append((x_coord, secret_poly.find_y(x_coord) % random_field_limit))

print(f"String Secret  : {s}")
print(f"Encoded Secret : {secret}")
print()
print(f"Total parts the secret is split into      : {total_parts}")
print(f"Minimum parts required for reconstruction : {min_parts_required}")
print()
print(f"Random field limit : {random_field_limit}")
print(f"Random numbers for polynomial: {poly_numbers}")
print()
print(f"Secret Polynomial : {secret_poly}")
print(f"Secret Parts : ")
for part in parts:
    print(part)
