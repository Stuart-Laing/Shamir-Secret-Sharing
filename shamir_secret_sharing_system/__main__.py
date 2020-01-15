import argcurse
import shamir_secret_sharing_system as ssss

# TODO
# Allow output and inputs in the form of base 64 or 16
# Make sure n is larger or the same as k
# Allow you to save numbers instead of letters, using the actual number value would be faster
# Only the part values need to be in various bases, the numbers/x_coordinates must be in base 10
# Verify base
# make better errors
# Possible option to not bother with field limits
# Learn how sub packages work
# Print more messages about the created secret or parts list, give more detail to the user
# type hints son
# Have verify return more specific errors
# Make all functions use in built verify functionality
# kill self

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
    secret_string = arg_handler.results.result_dict["-s"].flag_content
    ssss.verify.Secret(secret_string)

    total_parts_to_create = arg_handler.results.result_dict["-n"].flag_content
    min_parts_to_reconstruct = arg_handler.results.result_dict["-k"].flag_content
    ssss.verify.NAndK(total_parts_to_create, min_parts_to_reconstruct, command_line_arg=True)

    if arg_handler.results.result_dict["-ob"].flag_used:
        base = arg_handler.results.result_dict["-ob"].flag_content
        ssss.verify.Base(base)
    else:
        base = 10

    secret_number = ssss.conversions.string_to_integer(secret_string)

    parts_list, field_limit = ssss.creation.create_part_list(secret_number, int(total_parts_to_create),
                                                             int(min_parts_to_reconstruct))

    print(f"Field Limit : {field_limit}")
    print()
    print("Part Number | Value")
    for part in parts_list:
        print(f"{part[0]} | {part[1]}")

elif arg_handler.results.mode_used == "reconstruct":
    parts_file_path = arg_handler.results.result_dict["-p"].flag_content

    try:
        ssss.verify.PartsFile(parts_file_path, 10)
    except FileExistsError:
        print("ERROR")
        print("Chosen parts file does not exist")
        exit()
    except PermissionError:
        print("ERROR")
        print("Chosen part file cannot be opened")
        exit()
    except ssss.errors.PartsFileCountError:
        print("ERROR")
        print("Chosen file does not contain enough entries")
        exit()
    except ssss.errors.PartsFileFormatError:
        print("ERROR")
        print("Parts File must be in the format '<PartNum> <PartValue>' 1 per line")
        exit()
    except ssss.errors.PartsFileBaseError:
        print("ERROR")
        print("Part values must be in the specified base")
        exit()

    if arg_handler.results.result_dict["-ib"].flag_used:
        base = arg_handler.results.result_dict["-ib"].flag_content
        ssss.verify.Base(base)

        base = int(base)
    else:
        base = 10

    field_limit = arg_handler.results.result_dict["-f"].flag_content
    ssss.verify.FieldLimit(field_limit, base)

    parts_list = ssss.reconstruction.read_parts_from_file(parts_file_path, base)

    secret = ssss.reconstruction.retrieve_secret_number(parts_list, field_limit)
    print(f"Secret : '{secret}'")
