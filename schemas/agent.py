from pydantic import AliasChoices, BaseModel, Field
from typing import Annotated, List

class NameSchema(BaseModel):
    name: Annotated[str, Field(...,description="姓名")]
    reference: Annotated[str, Field(..., validation_alias=AliasChoices("reference", "cultural_background"), description="出处")]
    moral: Annotated[str, Field(..., validation_alias=AliasChoices("moral", "meaning"), description="寓意")]

class NameResultSchema(BaseModel):
    names: List[NameSchema]
