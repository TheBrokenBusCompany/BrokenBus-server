// Get the modal
var modal = document.getElementById("infoEMT");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
function showModal(element) {
    modal.style.display = "block";
    var properties = element.target.feature.properties;
    document.getElementById("modalTitle").innerText = "Bus " + properties.busCode;
    document.getElementById("modalLineCode").innerText = "Line: " + properties.codLine;
    document.getElementById("modalDirection").innerText = "Direction: " + properties.direction;
    document.getElementById("modalLastUpdate").innerText = "Last update: " + properties.lastUpdate;
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}