import csv
from collections import namedtuple
from constants import SAT_CSV
from operator import attrgetter


def format_str_for_namedtuple(stack):
    """
    A helper function that takes a list of strings and replaces
    the spaces of the strings with '_' so that is will be easy
    to create a namedtuple.

    :param stack: list of strings
    :return: list of strings
    """
    result = []
    for item in stack:
        tempt = item.replace(" ", "_")
        result.append(tempt)
    return result


def read_csv(file):
    """
    Reads the CSV file and creates a list of named tuples.

    :param file: str - Path the csv file
    :return: list of data, boolean - denotes if it has a header,
    """
    sniffer = csv.Sniffer()

    with open(file, "r") as file:
        # Holds lines of file
        data_list = []

        # First line of file
        sample = file.readline()

        # Does a header exist?
        header = sniffer.has_header(sample=sample)

        # obtains delimiter
        dialect = sniffer.sniff(sample=sample)

        # resets the file to the beginning
        file.seek(0)

        lines = csv.reader(file)
        for index, line in enumerate(lines):

            # Looks at the first line of the file
            if index == 0:
                print(line)

                if header:
                    # Dynamically creates a namedtuple
                    new_line = format_str_for_namedtuple(line)
                    data = namedtuple("Data", ", ".join(new_line))

                else:  # Put the first line in the list
                    data_list.append(line)

            else:
                # If a namedtuple exists, create one. Else put the
                # data in the list as is.
                if data:
                    tempt = data(*line)
                else:
                    tempt = line
                data_list.append(tempt)

        return data_list, header, dialect


def is_number(data):
    """
    Checks to see if I can passed parameter can be converted to
    an int
    :param data: string (typically)
    :return: Boolean
    """
    result = False
    try:
        int(data.Number_of_Test_Takers)
        result = True
    except ValueError:
        pass
    return result


def clean_data(stack, fields):
    """
    Creates a new list of namedtuples where the number values such as
    number of test takers, math mean, etc are integers.

    :param stack: list of namedtuples
    :param fields: list of namedtuple fields
    :return: new list of namedtuples
    """
    results = []
    Data = namedtuple("Data", format_str_for_namedtuple(fields))
    for item in stack:
        tempt = Data(item[0], item[1], int(item[2]), int(item[3]), int(item[4]), int(item[5]))
        results.append(tempt)

    return results


def preview_list(stack, limit):
    """
    This functions allows you to preview an iterable by
    printing out "x" amount of items from it.
    
    :param stack: iterable
    :param limit: int
    :return:None
    """
    for index, item in enumerate(stack):
        print(item)
        if index > limit:
            break


if __name__ == "__main__":
    stack, has_header, dialect = read_csv(SAT_CSV)
    print("has_header: ", has_header)
    print("deliminator: ", dialect.delimiter)
    print("has_header:", has_header)

    filtered_data = filter(is_number, stack)
    new_data = clean_data(filtered_data, stack[0]._fields)

    new_data = sorted(new_data, key=attrgetter("Mathematics_Mean"), reverse=True)

    print("\n\n\n")
    preview_list(new_data, 10)