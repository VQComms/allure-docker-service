import json
import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Label:
    name: str
    value: str

@dataclass
class StatusDetails:
    known: Optional[bool] = False
    muted: Optional[bool] = False
    flaky: Optional[bool] = False
    message: Optional[str] = ""
    trace: Optional[str] = None

@dataclass
class Step:
    status: str
    statusDetails: StatusDetails
    stage: str
    steps: List['Step'] = field(default_factory=list)
    attachments: List[Any] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    start: int = 0
    name: str = ""
    stop: int = 0   


@dataclass
class TestResult:
    uuid: str
    historyId: Optional[str] = None
    fullName: Optional[str] = None
    labels: List[Label] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    name: str = ""
    status: str = ""
    statusDetails: StatusDetails = field(default_factory=StatusDetails)
    stage: str = ""
    steps: List[Step] = field(default_factory=list)
    attachments: List[Any] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    start: int = 0
    stop: int = 0
    testCaseId: Optional[str] = None

def convert_results_files_to_python_object_list(results_dir, logger):
    results_object_list = []

    if logger is not None:
        logger.info("results dir: " + results_dir)

    results_files = [f for f in os.listdir(results_dir) if '-result.json' in f]

    for file_name in results_files:
        logger.info("filename: " + file_name)
        
        with open(results_dir + '/' + file_name, 'r') as result_file:
            data = json.load(result_file)
            logger.info("file contents as json: " + str(data))
            
            results_object_list.append(TestResult(**data))

    return results_object_list

def read_count_from_file(file_path):
    with open(file_path, 'r') as f:
        return int(f.read().strip())
