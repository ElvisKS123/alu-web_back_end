#!/usr/bin/env python3
"""Defines a Server class that paginates a dataset of popular baby names."""
import csv
from typing import List

index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server with an empty cached dataset."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Return the cached dataset, loading it from disk if needed."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the requested page of the dataset.

        Args:
            page: the 1-indexed page number to return.
            page_size: the number of rows per page.

        Returns:
            The list of rows for the requested page, or an empty list
            if the page is out of range for the dataset.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
