import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class Test_user_registration:

    @pytest.fixture(scope='class', autouse=True)
    async def setup_class(self, ac: AsyncClient):
        return {
            'ac': ac,
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
            'company_name': 'TestCompany',
            'employee_email': 'employeer@gmail.com',
            'invite_token': None,
            'access_token': None,
            'headers': None
        }

    async def test_check_account(self, setup_class):
        ac = setup_class['ac']
        email = setup_class['email']
        response = await ac.get(f'/auth/check_account/{email}')
        assert response.status_code == 200
        setup_class['invite_token'] = response.json().get('invite_token')
        assert setup_class['invite_token'] is not None

    async def test_sign_up(self, setup_class):
        ac = setup_class['ac']
        params = {
            'account': setup_class['email'],
            'invite_token': setup_class['invite_token']
        }

        response = await ac.post(
            '/auth/sign-up/',
            params=params
        )

        assert response.status_code == 200
        assert response.json() == {
            "message": "Invite token validated"
        }

    async def test_test_sign_up_complete(self, setup_class):
        ac = setup_class['ac']

        params = {
            'email': setup_class['email'],
            'username': 'test',
            'password': setup_class['password'],
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'is_admin': True,
            'company_name': setup_class['company_name']
        }
        response = await ac.post(
            '/auth/sign-up-complete/',
            params=params
        )
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
        assert response.status_code == 200
        assert response.json() == {
            "message": "Registration complete. Admin user created."
        }

    async def test_login(self, setup_class):
        ac = setup_class['ac']
        params = {
            'email': setup_class['email'],
            'password': setup_class['password']
        }
        response = await ac.post('/auth/login', params=params)
        assert response.status_code == 200
        setup_class['access_token'] = response.json().get('access_token')
        assert setup_class['access_token'] is not None

        setup_class['headers'] = {
            'Authorization': f'Bearer {setup_class['access_token']}'
        }

    async def test_create_employee(self, setup_class):
        ac = setup_class['ac']
        params = {
            'email': setup_class['employee_email'],
            'username': 'test_emp',
            'first_name': 'test_emp',
            'last_name': 'test_emp',
            'is_admin': False
        }

        response = await ac.post(
            '/auth/create-employee/',
            params=params,
            headers=setup_class['headers']
        )
        assert response.status_code == 200
        assert response.json() == {
            'messege': "Employee created and invite sent to email"
        }

    async def test_name_update(self, setup_class):
        ac = setup_class['ac']
        params = {
            'first_name': 'test_upd',
            'last_name': 'test_upd'
        }
        response = await ac.put(
            '/auth/name_update/',
            params=params,
            headers=setup_class['headers']
        )
        assert response.status_code == 200
        assert response.json() == {'message': 'Name update successfully'}
