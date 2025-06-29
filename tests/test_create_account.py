import random
from application.use_cases.create_account import CreateAccount
from infrastructure.persistence.repository_impl import ClientRepositoryImpl

def test_create_account():
    client_repo = ClientRepositoryImpl()
    uc = CreateAccount(client_repo)
    rand = random.randint(1_000_000, 9_999_999)
    email = f"alice{rand}@example.com"
    client_id = uc.execute("Alice", email, "+33123456789")
    assert client_id
