import random
from application.use_cases.create_account import CreateAccount
from application.use_cases.top_up_wallet import TopUpWallet
from infrastructure.persistence.repository_impl import ClientRepositoryImpl

def test_top_up_wallet():
    client_repo = ClientRepositoryImpl()
    create_uc = CreateAccount(client_repo)
    top_up_uc = TopUpWallet(client_repo)

    rand = random.randint(1_000_000, 9_999_999)
    email = f"bob{rand}@example.com"
    client_id = create_uc.execute("Bob", email, "+33123456780")
    top_up_uc.execute(client_id, 100, "EUR")
    client = client_repo.get(client_id)
    assert client.wallet.balance.amount == 100
