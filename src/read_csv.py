import csv
from collections import namedtuple
from constants import SAT_CSV
from operator import itemgetter, attrgetter


def format_str_for_namedtuple(stack):
    result = []
    for item in stack:
        tempt = item.replace(" ", "_")
        result.append(tempt)
    return result


def get_file_info(file):
    """

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


def is_number(num):
    result = False
    try:
        int(num.Number_of_Test_Takers)
        result = True
    except ValueError:
        pass
    return result


def clean_data(stack, fields):
    results = []
    Data = namedtuple("Data", format_str_for_namedtuple(fields))
    for item in stack:
        tempt = Data(item[0], item[1], int(item[2]), int(item[3]), int(item[4]), int(item[5]))
        results.append(tempt)

    return results


def practice(file, named_tuple=None, has_header=False):
    with open(file, "r") as file:
        if not named_tuple and has_header:
            Data = named_tuple("Data", file.readline())
            print("Data:", Data)


def practice2(file):
    return csv.get_dialect(file)


def preview_list(stack, limit):
    for index, item in enumerate(stack):
        print(item)
        if index > limit:
            break


if __name__ == "__main__":
    stack, has_header, dialect = get_file_info(SAT_CSV)
    print("has_header: ", has_header)
    print("deliminator: ", dialect.delimiter)
    print("has_header:", has_header)

    test = stack[0]
    print(dir(test))
    print(test._fields)
    """
    Create a dictionary that maps the ... Think about it more...
    """
    sorted_list1 = sorted(stack, key=attrgetter("Number_of_Test_Takers"), reverse=False)

    sorted_list2 = filter(is_number, stack)
    sorted_list2 = clean_data(sorted_list2, test._fields)
    sorted_list2 = sorted(sorted_list2, key=attrgetter("Number_of_Test_Takers"), reverse=False)

    preview_list(sorted_list1, 10)
    print("\n\n\n")
    preview_list(sorted_list2, 10)