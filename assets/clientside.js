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
        const blue_button = document.getElementById('row-button');
        const cohort = document.getElementById('segment-dropdown');
        const subcohort = document.getElementById('sub-segment-dropdown');
        const timeline = document.getElementById('start-year-dropdown');
        const endyear = document.getElementById('end-year-dropdown');
        const cohort_label = document.getElementById('Cohort');
        const subcohort_label = document.getElementById('SubCohort');
        const timeline_label = document.getElementById('Timeline');
        if (blue_button, cohort, subcohort, timeline, endyear, 
            cohort_label, subcohort_label, timeline_label) {
            updateLayoutBasedOnWidth();
            clearInterval(checkButtonInterval);
        }
    }, 100); // Check every 100 milliseconds

    window.addEventListener('resize', updateLayoutBasedOnWidth);
});

function updateLayoutBasedOnWidth() {
    const screenWidth = window.innerWidth;
    const blue_button = document.getElementById('row-button');
    const cohort = document.getElementById('segment-dropdown');
    const subcohort = document.getElementById('sub-segment-dropdown');
    const timeline = document.getElementById('start-year-dropdown');
    const endyear = document.getElementById('end-year-dropdown');
    const cohort_label = document.getElementById('Cohort');
    const subcohort_label = document.getElementById('SubCohort');
    const timeline_label = document.getElementById('Timeline');

    //smartphone viewing
    const big_width_segment_s = '300%';
    const small_width_segment_s = '50%';
    const label_size_s = '2.55vw';
    const font_size_s = '2.5vw';
    
    
    // laptop viewing
    const big_width_segment = '95%';
    const small_width_segment = '27%';
    const label_size = '1.55vw';
    const font_size = '1.5vw';

    

    
    if (blue_button) { // Always check if button exists before applying styles
        // phone viewing
        if (screenWidth <= 500) {
            blue_button.style.fontSize = "2.3vw";
            blue_button.style.width = "80%";
            // LEFT ////////////////
            // cohort how left
            const cohort_left = "-20px";
            cohort.style.marginLeft = cohort_left;
            cohort_label.style.marginLeft = cohort_left;
            // timeline how left
            const timeline_left = "20px";
            timeline.style.marginLeft = timeline_left;
            timeline_label.style.marginLeft = timeline_left;
            // endyear button how left
            const endyear_left = "46px";
            endyear.style.marginLeft = endyear_left;
            // SIZES ////////////////
            // cohort sizes
            cohort.style.width = big_width_segment_s;
            cohort.style.fontSize = font_size_s;
            // subcohort sizes
            subcohort.style.width = big_width_segment_s;
            subcohort.style.fontSize = font_size_s;
            // subcohort.style.marginLeft = "0px";
            // timeline sizes
            timeline.style.width = small_width_segment_s;
            timeline.style.fontSize = font_size_s;    
            // endyear sizes
            endyear.style.width = small_width_segment_s; 
            endyear.style.fontSize = font_size_s;    
            endyear.style.marginTop = "3.4px";
            // label sizes
            cohort_label.style.fontSize = label_size_s;
            subcohort_label.style.fontSize = label_size_s;
            timeline_label.style.fontSize = label_size_s;



        // laptop viewing
        } else if (screenWidth > 500 && screenWidth <= 1100){
            console.log("laptop viewing")
            blue_button.style.fontSize = "1.4vw";

            cohort.style.width = big_width_segment;
            cohort.style.fontSize = font_size;
            cohort.style.marginLeft = "0px";

            subcohort.style.width = big_width_segment;
            subcohort.style.fontSize = font_size;
            subcohort.style.marginLeft = "0px";

            timeline.style.width = small_width_segment;
            timeline.style.fontSize = font_size;    
            timeline.style.marginLeft = "0px";

            endyear.style.width = small_width_segment; 
            endyear.style.fontSize = font_size;    
            endyear.style.marginLeft = "-4px";
            endyear.style.marginTop = '4.1px';

            cohort_label.style.fontSize = label_size;
            cohort_label.style.marginLeft = "0px";
            subcohort_label.style.fontSize = label_size;
            subcohort_label.style.marginLeft = "0px";
            timeline_label.style.fontSize = label_size;
            timeline_label.style.marginLeft = "0px";

        } else {
            endyear.style.marginTop = '7.0px';
        }
    }
}


// var lastScreenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

// // Function to check screen width and log message
// function checkScreenWidth() {
//   var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
//   var screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

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