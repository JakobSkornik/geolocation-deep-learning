def loader(current, max):
    if current == 0:
        print("[", end="")

    if current % (max / 10) == 0:
        print("#", end="")
    
    if current == max - 1:
        print("]")