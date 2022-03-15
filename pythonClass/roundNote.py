def roundNote(n):
    n = str(n)
    if n[1:3] == ".0":
        return n[0]
    else:
        return n[0:3]

# note = 4.333
# print(roundNote(note))
