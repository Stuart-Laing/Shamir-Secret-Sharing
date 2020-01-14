import random
import conversions

import reconstruction

MERSENNE_PRIMES_EXPONENTS = (5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279)


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

    def find_y(self, x, field_limit):
        y = 0
        for index, value in enumerate(self.values):
            exponentiation = (x ** index) % field_limit  # X^2, X^3 ect
            term = (value * exponentiation) % field_limit  # 29876128573619287 * (X^3)
            y = (y + term) % field_limit

            # y += (value * (x ** index)) % field_limit
        return y

        # exponentiation = (x ** i) % prime
        # term = (coefficients[i] * exponentiation) % prime
        # y = (y + term) % prime

def check_reconstruct(parts_list, minimum_parts_for_reconstruction, field_limit, secret_string):
    return True


    for i in range(0, len(parts_list), minimum_parts_for_reconstruction):
        current_check_block = parts_list[i:i + minimum_parts_for_reconstruction]

        current_check_block += [parts_list[filler_index] for filler_index in
                                range(0, minimum_parts_for_reconstruction - len(current_check_block))]

        try:
            possible_secret_number = reconstruction.retrieve_secret(current_check_block, field_limit)
        except ValueError:
            return False

        if possible_secret_number == secret_string:
            return True
        return False


def create_part_list(secret_string, total_parts_to_create, minimum_parts_for_reconstruction):
    secret_number = conversions.encode(secret_string)

    field_limit = 0
    for exponent in MERSENNE_PRIMES_EXPONENTS:
        if (2 ** exponent) - 1 > max(secret_number, total_parts_to_create):
            field_limit = (2 ** exponent) - 1
            break

    if field_limit == 0:
        pass
        # TODO Raise an error boi

    reconstruct_successful = False

    parts = []

    while not reconstruct_successful:
        # ########## THIS PART IS SCUFFED ##########
        poly_numbers = set()
        while len(poly_numbers) != (minimum_parts_for_reconstruction - 1):
            poly_numbers.add(random.randint(2, field_limit - 1))
        # ########## THIS PART IS SCUFFED ##########

        # print(f"secret='{secret_string}'")
        # print(f"secret_number={secret_number}")
        # print()
        # print(f"field_limit={field_limit}")
        # print(f"poly_numbers={poly_numbers}")

        secret_poly = Polynomial(secret_number, *poly_numbers)

        # print(f"Polynomial={secret_poly}")
        # print()

        parts = []
        for x_coord in range(1, total_parts_to_create + 1):
            # print(f"Part Num : {x_coord}")
            # print(f"    x coord           : {x_coord}")
            # print(f"    y coord           : {secret_poly.find_y(x_coord)}")
            # print(f"    field limit       : {field_limit}")
            # print(f"    y mod field limit : {secret_poly.find_y(x_coord) % field_limit}")
            # print(f"    {secret_poly.find_y(x_coord)} % {field_limit} : {secret_poly.find_y(x_coord) % field_limit}")
            parts.append((x_coord, secret_poly.find_y(x_coord, field_limit)))

        if check_reconstruct(parts, minimum_parts_for_reconstruction, field_limit, secret_string):
            reconstruct_successful = True

    return parts, field_limit


"""
parts_list, fieldf_limit = create_part_list("WoW", 5, 3)
m : {x_coord}")
        print(f"    x coord           : {x_coord}")
        print(f"    y coord           : {secret_poly.find_y(x_coord)}")
        print(f"    field limit       : {field_limit}")
        print(f"    y mod field limit : {secret_poly.find_y(x_coord) % field_limit}")
        print(f"    {secret_poly.
import reconstruction
try:
    secret_num = reconstruction.retrieve_secret([parts_list[0]] + [parts_list[1]] + [parts_list[3]], fieldf_limit)

    print()
    print(f"secret_num : {secret_num}")
    print(f"secret_string : {text_conversion.decode(secret_num)}")
except ValueError:
    print()
    print("Failed")
"""

"""
field_limit = 12530321

Correct poly numbers
     12530321
    {7850883, 8919095}
    {7734833, 11425650}
    {1152528, 2158133}
    {3544734, 2046382}
    {2235755, 9316350}
    
Incorrect poly numbers
     12530321
    {5626665,  6852859}
    {6097572,  5750599}
    {11628633, 11202851}
    {4099041,  5587235}
    {1204458,  10425771}
"""
