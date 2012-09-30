<script>
  //  Remove the existing style element
  var style = document.body.getElementsByTagName("style")[0];
  if (style) {
    style.parentNode.removeChild(style);
  }

  // Download and apply new css every .5 seconds
  setInterval(updateCss, 500);
  function updateCss() {  
    // First grab a copy of the old one (we delete it later instead of now to avoid flickering)
    var oldStyle = document.getElementById("updatingCss");

    var ss = document.createElement("link");
    ss.id = "updatingCss";
    ss.type = "text/css";
    ss.rel = "stylesheet";
    ss.href = "http://##AddressGoesHere##/style.css?"+Date.now();
    document.body.appendChild(ss);

    // Cheap hack to avoid flickering. Delete the old style a little while after the old one has finished.
    // I am positive there is a better way to do this.
    setTimeout(function () {
      if (oldStyle) {
        document.body.removeChild(oldStyle);
      }
    }, 200);
  }
</script>