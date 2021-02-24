import os
from BaseXClient import BaseXClient
from lxml import etree
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from proj1EDC.settings import BASE_DIR
from .feed.news.news import *
import xmltodict
import xml.etree.ElementTree as ET
from .forms import ImageForm
import sqlite3


STATIC_PATH = os.path.join(BASE_DIR, "app", "static")
XML_PATH = os.path.join(STATIC_PATH, "xml")
ANUNCIOS_XSLT_FILE_PATH = os.path.join(XML_PATH, "anuncios.xsl")
DEALS_XSLT_FILE_PATH = os.path.join(XML_PATH, "deals.xsl")
ITEMCAR_XSLT_FILE_PATH = os.path.join(XML_PATH, "itemcar.xsl")

# Create your views here.

def index(request):
    #marca = []
    try:

        ########################################################################################
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        #input = "<root> { for $a in collection('Anuncios')//anuncio return <elem> {$a/id} {$a/imagens/imagem} {$a/marca} {$a/modelo} {$a/preco} </elem>} </root>"
        #query = session.query(input)

        #res = query.execute()
        #print(res)
        #xml_file = etree.fromstring(res)

        #xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
        #transform = etree.XSLT(xslt_file)
        #html = transform(xml_file)

        ########################################################################################

        inputDeals = "let $tmp:=(for $d in collection('anuncios')//anuncio where $d/venda = 'naovendido' order by number($d/preco) descending return $d )\
                        return <root>{ let $b := $tmp[position()<7] for $f in $b return <elem> {$f/id} {$f/marca} {$f/modelo} {$f/preco} {$f/registo} {$f/transmissao} {$f/quilometros} {$f/imagens/imagem} </elem> }</root>"
        queryDeals = session.query(inputDeals)

        resDeals = queryDeals.execute()
        #print(resDeals)
        xml_fileDeals = etree.fromstring(resDeals)

        xslt_fileDeals = etree.parse(DEALS_XSLT_FILE_PATH)
        transform = etree.XSLT(xslt_fileDeals)
        deals = transform(xml_fileDeals)
        ########################################################################################
        input1 = "<root> { for $d in distinct-values(doc('anuncios')//marca) return <elem> {$d} </elem>} </root>"
        query1 = session.query(input1)
        res1 = query1.execute()
        #print(res2)

        xml_string1 = res1

        root1 = ET.fromstring(xml_string1)
        marcas = [node.text.strip() for node in root1]


        #print(marcas)
        ########################################################################################
        input2 = "<root> { for $d in distinct-values(doc('anuncios')//modelo) return <elem> {$d} </elem>} </root>"
        query2 = session.query(input2)
        res2 = query2.execute()
        #print(res2)

        xml_string2 = res2

        root2 = ET.fromstring(xml_string2)
        modelos = [node.text.strip() for node in root2]
        #print(modelos)

        ########################################################################################
        input3 = "<root> { for $d in distinct-values(doc('anuncios')//combustivel) return <elem> {$d} </elem>} </root>"
        query3 = session.query(input3)
        res3 = query3.execute()
        # print(res2)

        xml_string3 = res3

        root3 = ET.fromstring(xml_string3)
        combustivel = [node.text.strip() for node in root3]
        #print(combustivel)

        ########################################################################################
        input4 = "<root> { for $d in distinct-values(doc('anuncios')//preco) return <elem> {$d} </elem>} </root>"
        query4 = session.query(input4)
        res4 = query4.execute()
        # print(res2)

        xml_string4 = res4

        root4 = ET.fromstring(xml_string4)
        preços = [node.text.strip() for node in root4]
        #print(preços)

        ########################################################################################
        input5 = "<root> { for $d in distinct-values(doc('anuncios')//registo) order by $d return <elem> {$d} </elem>} </root>"
        query5 = session.query(input5)
        res5 = query5.execute()
        # print(res2)

        xml_string5 = res5

        root5 = ET.fromstring(xml_string5)
        registo = ([node.text.strip() for node in root5])

        #print(registo)

        ########################################################################################
        input6 = "<root> { for $d in distinct-values(doc('anuncios')//kilometros) return <elem> {$d} </elem>} </root>"
        query6 = session.query(input6)
        res6 = query4.execute()
        # print(res2)

        xml_string6 = res6

        root6 = ET.fromstring(xml_string6)
        kilometros = [node.text.strip() for node in root6]
        #print(kilometros)

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
        #print(str(selectedmarca))
        #print(str(selectedmodelo))
        #print(str(selectedcombustivel))
        #print(str(selectedquilometros))
        #print(str(selectedregisto))
        #print(str(selectedpreco))

        if not selectedquilometros:
            selectedquilometros = 1000000000
        if not selectedpreco:
            selectedpreco = 1000000000
        if not selectedregisto:
            selectedregisto = 1900

        if selectedmarca:
            if selectedmodelo:
                if selectedcombustivel:

                    input = "<root> { for $d in collection('anuncios')//anuncio where $d/marca=\"" + str(
                        selectedmarca).lower() + "\" and $d/modelo =\"" + str(
                        selectedmodelo).lower() + "\" and $d/combustivel =\"" + str(
                        selectedcombustivel).lower() + "\" and $d/preco <" + str(selectedpreco) + " and $d/quilometros <" + str(
                        selectedquilometros) + " and $d/registo >" + str(
                        selectedregisto) + " return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                    query = session.query(str(input))

                    res = query.execute()
                    xml_file = etree.fromstring(res)

                    xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                    transform = etree.XSLT(xslt_file)
                    html = transform(xml_file)

                else:

                    input = "<root> { for $d in collection('anuncios')//anuncio where $d/marca=\"" + str(
                        selectedmarca).lower() + "\" and $d/modelo =\"" + str(selectedmodelo).lower() + "\" and $d/preco <" + str(
                        selectedpreco) + " and $d/quilometros <" + str(selectedquilometros) + " and $d/registo >" + str(
                        selectedregisto) + " return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                    query = session.query(input)

                    res = query.execute()
                    # print(res)
                    xml_file = etree.fromstring(res)

                    xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                    transform = etree.XSLT(xslt_file)
                    html = transform(xml_file)

            elif selectedcombustivel:
                input = "<root> { for $d in collection('anuncios')//anuncio where $d/marca=\"" + str(
                    selectedmarca).lower() + "\" 8and $d/combustivel=\"" + str(selectedcombustivel).lower() + "\" and $d/preco <" + str(
                    selectedpreco) + " and $d/quilometros <" + str(selectedquilometros) + " and $d/registo >" + str(
                    selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                query = session.query(input)

                res = query.execute()
                # print(res)
                xml_file = etree.fromstring(res)

                xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                transform = etree.XSLT(xslt_file)
                html = transform(xml_file)

            else:

                input = "<root> { for $d in collection('anuncios')//anuncio where $d/marca=\"" + str(
                    selectedmarca).lower() + "\" and $d/preco <" + str(selectedpreco) + " and $d/quilometros <" + str(
                    selectedquilometros) + " and $d/registo >" + str(
                    selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                query = session.query(input)

                res = query.execute()
                # print(res)
                xml_file = etree.fromstring(res)

                xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                transform = etree.XSLT(xslt_file)
                html = transform(xml_file)

        elif selectedmodelo:
            if selectedcombustivel:
                input = "<root> { for $d in collection('anuncios')//anuncio where $d/modelo=\"" + str(
                    selectedmodelo).lower() + "\" and $d/combustivel=\"" + str(selectedcombustivel).lower() + "\" and $d/preco <" + str(
                    selectedpreco) + " and $d/quilometros <" + str(selectedquilometros) + " and $d/registo >" + str(
                    selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                query = session.query(input)

                res = query.execute()
                # print(res)
                xml_file = etree.fromstring(res)

                xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                transform = etree.XSLT(xslt_file)
                html = transform(xml_file)

            else:
                input = "<root> { for $d in collection('anuncios')//anuncio where $d/modelo=\"" + str(
                    selectedmodelo).lower() + "\" and $d/preco <" + str(selectedpreco) + " and $d/quilometros <" + str(
                    selectedquilometros) + " and $d/registo >" + str(
                    selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
                query = session.query(input)

                res = query.execute()
                # print(res)
                xml_file = etree.fromstring(res)

                xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
                transform = etree.XSLT(xslt_file)
                html = transform(xml_file)

        elif selectedcombustivel:
            input = "<root> { for $d in collection('anuncios')//anuncio where $d/combustivel=\"" + str(
                selectedcombustivel).lower() + "\" and $d/preco <" + str(selectedpreco) + " and $d/quilometros <" + str(
                selectedquilometros) + " and $d/registo >" + str(
                selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
            query = session.query(input)

            res = query.execute()
            # print(res)
            xml_file = etree.fromstring(res)

            xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
            transform = etree.XSLT(xslt_file)
            html = transform(xml_file)

        else:
            input = "<root> { for $d in collection('anuncios')//anuncio where $d/preco <" + str(
                selectedpreco) + " and $d/quilometros <" + str(selectedquilometros) + " and $d/registo >" + str(
                selectedregisto) + "  return <elem> {$d/id} {$d/preco} {$d/imagens/imagem} {$d/modelo} {$d/marca} </elem>} </root>"
            query = session.query(input)

            res = query.execute()
            # print(res)
            xml_file = etree.fromstring(res)

            xslt_file = etree.parse(ANUNCIOS_XSLT_FILE_PATH)
            transform = etree.XSLT(xslt_file)
            html = transform(xml_file)


        context = {
            "content": html,
            "deals": deals,
            "news": getNews(3),
            "marcas": marcas,
            "modelos": modelos,
            "combustivel": combustivel,
            "preços": preços,
            "registo": registo,
            "kilometros" : kilometros
        }

        query.close()
    finally:
        if session:
            session.close()

    return render(request, 'index.html', context)

def anuncio(request):
    assert isinstance(request, HttpRequest)
    id = ""
    try:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

        if 'carID' in request.POST and 'Apagar' in request.POST:
            id = request.POST['carID']
            print(id)

            inputDelete = "for $d in collection('anuncios')//anuncio where $d/id='"+id+"' return delete node $d"
            queryDelete = session.query(inputDelete)
            print(queryDelete)
            queryDelete.execute()

            os.remove(STATIC_PATH + '/products-images/'+id+'.png')

            return redirect('/')
        else:
            if 'carID' in request.POST and 'Comprar' in request.POST:
                id = request.POST['carID']
                print(id)

                inputUpdate = "for $d in collection('anuncios')//anuncio where $d/id='"+id+"' \
                                return replace node $d/venda/text() with 'vendido'"
                queryUpdate = session.query(inputUpdate)
                print(queryUpdate)
                queryUpdate.execute()

            else:
                id = request.GET['id']

            input = "<root> { for $a in collection('anuncios')//anuncio where $a/id ='"+ id +"' return <elem> {$a} </elem> } </root>"
            query = session.query(input)

            res = query.execute()
            xml_file = etree.fromstring(res)

            xslt_file = etree.parse(ITEMCAR_XSLT_FILE_PATH)
            transform = etree.XSLT(xslt_file)
            html = transform(xml_file)

    finally:
        if session:
            session.close()

    tparams = {
        'info': html
    }
    return render(request, 'itemCar.html', tparams)

context = { "content": ""}
def criaranuncio(request):
    global context;
    res = None
    assert isinstance(request, HttpRequest)


    if 'nome' in request.POST and 'email' in request.POST and 'contacto' in request.POST and 'marca' in request.POST and 'modelo' in request.POST and 'cilindrada' in request.POST and 'transmissao' in request.POST and 'registo' in request.POST and 'mes' in request.POST and 'estado' in request.POST and 'potencia' in request.POST and 'quilometros' in request.POST and 'numportas' in request.POST and 'lotacao' in request.POST and 'preco' in request.POST and 'descricao' in request.POST:
        try:
            session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
            input = "let $i := (for $id in collection('anuncios')//anuncio return sum($id/id)) return $i[last()]+1"
            query = session.query(input)

            res = query.execute()
        finally:
            if session:
                session.close()


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

            try:
                session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

                test1 = "copy $c:= collection('anuncios') modify (let $d := $c//anuncio[last()] \
                                        return insert nodes ( \
                                        <anuncio> \
                                            <id>" + str(res) + "</id>\
                                            <venda>naovendido</venda> \
                                            <preco>" + str(preco) + "</preco> \
                                            <nome>" + str(nome) + "</nome>\
                                            <contacto>" + str(contacto) + "</contacto>\
                                            <email>" + str(email) + "</email>\
                                            <marca>" + str(marca).lower() + "</marca>\
                                            <modelo>" + str(modelo).lower() + "</modelo>\
                                            <cilindrada>" + str(cilindrada) + "</cilindrada>\
                                            <combustivel>" + str(combustivel) + "</combustivel>\
                                            <transmissao>" + str(transmissao) + "</transmissao>\
                                            <registo>" + str(registo) + "</registo>\
                                            <mes>" + str(mes) + "</mes>\
                                            <estado>" + str(estado) + "</estado>\
                                            <potencia>" + str(potencia) + "</potencia>\
                                            <quilometros>" + str(quilometros) + "</quilometros>\
                                            <numportas>" + str(numportas) + "</numportas>\
                                            <lotacao>" + str(lotacao) + "</lotacao>\
                                            <imagens><imagem>" + str(res) + ".png</imagem></imagens>\
                                            <descricao>" + str(descricao) + "</descricao>\
                                              </anuncio>\
                                            ) after $d ) return $c"

                query2 = session.query(test1)

                res2 = query2.execute()

                xml_file = etree.fromstring(res2)
                xsd_tree = etree.parse(XML_PATH + '/anuncios.xsd')

                xds_schema = etree.XMLSchema(xsd_tree)

                if xds_schema.validate(xml_file):

                    if form.is_valid():
                        try:
                            form.save()
                        except sqlite3.OperationalError:
                            pass

                    input = "let $d := doc('anuncios')//anuncio[last()] \
                            return insert nodes ( \
                            <anuncio> \
                                <id>"+ str(res) +"</id>\
                                <venda>naovendido</venda> \
                                <preco>"+ str(preco) +"</preco> \
                                <nome>"+ str(nome) +"</nome>\
                                <contacto>"+ str(contacto) +"</contacto>\
                                <email>"+ str(email) +"</email>\
                                <marca>"+ str(marca).lower() +"</marca>\
                                <modelo>"+ str(modelo).lower() +"</modelo>\
                                <cilindrada>"+ str(cilindrada) +"</cilindrada>\
                                <combustivel>"+ str(combustivel) +"</combustivel>\
                                <transmissao>"+ str(transmissao) +"</transmissao>\
                                <registo>"+ str(registo) +"</registo>\
                                <mes>"+ str(mes) +"</mes>\
                                <estado>"+ str(estado) +"</estado>\
                                <potencia>"+ str(potencia) +"</potencia>\
                                <quilometros>"+ str(quilometros) +"</quilometros>\
                                <numportas>"+ str(numportas) +"</numportas>\
                                <lotacao>"+ str(lotacao) +"</lotacao>\
                                <imagens><imagem>"+str(res)+".png</imagem></imagens>\
                                <descricao>"+ str(descricao) +"</descricao>\
                                  </anuncio>\
                                ) after $d"
                    query = session.query(input)

                    res = query.execute()

                else:
                    return render(
                        request,
                        'criarAnuncio.html',
                        {
                            'form': form,
                            'error': True
                        }
                    )

            finally:
                if session:
                    session.close()

            return redirect('/')
        else:
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


''' def authenticate(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'authenticate.html', {'error_message': 'Invalid login'})
    return render(request, 'authenticate.html')
'''

def dados(request):
    return HttpResponse(open('app/static/xml/anuncios.xml').read(), content_type='text/xml')




