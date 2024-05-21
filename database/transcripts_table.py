import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from database import Session
from database.models import Transcript
from utilities.responses import success, error_404, error_500


def create_record(audio_file_name, recording_name):
    # Create a new session
    session = Session()
    record = None
    try:
        # Check if a record with the same audio file name exists
        record = get_by_name(audio_file_name)

        if not record:
            # If no record exists, create a new one
            timestamp = datetime.now()
            record = Transcript(
                id=str(uuid4()),
                recording_name=recording_name,
                audio_file_name=audio_file_name,
                tracks="",
                transcript="",
                summary="",
                timestamp=timestamp
            )
            # Add the new record to the session
            session.add(record)
            # Commit the transaction
            session.commit()
            print(f"New record created for {audio_file_name} with ID: {record.id}")
        else:
            print(f"Record for {audio_file_name} already exists.")

    except IntegrityError as e:
        # Handle IntegrityError (e.g., duplicate audio_file_name)
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()

    return record


def update_audio_file_name(audio_id, audio_file_name):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_id
        record = session.query(Transcript).filter_by(id=audio_id).first()

        if record:
            # Update the audio_file_name attribute
            record.audio_file_name = audio_file_name
            # Commit the transaction
            session.commit()
            print(f"Audio file name updated for ID {audio_id}")
        else:
            print(f"No record found for ID {audio_id}")

    except IntegrityError as e:
        # Handle IntegrityError
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def update_tracks(audio_id, tracks):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_id
        record = session.query(Transcript).filter_by(id=audio_id).first()

        if record:
            # Update the tracks attribute
            record.tracks = json.dumps(tracks)
            # Commit the transaction
            session.commit()
            print(f"Tracks updated for ID {audio_id}")
        else:
            print(f"No record found for ID {audio_id}")

    except Exception as e:
        # Handle exceptions
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def update_transcript(audio_id, transcript):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_id
        record = session.query(Transcript).filter_by(id=audio_id).first()

        if record:
            # Update the transcript attribute
            record.transcript = transcript
            # Commit the transaction
            session.commit()
            print(f"Transcript updated for ID {audio_id}")
        else:
            print(f"No record found for ID {audio_id}")

    except Exception as e:
        # Handle exceptions
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def update_summary(audio_id, summary):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_id
        record = session.query(Transcript).filter_by(id=audio_id).first()

        if record:
            # Update the transcript attribute
            record.summary = summary
            # Commit the transaction
            session.commit()
            print(f"Transcript updated for ID {audio_id}")
        else:
            print(f"No record found for ID {audio_id}")

    except Exception as e:
        # Handle exceptions
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def update_recording_name(audio_id, recording_name):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_id
        record = session.query(Transcript).filter_by(id=audio_id).first()

        if record:
            # Update the recording_name attribute
            record.recording_name = recording_name
            # Commit the transaction
            session.commit()
            return success(f"Transcript updated for ID {audio_id}")
        else:
            return error_404(f"No record found for ID {audio_id}")

    except Exception as e:
        # Handle exceptions
        session.rollback()
        return error_500(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def get_by_id(_id):
    # Create a new session
    session = Session()

    try:
        # Query the record by doc_id
        record = session.query(Transcript).filter_by(id=_id).first()
        if not record:
            return error_404(f"The record you are looking for doesn't exist")

        # Convert the SQLAlchemy object to a dictionary
        record_dict = record.__dict__

        # Remove the '_sa_instance_state' key from the dictionary
        record_dict.pop('_sa_instance_state', None)
        return record_dict

    except Exception as e:
        # Handle exceptions
        return error_500(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def get_by_name(audio_file_name):
    session = Session()
    try:
        # Query the record by audio_file_name
        record = session.query(Transcript).filter_by(audio_file_name=audio_file_name).first()
        # Convert the SQLAlchemy object to a dictionary
        record_dict = record.__dict__

        # Remove the '_sa_instance_state' key from the dictionary
        record_dict.pop('_sa_instance_state', None)

        return record_dict

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def get_all():
    # Create a new session
    session = Session()

    try:
        # Query all records from the Transcript table
        records = session.query(Transcript).all()
        # Convert SQLAlchemy objects to dictionaries
        record_dicts = [record.__dict__ for record in records]

        # Remove the '_sa_instance_state' key from each dictionary
        for record_dict in record_dicts:
            record_dict.pop('_sa_instance_state', None)

        return record_dicts

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def remove(audio_file_name):
    # Create a new session
    session = Session()

    try:
        # Query the record by audio_file_name
        record = session.query(Transcript).filter_by(audio_file_name=audio_file_name).first()

        if record:
            # Delete the record
            session.delete(record)
            # Commit the transaction
            session.commit()
            return success(f"Record removed for audio file name {audio_file_name}")
        else:
            return error_404(f"No record found for audio file name {audio_file_name}")

    except Exception as e:
        # Handle exceptions
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()


def is_summarizing_completed_for_recording(recording_name):
    # Create a new session
    session = Session()

    try:
        # Query the record by recording_name
        record = session.query(Transcript).filter_by(recording_name=recording_name).first()

        if record and record.tracks and record.transcript and record.summary:
            return True
        else:
            return False

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        return False
    finally:
        # Close the session
        session.close()
