import pandas as pd

from argparse import ArgumentParser
from pathlib import Path

from solver import Solver
from preprocess import DataProcessor

# parameters initialization
LOWER_BOUND = 3
UPPER_BOUND = 3

time_table = {
    "3/11": {
        "day": [
            "19:00-19:30",
            "19:40-20:10",
            "20:20-20:50",
            "21:00-21:30"
        ]
    },
    "3/12": {
        "morning": [
            "9:35-10:05",
            "10:10-10:40",
            "10:45-11:15",
            "11:20-11:50",
            "11:55-12:25",
        ],
        "afternoon": [
            "13:30-14:00",
            "14:05-14:35",
            "14:40-15:10",
            "15:15-15:45",
            "15:50-16:20",
            "16:25-16:55",
        ]
    },
    "3/13": {
        "morning": [
            "9:00-9:30",
            "9:35-10:05",
            "10:10-10:40",
            "10:45-11:15",
            "11:20-11:50",
            "11:55-12:25",
        ],
        "afternoon": [
            "13:30-14:00",
            "14:05-14:35",
            "14:40-15:10",
            "15:15-15:45",
            "15:50-16:20",
            "16:25-16:55"
        ]
    }
}
    

def main(args):
    # read file
    df = pd.read_excel(args.file_path)
    people = df.filter(items=["你ㄉ大名！"])
    # for all selected data
    times = df.filter(like="你可以ㄉ時段")
    whole_times = df.filter(like=":")
    Data = DataProcessor(time_table, people, times, whole_times)
    Data.transform_data()
    solver = Solver(Data.data, Data.time_count, LOWER_BOUND, UPPER_BOUND)
    result = solver.solve()
    Data.res_output(result, args.output_path)
    
def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "--file_path",
        type=Path,
        help="path to the xlsx file.",
        default="./forms.xlsx",
    )

    parser.add_argument(
        "--output_path",
        type=Path,
        help="file to the output file.",
        default="./output/result.txt",
    )
    
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
