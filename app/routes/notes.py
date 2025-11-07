from fastapi import APIRouter, Depends, status,HTTPException, Response
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_user_details
from  typing import List
from .. import models
from .. import schema
router = APIRouter(tags=['Notes'], prefix='/notes')

@router.get('/',)
def get_notes(db:Session = Depends(get_db), user_id:str = Depends(get_user_details)):
    notes = db.query(models.Note).filter(models.Note.owner_id ==user_id).all()
    return {
        'data':notes
    }
    

@router.post('/',status_code= status.HTTP_201_CREATED)
def post_notes(payload:schema.NoteCreate, db:Session = Depends(get_db), user_id:str = Depends(get_user_details)):

    post_data = {**payload.model_dump(), "owner_id":user_id}
    post = models.Note(**post_data)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post


@router.get('/{id}',status_code= status.HTTP_200_OK)
def get_note(id:str, db:Session = Depends(get_db), user_id:str = Depends(get_user_details)):

   print('This is id', id)
    
   note = db.query(models.Note).filter((models.Note.owner_id ==user_id) & (models.Note.id == id )).first()
    
   if not note:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
 
   return {
        'data':note
    }
    
@router.put('/{id}',status_code= status.HTTP_200_OK)
def update_note(id:str,payload:schema.NoteUpdate, db:Session = Depends(get_db), user_id:str = Depends(get_user_details), ):

   print('This is id', id)
    
   note = db.query(models.Note).filter((models.Note.owner_id ==user_id) & (models.Note.id == id ))
    
   if not note.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
   note.update(payload.model_dump(), synchronize_session=False)
   
   db.commit()
    
    
   return {
        'data':note.first()
    }

@router.delete('/{id}',status_code= status.HTTP_200_OK)
def delete_note(id:str, db:Session = Depends(get_db), user_id:str = Depends(get_user_details), ):

   print('This is id', id)
    
   note = db.query(models.Note).filter((models.Note.owner_id ==user_id) & (models.Note.id == id ))
    
   if not note.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
   note.delete( synchronize_session=False)
   
   db.commit()
    
    
   return Response(status_code=status.HTTP_204_NO_CONTENT)