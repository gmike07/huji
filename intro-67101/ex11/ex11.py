import itertools


class Node:
    """
    this object represent one part of the tree and his connections
    """

    def __init__(self, data, pos=None, neg=None):
        """
        :param data: gets a string of the data of the node
        :param pos: gets the positive child (Node) (default None)
        :param neg: gets the negative child (Node) (default None)
        """
        self.data = data
        self.positive_child = pos
        self.negative_child = neg

    def is_leaf(self):
        """
        :return: returns true if it is a leaf, else false
        """
        return self.positive_child is None and self.negative_child is None

    def has_left(self):
        """
        :return: returns true if it has a left child, else false
        """
        return self.negative_child is not None

    def has_right(self):
        """
        :return: returns true if it has a right child, else false
        """
        return self.positive_child is not None

    def get_left(self):
        """
        :return: returns the left child
        """
        return self.negative_child

    def get_right(self):
        """
        :return: returns the left child
        """
        return self.positive_child

    def set_right(self, node):
        """
        :param node: a Node object
        this function sets the right node to node
        """
        self.positive_child = node

    def set_left(self, node):
        """
        :param node: a Node object
        this function sets the left node to node
        """
        self.negative_child = node

    def set_data(self, data):
        """
        :param data: gets data
        this function sets the data to the input
        """
        self.data = data

    def get_data(self):
        """
        :return: returns the data of the tree
        """
        return self.data


class Record:
    """
    this object represents an illness by having the illness and it's symptoms
    """

    def __init__(self, illness, symptoms):
        """
        :param illness: gets an illness (string)
        :param symptoms: gets a list of string that represents the symptoms
        """
        self.illness = illness
        self.symptoms = symptoms

    def get_symptoms(self):
        """
        :return: returns the symptoms list
        """
        return self.symptoms

    def get_illness(self):
        """
        :return: returns the illness
        """
        return self.illness


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """
    this object is responsible for diagnosing the illness
    """

    def __init__(self, root):
        """
        :param root: gets the head of the tree
        """
        self.root = root

    def diagnose(self, symptoms):
        """
        :param symptoms: gets a list of string that represents the symptoms
        :return: the illness corresponding to the symptoms in the tree
        """
        return self.diagnose_helper(symptoms, self.root)

    def diagnose_helper(self, symptoms, root):
        """
        :param symptoms: gets a list of string that represents the symptoms
        :param root: gets a part of the tree (Node)
        :return: the illness corresponding to the symptoms in the tree (string)
        """
        if root.is_leaf():
            return root.get_data()
        if root.get_data() in symptoms:
            return self.diagnose_helper(symptoms, root.get_right())
        return self.diagnose_helper(symptoms, root.get_left())

    def calculate_success_rate(self, records):
        """
        :param records: gets a list of Records (Record)
        :return: a float of the success rate in analyzing the illnesses of the
        records
        """
        success_num = 0
        for record in records:
            if self.diagnose(record.get_symptoms()) == record.get_illness():
                success_num += 1
        return success_num / len(records)

    def all_illnesses(self):
        """
        :return: a list of all ilnnesses of the tree sorted
        """
        illnesses_repeatable = self.all_illnesses_helper(self.root)
        illnesses = self.create_dict_no_repeat(illnesses_repeatable)
        lst = self.convert_dict_to_lst(illnesses)
        self.sort_list_by_appearances(lst)
        return self.delete_count_lst(lst)

    @staticmethod
    def delete_count_lst(lst):
        """
        :param lst: gets a list of tuples (string, num)
        :return: returns a copy of the list but instead of the tuple, returns
            only the string from the tuple
        """
        ill_lst = []
        for ill in lst:
            illness, count = ill
            ill_lst.append(illness)
        return ill_lst

    @staticmethod
    def sort_list_by_appearances(lst):
        """
        :param lst: gets a list of tuples (string, num)
        :return: the list sorted by the numbers
        """
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                ill1, num1 = lst[i]
                ill2, num2 = lst[j]
                if num1 < num2:
                    lst[i] = ill2, num2
                    lst[j] = ill1, num1

    @staticmethod
    def convert_dict_to_lst(dictionary):
        """
        :param dictionary: gets a dictionary
        :return: returns a list of tuples when the tuple is (key, value)
            from the dictionary
        """
        lst = []
        for key in dictionary:
            lst.append((key, dictionary[key]))
        return lst

    @staticmethod
    def create_dict_no_repeat(lst_repeatable):
        """
        :param lst_repeatable: gets a list of of strings
        :return: returns a dictionary without repeats when the key is the
                values of the list and dict[key] is the amount of times the
                key appeared in the lst_repeatable
        """
        illnesses = {}
        for illness in lst_repeatable:
            if illness in illnesses:
                illnesses[illness] += 1
            else:
                illnesses[illness] = 1
        return illnesses

    def all_illnesses_helper(self, root):
        """
        :param root: gets a part of the tree (Node)
        :return: a list of all illnesses
        """
        if root.is_leaf():
            return [root.get_data()]
        lst = []
        if root.has_left():
            lst += self.all_illnesses_helper(root.get_left())
        if root.has_right():
            lst += self.all_illnesses_helper(root.get_right())
        return lst

    def most_rare_illness(self, records):
        """
        :param records: gets a list of Records
        :return: returns the rarest illness (string) in the diagnozer
        """
        illnesses = self.create_dict_no_repeat([record.get_illness() for
                                                record in records])
        for illness in set(self.all_illnesses_helper(self.root)):
            if illness not in illnesses:
                return illness
        rare_illness = records[0].get_illness()
        for key in illnesses:
            if illnesses[rare_illness] > illnesses[key]:
                rare_illness = key
        return rare_illness

    def paths_to_illness(self, illness):
        """
        :param illness: gets an illness (string)
        :return: returns a list of lists of booleans that represent the paths
            to arrive to the illness in the tree
        """
        return self.paths_to_illness_helper(illness, self.root, [])

    def paths_to_illness_helper(self, illness, root, lst):
        """
        :param illness: gets an illness (string)
        :param root: gets a part of the tree (Node)
        :param lst: gets a list (the current path)
        :return: a list of all illnesses
        """
        if root.is_leaf() and root.get_data() == illness:
            return [lst]
        new_lst = []
        if root.has_left():
            new_lst += self.paths_to_illness_helper(
                illness, root.get_left(), lst + [False])
        if root.has_right():
            new_lst += self.paths_to_illness_helper(
                illness, root.get_right(), lst + [True])
        return new_lst


def build_tree(records, symptoms):
    """
    :param records: gets a list of Records
    :param symptoms: gets a list of string that represents the symptoms
    :return: returns a tree corresponding to the symptoms and the records
    """
    tree = Node("")
    build_tree_helper(records, symptoms, tree, [], [])
    return tree


def build_tree_helper(records, symptoms, root, chosen_symptoms,
                      unchosen_symptoms):
    """
    :param records: gets a list of Records
    :param symptoms: gets a list of string that represents the symptoms
    :param root: gets a part of the tree (Node)
    :param chosen_symptoms: gets a list of the yes answers up to now
    :param unchosen_symptoms: gets a list of the no answers up to now
    :return: returns a tree corresponding to the symptoms and the records
    """
    if len(symptoms) == 0:
        root.set_data(analyze_best_illness(records, chosen_symptoms,
                                           unchosen_symptoms))
        return
    else:
        root.set_data(symptoms[0])
    root.set_left(Node(""))
    root.set_right(Node(""))
    build_tree_helper(records, symptoms[1:], root.get_right(),
                      chosen_symptoms + [symptoms[0]], unchosen_symptoms)
    build_tree_helper(records, symptoms[1:], root.get_left(),
                      chosen_symptoms, unchosen_symptoms + [symptoms[0]])


def analyze_best_illness(records, chosen_symptoms, unchosen_symptoms):
    """
    :param records: gets a list of Records
    :param chosen_symptoms: gets a list of the yes answers up to now
    :param unchosen_symptoms: gets a list of the no answers up to now
    :return: returns the most fitting illness to the chosen_symptom and
        unchosen_symptoms from the records
    """
    illnesses = []
    for record in records:
        num = symptoms_fit_record(record, chosen_symptoms, unchosen_symptoms)
        illnesses.append((record.get_illness(), num))
    return get_best_illness(illnesses[0], illnesses)


def get_best_illness(best_illness, illnesses):
    """
    :param best_illness: gets the first tuple of illness and how good it is
    :param illnesses: gets a list of tuple of illnesses and how good are they
    :return: the best illness from the lst
    """
    best_illness = find_best_illness(best_illness, illnesses)
    best_ill, best_num = best_illness
    dct = create_fitting_dict(best_num, illnesses)
    # find the best illness in the dictionary
    for key in dct:
        best_ill, best_num = best_illness
        if dct[key] > dct[best_ill]:
            best_illness = (key, dct[key])
    best_ill, best_num = best_illness
    return best_ill


def create_fitting_dict(best_num, illnesses):
    """
    :param best_num: gets the best number that wr need to censor by
    :param illnesses: gets the list to censor
    :return: a dictionary of the censored data
    """
    dct = {}
    for illness in illnesses:
        ill, num = illness
        if num == best_num:
            if ill in dct:
                dct[ill] += 1
            else:
                dct[ill] = 1
    return dct


def find_best_illness(best_illness, illnesses):
    """
    :param best_illness: gets the first tuple of illness and how good it is
    :param illnesses: gets a list of tuple of illnesses and how good are they
    :return: the best tuple in the list
    """
    for illness in illnesses:
        best_ill, best_num = best_illness
        ill, num = illness
        if num > best_num:
            best_illness = ill, num
    return best_illness


def symptoms_fit_record(record, chosen_symptoms, unchosen_symptoms):
    """
    :param record: gets a Record
    :param chosen_symptoms: gets a list of the yes answers up to now
    :param unchosen_symptoms: gets a list of the no answers up to now
    :return: returns an int, if an unchosen_symptom is in the record it
        returns -1, else it returns the number of chosen_symptoms in the
        records list + 1
     """
    counter = 0
    for symptom in record.get_symptoms():
        if symptom in chosen_symptoms:
            counter += 1
        if symptom in unchosen_symptoms:
            return -1
    return counter


def optimal_tree(records, symptoms, depth):
    """
    :param records: gets a list of Records
    :param symptoms: gets a list of string that represents the symptoms
    :param depth: gets an int of depth of the tree
    :return: returns the best tree with depth (depth) from the records and
        symptoms
    """
    best_tree = None
    best_success = 0
    for combination in itertools.combinations(symptoms, depth):
        tree = build_tree(records, list(combination))
        diagnoser = Diagnoser(tree)
        success = diagnoser.calculate_success_rate(records)
        if best_success < success:
            best_tree = tree
            best_success = success
    return best_tree


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root1 = Node("cough", inner_vertex, healthy_leaf)

    diagnoser1 = Diagnoser(root1)

    # Simple test
    diagnosis = diagnoser1.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root1 = Node("cough", inner_vertex, healthy_leaf)
    # Add more tests for sections 2-7 here.
