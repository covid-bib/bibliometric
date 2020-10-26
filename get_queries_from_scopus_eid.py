import pandas as pd

def chunks(eids, q_max):
    n = int(len(eids)/q_max)
    return [eids[(i-1)*q_max:i*q_max ]for i in range(1,n+1)] + [eids[n*q_max:]]

def get_query(eid):
    return "".join([" EID("+e+") OR" for e in eid])[1:-3]

def get_queries_from_scopus(fn, q_max=2000, out="queries.csv"):
    df = pd.read_csv(fn, error_bad_lines=False)

    eids = df["EID"].to_list()
    Eid = chunks(eids, q_max)
    Q = [get_query(eid) for eid in Eid]

    df_q = pd.DataFrame(Q, columns=["query"])
    df_q.to_csv(out, index=False)

if __name__ == "__main__":
    
    """ Instructions for usage
    
    If your Scopus query results in more than 2.000 documents (and less than 20.000)
    you can select first 20.000 documents and export citation information only
    (you get link to scopus.csv by email).
    
    To collect other information (bibliographic information, 
    abstract & keywords, funding details and other information)
    use this script. It takes scopus.scv file as input and creates queries
    in Scopus Advanced syntax which can be directly copied to search engine.
    The search results are saved to queries.csv
    
    By default, 2000 (maximal number of documents that can be extracted)
    documents are selected (by their unique identifier EID).
    
    Partial data csv can be merged to one file using 
    script merge_from_scopus_csv.py
   
    """
    
    get_queries_from_scopus("scopus.csv", q_max=2000, out="queries.csv")