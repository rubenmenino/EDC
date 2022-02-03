<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="hot_deals slider-items-products container">
            <div class="row">
                <div class="col-md-12">
                <xsl:for-each select="root/elem">
                    <xsl:variable name="carID">
                        <xsl:value-of select="id"/>
                    </xsl:variable>
                    <xsl:variable name="carURL">
                        <xsl:value-of select="concat('anuncio?id=',$carID)"/>
                    </xsl:variable>
                    <xsl:variable name="imageName">
                        <xsl:value-of select="imagem"/>
                    </xsl:variable>
                    <xsl:variable name="marcaName">
                        <xsl:value-of select="marca"/>
                    </xsl:variable>
                    <xsl:variable name="modeloName">
                        <xsl:value-of select="modelo"/>
                    </xsl:variable>
                    <div class="col-md-3" style="border: 4px solid #3E6274; border-radius:5px; margin-left:4%; margin-right:4%; margin-top:2%;">
                        <div class="item">
                            <div class="item-inner">
                                <div class="item-img">
                                    <a class="product-image">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="concat('anuncio?id=',$carID)"/>
                                        </xsl:attribute>
                                        <img>
                                            <xsl:attribute name="src">
                                                <xsl:value-of select="concat('static/products-images/',$imageName)"/>
                                            </xsl:attribute>
                                            <xsl:attribute name="width">
                                                <xsl:value-of select="concat('300px','')"/>
                                            </xsl:attribute>
                                            <xsl:attribute name="height">
                                                <xsl:value-of select="concat('200px','')"/>
                                            </xsl:attribute>
                                        </img>
                                    </a>
                                </div>
                                <div class="item-info">
                                    <div class="info-inner">
                                        <a>
                                            <xsl:attribute name="href">
                                                <xsl:value-of select="concat('anuncio?id=',$carID)"/>
                                            </xsl:attribute>
                                            <div class="item-title" style="text-transform: capitalize; font-size: 16px;">
                                                <xsl:value-of select="concat($marcaName,' ',$modeloName)"/>
                                            </div>
                                            <div class="item-price" style="text-transform: capitalize; font-size: 16px;"><xsl:value-of select="preco"/>€</div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </xsl:for-each>
                </div>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>