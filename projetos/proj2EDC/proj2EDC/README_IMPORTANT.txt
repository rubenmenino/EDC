Engenharia de Dados e Conhecimento
Projeto 2: Stand de Automóveis
Grupo 06: Eduardo Coelho (88867), Joaquim Ramos (88812), Ruben Menino (89185)

---------------------------------------- Como executar o programa --------------------------------------------

Caso esteja em windows:
1 - Ter python3.8 instalado tal como Django3.1
2 - Abrir Installer_Win.bat para instalar todas as dependências necessárias (os seus nomes estão em 'req.txt')

Por cmd: pip3 install Django s4api pillow django-crispy-forms

Ter a certeza que o 'Working directory' do projeto (em 'edit configuration') é o diretório 'app'.

Em caso do erro 'runnerw.exe', ligar a opção 'Allow paralel run' em 'edit configuration' pode resolver.

Adicionar repositório 'Anuncios_RDF.n3' presente no diretório 'app/static/rdf/' ao GraphDB e definir como 'anuncios' os campos de title e id.
Mudar ruleset para 'No Inference'.

---------------------------------- Breve explicação do trabalho efetuado --------------------------------------

-Transformação dos dados xml para N3;
-Todas as funcionalidades anteriores continuam funcionais em rdf:
	-'Carros Premium Disponiveis' mostram os 7 anúncios com maior preço E que ainda não tenham sido vendidos;
	-Filtros de pesquisa podem ser usados todos ao mesmo tempo;
	-Criação de um anúncio, agora verifica se já existe a Marca e/ou o Vendedor, caso não exista é criado;
	-Ao comprar um carro, é alterado o seu triple de predicado "venda" de 'Não vendido' para 'Vendido';
	-Ao apagar um anúncio é apagado todas as triples relacionadas com o mesmo;
-5 Inferências (Marcas Verdes, Marcas SemiVerdes, Supercarros, Vendedores Verificados, Veículos Coupe);
-Rdfa implementado na página que carrega um anúncio ('itemCarRdfa.html');
-Chamada à DBpedia no fim da página principal, com abstract de uma marca aleatória a cada refresh;


---------------- Tipos de querys efetuados (linhas mencionadas são do ficheiro views.py) ----------------------

Selects:
	Botões de ver os resultados de uma certa inferência ('Marcas Verdes', etc.) (l.103-186);
	Para os 7 Premium cars que aparecem no início da página (l.189-220);
	Para preencher os dropdowns de marcas, modelos e combustíveis nos filtros (l.224-267);
	As 8 variações possíveis de preenchimento dos filtros (l.292-571);
	Chamada à DBpedia (l.575-587);
	Número atual de vendas de um vendedor (l.653-663);
	Todas as informações para mostrar na página de um anúncio, incluíndo as do vendedor (l.690-729);
	Para saber uma pessoa através do seu emal (l.835-842);
	Para listar todas as pessoas (l.914-921);

Insert: 
	Botão que aplica as 5 inferências (l.34-101);
	Botão de comprar, inserindo triplo com valor 'vendido' (l.632-649);
	Inserir o novo número de vendas incrementado por 1 (l.676-685);
	Para criar o anúncio (com as várias (4) combinações de existir marca e/ou pessoa ou não) (l.832-1002);

Delete:
	Botão de apagar anúncio (l.609-622);
	Botão de comprar, apagando triplo com valor 'naovendido' (l.632-649);
	Apagar o número antigo de vendas (l.666-674);

Ask:
	Verificar se uma pessoa já existe, para saber se é necessário criar (l.808-815);
	Verificar se uma marca já existe, para saber se é necessário criar (l.820-827);



