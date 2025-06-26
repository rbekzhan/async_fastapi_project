from pydantic import BaseModel, RootModel
from typing import Dict

class CatFactResponse(BaseModel):
    fact: str
    length: int

class ProcessedData(RootModel[Dict[str, str]]):
    pass

class ProcessDataResponse(BaseModel):
    processed_data: Dict[str, str]
    cat_fact: CatFactResponse
