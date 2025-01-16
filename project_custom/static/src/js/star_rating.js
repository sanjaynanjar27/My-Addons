odoo.define('project_custom.review_system', function(require) {
  "use strict";

  // Function to update the rating
  function gfg(n) {
    let stars = document.getElementsByClassName("star");
    let output = document.getElementById("output");
    remove();

    // Assign classes based on the rating
    for (let i = 0; i < n; i++) {
      if (n == 1) cls = "one";
      else if (n == 2) cls = "two";
      else if (n == 3) cls = "three";
      else if (n == 4) cls = "four";
      else if (n == 5) cls = "five";

      stars[i].className = "star " + cls;
    }

    // Update the output text
    output.innerText = "Rating is: " + n + "/5";
  }

  // Function to remove the pre-applied class styles
  function remove() {
    let i = 0;
    while (i < 5) {
      let stars = document.getElementsByClassName("star");
      stars[i].className = "star";
      i++;
    }
  }

  // Expose the function globally (optional in case of modular code)
  window.gfg = gfg;
});
