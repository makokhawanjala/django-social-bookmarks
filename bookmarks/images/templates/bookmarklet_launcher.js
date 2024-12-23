(function () {
  if (!window.bookmarklet) {
    // create <script> and load the real bookmarklet code from STATIC files
    var bookmarklet_js = document.body.appendChild(document.createElement('script'));
    bookmarklet_js.src = '//127.0.0.1:8000/static/images/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
    // mark as loaded so repeated clicks won’t re-inject it
    window.bookmarklet = true;
  } else {
    // already loaded once on this page: just relaunch the UI
    bookmarkletLaunch();
  }
})();
