import csv
import random
import math


def read_file(filename):
    lines = csv.reader(open(filename))
    dataset = list(lines)
    for i in range(1, len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    # for i in dataset:
    #     print(i)
    return dataset[1:]


def split_data(dataset, test_ratio):
    train = []
    for i in range(int(len(dataset) * test_ratio)):
        train.append(dataset.pop(random.randint(0, len(dataset)-1)))
    # returns train and test dataset
    return train, dataset


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


# def get_mean_and_stdev_for_every_attribute_by_class(dataset):
#     no, yes = separate_by_class(dataset)
#     return calculate_mean_stdev(no), calculate_mean_stdev(yes)


def calculate_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1/(math.sqrt(2*math.pi)*stdev))*exponent


def calculate_probability_for_class(item, dataset):
    values = []
    for i in range(len(dataset)):
        values.append(calculate_probability(item[i], dataset[i][0], dataset[i][1]))
    prob = 1
    for x in values:
        prob *= x
    return prob

def result(no, yes):
    if no > yes:
        return 0
    return 1


def getAccuracy(answers, test):
    good = 0
    for i in range(len(answers)):
        if int(test[i][8]) == answers[i]:
            good += 1
    return round(good*100/len(test), 1)


def controller():
    # dataset read from csv file
    dataset = read_file('diabetes.csv')
    # train and test dataset given from previous dataset
    train, test = split_data(dataset, 0.33)  # train : test = 1 : 2
    # tables of healthy people and the ones with diabetes
    no, yes = separate_by_class(train)
    # calculated means and standard deviations for every attribute in class dataset
    mean_stdev_for_no = calculate_mean_stdev_for_every_attribute(no)
    mean_stdev_for_yes = calculate_mean_stdev_for_every_attribute(yes)
    answers = []
    for i in test:
        prob_no = calculate_probability_for_class(i, mean_stdev_for_no)
        prob_yes = calculate_probability_for_class(i, mean_stdev_for_yes)
        answers.append(result(prob_no, prob_yes))

    return getAccuracy(answers, test)




accuracy = controller()

print("accuracy of this algorithm is " + str(accuracy) + "%")