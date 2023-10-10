import HAT

while True:
    text = input("HAT shell ->\n")
    result, error = HAT.run('stdin', text)

    if error: print(error.asString())
    else: print(result)