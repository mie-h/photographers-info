from typing import List
from pydantic import BaseModel
 

class EventType(BaseModel):
    type: List


class Coordinates(BaseModel):
    lat: float
    lng: float


class Address(BaseModel):
    city: str
    street_name: str
    street_address: str
    zip_code: str
    state: str
    country: str
    coordinates: Coordinates


class CreditCard(BaseModel):
    cc_number: str


class Subscription(BaseModel):
    plan: str
    status: str
    payment_method: str
    term: str


class Photographer(BaseModel):
    id: int
    uid: str
    password: str
    first_name: str
    last_name: str
    username: str
    email: str
    avatar: str
    gender: str
    phone_number: str
    social_insurance_number: str
    date_of_birth: str
    event_type: EventType
    address: Address
    credit_card: CreditCard
    subscription: Subscription
