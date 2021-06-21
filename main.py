"""
@Author: Jackson Elowitt
@Date: 6/19/21
@Contact: jkelowitt@protonmail.com
@Site: https://github.com/jkelowitt/EnergySearchAndSort

Given a directory containing log files, output a csv file containing sorted
energy data.

"""

import re
from glob import glob

from pandas import DataFrame


def main():
    # From where to where
    dir = input("Enter the directory of the .log files: ")
    output_name = input("What do you want to name the output csv file: ")

    # dir = r"F:\Coding Projects\Python\EnergySearchAndSort\datas"
    # output_name = "123"

    # Get the files to parse
    files = glob(dir + "/*.log")

    if not files:
        input("No log files found in given directory. Press enter to exit.")
        raise SystemExit

    names = []
    energies = []

    # Parse geometry and write the files
    for file in files:
        # Search for the energy value
        with open(file, "r+") as f:
            # Convert the data into a single string with no new lines
            data = "".join(f.readlines()).replace("\n ", "")

        if not data:
            print(f"{file[len(dir) + 1:]} had no data, skipping")
            continue

        # print(data)
        # Find the energy using RegEx
        # Give me a string which starts with "HF="
        # Following that, give me ( () ) one or more (+)
        # digits (\d),
        # newlines (\b),
        # spaces ( ),
        # or (|) dashes (-),
        # but no slashes [^\\].
        # Once you reach a slash, end the string.

        pattern = re.compile(r'HF=(\d|\n| |-|[^\\])+')
        energy = pattern.search(data)
        if energy:
            energies.append(float(energy[0][3:]))
        else:
            energies.append(None)

        name = file[len(dir) + 1:]
        names.append(name)

    # Make a pandas dataframe
    csv_data = DataFrame({"File Name": names, "Hartrees": energies})

    # Add a column for wavenumber conversion
    csv_data["Wavenumbers"] = csv_data["Hartrees"] * 219474.63

    # Add a column finding the difference between the current and minimum energy compoound
    csv_data["Diff"] = csv_data["Wavenumbers"] - min(csv_data["Wavenumbers"])

    # Sort data by the difference in energy
    csv_data.sort_values(by="Diff", na_position="first", inplace=True)

    # Write the data to a csv
    csv_data.to_csv(output_name + ".csv", index=False)


if __name__ == "__main__":
    print("EnergySearchAndSort".center(50, "~"))
    print("Author: Jackson Elowitt")
    print("Repo: https://github.com/jkelowitt/EnergySearchAndSort")
    print("Version: v2")
    print("".center(50, "~"))
    print()

    main()

    input("\nFile saved in the .exe's directory. Press enter to exit.")
