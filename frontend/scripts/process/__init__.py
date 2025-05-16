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

HEADER_ONLY_JSON = {
    "accept": "application/json",
    "Content-Type": "application/json"
}