
from pydantic import BaseModel, Field, ConfigDict



class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


