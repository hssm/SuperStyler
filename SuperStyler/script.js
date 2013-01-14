<script>

var cardClass = "##ClassGoesHere##";
var initialRun = false;

function initial() {
    initialRun = true;
    
    // Remove the existing style element
    var style = document.body.getElementsByTagName("style")[0];
    if (style) {
        style.parentNode.removeChild(style);
    }
    
    // Replace the class attribute of the card-containing element to correspond
    // to the card of the base card type we are copying. This is to allow
    // card-specific styling to work.

    // Desktop places attribute in body element
    if (document.body.className.indexOf("card") !== -1) {
        document.body.className = cardClass;
    }

    // AnkiDroid places it in the first span inside body
    var cspan = document.body.getElementsByTagName("span")[0];
    if (cspan != undefined && cspan.className.indexOf("card") !== -1) {
        cspan.className = cardClass;
    }
    
    // AnkiWeb puts it in qa_box
    var qa_box = document.getElementById("qa_box");
    if (qa_box != undefined && qa_box.className.indexOf("card") !== -1) {
        qa_box.className = cardClass;
    }
}

function updateCss() {
    if (!initialRun)
        initial();
    
    // Grab a copy of the old css (we delete it later instead of now
    // to avoid flickering).
    var oldStyle = document.getElementById("updatingCss");

    var ss = document.createElement("link");
    ss.id = "updatingCss";
    ss.type = "text/css";
    ss.rel = "stylesheet";
    
    ss.onload = function() {
    	if (oldStyle)
            document.body.removeChild(oldStyle);
    }
    
    // Unfortunately I have to add a random tag on the end because the Android
    // WebView refuses to fetch a new one, even when asked not to cache it.
    ss.href = "http://##AddressGoesHere##/style.css?"+Date.now();
    document.body.appendChild(ss);
}

// Download and apply the new stylesheet three times a second
setInterval(updateCss, 333);

</script>