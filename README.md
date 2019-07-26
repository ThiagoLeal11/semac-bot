# Semac Bot
O robô da semac é uma prova de conceito feito com o objetivo de facilitar o deploy das novas versões do backend e do frontend. Adicionalmente, ele responde a interações de boas vindas e corrige caso o usuário fale algum palavrão.

# Funcionamento
As mensagens são recebidas utilizando a biblioteca _pytgbot_ e são processadas no arquivo ```nlp.py```.
O texto de entrada é convertido para lowercase, tem expaços adicionais removidos e todos os caracteres especiais são convertidos.
No ```nlp.py``` também se  encrontra o dicionario de _intents_ cuja estrutura descreve o nome da ação seguido pelas suas palavras chaves de ativação.

Adicionalmente, pode ser utilizado os _parameters_ que são um complemento para os _intents_. Um exemplo é que a mesma ação de _deploy_ pode ser feita para o _backend_ ou para o _frontend_. Nesse caso, o tipo é um parametro.

Depois do processamento isso é adicionado no contexto e volta para o ```bot.py```, onde uma série de _if's_ ira fazer a seleção da ação.

Nesse meio tempo, varias mesagens de _log_ são enviadas para o usuário que solicitou a ação, informando quais comandos estão sendo processados.
