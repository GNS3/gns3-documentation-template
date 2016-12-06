<? include '../../header.php' ?>
<div class="header-push"></div>
<div class="subheader">

      <div class="title">
         <a href="/">
            <b>Documentation</b>
         </a>
         &nbsp; /  &nbsp;
         <a href="/release-notes">Release Notes</a>
      </div>
      <div class="search-input">
         <div class="icon ion-android-search"></div>
         <input type="text" placeholder="Search Documentation">
      </div>
</div>

<div class="gns3-article-toc">

   <div class="heading">What's new in<br/>GNS3 version 2.0</div>
   <div class="subheading active">Before upgrading</div>
   <div class="subheading">FAQ</div>
   <div class="heading">New Features</div>
   <div class="subheading">Save as you go</div>
   <div class="subheading">Multiple users can be connected to the same project</div>
   <div class="subheading">Smart packet capture</div>
   <div class="heading">New API</div>
</div>

<div class="gns3-main">
<div class="gns3-wrapper gns3-article">
   <div class="meta">
      <b>Last updated</b><br/>
      December 1, 2016
      <br/>
      <br/>
      <b>Contributors</b><br/>
      Julien Duponchelle<br/>
      Jeremy Grossman
   </div>
   <div>
      <div class="doc-icon icon ion-document-text"></div>
      <p class="title" id="h.k7ma3vyzxywb">What’s new in GNS3 version 2.0</p>
      <p></p>
      <p>Version 2.0 is a new major release of GNS3 which brings major architectural changes and also &nbsp;new features.</p>
      <p></p>
      <p>GNS3 was only a desktop application from the first version up to version 0.8.3. With the more recent 1.x versions, GNS3 has the possibility to use remote servers. Now, in version 2.0, multiple clients could control GNS3 at the same time, also all the “application intelligence” has &nbsp;been moved to the GNS3 server.</p>
      <p></p>
      <p>
         <b>What does it mean?</b>
      </p>
      <p></p>
      <ul class="lst-kix_9nnm7dkh2fs2-0 start">
      <li>Third parties can make applications controlling GNS3.</li>
      <li>Multiple users can be connected to the same project and see each other modifications in real time.</li>
      <li>No need to duplicate your settings on different computers if they connect to the same central server.</li>
      <li>Easier to contribute to GNS3, the separation between the graphical user interface and the server/backend is a lot clearer. </li>
      </ul>
      <p></p>
      <p>All the complexity of connecting multiple emulators has been abstracted in what we call the controller (part of GNS3 server). From a user point of view, it means that it is possible to start a packet capture on any link, connect anything to a cloud etc.</p>
      <p></p>
      <p>Finally, by using the NAT object in GNS3, connections to Internet work out of the box. Please note this is only available with the GNS3 VM or a Linux OS with libvirt installed.</p>
      <p></p>
      <h2 id="h.et27z8ebmayh">Before upgrading</h2>
      <p>No rollback is possible. Backup all your projects, settings and snapshot the GNS3 VM. <strong>Version 2.0 is in alpha stage</strong>&nbsp;which means many things could be broken or not work as expected.</p>
      <p></p>
      <p>If you still have project created with 0.8.x open them with a 1.X version of GNS3 before switching to 2.0. No direct conversion from 0.8 to 2.0 will be supported. </p>
      <h2 id="h.oczpbh6n5938">F.A.Q</h2>
      <h3 id="h.2y3qj318rn03">When can I expect the final release of version 2.0?</h3>
      <p>Around the end of 2016 or early 2017. We will ship many beta and release candidate versions before that date. We want to make sure this version is well tested with no unexpected regressions.</p>
      <p></p>
      <h3 id="h.k4nmgwpcutou">Will a new 1.5.x version be released?</h3>
      <p>Version 1.5.3 will be released in order to fix remaining bugs found in 1.5. This version will not introduce new features in order to keep it stable.</p>
      <h3 id="h.unbn4xhl3ihk">Will my projects made with 1.5.x be compatible with 2.0?</h3>
      <p>Yes excepting unexpected bugs.</p>
      <p></p>
      <h3 id="h.bj84lx4r1f5c">I have a certification exam next week, should I upgrade?</h3>
      <p>NO! Upgrade only if you are not in the middle of something important. We put huge effort to make sure to test each release but due to the nature of GNS3 we cannot possibly test all the scenarios, environments, images etc. &nbsp;</p>
      <p></p>
      <h3 id="h.26dg4eyginl1">What is not included with 2.0?</h3>
      <p>No web app is provided with version 2.0. We have experimental application on Github but it is only to validate our architecture.</p>
      <p></p>
      <p>Appliances management is still fully in the GUI, we hope to move it to our back-end and expose that part to third parties.</p>
      <h1 id="h.g5exp0olb6dn"></h1>
      <hr style="page-break-before:always;display:none;">
      <h1 id="h.iizor8v1b0p6"></h1>
      <h1 id="h.acu4ntly5utg">New features</h1>
      <h2 id="h.eow5mk7f6cg">Save as you go</h2>
      <p></p>
      <p>Your projects are automatically saved as you make changes to them, there is no need to press any save button anymore. An additional benefit is this will avoid synchronisation issues between the emulators’ virtual disks and projects.</p>
      <p></p>
      <h2 id="h.awdpyz2k1u4m">Multiple users can be connected to the same project</h2>
      <p></p>
      <p>Multiple user can be connected to the same project and see each other changes in real time and collaborate. If you open a console to a router you will see the commands send by other users.</p>
      <p></p>
      <h2 id="h.xrg5ywvqvipt">Smart packet capture</h2>
      <p></p>
      <p>Now starting a packet capture is just as easy as clicking on a link and asking for new capture. GNS3 will guess the pick the best interface where to capture from.</p>
      <p></p>
      <p>The packet capture dialog has also been redesigned to allow changing the name of the output file or to prevent automatically starting Wireshark:</p>
      <p></p>
      <p><span class="image"><a alt="Capture d’écran 2016-04-27 à 11.04.18.png" title="" class="image" href="4fa6a3c24ead59acf36ebd942c4f5542.jpg" target="_blank"><img src="4fa6a3c24ead59acf36ebd942c4f5542.jpg"></a></span></p>
      <h2 id="h.digwh4dcx9cv">Capture on any link between any nodes</h2>
      <p></p>
      <p>There is no longer any restriction on what kind of node can be used for a packet capture. Previously VPCS and Qemu were not supported.</p>
      <h2 id="h.q1os0ozgmdld">Select where to run a VPCS node</h2>
      <p>Like for hubs and switches, it is possible to select which server to use when VPCS node is dropped into a project .</p>
      <h2 id="h.cq0cb1avdikv">Delete a project from the GUI</h2>
      <p>Now you can delete a project from the file menu. All files will be deleted from your hard drive and remote servers.</p>
      <p><span class="image"><a alt="Capture d’écran 2016-05-26 à 11.22.50.png" title="" class="image" href="409e2a7a40e57aa540e7d955b73e0a9d.jpg" target="_blank"><img src="409e2a7a40e57aa540e7d955b73e0a9d.jpg"></a></span></p>
      <p></p>
      <p>Or via the project dialog</p>
      <p></p>
      <p><span class="image"><a alt="" title="" class="image" href="5225bee6dd7e31be525c2ec9e2546589.jpg" target="_blank"><img src="5225bee6dd7e31be525c2ec9e2546589.jpg"></a></span></p>
      <h2 id="h.abd8i7eqqzsf">Project options</h2>
      <p></p>
      <p>There are now multiple options allowing you to load a project with GNS3 in background and even to auto start the nodes.</p>
      <p></p>
      <p><span class="image"><a alt="" title="" class="image" href="97b677e1cec6aa355f79c7e6df1a7289.jpg" target="_blank"><img src="97b677e1cec6aa355f79c7e6df1a7289.jpg"></a></span></p>
      <h2 id="h.c0qwxztelkb6">The cloud is a real node</h2>
      <p></p>
      <p>In previous versions of GNS3, the cloud was in fact a direct usage of the emulator capabilities to connect to external networks. In version 2.0, the cloud is a real node, this means:</p>
      <p></p>
      <ul class="lst-kix_nwbte948efr8-0 start">
      <li>Possibility to connect anything to any cloud</li>
      <li>All links to a cloud support packet capture</li>
      <li>There is no need to run emulators as root to connect to a cloud (only uBridge requires admin permission).</li>
      </ul>
      <h2 id="h.x8n9ccpvrexr">Cloud templates</h2>
      <p>You can create cloud templates with your favorite interfaces and symbols.</p>
      <h2 id="h.trg3qh53krs9">New cloud interface</h2>
      <p>The cloud interface is simpler with a unique select dialog for ethernet interfaces. We also merged host object into the cloud since the difference between the 2 objects was not clear for most users.</p>
      <p><span class="image"><a alt="" title="" class="image" href="3ea00b2275dff582d1f0cf17196ac698.jpg" target="_blank"><img src="3ea00b2275dff582d1f0cf17196ac698.jpg"></a></span></p>
      <h2 id="h.eivuhqccr9qo">VPCS / Ethernet Switch / Ethernet Hub templates</h2>
      <p>You can create template for these nodes just like other nodes.</p>
      <p></p>
      <h2 id="h.3mdkf0y784p2">Search OS images in multiple locations</h2>
      <p>OS images can be stored in selected folder and used without providing the full path. GNS3 will scan these folders in order to find the correct images.</p>
      <p><span class="image"><a alt="" title="" class="image" href="ad6f1f72896c3bb1cdaf92dd50ca225c.jpg" target="_blank"><img src="ad6f1f72896c3bb1cdaf92dd50ca225c.jpg"></a></span></p>
      <p></p>
      <p>VM wizards offer a list of images available locally or remotely. GNS3 will upload an image for you if it can only be found locally.</p>
      <p></p>
      <h2 id="h.7m79qbzhtyyl">Periodic extraction of startup configs for Dynamips and IOU</h2>
      <p></p>
      <p>Startup configs are extracted at regular interval to avoid configuration loss if Dynamips or IOU crashes.</p>
      <h2 id="h.iwlibod46dd">Custom cloud, Ethernet hub and Ethernet switch templates</h2>
      <p></p>
      <p>It is possible to create custom templates (symbol, name format etc.)</p>
      <p></p>
      <h2 id="h.p108z6pa6xnb">Snap to grid for all objects</h2>
      <p>In version 1.5, we introduced the snap to grid feature. Now you can use it for rectangles, ellipses, images etc.</p>
      <h2 id="h.2201mbpz44k">Synchronize the node templates when using multiple GUI</h2>
      <p>Node templates are sync between all the GUIs.</p>
      <h2 id="h.kvvle02n20qj">Link label style</h2>
      <p>The style of link labels can be changed just like labels for nodes (color, font, orientation etc.)</p>
      <h2 id="h.lqv4uu1s6oe2">New place holders in command line for opening consoles</h2>
      <h3 id="h.ujv3us3qkfx">%i will be replaced by the project UUID </h3>
      <p>When you open a console to a node you can pass %i to the console command line, this will be replaced by the project UUID allowing scripts to interact with your project.</p>
      <h3 id="h.s83fxx5z05fx">%c will be replaced by the connection string</h3>
      <p>When you open a console to a node you can pass %c to the console command line, this will be replaced by the connection string to the GNS3 server allowing your scripts to know how to connect to the GNS3 API.</p>
      <h2 id="h.xrzyftot9rmr">Export a portable project from multiple remote servers</h2>
      <p>It is possible to export a project and reimport it to a single GNS3 VM if you a have a project running on multiple remote servers.</p>
      <p></p>
      <p>Note: You cannot re-import a project to the original multiple remotes or non GNS3 VM server. This a limitation of the export file format.</p>
      <h2 id="h.2o4qgan6qfkv">New save as</h2>
      <p>The old “save as” has been replaced by a project duplication feature. This feature will duplicate not just the .gns3 but also the disk data from all GNS3 servers.</p>
      <p></p>
      <p>With evolution of emulators, the complexity of the tasks to duplicate was bigger and we could no longer just duplicate the raw data. Behind the scene the import / export system introduced in version 1.5 using .gns3project extension is now used for duplicated projects.</p>
      <p></p>
      <h2 id="h.8eqabjexl0kb">Snapshots with remote servers</h2>
      <p>Snapshots are not supported when using remote servers. Behind the scene the import / export system introduced in version 1.5 is used for snapshots.</p>
      <h2 id="h.wob934m9xjag">Better start / stop / suspend all nodes</h2>
      <p>Start / stop / suspend all nodes feature will limit the amount of process starting at the same time to optimize CPU usage.</p>
      <h2 id="h.4sgnwd7wfz2o">Edit config</h2>
      <p>Dynamips, VPCS and IOU nodes support configuration editing from within GNS3. Note: this feature doesn’t automatically reload the config in the node.</p>
      <h2 id="h.pt8k6a5727d2">NAT node</h2>
      <p>NAT node can be used to connect GNS3 nodes to the Internet without any configuration, this requires the GNS3 VM or Linux. This node uses the libvirt nat interface.</p>
      <p></p>
      <p>This also replaces the Internet VM, the conversion will be automatic for internet VM users. An additional benefit is that this will consume less RAM and CPU.</p>
      <h2 id="h.g2gq835ldl82">Support for colorblind users</h2>
      <p>The stop symbol is now a square in order to help colorblind users to see the differences with running devices.</p>
      <p><span class="image"><a alt="" title="" class="image" href="a582c2beec2c0f7b48cd85a8f68c808d.jpg" target="_blank"><img src="a582c2beec2c0f7b48cd85a8f68c808d.jpg"></a></span></p>
      <h2 id="h.gsnf6k4i9s5m">Support for non local server</h2>
      <p>In previous version, disabling the local server was not officially supported.</p>
      <p></p>
      <p>Now if you disable the local server you can put settings for a remote server that will replace your local server.</p>
      <h2 id="h.k5108t1q804e">Support for profiles</h2>
      <p></p>
      <p>GNS3 can be started with the parameter --profile PROFILNAME in order to have different settings applied. This can be useful if one needs different settings for different usage of GNS3 (home vs office).</p>
      <p></p>
      <p>Or enable a dialog at startup<span class="image"><a alt="" title="" class="image" href="b0e6705540d94de6a86a51be366fb840.jpg" target="_blank"><img src="b0e6705540d94de6a86a51be366fb840.jpg"></a></span></p>
      <p></p>
      <h2 id="h.ffowgdo3yrog">Suspend the GNS3VM when closing GNS3</h2>
      <p></p>
      <p>For fastest exit and restart of GNS3 you can now suspend the VM. This works well with an SSD disk. For instance, it takes less than 4 seconds on an old macbook when previously the start time was 30 seconds.</p>
      <p></p>
      <h2 id="h.2kgl9dgmu68h">Edit the scene size</h2>
      <p></p>
      <p>The scene size can be changed if your project is bigger than the standard one.</p>
      <p></p>
      <h2 id="h.h8p2jcbu1l1z">IOU licence improved</h2>
      <p>Instead of the old licence file system. Now you can import the IOU licence and it will be sync across your devices.</p>
      <h1 id="h.qwgh66fii3r8">New API</h1>
      <p>Developers can find out how to control GNS3 using an API here: <span><a href="http://api.gns3.net/en/2.0/">http://api.gns3.net/en/2.0/</a></span></p>
      <p></p>
      <p>Thanks to our controller, it is no longer required to deal with multiple GNS3 servers since most of the information is available in the API.</p>
      <p></p>
      <p>All the visual objects are exposed as SVG.</p>
      <p></p>
      <p>This API is quite complete, the only major missing part at the moment is creation and use of node templates.</p>
      <h1 id="h.7ib4pux0tyyg">Warning</h1>
      <p>Opening a project in version 2.0 will automatically convert it to our 2.0 file format. This means you will no longer be able to open it using previous versions of GNS3. Note this is the normal case with any new major version of GNS3.</p>
      <p></p>
      <p>Please, backup your projects and settings before upgrading. Also create a snapshot in the GNS3 VM before upgrading it.</p>
      <h1 id="h.jozsrunoeugo">Deprecated features</h1>
      <p>Deprecated features should not impact you, these are rarely used features which are usually not documented.</p>
      <h2 id="h.740wvpm53i45">Conversions</h2>
      <p>Starting with version 2.0, the conversion from .net (project files made before version 1.0) will no longer been included in GNS3 builds. Conversion will still be possible using a separate program. This converter was a community effort but the author of this code stopped any development of it.</p>
      <p></p>
      <p>The converter to go from a IOU VM to a GNS3 VM will also be removed. We recommend to switch to version 1.4 or 1.5 with the GNS3 VM if you still use the IOU VM.</p>
      <h2 id="h.6ewqq2djbuwi">VPCS multi-host</h2>
      <p>The VPCS multi-host feature that could be found in the tools menu has been removed. This option was not documented and seldom used by anyone. Also, this feature is hard to support by design in version 2.0 (nodes are isolated from each other).</p>
      <p></p>
      <h2 id="h.uwlnpe7thlhr">Temporary projects</h2>
      <p></p>
      <p>Originally it was design has a playground for quick tests however this was confusing and some users would lose data. It was also complex to support because data needed to be moved to a new location on disk when a temporary project was saved to a permanent one.</p>
      <p></p>
      <p>Now GNS3 guarantee that all data is saved in a real project and whatever happens you can be assured it is saved on your disk.</p>
      <p></p>
      <h2 id="h.3hgfu5wlcv61">Run as admin</h2>
      <p></p>
      <p>You should not have to run GNS3 as an admin user to connect to a cloud. We encourage you to switch to a normal user.</p>
      <h2 id="h.wjtb653if12e">Cloud</h2>
      <p></p>
      <p>The cloud interface has been streamlined and the following cloud NIOs have been dropped:</p>
      <p></p>
      <ul class="lst-kix_yt6ur4ypn7az-0 start">
      <li>NIO NAT</li>
      <li>NIO UNIX</li>
      <li>NIO VDE</li>
      <li>NIO NULL</li>
      </ul>
      <p></p>
      <p>We may reintroduce some of them if there is a demand (we must add support into uBridge in order to do so).</p>
      <p></p>
      <h2 id="h.v1gtj61tyku5">Upload the images via the web page / upload</h2>
      <p>Since version 1.4, OS images are uploaded for you, you no longer need to upload them manually. That’s why the upload page has been removed.</p>
      <h2 id="h.hayglrya3rjc">No automatic screenshot for projects</h2>
      <p>In version 1.X, a screenshot of your topology was taken every time a project was saved but due to the fact the project management has been moved to our backend, it is not possible to have the code &nbsp;render a topology to a file.</p>
      <p></p>
      <p>You can still use the screenshot button in the interface in order to get one.</p>
      <p></p>
      <p>More information can be found there:</p>
      <p><span><a href="https://github.com/GNS3/gns3-server/issues/588">https://github.com/GNS3/gns3-server/issues/588</a></span></p>
      <p></p>
      </div>
</div>
</div>
<? include '../../footer.php' ?>
