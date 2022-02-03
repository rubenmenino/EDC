import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from proj2EDC.settings import BASE_DIR
from .feed.news.news import *
from .forms import ImageForm
from . import models
import sqlite3
from django.db import OperationalError
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from SPARQLWrapper import SPARQLWrapper,JSON
import random

endpoint = "http://localhost:7200"
repo_name = "anuncios"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


STATIC_PATH = os.path.join(BASE_DIR, "app", "static")
XML_PATH = os.path.join(STATIC_PATH, "xml")
ANUNCIOS_XSLT_FILE_PATH = os.path.join(XML_PATH, "anuncios.xsl")
DEALS_XSLT_FILE_PATH = os.path.join(XML_PATH, "deals.xsl")
ITEMCAR_XSLT_FILE_PATH = os.path.join(XML_PATH, "itemcar.xsl")

# Create your views here.
def index(request):
        disableBtn = 'False'
        inferencia = []
        dbpedia = ''

        if 'CriarInferencias' in request.POST:
            disableBtn = 'True'
            inputVerdes="""
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                insert {?id_marca a stand:Ecologica}
                where {
                    ?id_anuncio a stand:Anuncio.
                    ?id_anuncio stand:marca ?id_marca.
                    ?id_anuncio stand:combustivel ?combustivel.
                    filter regex(?combustivel,"elétrico")
                }
            """
            accessor.sparql_update(body={"update": inputVerdes}, repo_name=repo_name)

            inputSemiVerdes = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                insert {?id_marca a stand:SemiEcologica}
                where {
                    ?id_anuncio a stand:Anuncio.
                    ?id_anuncio stand:marca ?id_marca.
                    ?id_anuncio stand:combustivel ?combustivel.
                    filter regex(?combustivel,"híbrido")
                }
            """
            accessor.sparql_update(body={"update": inputSemiVerdes}, repo_name=repo_name)

            inputSupercarros = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                insert {?id_anuncio a stand:Supercar}
                where {
                    ?id_anuncio a stand:Anuncio.
                    ?id_anuncio stand:potencia ?cavalos.
                    filter (?cavalos > "480"^^xsd:integer)
                }
            """
            accessor.sparql_update(body={"update": inputSupercarros}, repo_name=repo_name)

            inputVendedoresVerificados = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                insert {?id_vendedor a stand:Verified}
                where {
                    ?id_vendedor a stand:Person.
                    ?id_vendedor stand:numvendas ?vendas.
                    filter (?vendas > "0"^^xsd:integer)
                }
            """
            accessor.sparql_update(body={"update": inputVendedoresVerificados}, repo_name=repo_name)

            inputCoupes = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                insert {?id_anuncio a stand:Coupe}
                where {
                    ?id_anuncio a stand:Anuncio.
                    ?id_anuncio stand:lotacao ?num_pessoas.
                    filter (?num_pessoas < "3"^^xsd:integer)
                }
            """
            accessor.sparql_update(body={"update": inputCoupes}, repo_name=repo_name)

        elif 'MarcasVerdes' in request.POST:
            inputinf = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                select ?id_marca ?nome_marca where{
                    ?id_marca a stand:Ecologica.
                    ?id_marca stand:nome ?nome_marca.
                }
            """
            resinf = accessor.sparql_select(body={"query": inputinf}, repo_name=repo_name)
            resinf = json.loads(resinf)
            for dict in resinf['results']['bindings']:
                inferencia.append('{id:' + dict['id_marca']['value'] + '; nome_marca:' + dict['nome_marca']['value'] + '}')

        elif 'MarcasSemiverdes' in request.POST:
            inputinf = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                select ?id_marca ?nome_marca where{
                    ?id_marca a stand:SemiEcologica.
                    ?id_marca stand:nome ?nome_marca.
                }
            """
            resinf = accessor.sparql_select(body={"query": inputinf}, repo_name=repo_name)
            resinf = json.loads(resinf)
            for dict in resinf['results']['bindings']:
                inferencia.append('{id:' + dict['id_marca']['value'] + '; nome_marca:' + dict['nome_marca']['value'] + '}')

        elif 'Supercarros' in request.POST:
            inputinf = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                select ?nome_marca ?modelo ?id_anuncio ?potencia where{
                    ?id_anuncio a stand:Supercar.
                    ?id_anuncio stand:marca ?id_marca.
                    ?id_marca a stand:Marca.
                    ?id_marca stand:nome ?nome_marca.
                    ?id_anuncio stand:modelo ?modelo.
                    ?id_anuncio stand:potencia ?potencia.
                }
            """
            resinf = accessor.sparql_select(body={"query": inputinf}, repo_name=repo_name)
            resinf = json.loads(resinf)
            for dict in resinf['results']['bindings']:
                inferencia.append('{id:' + dict['id_anuncio']['value'] + '; nome_marca:' + dict['nome_marca']['value'] + '; modelo:' + dict['modelo']['value'] + '; potencia:' + dict['potencia']['value'] + 'cv' + '}')

        elif 'Verificados' in request.POST:
            inputinf = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                select ?id_vendedor ?nome_vendedor ?email_vendedor ?telefone ?numvendas where{
                    ?id_vendedor a stand:Verified.
                    ?id_vendedor stand:nome ?nome_vendedor.
                    ?id_vendedor stand:email ?email_vendedor.
                    ?id_vendedor stand:contacto ?telefone.  
                    ?id_vendedor stand:numvendas ?numvendas.     
                }
            """
            resinf = accessor.sparql_select(body={"query": inputinf}, repo_name=repo_name)
            resinf = json.loads(resinf)
            for dict in resinf['results']['bindings']:
                inferencia.append('{id:' + dict['id_vendedor']['value'] + '; nome:' + dict['nome_vendedor']['value'] + '; email:' + dict['email_vendedor']['value']+ '; telefone:' + dict['telefone']['value'] + '; numvendas:' + dict['numvendas']['value'] + '}')

        elif 'Coupe' in request.POST:
            inputinf = """
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                select ?nome_marca ?modelo ?id_anuncio where{   
                    ?id_anuncio a stand:Coupe.
                    ?id_anuncio stand:marca ?id_marca.
                    ?id_marca a stand:Marca.
                    ?id_marca stand:nome ?nome_marca.
                    ?id_anuncio stand:modelo ?modelo.
                }
            """
            resinf = accessor.sparql_select(body={"query": inputinf}, repo_name=repo_name)
            resinf = json.loads(resinf)
            for dict in resinf['results']['bindings']:
                inferencia.append('{id:' + dict['id_anuncio']['value'] + '; nome_marca:' + dict['nome_marca']['value'] + '; modelo:' + dict['modelo']['value'] + '}')

        ########################################################################################
        inputDeals = """
            PREFIX stand: <http://stand.com/>
            select distinct ?id ?marca ?modelo ?preco ?registo ?transmissao ?quilometros ?imagem where { 
                ?s a stand:Anuncio. 
                ?s stand:id ?id.
                ?s stand:marca ?id_marca.
                ?id_marca a stand:Marca. 
                ?id_marca stand:nome ?marca.
                ?s stand:modelo ?modelo.
                ?s stand:preco ?preco.
                ?s stand:registo ?registo.
                ?s stand:transmissao ?transmissao.
                ?s stand:quilometros ?quilometros.
                ?s stand:imagem ?imagem.
                ?s stand:venda ?venda.
                FILTER regex(?venda,"naovendido").
            }
            order by desc(xsd:integer(?preco)) limit 7
        """
        resDeals = accessor.sparql_select(body={"query": inputDeals},repo_name=repo_name)
        resDeals = json.loads(resDeals)
        deals = []
        for anuncio in resDeals['results']['bindings']:
            id = anuncio['id']['value']
            marca = anuncio['marca']['value']
            modelo = anuncio['modelo']['value']
            preco = anuncio['preco']['value']
            registo = anuncio['registo']['value']
            transmissao = anuncio['transmissao']['value']
            quilometros = anuncio['quilometros']['value']
            imagem = anuncio['imagem']['value']
            deals.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'registo': registo, 'transmissao': transmissao, 'quilometros': quilometros, 'imagem': imagem})


        ########################################################################################
        input1 = """
            PREFIX stand: <http://stand.com/>
            select ?nome where { 
                ?s a stand:Marca. 
                ?s stand:nome ?nome.
            }   
        """
        res1 = accessor.sparql_select(body={"query": input1},repo_name=repo_name)
        res1 = json.loads(res1)
        marcas=[]
        for nome in res1['results']['bindings']:
            marcas.append(nome['nome']['value'])


        ########################################################################################
        input2 = """
            PREFIX stand: <http://stand.com/>

            select distinct ?modelo where { 
                ?s a stand:Anuncio. 
                ?s stand:modelo ?modelo.
            }  
        """
        res2 = accessor.sparql_select(body={"query": input2},repo_name=repo_name)
        res2 = json.loads(res2)
        modelos = []
        for modelo in res2['results']['bindings']:
            modelos.append(modelo['modelo']['value'])


        ########################################################################################
        input3 = """
            PREFIX stand: <http://stand.com/>

            select distinct ?combustivel where { 
                ?s a stand:Anuncio. 
                ?s stand:combustivel ?combustivel.
            }  
        """
        res3 = accessor.sparql_select(body={"query": input3},repo_name=repo_name)
        res3 = json.loads(res3)
        combustivel = []
        for c in res3['results']['bindings']:
            combustivel.append(c['combustivel']['value'])

        ########################################################################################
        ########################################################################################
        ########################################################################################
        ########################################################################################

        selectedmarca = request.POST.get('marca', False)
        selectedmodelo = request.POST.get('modelo', False)
        selectedcombustivel = request.POST.get('combustivel', False)
        selectedquilometros = request.POST.get('quilometros', False)
        selectedregisto = request.POST.get('registo', False)
        selectedpreco = request.POST.get('preco', False)


        if not selectedquilometros:
            selectedquilometros = 1000000000
        if not selectedpreco:
            selectedpreco = 1000000000
        if not selectedregisto:
            selectedregisto = 1900

        if len(str(selectedcombustivel))>6 and selectedcombustivel.lower()[0] == 'h':
            selectedcombustivel = "híbrido"

        if selectedmarca:
            if selectedmodelo:
                if selectedcombustivel:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        
                        select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                            ?s a stand:Anuncio. 
                            ?s stand:id ?id.
                            ?s stand:marca ?id_marca.
                            ?id_marca a stand:Marca. 
                            ?id_marca stand:nome ?marca.
                            ?s stand:modelo ?modelo.
                            ?s stand:preco ?preco.
                            ?s stand:registo ?registo.
                            ?s stand:combustivel ?combustivel.
                            ?s stand:quilometros ?quilometros.
                            ?s stand:imagem ?imagem.
                            filter regex(?marca,'""", str(selectedmarca).lower(), """')
                            filter regex(?modelo,'""", str(selectedmodelo).lower(), """')
                            filter regex(?combustivel,'""", str(selectedcombustivel).lower(), """')
                            filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                            filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                            filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                        }   
                    """])

                    res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                    res = json.loads(res)
                    html = []
                    for anuncio in res['results']['bindings']:
                        id = anuncio['id']['value']
                        marca = anuncio['marca']['value']
                        modelo = anuncio['modelo']['value']
                        preco = anuncio['preco']['value']
                        imagem = anuncio['imagem']['value']
                        html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})


                else:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        
                        select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                            ?s a stand:Anuncio. 
                            ?s stand:id ?id.
                            ?s stand:marca ?id_marca.
                            ?id_marca a stand:Marca. 
                            ?id_marca stand:nome ?marca.
                            ?s stand:modelo ?modelo.
                            ?s stand:preco ?preco.
                            ?s stand:registo ?registo.
                            ?s stand:combustivel ?combustivel.
                            ?s stand:quilometros ?quilometros.
                            ?s stand:imagem ?imagem.
                            filter regex(?marca,'""", str(selectedmarca).lower(), """')
                            filter regex(?modelo,'""", str(selectedmodelo).lower(), """')
                            filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                            filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                            filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                        } 
                    """])
                    res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                    res = json.loads(res)
                    html = []
                    for anuncio in res['results']['bindings']:
                        id = anuncio['id']['value']
                        marca = anuncio['marca']['value']
                        modelo = anuncio['modelo']['value']
                        preco = anuncio['preco']['value']
                        imagem = anuncio['imagem']['value']
                        html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

            elif selectedcombustivel:
                input = ''.join(["""
                    PREFIX stand: <http://stand.com/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    
                    select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                        ?s a stand:Anuncio. 
                        ?s stand:id ?id.
                        ?s stand:marca ?id_marca.
                        ?id_marca a stand:Marca. 
                        ?id_marca stand:nome ?marca.
                        ?s stand:modelo ?modelo.
                        ?s stand:preco ?preco.
                        ?s stand:registo ?registo.
                        ?s stand:combustivel ?combustivel.
                        ?s stand:quilometros ?quilometros.
                        ?s stand:imagem ?imagem.
                        filter regex(?marca,'""", str(selectedmarca).lower(), """')
                        filter regex(?combustivel,'""", str(selectedcombustivel).lower(), """')
                        filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                        filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                        filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                    }
                """])
                res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                res = json.loads(res)
                html = []
                for anuncio in res['results']['bindings']:
                    id = anuncio['id']['value']
                    marca = anuncio['marca']['value']
                    modelo = anuncio['modelo']['value']
                    preco = anuncio['preco']['value']
                    imagem = anuncio['imagem']['value']
                    html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

            else:
                input = ''.join(["""
                    PREFIX stand: <http://stand.com/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    
                    select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                        ?s a stand:Anuncio. 
                        ?s stand:id ?id.
                        ?s stand:marca ?id_marca.
                        ?id_marca a stand:Marca. 
                        ?id_marca stand:nome ?marca.
                        ?s stand:modelo ?modelo.
                        ?s stand:preco ?preco.
                        ?s stand:registo ?registo.
                        ?s stand:combustivel ?combustivel.
                        ?s stand:quilometros ?quilometros.
                        ?s stand:imagem ?imagem.
                        filter regex(?marca,'""", str(selectedmarca).lower(), """')
                        filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                        filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                        filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                    }
                """])
                res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                res = json.loads(res)
                html = []
                for anuncio in res['results']['bindings']:
                    id = anuncio['id']['value']
                    marca = anuncio['marca']['value']
                    modelo = anuncio['modelo']['value']
                    preco = anuncio['preco']['value']
                    imagem = anuncio['imagem']['value']
                    html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

        elif selectedmodelo:
            if selectedcombustivel:
                input = ''.join(["""
                    PREFIX stand: <http://stand.com/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    
                    select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                        ?s a stand:Anuncio. 
                        ?s stand:id ?id.
                        ?s stand:marca ?id_marca.
                        ?id_marca a stand:Marca. 
                        ?id_marca stand:nome ?marca.
                        ?s stand:modelo ?modelo.
                        ?s stand:preco ?preco.
                        ?s stand:registo ?registo.
                        ?s stand:combustivel ?combustivel.
                        ?s stand:quilometros ?quilometros.
                        ?s stand:imagem ?imagem.
                        filter regex('""", str(selectedmodelo).lower(), """')
                        filter regex('""", str(selectedcombustivel).lower(), """')
                        filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                        filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                        filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                    }
                """])
                res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                res = json.loads(res)
                html = []
                for anuncio in res['results']['bindings']:
                    id = anuncio['id']['value']
                    marca = anuncio['marca']['value']
                    modelo = anuncio['modelo']['value']
                    preco = anuncio['preco']['value']
                    imagem = anuncio['imagem']['value']
                    html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

            else:
                input = ''.join(["""
                    PREFIX stand: <http://stand.com/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    
                    select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                        ?s a stand:Anuncio. 
                        ?s stand:id ?id.
                        ?s stand:marca ?id_marca.
                        ?id_marca a stand:Marca. 
                        ?id_marca stand:nome ?marca.
                        ?s stand:modelo ?modelo.
                        ?s stand:preco ?preco.
                        ?s stand:registo ?registo.
                        ?s stand:combustivel ?combustivel.
                        ?s stand:quilometros ?quilometros.
                        ?s stand:imagem ?imagem.
                        filter regex(?modelo,'""", str(selectedmodelo).lower(), """')
                        filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                        filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                        filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                    }
                """])
                res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
                res = json.loads(res)
                html = []
                for anuncio in res['results']['bindings']:
                    id = anuncio['id']['value']
                    marca = anuncio['marca']['value']
                    modelo = anuncio['modelo']['value']
                    preco = anuncio['preco']['value']
                    imagem = anuncio['imagem']['value']
                    html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

        elif selectedcombustivel:
            input = ''.join(["""
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX stand: <http://stand.com/>
                
                select distinct ?id ?marca ?modelo ?preco ?imagem where {
                    ?s a stand:Anuncio.
                    ?s stand:id ?id.
                    ?s stand:marca ?id_marca.
                    ?id_marca a stand:Marca.
                    ?id_marca stand:nome ?marca.
                    ?s stand:modelo ?modelo.
                    ?s stand:preco ?preco.
                    ?s stand:registo ?registo.
                    ?s stand:combustivel ?combustivel.
                    ?s stand:quilometros ?quilometros.
                    ?s stand:imagem ?imagem.
                    filter regex(?combustivel,'""", str(selectedcombustivel).lower(), """')
                    filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer)
                    filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                    filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                }
            """])
            res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
            res = json.loads(res)
            html = []
            for anuncio in res['results']['bindings']:
                id = anuncio['id']['value']
                marca = anuncio['marca']['value']
                modelo = anuncio['modelo']['value']
                preco = anuncio['preco']['value']
                imagem = anuncio['imagem']['value']
                html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

        else:
            input = ''.join(["""
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                
                select distinct ?id ?marca ?modelo ?preco ?imagem where { 
                    ?s a stand:Anuncio. 
                    ?s stand:id ?id.
                    ?s stand:marca ?id_marca.
                    ?id_marca a stand:Marca. 
                    ?id_marca stand:nome ?marca.
                    ?s stand:modelo ?modelo.
                    ?s stand:preco ?preco.
                    ?s stand:registo ?registo.
                    ?s stand:combustivel ?combustivel.
                    ?s stand:quilometros ?quilometros.
                    ?s stand:imagem ?imagem.
                    filter (?registo >= '""", str(selectedregisto), """'^^xsd:integer) 
                    filter (?preco <= '""", str(selectedpreco), """'^^xsd:integer)
                    filter (?quilometros <= '""", str(selectedquilometros), """'^^xsd:integer)
                }
            """])
            res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
            res = json.loads(res)
            html = []
            for anuncio in res['results']['bindings']:
                id = anuncio['id']['value']
                marca = anuncio['marca']['value']
                modelo = anuncio['modelo']['value']
                preco = anuncio['preco']['value']
                imagem = anuncio['imagem']['value']
                html.append({'id': id, 'marca': marca, 'modelo': modelo, 'preco': preco, 'imagem': imagem})

        possiveis = ['Ferrari','McLaren','Mercedes-Benz','Renault','Volkswagen','Tesla,_Inc.','Citroën','Porsche']

        while(dbpedia == ''):
            selectrandom = random.choice(possiveis)
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery("""
                SELECT ?label
                WHERE { <http://dbpedia.org/resource/"""+selectrandom+"""> dbo:abstract ?label }
            """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            for result in results["results"]["bindings"]:
                if result['label']['xml:lang'] == 'pt':
                    dbpedia += result['label']['value']

        context = {
            "content": html, #agora este content tem de retornar o json com a info de forma a poder fazer 'for c in content' no index.html
            "deals": deals, #agora este deals tem de retornar o json com a info de forma a poder fazer 'for deal in deals' no index.html
            "news": getNews(3),
            "marcas": marcas,
            "modelos": modelos,
            "combustivel": combustivel,
            "disableBtn": disableBtn,
            "inferencia": inferencia,
            "dbpedia": dbpedia,
        }

        return render(request, 'index.html', context)

def anuncio(request):
    assert isinstance(request, HttpRequest)
    id = ""
    if 'carID' in request.POST and 'Apagar' in request.POST:
        id = request.POST['carID']

        inputDelete = ''.join(["""
            PREFIX stand: <http://stand.com/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            DELETE { ?s ?p ?o}
            WHERE
            {
                ?s stand:id ?id.
                filter (?id = '""",id,"""'^^xsd:integer).

                ?s ?p ?o .
            }
        """])
        resDelete = accessor.sparql_update(body={"update": inputDelete}, repo_name=repo_name)

        os.remove(STATIC_PATH + '/products-images/'+id+'.png')

        return redirect('/')
    else:
        if 'carID' in request.POST and 'Comprar' in request.POST and 'person' in request.POST:
            id = request.POST['carID']
            person = request.POST['person'][17:]

            inputUpdate = ''.join([""" 
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                DELETE { ?s a stand:Anuncio. 
                            ?s stand:venda 'naovendido' }
                
                INSERT { ?s a stand:Anuncio. 
                         ?s stand:venda 'vendido' }
                
                WHERE
                  { ?s a stand:Anuncio. 
                    ?s stand:id ?id.
                    ?s stand:venda 'naovendido'
                    filter (?id = '""",id,"""'^^xsd:integer)
                  }
            """])
            accessor.sparql_update(body={"update": inputUpdate}, repo_name=repo_name)

            #incrementar numero de vendas da Person
            #pesquisar numero de vendas
            inputVendas = ''.join([""" 
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                select ?vendas where{
                    stand:""", person, """ stand:numvendas ?vendas.
                }
            """])
            resVendas = accessor.sparql_select(body={"query": inputVendas}, repo_name=repo_name)
            resVendas = json.loads(resVendas)
            resVendas = resVendas['results']['bindings'][0]['vendas']['value']

            #apagar numero de vendas com o "0" substituido pelo valor acima
            inputApagar = ''.join([""" 
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                delete data {
                    stand:""",person,""" stand:numvendas '""",resVendas,"""'^^xsd:integer.
                }
            """])
            accessor.sparql_update(body={"update": inputApagar}, repo_name=repo_name)

            #inserir numero de vendas com valor acima + 1
            inputInserir = ''.join([""" 
                PREFIX stand: <http://stand.com/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                insert data {
                    stand:""",person,""" stand:numvendas '""",str(int(resVendas)+1),"""'^^xsd:integer.
                }
            """])
            accessor.sparql_update(body={"update": inputInserir}, repo_name=repo_name)

        else:
            id = request.GET['id']

        input = ''.join(["""
            PREFIX stand: <http://stand.com/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            select ?id ?venda ?preco ?vendedor ?contacto ?email ?numvendas ?marca ?modelo ?cilindrada ?combustivel ?transmissao ?registo ?mes ?estado ?potencia ?quilometros ?numportas ?lotacao ?imagem ?descricao ?cenasVendedor where { 

                ?s a stand:Anuncio. 
                ?s stand:id ?id.
                ?s stand:venda ?venda.
                ?s stand:preco ?preco.
            
                ?s stand:vendedor ?cenasVendedor.
                ?cenasVendedor a stand:Person. 
                ?cenasVendedor stand:nome ?vendedor. 
                ?cenasVendedor stand:contacto ?contacto.
                ?cenasVendedor stand:email ?email.
                ?cenasVendedor stand:numvendas ?numvendas.
            
                ?s stand:marca ?id_marca.
                ?id_marca a stand:Marca. 
                ?id_marca stand:nome ?marca.
                ?s stand:modelo ?modelo.
                ?s stand:cilindrada ?cilindrada.
                ?s stand:combustivel ?combustivel.
                ?s stand:transmissao ?transmissao.
                ?s stand:registo ?registo.
                ?s stand:mes ?mes.
                ?s stand:estado ?estado.
                ?s stand:potencia ?potencia.
                ?s stand:quilometros ?quilometros.
                ?s stand:numportas ?numportas.
                ?s stand:lotacao ?lotacao.
                ?s stand:imagem ?imagem.
                ?s stand:descricao ?descricao.
                filter (?id = '""",id,"""'^^xsd:integer) 
            } 
        """])
        res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
        res = json.loads(res)
        anuncio = res['results']['bindings'][0]

        id = anuncio['id']['value']
        venda = anuncio['venda']['value']
        preco = anuncio['preco']['value']
        vendedor = anuncio['vendedor']['value']
        contacto = anuncio['contacto']['value']
        email = anuncio['email']['value']
        numvendas = anuncio['numvendas']['value']
        marca = anuncio['marca']['value']
        modelo = anuncio['modelo']['value']
        cilindrada = anuncio['cilindrada']['value']
        combustivel = anuncio['combustivel']['value']
        transmissao = anuncio['transmissao']['value']
        registo = anuncio['registo']['value']
        mes = anuncio['mes']['value']
        estado = anuncio['estado']['value']
        potencia = anuncio['potencia']['value']
        quilometros = anuncio['quilometros']['value']
        numportas = anuncio['numportas']['value']
        lotacao = anuncio['lotacao']['value']
        imagem = anuncio['imagem']['value']
        descricao = anuncio['descricao']['value']
        person = anuncio['cenasVendedor']['value']
        html = {'id': id, 'venda':venda, 'preco':preco, 'vendedor':vendedor, 'contacto':contacto,'email':email,
                'numvendas':numvendas,'marca': marca, 'modelo': modelo,'cilindrada':cilindrada,'combustivel':combustivel,
                'transmissao':transmissao,'registo':registo,'mes':mes,'estado':estado,'potencia':potencia, 'quilometros':quilometros,
                'numportas':numportas, 'lotacao':lotacao,'imagem':imagem, 'descricao':descricao, 'person':person}



    tparams = {
        'info': html
    }
    return render(request, 'itemCarRdfa.html', tparams)

context = { "content": ""}
def criaranuncio(request):
    global context;
    res = None
    assert isinstance(request, HttpRequest)

    if 'nome' in request.POST and 'email' in request.POST and 'contacto' in request.POST and 'marca' in request.POST and 'modelo' in request.POST and 'cilindrada' in request.POST and 'transmissao' in request.POST and 'registo' in request.POST and 'mes' in request.POST and 'estado' in request.POST and 'potencia' in request.POST and 'quilometros' in request.POST and 'numportas' in request.POST and 'lotacao' in request.POST and 'preco' in request.POST and 'descricao' in request.POST:

        newID = str(models.get_id()) #calcular ultimo id + 1

        nome = request.POST['nome']
        email = request.POST['email']
        contacto = request.POST['contacto']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        cilindrada = request.POST['cilindrada']
        combustivel = request.POST['combustivel']
        transmissao = request.POST['transmissao']
        registo = request.POST['registo']
        mes = request.POST['mes']
        estado = request.POST['estado']
        potencia = request.POST['potencia']
        quilometros = request.POST['quilometros']
        numportas = request.POST['numportas']
        lotacao = request.POST['lotacao']
        preco = request.POST['preco']
        descricao = request.POST['descricao']

        if nome and email and contacto and preco and lotacao and numportas and quilometros and estado and potencia and mes and registo and transmissao and cilindrada and combustivel and marca and modelo:

            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    form.save()
                except OperationalError as e:
                    pass
                except sqlite3.OperationalError as e:
                    pass

            pessoaExiste = False
            marcaExiste = False

            askPessoa= """
                PREFIX stand: <http://stand.com/>
    
                ask{
                    ?id_person a stand:Person;
                        stand:email '"""+email+"""'.
                }
            """
            pessoaExiste = accessor.sparql_select(body={"query": askPessoa}, repo_name=repo_name)
            pessoaExiste = json.loads(pessoaExiste)
            pessoaExiste = pessoaExiste['boolean']

            askMarca= """
                PREFIX stand: <http://stand.com/>

                ask { 
                    ?id_marca a stand:Marca;
                           stand:nome '"""+marca.lower()+"""'.
                } 
            """
            marcaExiste = accessor.sparql_select(body={"query": askMarca}, repo_name=repo_name)
            marcaExiste = json.loads(marcaExiste)
            marcaExiste = marcaExiste['boolean']

            if pessoaExiste:
                # Retornar o id da pessoa através do mail
                inputp = """
                PREFIX stand:<http://stand.com/>

                select ?id_person
                    {
                        ?id_person a stand:Person;
                            stand:email '"""+email+"""'.
                    }
                """
                resp = accessor.sparql_select(body={"query": inputp}, repo_name=repo_name)
                resp = json.loads(resp)
                resp = resp['results']['bindings'][0]['id_person']['value'][17:]
                if marcaExiste:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        insert DATA { 
                            #inserir o anuncio
                            stand:a""", newID, """ a stand:Anuncio;
                                      stand:id '""", newID, """'^^xsd:integer;
                                      stand:venda "naovendido";
                                      stand:preco '""", preco, """'^^xsd:integer;
                                      stand:vendedor stand:""", resp, """;
                                      stand:marca stand:""", marca.replace(" ", "").lower(), """;
                                      stand:modelo '""", modelo, """';
                                      stand:cilindrada '""", cilindrada, """'^^xsd:integer;
                                      stand:combustivel '""", combustivel, """';
                                      stand:transmissao '""", transmissao, """';
                                      stand:registo '""", registo, """'^^xsd:integer;
                                      stand:mes '""", mes, """';
                                      stand:estado '""", estado, """';
                                      stand:potencia '""", potencia, """'^^xsd:integer;
                                      stand:quilometros '""", quilometros, """'^^xsd:integer;
                                      stand:numportas '""", numportas, """'^^xsd:integer;
                                      stand:lotacao '""", lotacao, """'^^xsd:integer;
                                      stand:imagem '""", newID, """.png';
                                      stand:descricao '""", descricao, """' .
                        }
                    """])  # criar o novo anuncio
                    accessor.sparql_update(body={"update": input}, repo_name=repo_name)



                else:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        insert DATA { 
                            #inserir marca
                            stand:""", marca.replace(" ", "").lower(), """ a stand:Marca;
                                         stand:nome '""", marca.lower(), """'.

                            #inserir o anuncio
                            stand:a""", newID, """ a stand:Anuncio;
                                      stand:id '""", newID, """'^^xsd:integer;
                                      stand:venda "naovendido";
                                      stand:preco '""", preco, """'^^xsd:integer;
                                      stand:vendedor stand:""", resp, """;
                                      stand:marca stand:""", marca.replace(" ", "").lower(), """;
                                      stand:modelo '""", modelo, """';
                                      stand:cilindrada '""", cilindrada, """'^^xsd:integer;
                                      stand:combustivel '""", combustivel, """';
                                      stand:transmissao '""", transmissao, """';
                                      stand:registo '""", registo, """'^^xsd:integer;
                                      stand:mes '""", mes, """';
                                      stand:estado '""", estado, """';
                                      stand:potencia '""", potencia, """'^^xsd:integer;
                                      stand:quilometros '""", quilometros, """'^^xsd:integer;
                                      stand:numportas '""", numportas, """'^^xsd:integer;
                                      stand:lotacao '""", lotacao, """'^^xsd:integer;
                                      stand:imagem '""", newID, """.png';
                                      stand:descricao '""", descricao, """' .
                        }
                    """])  # criar o novo anuncio
                    accessor.sparql_update(body={"update": input}, repo_name=repo_name)

            else:
                #temos de calcular o novo p'xx' para a pessoa stand:pxx
                inputp = """
                    PREFIX stand:<http://stand.com/>

                    select ?id_person
                    {
                        ?id_person a stand:Person;
                    }
                """
                resp = accessor.sparql_select(body={"query": inputp}, repo_name=repo_name)
                resp = json.loads(resp)
                resp = resp['results']['bindings'][-1]['id_person']['value'][17:]
                resp = ''.join([resp[0], str(int(resp[1:]) + 1)])

                if marcaExiste:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        insert DATA { 
                            #inserir pessoa
                            stand:""",resp, """ a stand:Person;
                                      stand:nome '""", nome, """';
                                      stand:contacto '""", contacto, """'^^xsd:integer;
                                      stand:email '""", email, """';
                                      stand:numvendas "0"^^xsd:integer.

                            #inserir o anuncio
                            stand:a""", newID, """ a stand:Anuncio;
                                      stand:id '""", newID, """'^^xsd:integer;
                                      stand:venda "naovendido";
                                      stand:preco '""", preco, """'^^xsd:integer;
                                      stand:vendedor stand:""",resp, """;
                                      stand:marca stand:""", marca.replace(" ", "").lower(), """;
                                      stand:modelo '""", modelo, """';
                                      stand:cilindrada '""", cilindrada, """'^^xsd:integer;
                                      stand:combustivel '""", combustivel, """';
                                      stand:transmissao '""", transmissao, """';
                                      stand:registo '""", registo, """'^^xsd:integer;
                                      stand:mes '""", mes, """';
                                      stand:estado '""", estado, """';
                                      stand:potencia '""", potencia, """'^^xsd:integer;
                                      stand:quilometros '""", quilometros, """'^^xsd:integer;
                                      stand:numportas '""", numportas, """'^^xsd:integer;
                                      stand:lotacao '""", lotacao, """'^^xsd:integer;
                                      stand:imagem '""", newID, """.png';
                                      stand:descricao '""", descricao, """' .
                        }
                    """])  # criar o novo anuncio
                    accessor.sparql_update(body={"update": input}, repo_name=repo_name)
                else:
                    input = ''.join(["""
                        PREFIX stand: <http://stand.com/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
                        insert DATA { 
                            #inserir marca
                            stand:""",marca.replace(" ","").lower(),""" a stand:Marca;
                                         stand:nome '""",marca.lower(),"""'.
                            
                            #inserir pessoa
                            stand:""",resp,""" a stand:Person;
                                      stand:nome '""",nome,"""';
                                      stand:contacto '""",contacto,"""'^^xsd:integer;
                                      stand:email '""",email,"""';
                                      stand:numvendas "0"^^xsd:integer.
                            
                            #inserir o anuncio
                            stand:a""",newID,""" a stand:Anuncio;
                                      stand:id '""",newID,"""'^^xsd:integer;
                                      stand:venda "naovendido";
                                      stand:preco '""",preco,"""'^^xsd:integer;
                                      stand:vendedor stand:""",resp,""";
                                      stand:marca stand:""",marca.replace(" ","").lower(),""";
                                      stand:modelo '""",modelo,"""';
                                      stand:cilindrada '""",cilindrada,"""'^^xsd:integer;
                                      stand:combustivel '""",combustivel,"""';
                                      stand:transmissao '""",transmissao,"""';
                                      stand:registo '""",registo,"""'^^xsd:integer;
                                      stand:mes '""",mes,"""';
                                      stand:estado '""",estado,"""';
                                      stand:potencia '""",potencia,"""'^^xsd:integer;
                                      stand:quilometros '""",quilometros,"""'^^xsd:integer;
                                      stand:numportas '""",numportas,"""'^^xsd:integer;
                                      stand:lotacao '""",lotacao,"""'^^xsd:integer;
                                      stand:imagem '""",newID,""".png';
                                      stand:descricao '""",descricao,"""' .
                        }
                    """]) #criar o novo anuncio
                    accessor.sparql_update(body={"update": input}, repo_name=repo_name)

            return redirect('/')
        else:
            form = ImageForm()
            return render(
                request,
                'criarAnuncio.html',
                {
                    'form': form,
                    'error': True
                }
            )
    else:
        form = ImageForm()
        return render(request, 'criarAnuncio.html', {'form': form, 'error': False})


def dados(request):
    return HttpResponse(open(STATIC_PATH + '/rdf/Anuncios_RDF.n3').read(), content_type='text')








