import argcurse
import creation
import reconstruction
import verify


# TODO
# Allow output and inputs in the form of base 64 or 16

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

arg_handler.add_flag("-f", "--field-limit", description="The field limit of the secret", required=True,
                     has_content=True, content_help="<Limit>", modes="reconstruct")
arg_handler.add_flag("-p", "--parts-file", description="The file holding the required parts", required=True,
                     has_content=True, content_help="<File Path>", modes="reconstruct")

arg_handler.generate_help_message("Secret-Sharing [mode] [options]")
arg_handler.compile()

if arg_handler.results.mode_used == "create":
    parts_list, field_limit = creation.create_part_list(arg_handler.results.result_dict["-s"].flag_content,
                                                        int(arg_handler.results.result_dict["-n"].flag_content),
                                                        int(arg_handler.results.result_dict["-k"].flag_content))

    print(f"Field Limit : {field_limit}")
    print()
    print("Part Number | Value")
    for part in parts_list:
        print(f"{part[0]} | {part[1]}")

elif arg_handler.results.mode_used == "reconstruct":
    parts_list = reconstruction.read_parts_from_file(arg_handler.results.result_dict["-p"].flag_content)
    field_limit = int(arg_handler.results.result_dict["-f"].flag_content)

    secret = reconstruction.retrieve_secret(parts_list, field_limit)
    print(f"Secret : {secret}")
