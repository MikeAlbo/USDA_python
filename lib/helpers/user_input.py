def welcome(options):
    print("USDA CSV DATA PARSER")
    print('Select "parse", "search", or "quit"')
    selection = _parse_select_or_quit()
    if selection == "search":
        print("search unavailable at this time...")
        quit()
    print("select parser:")
    return user_select_parse_type(options)


def user_select_parse_type(options):
    try:
        temp = input("Parser type:\n===========\n%s\n===========\nselect: " % _display_options(options))
        if temp not in options:
            raise temp
        print("lets go!")
        return temp
    except TypeError:
        print("Must select one of:\n%s" % _display_options(options))
        quit()


def _display_options(options):
    s = ""
    for i in options:
        s += "%s \n" % i
    return s


def _parse_select_or_quit():
    user_in = input().lower().strip()
    opt = ["parse", "search", "quit"]
    if user_in in opt:
        if user_in == "quit":
            print("Bye, Bye...")
            quit()
        return user_in
    print("must select: %s", _display_options(opt))


def user_ready():
    if input("Proceed? (y/n): ").lower() != "y":
        print("Until next time...")
        quit()







