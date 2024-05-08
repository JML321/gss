var count = 0
document.addEventListener('DOMContentLoaded', function() {
    var message = "Hover Over Question or Header for More Info";
    var message1 = "Show More Rows";
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                var addedNodes = mutation.addedNodes;
                for (var i = 0; i < addedNodes.length; i++) {
                    var node = addedNodes[i];
                    console.log(node);
                    if (node.classList.contains('tooltip') || node.classList.contains('dash-tooltip')
                                                           || count > 0) {
                        count++;
                        document.getElementById('row-button').style.backgroundColor = '#f8f9fa';
                        document.getElementById('row-button').style.color = '#495057';
                        document.getElementById('row-button').textContent = message1;
                    } else {
                        document.getElementById('row-button').style.backgroundColor = '#007bff';
                        document.getElementById('row-button').style.color = 'white';
                        document.getElementById('row-button').textContent = message;
                        
                    }
                    
                }
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
