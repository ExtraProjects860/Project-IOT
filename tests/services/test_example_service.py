from app.services.example_service import do_something

def test_do_something():
    result = do_something()
    assert result.unwrap() == "Operacao concluida"