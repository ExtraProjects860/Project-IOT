from app.utils.result import Result, Success, Failure

def do_something() -> Result:
    try:
        # x = 1/0
        return Success("Operacao concluida")
    except Exception as e:
        return Failure(e)
