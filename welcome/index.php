<div class="welcome-splash">
   <div id="welcome-particles"></div>
   <div class="welcome-headline">
      <div class="welcome-icon icon ion-ios-book-outline"></div>
      <div class="title">Documentation</div>
      <div class="subtitle">The official guide and reference for GNS3</div>
      <div class="search-input">
         <div class="icon ion-android-search"></div>
         <input type="text" placeholder="Search Documentation">
      </div>
   </div>
</div>
<div class="welcome-container">
   <div class="welcome-wrapper">
      <div class="welcome-title">
         <div class="title">Explore Documentation</div>
         <div class="date">Last Updated Dec 1, 2016</div>
      </div>
      <a href="/explore" class="welcome-tile">
         <span class="icon ion-folder green"></span>
         <span class="label">Explore Topics</span>
      </a>

      <a href="/release-notes" class="welcome-tile">
         <span class="icon ion-document-text green"></span>
         <span class="label">Releases notes</span>
      </a>

      <a class="welcome-tile">
         <span class="icon ion-social-windows"></span>
         <span class="label">Getting started<br/>Windows</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-social-apple"></span>
         <span class="label">Getting started<br/>Mac OSX</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-social-tux"></span>
         <span class="label">Getting started<br/>Linux</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-wrench blue"></span>
         <span class="label">Troubleshoot<br/>GNS3</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-arrow-down-a blue"></span>
         <span class="label">Download</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-help purple"></span>
         <span class="label">Support</span>
      </a>
      <a class="welcome-tile">
         <span class="icon ion-university purple"></span>
         <span class="label">Training</span>
      </a>
   </div>
</div>
<script type="text/javascript">
   $(function(){
      $.getJSON('/welcome/particles.json', function( data ) {
         particlesJS('welcome-particles', data)
      })
   })
</script>
