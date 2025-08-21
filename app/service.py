from groq import Groq
from SPARQLWrapper import SPARQLWrapper, JSON

# Lê o schema da ontologia
with open("/home/raylander/Desktop/Web semântica/Trabalho/KGs/ontologia-musica-br-trig.trig", "r", encoding="utf-8") as f:
    schema = f.read()

# Inicializa o cliente Groq
client = Groq(api_key="ADICIONE_SUA_CHAVE")

# Endpoint do GraphDB (ajuste conforme seu repositório)
sparql = SPARQLWrapper("http://localhost:7200/repositories/EKG_MUSICA_BR")
sparql.setReturnFormat(JSON)

# Monta a mensagem para o modelo
def montar_mensagem(pergunta):
    mensagem = f"""
    Você é um assistente que converte perguntas em linguagem natural para consultas SPARQL.
    Baseie-se no seguinte schema RDF: {schema}
    Lembre-se que esse schema fornece informações relevantes da junção de 3 bases de dados diferentes.
    Lembre-se retorne somente a consulta SPARQL.
    Não coloque nenhum comentário no meio da consulta.
    Lembre-se que pode fazer as consultas todas para a linguagem português.
    Lembre-se que quando pergunta se ela está presente é querendo saber se ela existe no banco de dados.
    Quando é falado me dê informações, procure saber o que é e me traga informações sobre.
    Quando perguntar qual o artista mais popular retornar o nome do artista.
    Lembre-se que album se refere a record.

    Pergunta do usuário: {pergunta}
    """
    return mensagem

def montar_mensagem_resposta(resposta, pergunta):
    mensagem = f"""
    Você é um assistente que converte retorno de consultas SPARQL realizadas no GraphDB para respostas em texto natural.
    Você tem a seguinte resposta do GraphDB: {resposta}
    Pergunta do usuário: {pergunta}
    Lembre-se, a resposta é liguagem natural, se uma busca retornar true apenas diga que a resposta da pergunta é verdade.
    """
    return mensagem

# Faz a chamada ao modelo
def chamar_modelo(pergunta):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  # ou outro modelo disponível
        messages=[
            {"role": "user", "content": montar_mensagem(pergunta)},
        ]
    )
    print(response.choices[0].message.content)
    return chamar_modelo_resposta(executar_consulta(response.choices[0].message.content), pergunta)

def chamar_modelo_resposta(resposta, pergunta):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  # ou outro modelo disponível
        messages=[
            {"role": "user", "content": montar_mensagem_resposta(resposta, pergunta)},
        ]
    )
    return response.choices[0].message.content

def executar_consulta(consulta):
    sparql.setQuery(consulta)
    resultados = sparql.query().convert()
    if "results" in resultados and "bindings" in resultados["results"]:
        for item in resultados["results"]["bindings"]:
            print(item)
        print("O resultado da consulta é:", resultados)
        return resultados
    else:
        print("Consulta SPARQL inválida ou sem resultados:", resultados)
        return resultados  # ou retorne uma mensagem de erro customizada

