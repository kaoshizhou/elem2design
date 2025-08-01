import random

import datasets as ds

from .base import BaseHFDSHelper
from .crello import CrelloHFDSHelper
from .mock import MockHFDSHelper
from .util import Example

_DATASET_HFDS_MAPPING = {
    "crello": "cyberagent/crello",
}


def hfds_factory(hfds_name: str) -> ds.dataset_dict.DatasetDict:
    return ds.load_dataset(_DATASET_HFDS_MAPPING[hfds_name], revision="4.0.0")


_CLUSTERING_ATTRIBUTE_SETS = {
    "crello": set(
        [
            "left",
            "top",
            "width",
            "height",
            "color",
            "font_size",
            "angle",
            "letter_spacing",
            "line_height",
        ]
    ),
    "mock": set(
        [
            "left",
            "top",
            "width",
            "height",
        ]
    ),
}


def clustering_attribute_set_factory(hfds_name: str) -> set[str]:
    return set(_CLUSTERING_ATTRIBUTE_SETS[hfds_name])


_HFDS_HELPER_FACTORY = {
    "crello": CrelloHFDSHelper,
    "mock": MockHFDSHelper,
}


def hfds_helper_factory(
    hfds_name: str, features: ds.Features | None = None
) -> BaseHFDSHelper:
    if features is None:
        features = ds.load_dataset(_DATASET_HFDS_MAPPING[hfds_name], split="test", revision="4.0.0")[
            "features"
        ]
    return _HFDS_HELPER_FACTORY[hfds_name](features=features)


def sample_example(hfds_name: str) -> tuple[Example, ds.Features]:
    assert hfds_name in _DATASET_HFDS_MAPPING, hfds_name
    dataset = ds.load_dataset(_DATASET_HFDS_MAPPING[hfds_name], split="test[:1%]", revision="4.0.0")
    example = dataset[random.randint(0, len(dataset) - 1)]
    return example, dataset.features