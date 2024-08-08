from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing_extensions import Annotated

router = APIRouter(tags=['Contacts'], prefix='/contacts', responses={404: {"message": 'no encontrado'}})

class Contact(BaseModel):
    id: int
    name: str
    last_name: str
    age: Annotated[int | None, Body(ge=18)] = None
    phone_number: int | None = None

class Image(BaseModel):
    name: str
    url: str

class Residence(BaseModel):
    name: str
    description: str
    image: Image | None = None

contacts_list = [Contact(id=1, name="Guillermo", last_name="Palermo", age=23, phone_number=77101245),
                 Contact(id=2, name="Samuel", last_name="Etoo", age=24, phone_number=77101115),
                 Contact(id=3, name="Titi", last_name="Henry", age=25, phone_number=77102245),
                 Contact(id=4, name="Kylian", last_name="Mbappe", age=26, phone_number=77104445),]

@router.get("", response_model=list[Contact])
def get_contacts(skip: int = 0, limit:int = 10):
    return contacts_list[skip: skip + limit]

@router.get('/{id}', response_model=Contact)
def get_specific_contact(id: int):
    result = search_contact(id)
    if type(result) == Contact:
        return result
    else:
        raise HTTPException(status_code=404, detail='Contact not found.')

@router.post('', status_code=201, response_model=Contact)
def create_contact(contact: Contact):
    if type(search_contact(contact.id)) == Contact:
        raise HTTPException(status_code=409, detail='User already registered.')
    else:
        contacts_list.append(contact)
        return contact

@router.put('', status_code=200, response_model=Contact)
def update_specific_contact(contact: Contact):
    result_contact = search_contact(contact.id)
    if type(result_contact) == Contact:
        result_contact.id = contact.id
        result_contact.name = contact.name
        result_contact.last_name = contact.last_name
        result_contact.age = contact.age
        result_contact.phone_number = contact.phone_number
        return result_contact
    raise HTTPException(status_code=404, detail="Contact wasn't found")


@router.delete('/id', status_code=200, response_model=Contact)
def delete_contact(id: int):
    result = search_contact(id)
    if type(result) == Contact:
        contacts_list.remove(result)
        return result
    else:
        raise HTTPException(status_code=404, detail="Contact wasn't found.")

def search_contact(id: int):
    result = filter(lambda x: x.id == id, contacts_list)
    try:
        return list(result)[0]
    except:
        return {"msg": "Contact wasn't found."}
    
@router.post("/multiple/body/parameters", tags=['body parameters validations'])
def multiple_body(contact: Contact, residence: Residence, importance: Annotated[int, Body()] ):
    return {"contact": contact, "residence": residence, "importance": importance}