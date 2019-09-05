import csv
import random
import math


# this method reads the data from csv file
def read_file(filename):
    lines = csv.reader(open(filename))
    dataset = list(lines)
    for i in range(1, len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset[1:]


# this method splits whole dataset to test and train datasets
def split_data(dataset, test_ratio):
    train = []
    for i in range(int(len(dataset) * test_ratio)):
        train.append(dataset.pop(random.randint(0, len(dataset)-1)))
    # returns train and test dataset
    return train, dataset


# this method separates items by diabetes 1-0
def separate_by_class(dataset):
    yes = []
    no = []
    for item in dataset:
        if item[-1] == 1:
            yes.append(item)
        else:
            no.append(item)
    return no, yes


def mean(numbers):
    return sum(numbers)/len(numbers)


def standard_deviation(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)


def calculate_mean_stdev_for_every_attribute(dataset):
    means_stdevs = []
    for a in range(len(dataset[0])):
        attribute_tab = []
        for b in range(len(dataset)):
            attribute_tab.append(dataset[b][a])
        means_stdevs.append([mean(attribute_tab), standard_deviation(attribute_tab)])
    return means_stdevs[:-1]


def calculate_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean, 2)/(2*math.pow(stdev, 2))))
    return (1/(math.sqrt(2*math.pi)*stdev))*exponent


def calculate_probability_for_class(item, dataset):
    values = []
    for i in range(len(dataset)):
        values.append(calculate_probability(item[i], dataset[i][0], dataset[i][1]))
    prob = 1
    for x in values:
        prob *= x
    return prob


def controller_for_single_item(item):
    dataset = read_file('diabetes.csv')
    no, yes = separate_by_class(dataset)
    mean_stdev_for_no = calculate_mean_stdev_for_every_attribute(no)
    mean_stdev_for_yes = calculate_mean_stdev_for_every_attribute(yes)
    prob_no = calculate_probability_for_class(item, mean_stdev_for_no)
    prob_yes = calculate_probability_for_class(item, mean_stdev_for_yes)
    if prob_no > prob_yes:
        return 'negative'
    return 'positive'


# print(controller_for_single_item())

person = []
print("Pregnancies : ")
person.append(float(input()))

print("Glucose : ")
person.append(float(input()))

print("Blood Pressure : ")
person.append(float(input()))

print("Skin Thickness: ")
person.append(float(input()))

print("Insulin: ")
person.append(float(input()))

print("BMI : ")
person.append(float(input()))

print("DiabetesPedigreeFunction: ")
person.append(float(input()))

print("Age : ")
person.append(float(input()))

person.append(0)

print('\n\n' + 'RESULT : ' + controller_for_single_item(person))




