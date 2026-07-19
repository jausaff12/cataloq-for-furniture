from pydantic import BaseModel, ConfigDict


class ProductImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    is_primary: bool
    display_order: int
