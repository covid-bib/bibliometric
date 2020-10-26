import pandas as pd

def merge_partial_files(n_max, f_out_name="merged"):
    """ Merges output results from scopus 
    and saves them to xlsx and csv format.
    
    Filenames should have by named scopus (0).csv, scopus (1).csv ...
    n_max is the highest label of partial scopus files
    """
    
    dfs = []

    for i in range(0, n_max):
        df = pd.read_csv("scopus (%d).csv" %i)
        dfs.append(df)
    
    merged = pd.concat(dfs)
    merged.to_excel(f_out_name + ".xlsx", index=False)
    merged.to_csv(f_out_name + ".csv", index=False)
    
if __name__ == "__main__":

    # Merges files copus (0).csv, scopus (1).csv, ... scopus(10).csv
    # and saves merged file to merged.xlsx and merged.csv    
    merge_partial_files(11)
