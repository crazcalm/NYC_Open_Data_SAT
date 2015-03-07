import csv
from collections import namedtuple
from constants import SAT_CSV


def format_str_for_namedtuple(stack):
    result = []
    for item in stack:
        tempt = item.replace(" ", "_")
        result.append(tempt)
    return result


def get_file_info(file):
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
                    print(tempt)
                else:
                    tempt = line
                data_list.append(tempt)

        return data_list, header, dialect


"""
Cases:
1: namedTuple, header
2. nameTuple, no header
3. no nameTuple, header
4. no namedTuple, no header
"""
def practice(file, named_tuple=None, has_header=False):
    with open(file, "r") as file:
        if not named_tuple and has_header:
            Data = named_tuple("Data", file.readline())
            print("Data:", Data)


def practice2(file):
    return csv.get_dialect(file)


if __name__ == "__main__":
    stack, has_header, dialect = get_file_info(SAT_CSV)
    print("has_header: ", has_header)
    print("deliminator: ", dialect.delimiter)

    print(has_header)