<?xml version="1.0"?>
<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tet="http://www.pdflib.com/XML/TET5/TET-5.0">
    <xsl:output method="text" encoding="utf-8"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="/">
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="tet:TET/tet:Document/tet:DocInfo"/>
        <xsl:apply-templates select="tet:TET/tet:Document"/>
        <xsl:apply-templates select="tet:TET/tet:Creation"/>
        <xsl:apply-templates select="tet:TET/tet:Document/tet:Pages"/>
        <xsl:text>}</xsl:text>
    </xsl:template>
    <xsl:template match="tet:TET/tet:Document/tet:DocInfo">
        <xsl:text>"author":"</xsl:text>
        <xsl:value-of select="tet:Author/text()"/>
        <xsl:text>"</xsl:text>
        <xsl:text>,"created":"</xsl:text>
        <xsl:value-of select="tet:CreationDate/text()"/>
        <xsl:text>"</xsl:text>
    </xsl:template>
    <xsl:template match="tet:TET/tet:Creation">
        <xsl:text>,"processed":"</xsl:text>
        <xsl:value-of select="@date"/>
        <xsl:text>"</xsl:text>
    </xsl:template>
    <xsl:template match="tet:TET/tet:Document">
        <xsl:text>,"file_name":"</xsl:text>
        <xsl:value-of select="@filename"/>
        <xsl:text>"</xsl:text>
        <xsl:text>,"page_count":</xsl:text>
        <xsl:value-of select="@pageCount"/>
        <xsl:text>,"file_size":</xsl:text>
        <xsl:value-of select="@filesize"/>
    </xsl:template>
    <xsl:template match="tet:TET/tet:Document/tet:Pages">
        <xsl:text>,"pages":[</xsl:text>
        <xsl:for-each select="tet:Page">
            <xsl:text>{</xsl:text>
            <xsl:text>"attributes":{</xsl:text>
            <xsl:text>"number":</xsl:text>
            <xsl:value-of select="@number"/>
            <xsl:text>,"width":</xsl:text>
            <xsl:value-of select="@width"/>
            <xsl:text>,"height":</xsl:text>
            <xsl:value-of select="@height"/>
            <xsl:text>,"granularity":"</xsl:text>
            <xsl:value-of select="tet:Content/@granularity"/>
            <xsl:text>"</xsl:text>
            <xsl:text>,"dehyphenation":</xsl:text>
            <xsl:value-of select="tet:Content/@dehyphenation"/>
            <xsl:text>,"dropcap":</xsl:text>
            <xsl:value-of select="tet:Content/@dropcap"/>
            <!-- TODO: other Content attributes and values to be injected here -->
            <xsl:text>}</xsl:text>
            <xsl:text>,"lines":[</xsl:text>
            <xsl:for-each select="tet:Content/tet:Para/tet:Box/tet:Line">
                <xsl:text>"</xsl:text>
                <xsl:value-of select="normalize-space(tet:Text/text())"/>
                <xsl:text>"</xsl:text>
                <xsl:if test="position() != last()">
                    <xsl:text>,</xsl:text>
                </xsl:if>
                <xsl:if test="position() = last()">
                    <xsl:text>]</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]</xsl:text>
    </xsl:template>
</xsl:stylesheet>
