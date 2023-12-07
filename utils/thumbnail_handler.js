document.addEventListener("DOMContentLoaded", function() {
    // Select all image elements within cards
    const cardImages = document.querySelectorAll(".thumbnail-section img");
    
    // Loop through each card image
    cardImages.forEach(function(image) {
        image.addEventListener("error", function() {
            // Make the missing image invisible by setting display to "none"
            this.style.display = "none";
        });
    });
});

window.onload = function() {
    // Select all image elements within cards
    const cardImages = document.querySelectorAll(".thumbnail-section img");
    
    // Loop through each card image
    cardImages.forEach(function(image) {
      image.addEventListener("error", function() {
        // Make the missing image invisible by setting display to "none"
        this.style.display = "none";
      });
    });
};