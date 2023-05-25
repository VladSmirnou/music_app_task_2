import uuid

from io import BytesIO

from flask import request, Blueprint, send_file
from pydub import AudioSegment

from .extentions import db
from .models import User, Track
from .validators import Validator


main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    
    handle = Validator(request)
    res = handle.validate_register()

    if not (user_name:= res[0].get('valid_data')):
        return res

    new_user_obj = User(
        user_name=user_name,
        user_access_token=str(uuid.uuid4()),
    )
    db.session.add(new_user_obj)
    db.session.commit()

    return {
        'status': 'success',
        'user_id': new_user_obj.user_id,
        'user_access_token': new_user_obj.user_access_token,
    }, 201


@main.route('/add_track', methods=['POST'])
def add_track():

    handle = Validator(request)
    res = handle.validate_add_track()
    
    if not (valid_data:= res[0].get('valid_data')):
        return res
    
    user_obj = User.query.filter_by(
        user_id=valid_data['user_id'],
        user_access_token=valid_data['user_access_token'],
    ).first()
    
    if not user_obj:
        return {
            'status': 'error',
            'message': 'Invalid credentials',
        }, 400
    
    mp3_file_name = valid_data['wav_file'].filename.rsplit('.', 1)[0]

    audio = AudioSegment.from_wav(valid_data['wav_file'])
    mp3_bytes = BytesIO()
    audio.export(mp3_bytes, format='mp3')
    mp3_bytes.seek(0)

    track_obj = Track(
        track_uuid=str(uuid.uuid4()), 
        track_file_bin=mp3_bytes.getvalue(),
        track_file_name=mp3_file_name,
        user_id=user_obj.user_id,
    )
    db.session.add(track_obj)
    db.session.commit()

    return (
        {'status': 'success'}, 
        201, 
        {'Location': f'{request.url_root}record?id={track_obj.track_uuid}&user={user_obj.user_id}'},
    )


@main.route('/record', methods=['GET'])
def get_track():

    handle = Validator(request)
    res = handle.validate_get_track()

    if not (valid_data:= res[0].get('valid_data')):
        return res

    track_obj = Track.query.filter_by(
        user_id=int(valid_data['user_id']),
        track_uuid=valid_data['track_uuid'],
    ).first()

    if not track_obj:
        return {
            'status': 'error',
            'message': 'Invalid credentials',
        }, 400

    file_bytes = BytesIO(track_obj.track_file_bin)

    return send_file(
        file_bytes,
        mimetype='audio/mpeg',
        as_attachment=True,
        download_name=f'{track_obj.track_file_name}.mp3',
    )