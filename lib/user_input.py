def user_select_parse_type(options):
    try:
        temp = input("Parser type: %s " % options)
        if temp not in options:
            raise temp
        print("lets go!")
        return temp
    except TypeError:
        print("Must select one of %s" % options)
        quit()


def user_ready():
    if input("Proceed? (y/n): ").lower() != "y":
        print("Until next time...")
        quit()
