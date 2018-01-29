import sys, math

input_file = open(sys.argv[1],"r")
output_file = open(sys.argv[2],"w")

line_number = 1
label_count = {}

for line in input_file.readlines():
    if line_number == 1:
        line_number = line_number + 1
        continue

    data = line.split(",")
    label = data[-1].rstrip()

    if not label_count.has_key(label):
        label_count[label] = 0

    label_count[label] = label_count[label] + 1

x, y = label_count.values()[0], label_count.values()[1]
total = x + y
x1 = x * 1.0 / total
y1 = y * 1.0 / total
entropy = - ((x1 * math.log(x1, 2)) + (y1 * math.log(y1, 2)))
min_count = min(x, y)
error = (min_count * 1.0 / total)

output_file.write("entropy: " + str(entropy) + "\n")
output_file.write("error: " + str(error) + "\n")

input_file.close()
output_file.close()

