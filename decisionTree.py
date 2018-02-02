import sys, math


class Node:
    def __init__(self):
        self.data_points = []
        self.left = None
        self.right = None
        self.attribute = None
        self.left_return_label = None
        self.right_return_label = None


class Tree:
    def __init__(self, max_depth):
        self.attributes_names = []
        self.attributes_values = []
        self.label_name = "None"
        self.label_values = []
        self.attribute_values_unique = {}
        self.label_values_unique = []
        self.root = Node()
        self.max_depth = max_depth

    def read_csv(self, csv_file):

        input_file = open(csv_file, "r")
        line_number = 1

        for line in input_file.readlines():
            data = line.split(",")
            if line_number == 1:
                line_number = line_number + 1
                self.attributes_names = data[0:-1]
                self.label_name = data[-1].rstrip()
            else:
                self.attributes_values.append(data[0:-1])
                self.label_values.append(data[-1].rstrip())

        for label in self.label_values:
            if label not in self.label_values_unique:
                self.label_values_unique.append(label)
            if len(self.label_values_unique) == 2:
                break

        for attr in self.attributes_names:
            if not self.attribute_values_unique.has_key(attr):
                self.attribute_values_unique[attr] = []

        for row in self.attributes_values:
            for i in range(0, len(self.attributes_names)):
                    attr_value = row[i]
                    if attr_value not in self.attribute_values_unique[self.attributes_names[i]]:
                        self.attribute_values_unique[self.attributes_names[i]].append(attr_value)
        #print self.attributes_names
        #print self.attributes_values
        #print self.label_name
        #print self.label_values
        #print self.attribute_values_unique
        #print self.label_values_unique

        input_file.close()

        for x in range(0, len(self.label_values)):
            self.root.data_points.append(x)

    def calculate_hofy(self, node):
        x = 0
        y = 0
        for i in node.data_points:
            label = self.label_values[i]
            if label == self.label_values_unique[0]:
                x = x + 1
            elif label == self.label_values_unique[1]:
                y = y + 1
        total = x + y
        x1 = x * 1.0 / total
        y1 = y * 1.0 / total
        entropy = - ((x1 * math.log(x1, 2)) + (y1 * math.log(y1, 2)))
        return entropy

    def calculate_hofy_given_x(self, node, attr):
        x = len(node.data_points)
        x0 = 0
        x1 = 0  #x=x0+x1
        x00 = 0
        x01 = 0 #x0=x00+x01
        x10 = 0
        x11 = 0 #x1=x10+x11

        col = self.attributes_names.index(attr)
        datapoints_x0 = []
        datapoints_x1 = []
        for i in node.data_points:
            attr_value = self.attributes_values[i][col]
            if attr_value == self.attribute_values_unique[attr][0]:
                x0 = x0 + 1
                datapoints_x0.append(i)
                label_value = self.label_values[i]
                if label_value == self.label_values_unique[0]:
                    x00 = x00 + 1
                elif label_value == self.label_values_unique[1]:
                    x01 = x01 + 1
            elif attr_value == self.attribute_values_unique[attr][1]:
                x1 = x1 + 1
                datapoints_x1.append(i)
                label_value = self.label_values[i]
                if label_value == self.label_values_unique[0]:
                    x10 = x10 + 1
                elif label_value == self.label_values_unique[1]:
                    x11 = x11 + 1
        #if (x0 + x1 != x) or (x00 + x01 != x0) or (x10 + x11 != x1):
            #print ("Something wrong")
        #else:
            #print x0, x00, x01, x1, x10, x11
        if x00 == 0 or x01 == 0:
           t01 = 0
        else:
            t0 = (x00 * 1.0 / x0)
            t1 = (x01 * 1.0 / x0)
            t01 = (t0 * math.log(t0, 2)) + (t1 * math.log(t1, 2))
        if x10 == 0 or x11 == 0:
            t23 = 0
        else:
            t2 = (x10 * 1.0 / x1)
            t3 = (x11 * 1.0 / x1)
            t23 = (t2 * math.log(t2, 2)) + (t3 * math.log(t3, 2))
        hofy_given_x = ((x0 * 1.0 / x) * (-t01)) + ((x1 * 1.0 / x) * (-t23))
        distribution = [datapoints_x0, x00, x01, datapoints_x1, x10, x11]
        return hofy_given_x, distribution

    def construct_tree(self, node, depth):
        if depth > int(self.max_depth):
            return
        max_mutual_info = 0.0
        max_attr = None
        max_distr = []
        hofy = self.calculate_hofy(node)
        for attr in self.attributes_names:
            hofy_given_x, distribution = self.calculate_hofy_given_x(node, attr)
            mutual_info = hofy - hofy_given_x
            if mutual_info > max_mutual_info:
                max_mutual_info = mutual_info
                max_attr = attr
                max_distr = distribution

        if max_mutual_info == 0.0:
            return
        #else:
            #print max_attr, max_distr[1], max_distr[2], max_distr[4], max_distr[5]

        node.attribute = max_attr

        node_right = Node()
        node.right = node_right
        node_right.data_points = max_distr[0]

        node_left = Node()
        node.left = node_left
        node_left.data_points = max_distr[3]

        if max_distr[1] == 0 or max_distr[2] == 0:
            if max_distr[1] == 0:
                index = 1
            if max_distr[2] == 0:
                index = 0
            node.right_return_label = self.label_values_unique[index]
        if max_distr[4] == 0 or max_distr[5] == 0:
            if max_distr[4] == 0:
                index = 1
            if max_distr[5] == 0:
                index = 0
            node.left_return_label = self.label_values_unique[index]

        if (max_distr[1] == 0 or max_distr[2] == 0) and (max_distr[4] == 0 or max_distr[5] == 0):
            return

        if max_distr[1] == 0 or max_distr[2] == 0:
            self.construct_tree(node_left, depth+1)
        elif max_distr[4] == 0 or max_distr[5] == 0:
            self.construct_tree(node_right, depth+1)
        else:
            self.construct_tree(node_right, depth+1)
            self.construct_tree(node_left, depth+1)

    def majority_vote_classifier(self):
        x = 0
        y = 0
        for label in self.label_values:
            if label == self.label_values_unique[0]:
                x = x + 1
            elif label == self.label_values_unique[1]:
                y = y + 1
            if x > y:
                index = 0
            else:
                index = 1
            majority_vote = self.label_values_unique[index]
            return majority_vote

    def print_tree(self, node):
        if node is None:
            return
        self.print_tree(node.right)
        print node.attribute, node.right_return_label, node.left_return_label
        self.print_tree(node.left)


max_depth = sys.argv[2]
t = Tree(max_depth)
t.read_csv(sys.argv[1])
if max_depth == 0:
    t.majority_vote_classifier()
else:
    t.construct_tree(t.root, 0)
t.print_tree(t.root)






