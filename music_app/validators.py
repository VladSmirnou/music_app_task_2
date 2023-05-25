from uuid import UUID


class Validator:

    def __init__(self, request=None):
        self.request = request

    def make_err(self, err_message, code):
        return {
            'status': 'error',
            'message': err_message,
        }, code

    def check_uuid(self, uuid, track_uuid=None):
        try:
            UUID(uuid)
        except:
            if track_uuid:
                return 'Incorrect track identifier'
            return 'Incorrect access token'

    def validate_request_type(self, required_ct):
        request_ct = self.request.content_type
        if not request_ct or required_ct not in request_ct:
            return self.make_err(f'Invalid MIME type. Must be [ {required_ct} ]', 415)

    def validate_register(self):
        if err:= self.validate_request_type("application/json"):
            return err

        user_name = self.request.get_json().get('user_name')

        if not isinstance(user_name, str):
            if user_name is None:
                return self.make_err('Invalid key or value is null.', 400)
            return self.make_err('Invalid value data type. Must be [ str ]', 400)
        
        if not 0 < len(user_name) <= 100:
            return self.make_err(
                'Invalid value length. Must be [ 0 < value <= 100 ]',
                400,
            )

        return {'valid_data': user_name}, None
    
    def validate_add_track(self):
        if err:= self.validate_request_type('multipart/form-data'):
            return err

        errors = []
        
        users_data = {
            'wav_file': self.request.files.get('wav_file'), 
            'user_access_token': self.request.form.get('user_access_token'), 
            'user_id': self.request.form.get('user_id'),
        }

        if any(inp is None for inp in users_data.values()):
            return self.make_err('Invalid key(s) or value(s) is null', 400)

        file_name = users_data['wav_file'].filename
        if not file_name.endswith('.wav'): 
            errors.append(f'Wrong file extention. Must be [ .wav ]')
        else:
            file_name_no_ext = file_name.rsplit('.', 1)[0]
            if not 10 < len(file_name_no_ext) <= 150:
                errors.append(f'Invalid file name length. Must be [ 10 < file_name <= 150 ] without extention part.')

        if err:= self.check_uuid(users_data['user_access_token']):
            errors.append(err)
        
        try:
            user_id = int(users_data['user_id'])
            if user_id <= 0:
                errors.append('[ user_id ] cannot be 0 or a negative number')
        except:
            errors.append('[ user_id ] is not a number')
        
        if errors:
            return self.make_err(errors, 400)
        
        return {'valid_data': users_data}, None

    def validate_get_track(self):
        query_attrs = self.request.args

        errors = []

        users_data = {
            'track_uuid': query_attrs.get('id'), 
            'user_id': query_attrs.get('user'),
        }

        if any(inp is None for inp in users_data.values()):
            return self.make_err('Invalid attribute(s) or value(s) is null', 400)
        
        if err:= self.check_uuid(users_data['track_uuid'], track_uuid=True):
            errors.append(err)

        try:
            user_id = int(users_data['user_id'])
            if user_id <= 0:
                errors.append('[ user ] cannot be 0 or a negative number')
        except:
            errors.append('[ user ] is not a number')
        
        if errors:
            return self.make_err(errors, 400)
        
        return {'valid_data': users_data}, None
