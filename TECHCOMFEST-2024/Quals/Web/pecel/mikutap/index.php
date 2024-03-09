<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
  <meta name="description" content="Versi khusus Hatsune Miku, interaktif dan buat musik sendiri dengan hanya menekan tombol keyboard.">
  <title>Mikutap</title>
  <link rel="apple-touch-icon" href="favicon.png">
  <link rel="shortcut icon" type="image/png" href="favicon.png"/>
  <link href="https://fonts.loli.net/css?family=Quicksand:400" rel="stylesheet">
  <link charset="UTF-8" href="shared/sp/css/common.css" rel="stylesheet">
  <link charset="utf-8" href="css/mikutap.css" rel="stylesheet">
  <script charset="utf-8" src="https://cdnjs.loli.net/ajax/libs/jquery/2.2.4/jquery.min.js" type="text/javascript"></script>
  <script charset="utf-8" src="https://cdnjs.loli.net/ajax/libs/pixi.js/3.0.11/pixi.min.js" type="text/javascript"></script>
  <script charset="utf-8" src="https://cdnjs.loli.net/ajax/libs/gsap/1.19.1/TweenMax.min.js" type="text/javascript"></script>
  <script charset="UTF-8" src="shared/js/common-2.min.js" type="text/javascript"></script>
  <script charset="utf-8" src="js/mikutap.min.js" type="text/javascript"></script>
</head>

<body>
  <div id="view"></div>
  <div id="scene_top">
    <h1>Relaksasi dengan Mikutap</h1>
    <div id="ng">
      <p class="atten">Maaf, <br>tetapi peramban Anda tidak mendukung persyaratan yang diperlukan oleh situs web ini!</p>
    </div>
    <div class="ok">
      <p id="bt_start"><a href=""><br>MULAI</a></p>
    </div>
    <p id="bt_about"><a href=""><br>-Info Tambahan-</a></p>
    <div class="ok">
      <p class="attention"><br>Nyalakan speaker atau pakai earphone dan nikmati musik dari Hatsune Miku</p>
    </div>
     <div class="ok">
     <p class="tit"><strong><br>Informasi lebih lanjut, hubungi: <a href="https://www.facebook.com/slytherinnn">Meoki</a><br> atau klik "Info Tambahan" di atas!</strong></p>
    </div>
  </div>
  <div id="scene_loading">
    <hr size="1" color="#fff"> </div>
  <div id="scene_main">
    <div class="set">
      <p class="attention">Klik &amp; seret mouse atau tekan tombol apa pun yang Anda sukai!</p>
      <p id="bt_backtrack"><a href="">MUSIK LATAR: Sedang aktif</a></p>
    </div>
  </div>
  <div id="about_cover"></div>
  <div id="about">
    <div id="about_in">
      <p class="close"><span id="bt_close">×</span></p>
      <p class="con"> Suara &amp; Suara <a href="https://ec.crypton.co.jp/pages/prod/vocaloid/mikuv4x" target="_blank">Hatsune Miku</a> </p>
      <p class="con"> Oleh <a href="https://aidn.jp" target="_blank">daniwell</a> (<a href="https://twitter.com/daniwell_aidn" target="_blank">Twitter</a>) </p>
      <p class="link"> Terinspirasi oleh <a href="http://patatap.com/" target="_blank">Patatap</a><br><br></p>
    </div>
  </div>
  <div id="bt_back">Balik, deh!</div>
  <div id="bt_fs">Belum, kan? Aktifkan layar penuh yuk!</div>
</body>

</html>
