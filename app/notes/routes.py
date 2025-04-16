from flask import Blueprint, jsonify, request
from .schemas import note_schema, notes_schema
from app.models import Note
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError


notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_notes():
    """A function to create and save notes"""
    try:
        data = note_schema.load(request.json)
        current_id = get_jwt_identity()
        new_note = Note(
            title = data['title'],
            content = data['content'],
            user_id = current_id
        )

        db.session.add(new_note)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Note created successfully",
            "note": note_schema.dump(new_note)
        }), 201
    
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": err.messages
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Unexpected error occurred"
        }), 500
       
@notes_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    """A function to retrieve all the notes from the db"""
    try:
        current_id = get_jwt_identity()
        notes = Note.query.filter_by(user_id=current_id).all()
        notes_list = [{"id": note.id, "title": note.title, "content": note.content, "user_id": note.user_id} for note in notes]

        return jsonify({
            "status": "success",
            "notes_list": notes_list
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Unexpected error occurred"
        }), 500
        

@notes_bp.route('/notes/<int:id>', methods=['GET'])
@jwt_required()
def get_note(id):
    """A function to get a single note with id"""
    note = Note.query.get_or_404(id, description="Note not Found")
    current_id = get_jwt_identity()

    if note.user_id != current_id:
        return jsonify({
            "status": "error",
            "message": "Only authorized users are allowed to access notes"
        })
    return jsonify({
            "status": "success",
            note:{
            "id":note.id, 
            "title": note.title, 
            "content": note.content
            }}), 200


@notes_bp.route('/notes/<int:id>', methods=['PUT'])
@jwt_required()
def update_note(id):
    try:
        current_id = int(get_jwt_identity())   #get the logged in user ID
        note = Note.query.get_or_404(id, description="note not found")
        
        #check if the logged in user is the owner of the note
        if note.user_id != current_id:
            return jsonify({
                "status": "error",
                "message": "Only authorized users are allow to access notes"
            }), 403
        #Load and validate data
        data = note_schema.load(request.json)

        #Update note details
        note.title = data.get('title', note.title)  #keep old title if not provided
        note.content = data.get('content', note.content) #keep old content if not provided

        db.session.commit()

        
        return jsonify({
            "status": "success",
            "message": "note updated successfully"
        }), 200
    
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": err.messages
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Unexpected error occurred"
        }), 500


@notes_bp.route('/notes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_note(id):
    """A function to delete a note"""
    try:
        current_id = int(get_jwt_identity())
        note = Note.query.get_or_404(id, description="note not found")

        if note.user_id != current_id:
            return jsonify({
                "status": "error",
                "message": "Only authorized users are allowed to access notes"
            }), 403
        
        db.session.delete(note)
        db.session.commit()

        print("Note ID to delete:", id)
        print("JWT user ID:", current_id)
        print("Found note:", note)
        print("Note owner:", note.user_id)

        return jsonify({
            "status": "success",
            "message": "note deleted successfully"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({
            "status": "error",
            "message": "Unexpected error occurred"
        }), 500