import os 
import re
import random
import time 
import pandas as pd
from typing import List, Dict
import pyalex
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders

from open_alex_helper import *

PATH_FILE_DATA = "/home/thaiv7/Desktop/python-project/scientific_paper/dataset/data/arxiv_metadata_filtered.parquet"

PATH_FILE_OUTPUT = "/home/thaiv7/Desktop/python-project/scientific_paper/dataset/data/open_alex_paper_info.parquet"

if __name__ == "__main__":

    paper_df = pd.read_parquet(PATH_FILE_DATA)
    print(f"Number of papers: {len(paper_df)}")

    list_paper_info = []

    start_time = time.time()
    for index, row in paper_df.iterrows():
        try:
            if index % 10_000 == 0:
                print(f"Processing paper {index}/{len(paper_df)}")

                # Saving checkpoint
                paper_info_df = pd.DataFrame(list_paper_info)
                paper_info_df.to_parquet(PATH_FILE_OUTPUT, index=False)

            arvix_id = row['id']
            paper_title = row['title']
            first_author = row['submitter']

            output = get_paper_from_query(paper_title, first_author)
            
            if not output:
                print(f"Index {index} - No paper found - Title: {paper_title}, First Author: {first_author}")
                continue
            
            # Example of how to use the helper functions
            open_alex_id = output.get('id', '')
            list_references = get_list_references(output)
            
            number_of_citations = get_number_of_citations(output)
            
            list_paper_keywords = get_keywords(output)
            
            venue_info = get_venue_info(output)
            
            first_author_name = get_first_author(output)

            list_paper_info.append({
                'arxiv_id': arvix_id,
                'open_alex_id': open_alex_id,
                'title': paper_title,
                'first_author': first_author_name,
                'number_of_citations': number_of_citations,
                'keywords': list_paper_keywords,
                'venue_type': venue_info['venue_type'],
                'venue_name': venue_info['venue_name'],
                'references': list_references
            })
        except Exception as e:
            continue
        time.sleep(random.uniform(0.05, 0.2)) 

    end_time = time.time()
    print(f"Time taken to process {len(list_paper_info)} papers: {end_time - start_time:.2f} seconds")

    paper_info_df = pd.DataFrame(list_paper_info)
    paper_info_df.to_parquet(PATH_FILE_OUTPUT, index=False)
    print(f"[DONE] Saved paper info to {PATH_FILE_OUTPUT}")