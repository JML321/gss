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
              // CONDITIONAL SEND n_clicks in - tooltip found 
              if (tooltipDetected) {
                  const listenerElement = document.getElementById('tooltip-detector');  // Ensure this ID matches your layout
                      // Dispatch a custom event when a tooltip is detected
                //   if (listenerElement) {
                  var event = new CustomEvent('custom-tooltip-detected');
                  listenerElement.dispatchEvent(event);
                  console.log("Custom event 'custom-tooltip-detected' dispatched.");
                 // }
                  
              }
          }
      });
  });

  // Start observing the document body for added elements
  observer.observe(document.body, { childList: true, subtree: true });
});


document.addEventListener('DOMContentLoaded', function() {
    let checkButtonInterval = setInterval(function() {
        const button = document.getElementById('row-button');
        console.log("this is the button ", button)
        if (button) {
            updateLayoutBasedOnWidth();
            clearInterval(checkButtonInterval);
        }
    }, 100); // Check every 100 milliseconds

    window.addEventListener('resize', updateLayoutBasedOnWidth);
});

function updateLayoutBasedOnWidth() {
    const screenWidth = window.innerWidth;
    const button = document.getElementById('row-button');
    
    if (button) { // Always check if button exists before applying styles
        if (screenWidth <= 500) {
            button.style.fontSize = "2.4vw";
            button.style.width = "100%";
        } else {
            button.style.fontSize = "1.4vw";
        }
    }
}


// var lastScreenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

// // Function to check screen width and log message
// function checkScreenWidth() {
//   var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
//   var screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
// //   var cohort = document.getElementById('segment-dropdown');
// //   var subcohort = document.getElementById('sub-segment-dropdown');
// //   var timeline = document.getElementById('start-year-dropdown');
// //   var endyear = document.getElementById('end-year-dropdown');
//   // console.log('Screen size:', screenWidth + 'x' + screenHeight);
  
//   // Check if the screen width is less than 400 pixels
//   var blue_width = 400;
//   if (lastScreenWidth > blue_width && screenWidth < blue_width) {
//     console.log('Screen width has changed from being over 400 pixels to less than 400 pixels');
//     const listenerElement1 = document.getElementById('tooltip-detector');
//     var event = new CustomEvent('blue-shrink-detected');
//     listenerElement.dispatchEvent(event);
//   }
  
//   // Update lastScreenWidth with the current screenWidth for the next check
//   lastScreenWidth = screenWidth;
// }

// // Call the checkScreenWidth function initially to check the width on page load
// document.addEventListener('DOMContentLoaded', checkScreenWidth);

// // Add event listener for window resize to recheck the width whenever the window size changes
// window.addEventListener('resize', checkScreenWidth);