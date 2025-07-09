#terminal: cd "C:\Users\50118731\OneDrive - ArcelorMittal\Documentos\Trabalho_Faculdade"
#streamlit run trabalho.py

 
import streamlit as st

# Conversor de Bases
def converter_base(valor: str, base_origem: str, base_destino: str) -> tuple[str, list[str]]:
    bases = {"Decimal": 10, "Binário": 2, "Hexadecimal": 16}
    log = [f"Iniciando conversão de '{valor}' da base {base_origem} ({bases[base_origem]}) para {base_destino}."]
    
    try:
        numero = int(valor, bases[base_origem])
        
        # Conversão para Decimal com detalhamento
        if base_destino == "Decimal":
            if base_origem == "Binário":
                total = 0
                passos = []
                passos.append("Detalhamento: o número binário foi convertido para decimal utilizando os expoentes de 2 antes da soma final.")
                # Percorre os dígitos de trás para frente
                for pos, digito in enumerate(reversed(valor)):
                    int_digito = int(digito)
                    contribuicao = int_digito * (2 ** pos)
                    passos.append(f"{digito} * (2^{pos}) = {int_digito} * {2**pos} = {contribuicao}")
                    total += contribuicao
                resultado = str(total)
                log.extend(passos)
            elif base_origem == "Hexadecimal":
                total = 0
                passos = []
                passos.append("Detalhamento: o número hexadecimal foi convertido para decimal utilizando os expoentes de 16 antes da soma final.")
                # Percorre os dígitos de trás para frente
                for pos, digito in enumerate(reversed(valor)):
                    if digito.isdigit():
                        int_digito = int(digito)
                    else:
                        int_digito = ord(digito.upper()) - ord('A') + 10
                    contribuicao = int_digito * (16 ** pos)
                    passos.append(f"{digito} (valor {int_digito}) * (16^{pos}) = {int_digito} * {16**pos} = {contribuicao}")
                    total += contribuicao
                resultado = str(total)
                log.extend(passos)
            else:
                resultado = str(numero)
                
        # Conversões de Decimal para outras bases
        else:
            divisor = bases[base_destino]
            if numero == 0:
                resultado = "0"
                log.append("Como o número é 0, o resultado é 0.")
            else:
                n = numero
                restos = []
                passos = []
                while n > 0:
                    quociente = n // divisor
                    resto = n % divisor
                    passos.append(f"{n} / {divisor} = {quociente} com resto {resto}")
                    restos.append(resto)
                    n = quociente
                restos.reverse()
                if base_destino == "Hexadecimal":
                    resultado = "".join(chr(ord('A') + r - 10) if r >= 10 else str(r) for r in restos)
                else:
                    resultado = "".join(str(r) for r in restos)
                log.extend(passos)
                
        log.append(f"Resultado final: {resultado}.")
        return resultado, log
    except ValueError:
        erro = "Erro: valor inválido para a base selecionada."
        log.append("Erro na conversão.")
        return erro, log

# Operações entre números em bases
def operacao_entre_numeros(valor1: str, valor2: str, base: str, operacao: str) -> tuple[str, str, list[str]]:
    logs = []
    
    def soma_binaria_passo_a_passo(a, b):
        logs_local = []
        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)
        resultado = ''
        carry = 0

        logs_local.append(f"Soma bit a bit com vai-um (da direita para a esquerda):")
        for i in range(max_len - 1, -1, -1):
            bit1 = int(a[i])
            bit2 = int(b[i])
            soma = bit1 + bit2 + carry
            resultado_bit = soma % 2
            carry = soma // 2
            resultado = str(resultado_bit) + resultado
            logs_local.append(f"{bit1} + {bit2} + vai-um({carry}) = {soma} -> bit: {resultado_bit}")
        if carry:
            resultado = '1' + resultado
            logs_local.append("Vai-um final = 1, adicionado ao início.")
        return resultado.lstrip('0') or '0', logs_local

    def subtracao_binaria_passo_a_passo(a, b):
        logs_local = []
        if len(b) > len(a) or (len(b) == len(a) and b > a):
            return "", ["Erro: subtração não suportada - número menor por maior."]
        a, b = list(a.zfill(len(b))), list(b.zfill(len(a)))
        resultado = ''
        emprestimo = 0
        logs_local.append("Subtração bit a bit com empréstimos (da direita para a esquerda):")

        for i in range(len(a)-1, -1, -1):
            ai, bi = int(a[i]), int(b[i])
            sub = ai - bi - emprestimo
            if sub < 0:
                sub += 2
                emprestimo = 1
            else:
                emprestimo = 0
            resultado = str(sub) + resultado
            logs_local.append(f"{ai} - {bi} - empréstimo({emprestimo}) = {sub}")

        return resultado.lstrip('0') or '0', logs_local

    def soma_hexadecimal_passo_a_passo(a, b):
        logs_local = []
        hex_map = {str(i): i for i in range(10)}
        hex_map.update({chr(ord('A') + i): 10 + i for i in range(6)})
        inv_hex_map = {v: k for k, v in hex_map.items()}
        a, b = a.upper(), b.upper()
        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)
        resultado = ''
        carry = 0
        logs_local.append("Soma hexadecimal com vai-um:")

        for i in range(max_len - 1, -1, -1):
            dig1, dig2 = hex_map[a[i]], hex_map[b[i]]
            soma = dig1 + dig2 + carry
            resultado_dig = inv_hex_map[soma % 16]
            carry = soma // 16
            resultado = resultado_dig + resultado
            logs_local.append(f"{a[i]}({dig1}) + {b[i]}({dig2}) + vai-um({carry}) = {soma} -> {resultado_dig}")
        if carry:
            resultado = inv_hex_map[carry] + resultado
            logs_local.append(f"Vai-um final = {carry}, adicionado ao início.")
        return resultado.lstrip('0') or '0', logs_local

    def subtracao_hexadecimal_passo_a_passo(a, b):
        logs_local = []
        hex_map = {str(i): i for i in range(10)}
        hex_map.update({chr(ord('A') + i): 10 + i for i in range(6)})
        inv_hex_map = {v: k for k, v in hex_map.items()}
        a, b = a.upper(), b.upper()

        if len(b) > len(a) or (len(b) == len(a) and b > a):
            return "", ["Erro: subtração não suportada - número menor por maior."]
        a, b = list(a.zfill(len(b))), list(b.zfill(len(a)))
        resultado = ''
        emprestimo = 0
        logs_local.append("Subtração hexadecimal com empréstimos:")

        for i in range(len(a)-1, -1, -1):
            ai, bi = hex_map[a[i]], hex_map[b[i]]
            sub = ai - bi - emprestimo
            if sub < 0:
                sub += 16
                emprestimo = 1
            else:
                emprestimo = 0
            resultado = inv_hex_map[sub] + resultado
            logs_local.append(f"{a[i]}({ai}) - {b[i]}({bi}) - emp({emprestimo}) = {sub} -> {inv_hex_map[sub]}")

        return resultado.lstrip('0') or '0', logs_local

    # DECIMAL
    if base == "Decimal":
        try:
            n1, n2 = int(valor1), int(valor2)
        except ValueError:
            return "", "Erro: entrada inválida para decimal.", []

        if operacao == "Soma":
            resultado = str(n1 + n2)
            logs.append(f"Soma: {n1} + {n2} = {resultado}")
        elif operacao == "Subtração":
            resultado = str(n1 - n2)
            logs.append(f"Subtração: {n1} - {n2} = {resultado}")
        elif operacao == "Multiplicação":
            resultado = str(n1 * n2)
            logs.append(f"Multiplicação: {n1} * {n2} = {resultado}")
        else:
            return "", "Operação desconhecida.", []
        return resultado, "", logs

    # BINÁRIO
    elif base == "Binário":
        if not all(c in '01' for c in valor1 + valor2):
            return "", "Erro: entrada inválida para binário.", []

        if operacao == "Soma":
            resultado, passos = soma_binaria_passo_a_passo(valor1, valor2)

        elif operacao == "Subtração":
            n1 = int(valor1, 2)
            n2 = int(valor2, 2)
            if n1 < n2:
                return "", "Erro: subtração resultaria em valor negativo (não suportado).", []
            diff = n1 - n2
            resultado = bin(diff)[2:]
            passos = [f"Subtração direta: {valor1} (={n1}) - {valor2} (={n2}) = {resultado} (binário)"]

        elif operacao == "Multiplicação":
            n1, n2 = int(valor1, 2), int(valor2, 2)
            resultado = bin(n1 * n2)[2:]
            passos = [f"Multiplicação direta: {valor1} * {valor2} = {resultado} (binário)"]

        else:
            return "", "Operação desconhecida.", []

        logs.extend(passos)
        return resultado, "", logs


    # HEXADECIMAL
    elif base == "Hexadecimal":
        valid_hex = set("0123456789ABCDEFabcdef")
        if not all(c in valid_hex for c in valor1 + valor2):
            return "", "Erro: entrada inválida para hexadecimal.", []

        valor1 = valor1.upper()
        valor2 = valor2.upper()

        if operacao == "Soma":
            resultado, passos = soma_hexadecimal_passo_a_passo(valor1, valor2)

        elif operacao == "Subtração":
            n1, n2 = int(valor1, 16), int(valor2, 16)
            if n1 < n2:
                return "", "Erro: subtração resultaria em valor negativo (não suportado).", []
            resultado, passos = subtracao_hexadecimal_passo_a_passo(valor1, valor2)

        elif operacao == "Multiplicação":
            n1, n2 = int(valor1, 16), int(valor2, 16)
            resultado = hex(n1 * n2)[2:].upper()
            passos = [f"Multiplicação direta: {valor1} * {valor2} = {resultado} (hexadecimal)"]

        else:
            return "", "Operação desconhecida.", []

        logs.extend(passos)
        return resultado.upper(), "", logs




# Algoritmo de Euclides Estendido
def algoritmo_euclides_estendido(a: int, b: int) -> tuple[int, int, int, list[str]]:
    logs = []
    a_inicial, b_inicial = a, b

    logs.append("Iniciando o Algoritmo de Euclides Estendido para cálculo de Bézout.")
    s0, s1 = 1, 0  # Coeficientes para a
    t0, t1 = 0, 1  # Coeficientes para b
    passo = 1
    while b != 0:
        q = a // b
        r = a % b
        logs.append(f"Equação {passo}: {a} = {q} × {b} + {r}")
        a, b = b, r
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
        passo += 1

    logs.append(f"Resultado Final: {a_inicial} × ({s0}) + {b_inicial} × ({t0}) = {a}")
    return a, s0, t0, logs



# Crivo de Eratóstenes
def crivo_eratostenes_matriz(n: int) -> tuple[list[bool], list[str]]:
    primos = [True] * (n + 1)
    logs = []
    primos[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if primos[i]:
            for j in range(i * i, n + 1, i):
                if primos[j]:
                    primos[j] = False
                    logs.append(f"Eliminado: {j} como múltiplo de {i}")
    return primos, logs

# Páginas do Streamlit
def pag_conversor():
    st.title("Conversor de Bases")
    valor = st.text_input("Digite o número:")
    base_origem = st.selectbox("Base de origem:", ["Decimal", "Binário", "Hexadecimal"])
    base_destino = st.selectbox("Base de destino:", ["Decimal", "Binário", "Hexadecimal"])

    if st.button("Converter"):
        resultado, log = converter_base(valor, base_origem, base_destino)
        st.success(f"Resultado: {resultado}")
        with st.expander("Detalhes do Cálculo"):
            for linha in log:
                st.write(linha)

def pag_operacoes():
    st.title(" Calculadora de Operações com Bases")

    st.markdown("### Insira os números e selecione a base e operação:")

    col1, col2, col3 = st.columns([3, 2, 3])
    with col1:
        valor1 = st.text_input("Primeiro número:", key="v1")
    with col2:
        operacao = st.selectbox("Operação:", ["Soma", "Subtração", "Multiplicação"])
    with col3:
        valor2 = st.text_input("Segundo número:", key="v2")

    base = st.radio("Escolha a base numérica:", ["Decimal", "Binário", "Hexadecimal"], horizontal=True)

    calcular = st.button(" Calcular")

    if calcular:
        resultado, erro, logs = operacao_entre_numeros(valor1, valor2, base, operacao)

        st.markdown("---")
        if erro:
            st.error(erro)
        else:
            st.markdown(f"<h3 style='text-align: center;'> Resultado: <code>{resultado}</code></h3>", unsafe_allow_html=True)

        with st.expander(" Detalhes do Cálculo"):
            for l in logs:
                st.code(l)


def pag_euclides():
    st.title("Algoritmo de Euclides Estendido")
    a = st.number_input("Valor de a:", step=1, format="%d")
    b = st.number_input("Valor de b:", step=1, format="%d")
    if st.button("Calcular"):
        if a == 0 and b == 0:
            st.error("a e b não podem ser ambos zero.")
        else:
            mdc, x, y, logs = algoritmo_euclides_estendido(int(a), int(b))
            st.success(f"MDC = {mdc}")
            st.write(f"Coeficientes de Bézout: x = {x}, y = {y}")
            st.latex(f"{int(a)} \\cdot ({x}) + {int(b)} \\cdot ({y}) = {mdc}")
        with st.expander("Detalhes do Cálculo"):
            for log in logs:
                if log == "---":
                    st.markdown("---")
                elif log.startswith("**") and log.endswith("**"):
                    st.markdown(f"### {log.strip('**')}")
                else:
                    st.write(log)


def pag_crivo():
    st.title(" Crivo de Eratóstenes")

    st.markdown("Insira um número para ver todos os primos até ele usando o algoritmo do Crivo de Eratóstenes.")
    n = st.number_input("Digite o valor de n:", min_value=2, step=1, value=100)

    if st.button(" Gerar Primos"):
        primos, logs = crivo_eratostenes_matriz(n)
        primos_lista = [i for i, p in enumerate(primos) if p]

        st.markdown("### Números Primos Encontrados:")
        
        # Mostrar os primos em colunas
        cols = st.columns(6)
        for i, primo in enumerate(primos_lista):
            cols[i % 6].write(f"🔹 {primo}")

        # Expander com os detalhes do cálculo
        with st.expander(" Detalhes do Cálculo"):
            for i, log in enumerate(logs):
                st.markdown(f"**Passo {i+1}:** {log}")


# Menu principal
def main():
    st.sidebar.title("Menu de Navegação")
    pagina = st.sidebar.radio("Escolha uma página:", ["Menu", "Conversor de Bases", "Operações em Bases", "Algoritmo Estendido de Euclides", "Crivo de Eratóstenes"])

    if pagina == "Menu":
        st.title("Trabalho do Vanvan")
        st.image("imagem.jpg", caption="Ana Elisa, Isabela e Vitória", use_container_width=True)
        st.write("Bem-vindo! Use o menu à esquerda para navegar.")
    elif pagina == "Conversor de Bases":
        pag_conversor()
    elif pagina == "Operações em Bases":
        pag_operacoes()
    elif pagina == "Algoritmo Estendido de Euclides":
        pag_euclides()
    elif pagina == "Crivo de Eratóstenes":
        pag_crivo()

if __name__ == '__main__':
    main()
