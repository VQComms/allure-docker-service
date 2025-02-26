import json
import os
import re
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Label:
    name: str
    value: str

@dataclass
class StatusDetails:
    known: bool
    muted: bool
    flaky: bool
    message: str

@dataclass
class TestResult:
    uuid: str
    historyId: str
    fullName: str
    labels: List[Label]
    links: List[str]
    name: str
    status: str
    statusDetails: StatusDetails
    stage: str
    steps: List[str]
    attachments: List[str]
    parameters: List[str]
    start: int
    stop: int

def convert_results_files_to_python_object_list(results_dir, logger):
    results_object_list = []

    if logger is not None:
        logger.info("results dir: " + results_dir)

    results_files = [f for f in os.listdir(results_dir) if '-result.json' in f]

    for file_name in results_files:
        logger.info("filename: " + file_name)
        
        with open(results_dir + file_name, 'r') as result_file:
            data = json.load(result_file)
            logger.info("file contents as json: " + data)
            
            results_object_list.append(TestResult(**data))

    return results_object_list

def read_count_from_file(file_path):
    with open(file_path, 'r') as f:
        return int(f.read().strip())
