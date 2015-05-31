<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:strip-space elements="*"/>
    <xsl:output method="html" />
    <xsl:template match="/">
	<html>
		<head>
			<title>Corpus</title>
			<link rel="stylesheet" href="phonemise.css" />
		</head>
		<body>
				<xsl:copy>
					<xsl:apply-templates select="@*|node()"/>
				</xsl:copy>
		</body>
    </html>
    </xsl:template>
    
	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="mot">
		<xsl:copy select=".">
			<xsl:copy-of select="@*"/>
			<xsl:text> </xsl:text><xsl:value-of select="@phon"/>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>        