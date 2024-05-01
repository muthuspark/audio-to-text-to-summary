from tinydb import TinyDB, Query

_db = TinyDB("database.json")

TranscriptQuery = Query()


def create_record(audio_file_name, recording_name):
    result = _db.search(TranscriptQuery.audio_file_name.matches(audio_file_name))
    if not result:
        record_id = _db.insert({
            'recording_name': recording_name,
            'audio_file_name': audio_file_name,
            'tracks': "",
            'transcript': "",
            'summary': ""
        })
        print(f"New record created for {audio_file_name} with ID: {record_id}")
    record = _db.get(TranscriptQuery.audio_file_name.matches(audio_file_name))
    return record


def update_audio_file_name(audio_id, audio_file_name):
    _db.update({
        'audio_file_name': audio_file_name
    }, doc_ids=[audio_id])


def update_tracks(audio_id, tracks):
    _db.update({
        'tracks': tracks
    }, doc_ids=[audio_id])


def update_transcript(audio_id, transcript):
    _db.update({
        'transcript': transcript
    }, doc_ids=[audio_id])


def update_summary(audio_id, summary):
    _db.update({
        'summary': summary
    }, doc_ids=[audio_id])


def get_by_id(audio_id):
    return _db.get(TranscriptQuery.doc_id.matches(audio_id))


def get_all():
    return _db.all()


def is_summarizing_completed_for_recording(recording_name):
    record = _db.get(TranscriptQuery.recording_name.matches(recording_name))
    if len(record['tracks']) > 0 and len(record['transcript']) and len(record['summary']):
        return True
    return False
