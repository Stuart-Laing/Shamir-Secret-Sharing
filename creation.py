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


def create_part_list(secret_string, total_parts_to_create, minimum_parts_for_reconstruction):
    secret_number = text_conversion.encode(secret_string)

    random_field_limit = random.randint(max(secret_number, total_parts_to_create) * 2,
                                        max(secret_number, total_parts_to_create) * 4)
    poly_numbers = []

    while len(poly_numbers) != (minimum_parts_for_reconstruction - 1):
        random_number = random.randint(2, random_field_limit - 1)
        if random_number not in poly_numbers:
            poly_numbers.append(random_number)

    secret_poly = Polynomial(secret_number, *poly_numbers)

    parts = []
    for x_coord in range(1, total_parts_to_create + 1):
        parts.append((x_coord, secret_poly.find_y(x_coord) % random_field_limit))

    return parts, random_field_limit
