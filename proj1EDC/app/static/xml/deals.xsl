<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <section class=" wow bounceInUp animated">
          <div class="hot_deals slider-items-products container">
            <div class="new_title">
              <h2>Carros Premium Disponiveis</h2>
              <div class="box-timer">
                <div class="countbox_1 timer-grid"></div>
              </div>
            </div>
              <div id="hot_deals" class="product-flexslider hidden-buttons">
                  <div class="slider-items slider-width-col4 products-grid" style="height:100%">
                  <xsl:for-each select="root/elem">
                      <xsl:variable name="carID">
                          <xsl:value-of select="id"/>
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
                      <xsl:variable name="precoName">
                          <xsl:value-of select="preco"/>
                      </xsl:variable>
                      <xsl:variable name="quilometrosName">
                          <xsl:value-of select="quilometros"/>
                      </xsl:variable>
                    <div class="item">
                      <div class="item-inner">
                        <div class="item-img">
                          <div class="item-img-info">
                              <a class="product-image" style="margin-top:5%">
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
                        </div>
                        <div class="item-info">
                            <div class="info-inner">
                                <div class="item-title">
                                    <a style="text-transform: capitalize">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="concat('anuncio?id=',$carID)"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="concat($marcaName,' ',$modeloName)"/>
                                    </a>
                                </div>
                                <div class="item-content">
                                  <div class="item-price">
                                    <div class="price-box"><span class="regular-price"><span class="price"><xsl:value-of select="concat($precoName,'€')"/></span> </span> </div>
                                  </div>
                                  <div class="other-info" style="padding-bottom:30px">
                                    <div class="col-km"><xsl:value-of select="concat($quilometrosName,'km')"/></div>
                                    <div class="col-engine"><xsl:value-of select="transmissao"/></div>
                                    <div class="col-date"><xsl:value-of select="registo"/></div>
                                  </div>
                                </div>
                            </div>
                        </div>
                      </div>
                    </div>
                  </xsl:for-each>
                </div>
              </div>
          </div>
        </section>
    </xsl:template>
</xsl:stylesheet>