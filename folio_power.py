def svg_power():
    return """
<svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">

  <style>
    .t{font-family:Arial,Helvetica,sans-serif; fill:#111;}
    .title{font-size:22px; font-weight:bold;}
    .sub{font-size:12px;}
    .txt{font-size:12px;}
    .tiny{font-size:10px;}
    .wire{stroke:#111; stroke-width:2; fill:none;}
    .thin{stroke:#dddddd; stroke-width:1; fill:none; stroke-dasharray:4 4;}
    .box{stroke:#111; stroke-width:1.4; fill:none;}
  </style>

  <!-- Cadre -->
  <rect x="20" y="20" width="1160" height="660" class="box"/>

  <!-- Titre -->
  <text x="40" y="50" class="t title">Folio 10 - Puissance</text>
  <text x="40" y="78" class="t sub">COFFRET TYPE FROID MONO-VENTIL</text>
  <text x="980" y="78" class="t sub">Schéma de puissance</text>

  <!-- Grille -->
  <g class="thin">
    <line x1="80" y1="100" x2="80" y2="620"/>
    <line x1="180" y1="100" x2="180" y2="620"/>
    <line x1="280" y1="100" x2="280" y2="620"/>
    <line x1="380" y1="100" x2="380" y2="620"/>
    <line x1="480" y1="100" x2="480" y2="620"/>
    <line x1="580" y1="100" x2="580" y2="620"/>
    <line x1="680" y1="100" x2="680" y2="620"/>
    <line x1="780" y1="100" x2="780" y2="620"/>
    <line x1="880" y1="100" x2="880" y2="620"/>
    <line x1="980" y1="100" x2="980" y2="620"/>
    <line x1="1080" y1="100" x2="1080" y2="620"/>

    <line x1="40" y1="120" x2="1140" y2="120"/>
    <line x1="40" y1="220" x2="1140" y2="220"/>
    <line x1="40" y1="320" x2="1140" y2="320"/>
    <line x1="40" y1="420" x2="1140" y2="420"/>
    <line x1="40" y1="520" x2="1140" y2="520"/>
  </g>

  <!-- ===================================================== -->
  <!-- DEPART CIRCULATEUR -->
  <!-- ===================================================== -->
  <text x="95" y="110" class="t tiny">L1</text>
  <text x="117" y="110" class="t tiny">L2</text>
  <text x="139" y="110" class="t tiny">L3</text>
  <text x="84" y="132" class="t txt">M1 Circulateur</text>

  <!-- fils principaux -->
  <line x1="100" y1="145" x2="100" y2="520" class="wire"/>
  <line x1="122" y1="145" x2="122" y2="520" class="wire"/>
  <line x1="144" y1="145" x2="144" y2="520" class="wire"/>

  <!-- repères fils -->
  <text x="88" y="160" class="t tiny">1</text>
  <text x="110" y="160" class="t tiny">2</text>
  <text x="132" y="160" class="t tiny">3</text>

  <!-- IG1 -->
  <rect x="92" y="170" width="60" height="24" class="box"/>
  <text x="110" y="186" class="t txt">IG1</text>

  <!-- Q1 -->
  <rect x="92" y="220" width="60" height="24" class="box"/>
  <text x="114" y="236" class="t txt">Q1</text>

  <!-- DM1 -->
  <rect x="92" y="270" width="60" height="24" class="box"/>
  <text x="107" y="286" class="t txt">DM1</text>

  <!-- contact puissance KM1 -->
  <rect x="92" y="330" width="60" height="24" class="box"/>
  <text x="107" y="346" class="t txt">KM1</text>
  <text x="165" y="346" class="t tiny">contact puissance</text>

  <!-- renvoi vers commande -->
  <text x="165" y="364" class="t tiny">→ 11 KM1 A1/A2</text>

  <!-- liaisons vers moteur -->
  <line x1="100" y1="354" x2="100" y2="392" class="wire"/>
  <line x1="122" y1="354" x2="122" y2="392" class="wire"/>
  <line x1="144" y1="354" x2="144" y2="392" class="wire"/>

  <line x1="100" y1="430" x2="100" y2="520" class="wire"/>
  <line x1="122" y1="430" x2="122" y2="520" class="wire"/>
  <line x1="144" y1="430" x2="144" y2="520" class="wire"/>

  <!-- moteur -->
  <line x1="100" y1="392" x2="110" y2="392" class="wire"/>
  <line x1="144" y1="392" x2="134" y2="392" class="wire"/>
  <line x1="100" y1="430" x2="110" y2="430" class="wire"/>
  <line x1="144" y1="430" x2="134" y2="430" class="wire"/>

  <circle cx="122" cy="411" r="19" class="box"/>
  <text x="116" y="416" class="t txt">M</text>
  <text x="165" y="416" class="t txt">M1</text>

  <!-- ===================================================== -->
  <!-- ALIMENTATION MXPRO -->
  <!-- ===================================================== -->
  <text x="340" y="132" class="t txt">Alimentation A1 MXPRO</text>
  <text x="350" y="110" class="t tiny">L</text>
  <text x="372" y="110" class="t tiny">N</text>

  <line x1="360" y1="145" x2="360" y2="250" class="wire"/>
  <line x1="382" y1="145" x2="382" y2="250" class="wire"/>

  <text x="348" y="
