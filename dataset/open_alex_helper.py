"""
In this file, we will implement functions
to extract various attributes from a scientific paper using the OpenAlex API.
"""

import os 
import re
from typing import List, Dict
import pyalex
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders

def remove_special_characters(string: str) -> str:
    """
    Remove special characters from a string.
    """
    return re.sub('[^A-Za-z0-9]+', ' ', string)


def get_paper_from_query(paper_title: str, first_author: str):
    """
    Since query result can contain multiple papers, 
    this function select the most suitable paper.

    Criteria for selection:
    - Priority to papers with title and first author match.
    - Priority paper from the conference or journal, instead of arvix.
    - If no match, return the first paper in the list.

    Returns:
        Dict: The best paper dictionary. 
    """
    paper_title = remove_special_characters(paper_title)
    first_author = remove_special_characters(first_author)

    list_output = Works().search_filter(title=paper_title).get()

    arvix_paper = None 
    venue_paper = None

    for output in list_output:
        queried_title = output.get('title', '').lower()
        if not queried_title:
            continue
        queried_title = remove_special_characters(queried_title)

        queried_first_author = output.get('authorships', [{}])[0].get('author', {}).get('display_name', '').lower()
        if not queried_first_author:
            continue
        queried_first_author = remove_special_characters(queried_first_author)
            
        if queried_title == paper_title.lower() and queried_first_author == first_author.lower():
            if output.get('source', {}).get('display_name', '').lower() != 'arxiv':
                return output
            else:
                arvix_paper = output   

    if arvix_paper:
        return arvix_paper

    # If no exact match, return first paper
    if list_output:
        return list_output[0]
    return {}



def get_first_author(output) -> str:
    authorships = output.get('authorships', [])
    if len(authorships) > 0:
        first_author = authorships[0].get('author', {}).get('display_name')
        return first_author
    return ""


def get_venue_info(output) -> dict:
    primary_location = output.get('primary_location', {})
    if not primary_location:
        return {}

    is_open_access = primary_location.get('is_oa', False)
    source = primary_location.get('source')
    if not source:
        return {
            'is_open_access': is_open_access,
            'venue_type': 'Unknown',
            'venue_name': 'Unknown'
        }

    venue_type = source.get('type', 'Unknown')
    venue_name = source.get('display_name', 'Unknown')  
    return {
        'is_open_access': is_open_access,
        'venue_type': venue_type,
        'venue_name': venue_name
    }


def get_keywords(output) -> List[str]:
    keywords = output.get('keywords', [])
    return [keyword.get('display_name') for keyword in keywords]


def get_number_of_citations(output) -> int:
    return output.get('cited_by_count', 0)


def get_list_references(output) -> List[str]:
    """
    Extracts a list of references from the OpenAlex output.
    """
    return output.get('referenced_works', [])


