<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="hot_deals slider-items-products container">
            <div class="row" style="margin: 2%;">
                <xsl:for-each select="root/elem/anuncio">
                <div class="col-md-12">
                    <xsl:variable name="carID">
                        <xsl:value-of select="id"/>
                    </xsl:variable>
                    <xsl:variable name="imageName">
                        <xsl:value-of select="imagens/imagem"/>
                    </xsl:variable>
                    <xsl:variable name="vendaName">
                        <xsl:value-of select="venda"/>
                    </xsl:variable>
                    <xsl:variable name="marcaName">
                        <xsl:value-of select="marca"/>
                    </xsl:variable>
                    <xsl:variable name="modeloName">
                        <xsl:value-of select="modelo"/>
                    </xsl:variable>
                    <div class="col-md-5" style="margin-left:4%; margin-right:4%;">
                        <div class="row">
                            <img style="display: block;margin-left: auto;margin-right: auto; max-width: 100%; max-height: 100%">
                                <xsl:attribute name="src">
                                    <xsl:value-of select="concat('../static/products-images/',$imageName)"/>
                                </xsl:attribute>
                            </img>
                        </div>
                        <div class="row" style="text-align:left;margin:30px;">
                            <p style="font-size:30px; color:black; text-align:left; text-transform: capitalize;"><xsl:value-of select="concat($marcaName,' ',$modeloName)"/></p>
                        </div>
                        <div class="row" style="text-align:left;margin:30px;">
                            <p style="font-size:40px; color:darkred; display: inline; padding: 20px 25px 0px 0px"><xsl:value-of select="preco"/>€</p>

                            <input type="hidden" id="carID" name="carID" value="{$carID}"/>
                            <a>
                                <input id="Comprar" name="Comprar" type="submit" value="Comprar" style="opacity:0.8;background-color:green;color:white;font-size:18px;font-weight: 600; margin-left:10px;"/>
                            </a>
                            <a>
                                <input id="Apagar" name="Apagar" type="submit" value="Apagar" style="opacity:0.8; background-color:darkred;color:white;font-size:18px;font-weight: 600; margin-left:10px;"/>
                            </a>
                        </div>
                        <div style="margin-left:30px">
                        <h2 style="color: #3E6274; font-weight:700">Dados do vendedor:</h2>
                        <span style="font-weight:600; font-size:18px; margin-bottom:5px;">Nome: </span><span style="font-size:18px;"><xsl:value-of select="nome"/></span>
                        <br/><span style="font-weight:600; font-size:18px; margin-bottom:5px;">Email: </span><span style="font-size:18px;"><xsl:value-of select="email"/></span>
                        <br/><span style="font-weight:600; font-size:18px; margin-bottom:5px;">Contacto Telefónico (+351): </span><span style="font-size:18px;"><xsl:value-of select="contacto"/></span>
                        </div>
                    </div>
                    <div class="col-md-5" style="margin-left:4%; margin-right:4%;">
                        <h2 style="color: #3E6274; font-weight:700">Mais informações:</h2>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <xsl:choose>
                                <xsl:when test="$vendaName = 'naovendido'">
                                    <span style="font-weight:600; font-size:18px;">Estado de Venda: </span><span style="font-size:18px;">Não Vendido</span>
                                </xsl:when>
                                <xsl:otherwise>
                                    <span style="font-weight:600; font-size:18px;">Estado de Venda: </span><span style="font-size:18px;">Vendido</span>
                                </xsl:otherwise>
                            </xsl:choose>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Combustivel: </span><span style="font-size:18px;"> <xsl:value-of select="combustivel"/></span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Cilindrada: </span><span style="font-size:18px;"> <xsl:value-of select="cilindrada"/>cc</span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Tipo de transmissão: </span><span style="font-size:18px;"> <xsl:value-of select="transmissao"/></span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Ano e mês de registo: </span><span style="font-size:18px;"> <xsl:value-of select="mes"/> de <xsl:value-of select="registo"/></span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Estado do automovel: </span><span style="font-size:18px;"> <xsl:value-of select="estado"/></span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Potencia: </span><span style="font-size:18px;"> <xsl:value-of select="potencia"/>cv</span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Quilometros: </span><span style="font-size:18px;"> <xsl:value-of select="quilometros"/>km</span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px;">Número de portas: </span><span style="font-size:18px;"> <xsl:value-of select="numportas"/></span>
                        </div>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <span style="font-weight:600; font-size:18px; ">Lotação: </span><span style="font-size:18px;"> <xsl:value-of select="lotacao"/></span>
                        </div>
                        <br/>
                        <br/>
                        <div style="display:inline-block; margin-bottom:10px;">
                            <p style="font-weight:600; font-size:18px; ">Descrição do Vendedor: </p>
                            <span style="font-size:18px;"> <xsl:value-of select="descricao"/></span>
                        </div>
                        <br/>
                    </div>
                </div>
                </xsl:for-each>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>