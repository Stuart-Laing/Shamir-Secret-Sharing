import argcurse

arg_handler = argcurse.Handler("-h", "--help")
arg_handler.add_default("""Usage: Secret-Sharing [options]
Try -h or --help for more info.""")

arg_handler.add_flag("-m", "--mode", description="Either 'create' or 'reconstruct'", required=True,
                     has_content=True, content_help="<Mode>")
arg_handler.add_flag("-s", "--secret", description="The secret that will be split", required=True,
                     has_content=True, content_help="<Secret>")
arg_handler.add_flag("-n", "--total-parts", description="The total number of parts to create", required=True,
                     has_content=True, content_help="<Parts>")
arg_handler.add_flag("-k", "--min-reconstruct", description="Minimum parts to reconstruct the secret", required=True,
                     has_content=True, content_help="<Parts>")


arg_handler.add_flag("-f", "--field-limit", description="The field limit of the secret", required=True,
                     has_content=True, content_help="<Limit>")
arg_handler.add_flag("-p", "--parts-file", description="The file holding the required parts", required=True,
                     has_content=True, content_help="<File Path>")

arg_handler.generate_help_message("Secret-Sharing [options]")

arg_handler.compile()
