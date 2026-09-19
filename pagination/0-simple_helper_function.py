#!/usr/bin/env python3
"""Defines index_range, a simple pagination helper function."""


def index_range(page, page_size):
    """Return the start and end index for a page of a given size.

    Args:
        page: the 1-indexed page number (page 1 is the first page).
        page_size: the number of items per page.

    Returns:
        A tuple (start_index, end_index) describing the slice of a
        list that corresponds to the requested page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
