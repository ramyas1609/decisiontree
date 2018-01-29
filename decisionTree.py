import sys, math


class Node:
    def __init__(self):
        self.data_points = []


class Tree:
    def __init__(self):
        self.attributes = []
        self.attributes_values = []
        self.label = []
        self.label_values = []
        self.root = Node()

    def readcsv(self, csv_file):
        input_file = open(csv_file, "r")
        line_number = 1

        for line in input_file.readlines():
            data = line.split(",")
            if line_number == 1:
                line_number = line_number + 1
                self.attributes = data[0:-1]
                self.label = data[-1].rstrip()
            else:
                x = 0
                self.attributes_values.append(data[0:-1])
                self.label_values.append(data[-1].rstrip())
        #print self.attributes
        #print self.attributes_values
        #print self.label
        #print self.label_values

        input_file.close()

        print len(self.label_values)

        for x in range(0,len(self.label_values)):
            self.root.data_points.append(x)

    def calculate_hofy(self, node):
        label_count = {}
        for i in node.data_points:
            label = self.label_values[i]
            if not label_count.has_key(label):
                label_count[label] = 0
            label_count[label] = label_count[label] + 1
        x, y = label_count.values()[0], label_count.values()[1]
        total = x + y
        x1 = x * 1.0 / total
        y1 = y * 1.0 / total
        entropy = - ((x1 * math.log(x1, 2)) + (y1 * math.log(y1, 2)))
        return entropy
        #print entropy


t = Tree()
t.readcsv(sys.argv[1])
t.calculate_hofy(t.root)
