# Name: Muhammad Mohsin Zafar
# Roll No. MS-18-ST-504826

import numpy as np
import pandas as pd


def get_data_as_array(filename):

    # Using Pandas Library we read file and construct the dataframe
    df = pd.read_csv(filename)

    # From data frame we can easily use keys() to construct an Numpy Array
    data = np.array(df[df.keys()])

    return data


# Test Code
if __name__ == '__main__':
    print("Contents of File are: \n", get_data_as_array("countries.csv"))

