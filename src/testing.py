x = -100000000000
for i in range(1000000):
    #print((x%360 + 360)%360, "------")
    #print(x%360)
    if str(x%360).find("-") != -1:
        print("DAWG")
    x += 1