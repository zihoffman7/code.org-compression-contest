# Load a new file with refreshed data
def load():
    global file
    # Create list of valid compression tokens
    chars = [chr(i) if len(chr(i)) == 1 else None for i in range(9728, 10200)]
    chars.pop(1)
    [chars.remove(i) for i in ["☔", "☕", "☘", "☙", "☦", "☧", "☩", "☨", "☪", "☫", "☬", "☭"]]
    # Set initial file data
    file = {"content" : "", "len" : 0, "dict" : {}, "chars" : chars}
    #GettysburgAddressLosslessCompressionContest
    with open("test.txt", "r") as f:
        file["content"] = f.read().replace(" ", "_").lower()
        file["len"] = len(file["content"])

# Get the percent improvement for a certain phrase or for the current file state
evaluate = lambda f, p="": 100 - (len(f["content"].replace(p if len(p) else " ", " ")) - 1 + len(f["dict"].keys()) + int(any(p)) + len(p) + sum((len(i) for i in f["dict"].values()))) / f["len"] * 100

# Replace a selected phrase with a compression token
def compress(d, phrase):
    if not phrase:
        return False
    d["content"] = d["content"].replace(phrase, d["chars"][0])
    d["dict"][d["chars"][0]] = phrase
    # Remove the compression token from the file data so it can't be reused
    d["chars"].pop(0)
    return d

# Greedy algorithm to choose the best phrase to be replaced
def greedy_optimum(min_str=2, max_str=12, min_score=0):
    # Initialize empty base data
    best = {"phrase" : "", "score" : min_score}
    # Test different indexes
    for i in range(0, len(file["content"])):
        # Test different lengths
        for j in range(min_str, max_str + 1):
            # Get the phrase
            sec = file["content"][i:i + j]
            # Evaluate the efficiency of the phrase being compressed
            eval = evaluate(file, sec)
            # If phrase is better, update best data
            if eval > best["score"]:
                best = {"phrase" : sec, "score" : eval}
    return best["phrase"] if len(best["phrase"]) else False

def compression(args={}):
    global file
    # Grab new data
    load()
    while (True):
        # Extract the best phrase according to greedy algorithm
        best = greedy_optimum(**args)
        # Quit if greedy optimum is not an improvement
        if not best:
            break
        # Double check that the greedy optimum is an improvement
        if evaluate(file) <= evaluate(file, best):
            compress(file, best)
        else:
            break
    # Return the optimum percentage and data
    return evaluate(file), file

def optimize(min_str_threshold=[2], max_str_threshold=[4, 12]):
    # Hold the best percentage and the data associated with it
    opt, opt_items, max_params = 0, [], []
    # Call algorithm with a different selection size
    for i in range(min_str_threshold[0], min_str_threshold[-1] + 1):
        for j in range(max_str_threshold[0], max_str_threshold[-1] + 1):
            # Evaluate the compression with specified selection data
            f = compression({"min_str" : i, "max_str" : j, "min_score" : 0})
            # If result is more optimal, update
            if f[0] > opt:
                opt = f[0]
                opt_items = [f[1]]
                max_params = [(i, j),]
            # If result is equal to optimum, record it
            elif f[0] == max:
                opt_items.append(f[1])
                opt_params.append((i, j),)
            print(f"Trial result: {f[0]}\nOptimum: {opt}\n")
    # Display all compressed values
    [print(i) for i in opt_items[0]["dict"].values()]
    print("\nListed above are the values to copy and paste\n")
    print(f"The greedy maximum is {str(opt)} % \nOptimal parameters: {max_params}\n\t0: min_str_threshold, 1: max_str_threshold\n")

optimize()
