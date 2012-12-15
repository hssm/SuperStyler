<script>
  // Remove the existing style element
  var style = document.body.getElementsByTagName("style")[0];
  if (style) {
    style.parentNode.removeChild(style);
  }

  // Download and apply the new stylesheet three times a second
  setInterval(updateCss, 333);
  function updateCss() {  
    // Grab a copy of the old css (we delete it later instead of now
    // to avoid flickering).
    var oldStyle = document.getElementById("updatingCss");

    var ss = document.createElement("link");
    ss.id = "updatingCss";
    ss.type = "text/css";
    ss.rel = "stylesheet";
    
    // Unfortunately I have to add a random tag on the end because the Android
    // WebView refuses to fetch a new one, even when asked not to cache it.
    ss.href = "http://##AddressGoesHere##/style.css?"+Date.now();   
    document.body.appendChild(ss);
    
    setTimeout(function () {
      if (oldStyle) {
        document.body.removeChild(oldStyle);
      }
    }, 200);
  }
</script>