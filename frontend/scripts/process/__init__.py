API_URL = 'http://localhost:8000'

#Users - api
API_LOGIN = f'{API_URL}/login'
API_REGISTER = f'{API_URL}/registration'
API_ACCOUNT = f'{API_URL}/account'

#Models - api
API_MODELS = f'{API_URL}/models'
API_MODEL_HISTORY = f'{API_URL}/model/history'
API_MODEL_INFO = f'{API_URL}/model/info'
API_CLASSIFY = f'{API_URL}/classify'
API_TRAIN = f'{API_URL}/train'

#Images - api
API_LOAD_IMAGES = f'{API_URL}/images/image/load'
API_APPROVE_IMAGES = f'{API_URL}/images/approve'
API_GET_TEMP_IMAGE = f'{API_URL}/temp/images/'
API_GET_UNVERIFY_IMAGES = f'{API_URL}/images/image/unverify'

#Labels - api
API_GET_LABELS = f'{API_URL}/labels'
API_GET_LABEL = f'{API_URL}/label'

HEADER_ONLY_JSON = {
    "accept": "application/json",
    "Content-Type": "application/json"
}