import os


def create_relative_path(path):
    rel_path = os.sep.join(path)
    return os.path.join(os.path.dirname(__file__), rel_path)

_SAT_csv = ("csv_files", "SAT__College_Board__2010_School_Level_Results.csv")
SAT_CSV = create_relative_path(_SAT_csv)


if __name__ == "__main__":
    print(SAT_CSV)