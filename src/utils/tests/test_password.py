import pytest

from src.utils.password import BCryptPasswordService


@pytest.mark.anyio
class TestBCryptPasswordService:
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.service = BCryptPasswordService()

    async def test_hash_returns_hashed_password(self):
        plain_password = "StrongPass1!"
        hashed_password = self.service.hash(plain_password)

        assert isinstance(hashed_password, str)
        assert hashed_password != plain_password

    async def test_verify_returns_true_for_correct_password(self):
        plain_password = "StrongPass1!"
        hashed_password = self.service.hash(plain_password)

        assert self.service.verify(plain_password, hashed_password) is True

    async def test_verify_returns_false_for_incorrect_password(self):
        plain_password = "StrongPass1!"
        hashed_password = self.service.hash(plain_password)

        assert self.service.verify("WrongPassword", hashed_password) is False

    async def test_hash_raises_error_if_not_string(self):
        with pytest.raises(TypeError):
            self.service.hash(12345)  # Passing a non-string value

    async def test_verify_raises_error_if_hashed_password_not_string(self):
        with pytest.raises(TypeError):
            self.service.verify(
                "StrongPass1!", 12345
            )  # Passing a non-string hashed password
