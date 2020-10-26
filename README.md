# bibliometric
Scripts used in analyzing bibliometric data of COVID-19 research.

Script get_queries_from_scopus_eid.py helps you collect data for more than 2.000 documents from Scopus

Instruction for usage
    
    If your Scopus query results in more than 2.000 documents, you can select first 20.000 documents and export citation 
    information only (you get link to download file named scopus.csv by email).
    
    Use downloaded file for the script in order to collect other information (bibliographic information, abstract & keywords, 
    funding details and other information).
    
    The script takes scopus.scv file as input and creates queries in Scopus Advanced syntax format which can be directly
    copied to search engine to obtain chunks of documents with less than 2000 documents.
    
    The search results are saved to queries.csv (copy-paste information from each row).
    
    By default, 2.000 (maximal number of documents that can be extracted)
    documents are selected (by their unique identifier EID).
    
    Partial data csv can be merged to one file using script merge_from_scopus_csv.py
    
    Note: if your search query results in more than 20.000 documents, 
    we advise that you split the results into smaller chunks directly in Scopus.
	
Script merge_from_scopus_csv.py
merges document information from several small csv file to a single one (and also in xlsx format)

Instructions for usage
	
	Rename smaller smaller csv files from Scopus in the following format
	scopus (0).csv, scopus (1).csv ...
	
	Use the main function merge_partial_files to merged them. 
	The parameter n_max corresponds to the number of csv files to be merged.

	
Script add_sciences_to_scopus.py
merges information about the documents with the information about the sources from which these documents originate

Instruction for usage
	
	NOTE! Most of the files used for running the code are available for Scopus registered users only and are due to copyright issues not available on GitHub.
    
    	However, for registered Scopus users the detailed information how to get the data is provided.
	
	In order to run the code three files have to be provided by user:
	
	fn_documents: 
		File that contains bibliographic properties of documents from Scopus (for Scopus registered users only)
		fn_document shoud be in Excel format (in case, you have it in csv format, we suggest to convert in in pandas)
		The file contains bibliographic properties of documents from Scopus. It can be directly downloaded from Scopus.
		In case, that the search query results in more than 2.000 documents, 
		we recommend using the get_queries_from_scopus_eid.py script
	
	fn_sources: 
		File that contains source titles and metrics (for Scopus registered users only)
		To get the file
			Visit: https://www.scopus.com/sources?utm_medium=SORG&utm_source=TW&dgcid=STMJ_1592825286_PMES_IM
			Click on Download Scopus Source List
			Choose Download source titles and metrics
			Extract zip file
			Copy data from sheet CiteScore 2019 to new Excel file
	
	fn_classification:
		File is available on GitHub under name scopus_subject_area.xlsx
		It summarizes freely available information from
			https://service.elsevier.com/app/answers/detail/a_id/14882/supporthub/scopus/~/what-are-the-most-frequent-subject-area-categories-and-classifications-used-in/
			https://service.elsevier.com/app/answers/detail/a_id/15181/supporthub/scopus/
			
Script jaccard_sac.py plots clustermap of Subject are classifications based on Jaccard's distance

Instruction for usage
		
		Run the code with the provided file binary_sac.xlsx
		The file binary_sac.xlsx is computed from Scopus document dataset 
		where each row represents a document and each column a Subject area classification.
		The value 1 indicates that a document is classified to a particular SAC, and 0 otherwise.
		The original information about the documents from Scopus are removed from the xlsx file due to copyright issues.
