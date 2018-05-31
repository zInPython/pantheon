import sys

bw = 12.0
for arg in sys.argv:
    arg_val = None

    if "=" in arg:
        arg_val = arg[arg.find("=") + 1:]

    if "--bw=" in arg:
        bw = float(arg_val)

next_val = 0
excess = 0.0
with open("link.trace", "w") as trace:
    for i in range(0, 30000):
        excess += 1.0/bw
        while (excess >= 1.0/12.0):
            next_val += 1
            excess -= 1.0/12.0
        trace.write(str(next_val) + "\n")
