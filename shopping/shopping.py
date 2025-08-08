import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # this is the list of all of the keys that are to be turned into an integer
    integer_list = ["Administrative", "Informational", "ProductRelated",
                    "OperatingSystems", "Browser", "Region", "TrafficType"]
    # this is the list of all of the keys that are to be turned into a float
    floating_list = ["Administrative_Duration", "Informational_Duration",
                     "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
    # dictionary that stores the values of months as keys against the numbers required
    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "Jun": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    # list for headers in order
    column_order = [
        "Administrative", "Administrative_Duration", "Informational", "Informational_Duration",
        "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates",
        "PageValues", "SpecialDay", "Month", "OperatingSystems", "Browser",
        "Region", "TrafficType", "VisitorType", "Weekend"
    ]

    evidence = []  # this will be the list that will store the evidence
    labels = []  # list that will store the labels

    with open(filename) as file:
        reader = csv.DictReader(file)
        reader_dict = list(reader)  # turning DictReader() into a list()

        for row in reader_dict:  # loop iterates iver the list
            inner_evidence = []
            for header in column_order:  # innerloop iterates over column_order
                data_1 = 0  # this will store the data that is to be appended against each key

                '''
                    the logic underneath checks what group each key belongs and turns the value from the csv into that type(int(), float(), 0/1)
                '''
                if header in integer_list:
                    data_1 = int(row[header])
                elif header in floating_list:
                    data_1 = float(row[header])
                elif row[header] in months:
                    data_1 = int(months[row[header]])
                elif header == "VisitorType":
                    if row[header] == "Returning_Visitor":
                        data_1 = 1
                    else:
                        data_1 = 0
                elif header == "Weekend":
                    if row[header] == "TRUE":
                        data_1 = 1
                    else:
                        data_1 = 0

                inner_evidence.append(data_1)  # this is appended to the inner list

            evidence.append(
                inner_evidence  # after one complete cycle the inner list is appended into the outer list
            )
            labels.append(1 if row["Revenue"] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    training_model = KNeighborsClassifier(n_neighbors=1)
    training_model.fit(evidence, labels)

    return training_model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1 and predicted == 1:
            true_positives += 1
        elif actual == 0 and predicted == 0:
            true_negatives += 1
        elif actual == 0 and predicted == 1:
            false_positives += 1
        elif actual == 1 and predicted == 0:
            false_negatives += 1

    # Calculate sensitivity (true positive rate)
    if (true_positives + false_negatives) > 0:
        sensitivity = true_positives / (true_positives + false_negatives)
    else:
        sensitivity = 0

    # Calculate specificity (true negative rate)
    if (true_negatives + false_positives) > 0:
        specificity = true_negatives / (true_negatives + false_positives)
    else:
        specificity = 0

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
