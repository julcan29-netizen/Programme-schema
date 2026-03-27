def svg_power():
    return """
<svg width="1200" height="720" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">

  <style>
    .t{font-family:Arial,Helvetica,sans-serif; fill:#111;}
    .title{font-size:22px; font-weight:bold;}
    .sub{font-size:12px;}
    .txt{font-size:12px;}
    .tiny{font-size:10px;}
    .wire{stroke:#111; stroke-width:2; fill:none;}
    .thin{stroke:#999; stroke-width:1; fill:none; stroke-dasharray:4 4;}
    .box{stroke:#111; stroke-width:1.4; fill:none;}
  </style>

  <!-- Cadre -->
  <rect x="20" y="20" width="1160" height="680" class="box"/>

  <!-- Titre -->
  <text x="40" y="50" class="t title">Folio 10 - Puissance</text>
  <text x="40" y="78" class="t sub">COFFRET TYPE FROID MONO-VENTIL</text>

  <!-- Grille légère -->
  <g class="thin">
    <line x1="80" y1="100" x2="80" y2="640"/>
    <line x1="180" y1="100" x2="180" y2="640"/>
    <line x1="280" y1="100" x2="280" y2="640"/>
    <line x1="380" y1="100" x2="380" y2="640"/>
    <line x1="480" y1="100" x2="480" y2="640"/>
    <line x1="580" y1="100" x2="580" y2="640"/>
    <line x1="680" y1="100" x2="680" y2="640"/>
    <line x1="780" y1="100" x2="780" y2="640"/>
    <line x1="880" y1="100" x2="880" y2="640"/>
    <line x1="980" y1="100" x2="980" y2="640"/>
    <line x1="1080" y1="100" x2="1080" y2="640"/>

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

  <!-- renvoi vers bobine KM1 -->
  <text x="165" y="364" class="t tiny">→ 11 KM1 A1/A2</text>

  <!-- moteur sans fils traversants -->
  <line x1="100" y1="354" x2="100" y2="392" class="wire"/>
  <line x1="122" y1="354" x2="122" y2="392" class="wire"/>
  <line x1="144" y1="354" x2="144" y2="392" class="wire"/>

  <line x1="100" y1="430" x2="100" y2="520" class="wire"/>
  <line x1="122" y1="430" x2="122" y2="520" class="wire"/>
  <line x1="144" y1="430" x2="144" y2="520" class="wire"/>

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

  <text x="348" y="160" class="t tiny">10</text>
  <text x="370" y="160" class="t tiny">11</text>

  <rect x="348" y="180" width="46" height="24" class="box"/>
  <text x="360" y="196" class="t txt">Q3</text>

  <rect x="344" y="250" width="54" height="26" class="box"/>
  <text x="352" y="268" class="t txt">A1</text>

  <!-- renvoi vers folio commande -->
  <text x="408" y="262" class="t tiny">→ 11 A1 alim</text>

  <!-- ===================================================== -->
  <!-- TRANSFORMATEUR T1 -->
  <!-- ===================================================== -->
  <text x="540" y="132" class="t txt">Transformateur T1</text>
  <text x="548" y="110" class="t tiny">230V</text>
  <text x="612" y="110" class="t tiny">24V</text>

  <!-- primaire -->
  <line x1="560" y1="145" x2="560" y2="175" class="wire"/>
  <line x1="586" y1="145" x2="586" y2="175" class="wire"/>
  <text x="548" y="160" class="t tiny">20</text>
  <text x="574" y="160" class="t tiny">21</text>

  <!-- symbole -->
  <circle cx="556" cy="194" r="8" class="box"/>
  <circle cx="572" cy="194" r="8" class="box"/>
  <circle cx="600" cy="194" r="8" class="box"/>
  <circle cx="616" cy="194" r="8" class="box"/>
  <text x="636" y="198" class="t txt">T1</text>

  <!-- secondaire -->
  <line x1="600" y1="202" x2="600" y2="245" class="wire"/>
  <line x1="616" y1="202" x2="616" y2="245" class="wire"/>
  <text x="592" y="238" class="t tiny">30</text>
  <text x="608" y="238" class="t tiny">31</text>
  <text x="624" y="248" class="t tiny">24V / N</text>

  <!-- renvoi commande -->
  <text x="624" y="266" class="t tiny">→ 11 alim commande</text>

  <!-- ===================================================== -->
  <!-- ALIMENTATION ACTIONNEUR VANNE -->
  <!-- ===================================================== -->
  <text x="815" y="132" class="t txt">Alim actionneur YV1</text>
  <text x="832" y="110" class="t tiny">24V</text>
  <text x="856" y="110" class="t tiny">N</text>

  <line x1="840" y1="145" x2="840" y2="180" class="wire"/>
  <line x1="862" y1="145" x2="862" y2="180" class="wire"/>

  <text x="832" y="160" class="t tiny">40</text>
  <text x="854" y="160" class="t tiny">41</text>

  <rect x="834" y="180" width="34" height="22" class="box"/>
  <text x="842" y="196" class="t txt">PS1</text>

  <line x1="851" y1="202" x2="851" y2="290" class="wire"/>

  <rect x="842" y="290" width="18" height="30" class="box"/>
  <text x="875" y="308" class="t txt">YV1</text>
  <text x="875" y="324" class="t txt">Vanne 3 voies</text>

  <!-- renvois signal commande -->
  <text x="875" y="342" class="t tiny">AO+ / AO- ← 11 A1</text>

  <!-- bornier visible sur liaisons terrain -->
  <text x="875" y="360" class="t tiny">X1.9 / X1.10</text>

  <!-- Cartouche -->
  <rect x="20" y="650" width="1160" height="30" class="box"/>
  <line x1="1085" y1="650" x2="1085" y2="680" class="wire"/>
  <text x="30" y="670" class="t txt">Folio puissance</text>
  <text x="1100" y="670" class="t txt">10</text>

</svg>
"""
