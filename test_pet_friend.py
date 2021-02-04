from api import PetFriends
from  settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Тест получения API key для корректных email и пароля'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    '''Тест получения API key для не корректных email и пароля'''
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    '''Тест получения списка всех питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Тест получения списка моих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        '''Если питомцы отсутсвуют, добавляем питомца'''
        my_pets = pf.post_add_new_pet(auth_key, name='test', animal_type='test', age='10')
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert  status ==200
        assert len(result['pets']) > 0
    else:
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

def test_post_add_new_pet_valid(name='Ктулху', animal_type='Великий Древний', age='1000001'):
    '''Тест на добавление питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_post_add_new_pet_with_photo_valid(name='Ктулху', animal_type='Великий Древний', age='1000001', pet_photo='images/CTLH.jpg'):
    '''Тест на добавление питомца с фотографией'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_uppdate_pet_info_valid(name='КТУЛХУ', animal_type='Супер Великий Древний Бог', age = '1010101010'):
    '''Тест на изменение данных питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        '''Если питомцы отсутсвуют, добавляем питомца'''
        my_pets = pf.post_add_new_pet(auth_key, name='test', animal_type='test', age='10')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        status, result = pf.put_uppdate_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        status, result = pf.put_uppdate_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age

def test_delete_pet_valid():
    '''Тест на удаление питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        '''Если питомцы отсутсвуют, добавляем питомца'''
        my_pets = pf.post_add_new_pet(auth_key, name='test', animal_type='test', age='10')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        status = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        status = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200

def test_post_uppdate_pet_photo_valid(pet_photo='images/CatCTLH.jpg'):
    '''Тест обновление фотографии питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        '''Если питомцы отсутсвуют, добавляем питомца'''
        my_pets = pf.post_add_new_pet(auth_key, name='test', animal_type='test', age='10')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        status, result = pf.post_uppdate_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
         status, result = pf.post_uppdate_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
         assert status == 200

def test_post_add_new_pet_incorrect_request(name='Барсик', animal_type='Кот'):
    '''Тест добавление нового питоца некорректным запросом'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_invalid(auth_key, name, animal_type)
    assert status == 400

def test_delete_pet_incorrect_pet_id(pet_id='sredf'):
    '''Тест удаления несуществующего питомца(баг*)'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 200
   '''* мне кажется, что баг в том, что сервер не должен возращать статус ответа 200 при обращении к несуществующему питомцу'''

def test_uppdate_pet_info_incorrect_pet_id(pet_id='nejiv', name='КТУЛХУ', animal_type='Супер Великий Древний Бог', age = '1010101010'):
    '''Тест изменение данных несуществующего питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    html_response = pf.put_uppdate_pet_info(auth_key, pet_id, name, animal_type, age)
    assert  400 in html_response

def test_uppdate_pet_photo_incorrect_pet_id(pet_id='ffdfgh', pet_photo='images/CatCTLH.jpg'):
    '''Тест обновление фотографии несуществующего питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_uppdate_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 500
    '''В документации не прописанно, что сервер должен возращать ошибку 500, но мне кажется, что тест написан правильно'''

def test_uppdate_pet_photo_incorrect_photo_file(pet_photo='images/INC_FILE'):
    '''Тест обновление фотографии питомца с некорректным файлом'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        '''Если питомцы отсутсвуют, добавляем питомца'''
        my_pets = pf.post_add_new_pet(auth_key, name='test', animal_type='test', age='10')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        status, result = pf.post_uppdate_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
    else:
         status, result = pf.post_uppdate_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
         assert status == 500

    '''В документации не прописанно, что сервер должен возращать ошибку 500, но мне кажется, что тест написан правильно'''

def test_post_add_new_pet_invalid(name='', animal_type='', age=''):
    '''Тест на добавление питомца c пустыми данными (баг*)'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age)
    status == 200
    '''Считаю, что сервер не должен создавать питомца при пустых данных'''