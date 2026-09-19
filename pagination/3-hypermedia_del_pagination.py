#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
import csv
import math
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """Return a deletion-resilient page starting at index.

        Args:
            index: the starting index to query from. Defaults to 0.
            page_size: the number of rows to return.

        Returns:
            A dictionary with index, data, page_size, and next_index,
            where next_index is the index to use for the following
            request so that no rows are skipped even if rows before
            it were deleted from the dataset in the meantime.
        """
        data = self.indexed_dataset()
        assert index is None or (
            isinstance(index, int) and 0 <= index <= max(data.keys())
        )

        index = index if index is not None else 0
        page_data = []
        next_index = index

        for key in sorted(data.keys()):
            if key < index:
                continue
            if len(page_data) >= page_size:
                break
            page_data.append(data[key])
            next_index = key + 1

        return {
            'index': index,
            'data': page_data,
            'page_size': len(page_data),
            'next_index': next_index,
        }
