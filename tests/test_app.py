# test_basic.py

# Função simples que vamos testar
def somar(a, b):
    return a + b

# Teste simples para a função somar
def test_somar():
    assert somar(2, 3) == 5  # Espera-se que 2 + 3 seja igual a 5
