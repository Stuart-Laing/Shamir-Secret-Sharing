import argcurse
import shamir_secret_sharing_system as ssss


VERTICAL = "|"
HORIZONTAL = "-"
CROSS = "+"


def part_table(x_y_list):
    table_fields = ("X", "Y")
    clean_table = [[*table_fields]]

    max_x_length = len(table_fields[0])
    max_y_length = len(table_fields[1])

    for x_y in x_y_list:
        x, y = x_y
        x = str(x)
        y = str(y)

        if len(x) > max_x_length:
            max_x_length = len(x)

        if len(y) > max_y_length:
            max_y_length = len(y)

        clean_table.append([x, y])

    spaced_table = [["", ""] for _ in range(0, len(clean_table))]

    for row_index in range(0, len(clean_table)):
        spaced_table[row_index][0] = clean_table[row_index][0] + " " * (max_x_length - len(clean_table[row_index][0]))
        spaced_table[row_index][1] = clean_table[row_index][1] + " " * (max_y_length - len(clean_table[row_index][1]))

    formatted_table = f" {VERTICAL} {spaced_table[0][0]} {VERTICAL} {spaced_table[0][1]} {VERTICAL}\n"
    formatted_table += f" {CROSS}{HORIZONTAL * (max_x_length + 2)}{CROSS}{HORIZONTAL * (max_y_length + 2)}{CROSS}\n"

    for row in spaced_table[1:]:
        formatted_table += f" {VERTICAL} {row[0]} {VERTICAL} {row[1]} {VERTICAL}\n"

    return formatted_table


arg_handler = argcurse.Handler("-h", "--help")
arg_handler.add_default("""Usage: Secret-Sharing [mode] [options]
Try -h or --help for more info.""")

arg_handler.add_mode(options=("create", "reconstruct"), descriptions=("Create a new list of parts from a secret",
                                                                      "Create a secret from a list of parts"))

arg_handler.add_flag("-s", "--secret", description="The secret that will be split", required=True,
                     has_content=True, content_help="<Secret>", modes="create")
arg_handler.add_flag("-n", "--total-parts", description="The total number of parts to create", required=True,
                     has_content=True, content_help="<Parts>", modes="create")
arg_handler.add_flag("-k", "--min-reconstruct", description="Minimum parts to reconstruct the secret", required=True,
                     has_content=True, content_help="<Parts>", modes="create")
arg_handler.add_flag("-ob", "--output-base", description="The number base to outputs the results",
                     has_content=True, content_help="<Base>", modes="create", default="10")

arg_handler.add_flag("-f", "--field-limit", description="The field limit of the secret", required=True,
                     has_content=True, content_help="<Limit>", modes="reconstruct")
arg_handler.add_flag("-p", "--parts-file", description="The file holding the required parts", required=True,
                     has_content=True, content_help="<File Path>", modes="reconstruct")
arg_handler.add_flag("-ib", "--input-base", description="The number base of the input values",
                     has_content=True, content_help="<Base>", modes="reconstruct", default="10")

arg_handler.generate_help_message("Secret-Sharing [mode] [options]")
arg_handler.compile()

if arg_handler.results.mode_used == "create":
    print()
    secret_string = arg_handler.results.result_dict["-s"].flag_content
    try:
        ssss.verify.Secret(secret_string)
    except ssss.errors.SecretStringLengthError:
        print("### ERROR ###")
        print(f"Secret string length cannot be less than {ssss.verify.SECRET_STRING_MIN_LEN}"
              f" or greater than {ssss.verify.SECRET_STRING_MAX_LEN}")
        exit()
    except ssss.errors.SecretStringEncodingError:
        print("### ERROR ###")
        print("Secret string must only contain ascii characters")
        exit()

    total_parts_to_create = arg_handler.results.result_dict["-n"].flag_content
    min_parts_to_reconstruct = arg_handler.results.result_dict["-k"].flag_content
    try:
        ssss.verify.NAndK(total_parts_to_create, min_parts_to_reconstruct, command_line_arg=True)
    except TypeError:
        print("### ERROR ###")
        print("-n and -k must both be integers of base 10")
        exit()
    except ValueError:
        print("### ERROR ###")
        print("A parts list of length 1 would simply be the secret itself")
        exit()
    except ssss.errors.UnrecoverableSecretError:
        print("### ERROR ###")
        print("Creating fewer parts than required to reconstruct the secret would make it irrecoverable")
        exit()

    if arg_handler.results.result_dict["-ob"].flag_used:
        base = arg_handler.results.result_dict["-ob"].flag_content
        try:
            ssss.verify.Base(base, command_line_arg=True)

            base = int(base)
        except TypeError:
            print("### ERROR ###")
            print("Specified base must be an integer of base 10")
            exit()
        except ssss.errors.BaseNotSupportedError:
            print("### ERROR ###")
            print(f"The base specified is currently not supported please choose one of {ssss.verify.SUPPORTED_BASES}")
            exit()
    else:
        base = 10

    secret_number = ssss.conversions.string_to_integer(secret_string)

    parts_list, field_limit = ssss.creation.create_part_list(secret_number, int(total_parts_to_create),
                                                             int(min_parts_to_reconstruct))

    if base != 10:
        field_limit = ssss.conversions.base_converter(field_limit, 10, base)
        for part_index, part in enumerate(parts_list):
            parts_list[part_index] = (part[0], ssss.conversions.base_converter(part[1], 10, base))

    print(f"Splitting the secret '{secret_string}' into {total_parts_to_create} parts")
    print(f"Reconstruction of the secret will require a minimum of {min_parts_to_reconstruct} parts")
    print(f"Field limit and part y values are in base {base}")
    print()
    print(f"Field Limit : {field_limit}")
    print()
    print("Parts:")
    print(part_table(parts_list))

elif arg_handler.results.mode_used == "reconstruct":
    print()

    if arg_handler.results.result_dict["-ib"].flag_used:
        base = arg_handler.results.result_dict["-ib"].flag_content
        try:
            ssss.verify.Base(base, command_line_arg=True)
        except TypeError:
            print("### ERROR ###")
            print("Specified base must be an integer of base 10")
            exit()
        except ssss.errors.BaseNotSupportedError:
            print("### ERROR ###")
            print(f"The base specified is currently not supported please choose one of {ssss.verify.SUPPORTED_BASES}")
            exit()

        base = int(base)
    else:
        base = 10

    parts_file_path = arg_handler.results.result_dict["-p"].flag_content

    try:
        ssss.verify.PartsFile(parts_file_path, base)
    except FileExistsError:
        print("### ERROR ###")
        print("Chosen parts file does not exist")
        exit()
    except PermissionError:
        print("### ERROR ###")
        print("Chosen part file cannot be opened")
        exit()
    except ssss.errors.PartsFileCountError:
        print("### ERROR ###")
        print("Chosen file does not contain enough entries")
        exit()
    except ssss.errors.PartsFileFormatError:
        print("### ERROR ###")
        print("Parts File must be in the format '<PartNum> <PartValue>' 1 per line")
        exit()
    except ssss.errors.PartsFileBaseError:
        print("### ERROR ###")
        print("Part values must be in the specified base")
        exit()

    field_limit = arg_handler.results.result_dict["-f"].flag_content
    try:
        ssss.verify.FieldLimit(field_limit, base)

    except ValueError:
        print("### ERROR ###")
        print("Field limit must be in the specified base")
        exit()

    if base != 10:
        field_limit = ssss.conversions.base_converter(field_limit, base, 10)
    else:
        field_limit = int(field_limit)

    parts_list = ssss.reconstruction.read_parts_from_file(parts_file_path, base)

    secret_number = ssss.reconstruction.retrieve_secret_number(parts_list, field_limit)
    secret_string = ssss.conversions.integer_to_string(secret_number)

    print(f"Reconstructing the secret from {len(parts_list)} parts")
    print(f"Field limit has been defined as {field_limit}")
    print()
    print(f"Secret : '{secret_string}'")
