// when document loads
document.addEventListener('DOMContentLoaded', function () {
  const observer = new MutationObserver(function (mutations) {
     // check until tooltip appears 
      mutations.forEach(function (mutation) {
          if (mutation.type === 'childList') {
              let tooltipDetected = false;
              mutation.addedNodes.forEach(node => {
                  // console.log("Added node:", node);
                  // Check if the added node is a tooltip by class name
                  if (node.classList && (node.classList.contains('tooltip') || node.classList.contains('dash-tooltip'))) {
                      tooltipDetected = true;
                  }
              });
              // tooltip found 
              if (tooltipDetected) {
                  const inputElement = document.getElementById('tooltip-store');
                  const listenerElement = document.getElementById('tooltip-detector');  // Ensure this ID matches your layout
                      // Dispatch a custom event when a tooltip is detected
                  if (listenerElement) {
                      var event = new CustomEvent('custom-tooltip-detected', {
                          detail: {
                              value: inputElement.value
                          }
                      });
                      listenerElement.dispatchEvent(event);
                      console.log("Custom event 'custom-tooltip-detected' dispatched.");
                  }
                  
              }
          }
      });
  });

  // Start observing the document body for added elements
  observer.observe(document.body, { childList: true, subtree: true });
});





// Function to check screen width and log message
function checkScreenWidth() {
  var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  var screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
  var cohort = document.getElementById('segment-dropdown');
  var subcohort = document.getElementById('sub-segment-dropdown');
  var timeline = document.getElementById('start-year-dropdown');
  var endyear = document.getElementById('end-year-dropdown');
  // console.log('Screen size:', screenWidth + 'x' + screenHeight);
  
  // Check if the screen width is less than 400 pixels
  if (screenWidth < 400) {
    console.log('Screen width is less than 400 pixels');
  }
}

// Call the checkScreenWidth function initially to check the width on page load
document.addEventListener('DOMContentLoaded', checkScreenWidth);

// Add event listener for window resize to recheck the width whenever the window size changes
window.addEventListener('resize', checkScreenWidth);