import pandas as pd
import numpy as np

def issn_to_string(df, col):
    """
    Converts a column of pandas DataFrame that contains issn number
    to string of length 8. If issn is shorter than 8 characters 
    it adds 0s to the left.
    """
    if col is None:
        return df
    rows = []
    for index, row in df.iterrows():
        issn = str(row[col])
        if len(issn) < 8:
            issn = "0"*(8-len(issn)) + issn
        rows.append(issn)
    df[col] = rows
    return df

class ScopusFields:
    
    def __init__(self, fn_documents, fn_sources, fn_classification, 
                 fn_dropper=None, doc_issn="ISSN", source_issn="Print ISSN"):
        """
        fn_documents: File that contains bibliographic properities of documents from scopus (for Scopus registred users only)
        fn_sources: File that contains source titles and metircs (for Scopus registred users only)
        fn_classification: File that contains links between Scopus Code, Field, Subject area and Subject Area Classifications
        
        fn_dropper: File thath contains variales which are removed from merged dataset. If None, all the variables are kept.
        
        doc_issn: string that corresponds to ISSN number from documents dataset (from file fn_document)
        source_issn: string that corresponds to ISSN number from sources dataset (from file fn_sources)
        """
        self.df_documents = pd.read_excel(fn_documents)
        self.df_sources = pd.read_excel(fn_sources)
        self.df_sources = self.df_sources.dropna(subset=[source_issn])
        self.df_sources = self.df_sources.rename(columns={"Title":"Title (source)"})
        self.df_c = pd.read_excel(fn_classification)
        
        self.subject_areas = ["Multidisciplinary", "Health Sciences", "Life Sciences",
                            "Physical Sciences", "Social Sciences & Humanities"]
        
        if fn_dropper is not None:
            self.df_dropper = pd.read_excel(fn_dropper)
        
        self.sources = None
        self.doc_issn, self.source_issn = doc_issn, source_issn
        self.doc_match, self.source_match = self.doc_issn, self.source_issn

            
    def get_dct_fields(self):
        """
        Computes several dictionaries that map Scopus Code 
        to Filed, Subject area and Subject Area Classifications
        """
        self.dct_fields = self.df_c.set_index("Code").to_dict()["Field"]  
        self.dct_subject_area = self.df_c.set_index("Code").to_dict()["Subject area"]
        self.dct_subject_area_cl = self.df_c.set_index("Code").to_dict()["Subject Area Classifications"]
        self.subject_areas_cl  = self.df_c["Subject Area Classifications"].unique()
        
    def unify_issn(self):
        self.df_documents = issn_to_string(self.df_documents, self.doc_issn)
        self.df_sources = issn_to_string(self.df_sources, self.source_issn)
        
    def get_list_of_sources(self):
        self.sources_from_documents = self.df_documents[self.doc_match].unique()
        self.all_sources = self.df_sources[self.source_match]
        self.sources = set(self.sources_from_documents) & set(self.all_sources)
        
    def recude_to_snip(self):
        """
        Excludes sources without SNIP from merged dataset
        """
        if self.sources is None:
           self.get_list_of_sources()
        self.df_documents = self.df_documents[self.df_documents[self.doc_match].isin(self.sources)]
        self.df_sources = self.df_sources[self.df_sources[self.source_match].isin(self.sources)]
        self.n_documents = len(self.df_documents)
        
    def get_fields(self):
        self.fields = self.df_sources["Scopus Sub-Subject Area"].dropna().unique()
        self.fields_names = ["Field = "+s for s in self.fields]
        self.subject_areas_cl_names = ["SAC = " +s for s in self.subject_areas_cl]
        
    def aggregate_sources(self):
        self.df_sources_u = self.df_sources.astype(str).groupby(self.source_issn).agg(lambda x: '; '.join(x.unique()))
        
    def add_source_info(self, convert_to_float=True):
        issns = []
        for index, row in self.df_documents.iterrows():
            issns.append(row[self.doc_issn]) 
            
        self.df_documents_source_info = self.df_sources_u.loc[issns]
        
        if convert_to_float:
            for col in ["CiteScore", "Citation Count", "Scholarly Output", "Percent Cited", "SNIP", "SJR"]:
                self.df_documents_source_info[col] = pd.to_numeric(self.df_documents_source_info[col], errors='coerce')
        
    def get_field_info(self):
        """
        Computes several pandas binary DataFrames that contain information
        if a document belongs to Filed or Subject Area Classification
        New variables start with Field = or SAC = 
        """
        a = np.zeros(shape=(self.n_documents, len(self.fields)+len(self.subject_areas_cl_names)+5))
        self.df_fields = pd.DataFrame(a, columns=list(self.fields_names)+self.subject_areas_cl_names+
                           self.subject_areas)
        self.n_documents = len(self.df_documents)
        self.df_documents_source_info = self.df_documents_source_info.reset_index()
        
        sf = [x.split("; ") for x in self.df_documents_source_info["Scopus Sub-Subject Area"]]
        sfc = [x.split("; ") for x in self.df_documents_source_info["Scopus ASJC Code (Sub-subject Area)"]]
        
        for i in range(self.n_documents):
            for f in sf[i]: # for fields
                self.df_fields.loc[i, "Field = %s" %f] = 1
            for sa in sfc[i]: # for 5 Subject Area Classifications
                self.df_fields.loc[i, self.dct_subject_area[int(float(sa))]] = 1
                tmp_vr = "SAC = " + self.dct_subject_area_cl[int(float(sa))]
                self.df_fields.loc[i, tmp_vr] = 1
                        
    def reset_all_indices(self):
        self.df_documents = self.df_documents.reset_index(drop=True)
        self.df_documents_source_info = self.df_documents_source_info.reset_index(drop=True)
        self.df_fields = self.df_fields.reset_index(drop=True)
        
    def drop_variables(self, df=None, regex=["Funding"]):
        if df is None:
            df = self.df_merged
        self.df_dropper = self.df_dropper[self.df_dropper["drop"]==1]
        self.dropped = self.df_dropper["variable"].to_list()
        self.dropped = [x for x in self.dropped if x in df.columns]
        df = df.drop(columns=self.dropped)
        
        for reg in regex:
            df = df[df.columns.drop(list(df.filter(regex=reg)))]
        return df
             
    def prepare_all(self, drop=True, save=None):
        """
        Convenient function that performs all default steps in merging
        doument and sources info
        """
        self.get_dct_fields() # computes dct_fields (code: subject area)
        self.unify_issn()
        self.get_list_of_sources()
        self.recude_to_snip() # changes df_documents, df_sources; counputes n_documents
        self.get_fields() # computes fields
        self.aggregate_sources()
        self.add_source_info()
        self.get_field_info() # computes binary dataframe with indicators for fields and sub-subject areas
        self.reset_all_indices()
        self.df_merged = pd.concat([self.df_documents, self.df_documents_source_info, self.df_fields], axis=1)       
       
        if drop:
            self.df_merged = self.drop_variables()
        
        if save is not None:
            self.df_merged.to_excel(save+".xlsx")
            self.df_merged.to_csv(save+".csv")
            

if __name__ == "__main__":
    
    """ 
    NOTE! Most of the files used for running of the code are available for
    Scopus registred users only and are due to copyright issues 
    not available on Github.
    
    However, for registred Scopus users the detailed information
    how to get the data is provided.
    
    """
    
    fn_documents = "documents.xlsx" # for registred Scopus users only
    # File that contains bibliographic properities of documents from scopus
    # Available for Scopus regristred users only
    
    fn_sources = "scopus sources 2019.xlsx" # for registred Scopus users only
    # visit: https://www.scopus.com/sources?utm_medium=SORG&utm_source=TW&dgcid=STMJ_1592825286_PMES_IM
    # click on Download Scopus Source List
    # Then choose Download source titles and metircs
    # Extract zip file
    # copy data from sheet CiteScore 2019 to new Excel file
    
    fn_classification = "scopus subject area.xlsx"
    # available on Github
    # based on https://service.elsevier.com/app/answers/detail/a_id/14882/supporthub/scopus/~/what-are-the-most-frequent-subject-area-categories-and-classifications-used-in/
    # and https://service.elsevier.com/app/answers/detail/a_id/15181/supporthub/scopus/
    
    fn_dropper = "drop properties.xlsx"
    # available on Github
    # contains information that can be skipped from merged dataset
    
    ss = ScopusFields(fn_documents, fn_sources, fn_classification, fn_dropper=fn_dropper)
    
    ss.prepare_all(save="documents with fields")
