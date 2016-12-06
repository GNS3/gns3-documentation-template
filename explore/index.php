<?
   $headerStyle = 'welcome';
   include '../header.php'
?>

<div class="explore-header">
   <div class="headline">
      <div class="welcome-icon icon ion-ios-book-outline"></div>
      <div class="title">Explore Documentation</div>
      <div class="subtitle">The official guide and reference for GNS3</div>
      <div class="search-input">
         <div class="icon ion-android-search"></div>
         <input type="text" placeholder="Search Documentation">
      </div>
   </div>
</div>

<div class="explore-wrapper">
   <div class="explore-block">
      <div class="icon ion-ios-gear-outline"></div>
      <h1>Installation</h1>
      <a href="/article">Installation on Windows with a local server</a>
      <a href="/article">Installation on Windows with the GNS3 VM</a>
      <a href="/article">Installation on Mac OS X</a>
      <a href="/article">Installation on Linux</a>
      <a href="/article">Install on a remote server</a>
   </div>
   <div class="explore-block">
      <div class="icon ion-ios-bolt-outline"></div>
      <h1>Using GNS3</h1>
      <h2>Beginner</h2>
      <a href="#">Your first GNS3 topology</a>
      <a href="#">Your first Cisco GNS3 Topology</a>
      <a href="#">The GNS3 GUI</a>
      <a href="#">Change node symbol</a>
      <a href="#">GNS3 Styles</a>
      <a href="#">Connect GNS3 to the internet</a>
      <a href="#">Switching and GNS3</a>
      <div class="section-break"></div>
      <h2>Advanced</h2>
      <a href="#">GNS3 server configuration file</a>
      <a href="#">Running the GNS3 server as a daemon</a>
      <a href="#">Client server SSL encryption</a>
      <a href="#">Special IPs in GNS3</a>
   </div>
   <div class="explore-block">
      <div class="icon ion-ios-analytics-outline"></div>
      <h1>Emulators</h1>
      <a href="#">Which emulator shoud I use?</a>
      <a href="#">Dynamips</a>
      <a href="#">VMWare</a>
      <a href="#">Docker</a>
   </div>
</div>

<? include '../footer.php' ?>
