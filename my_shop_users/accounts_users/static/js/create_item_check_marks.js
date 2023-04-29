const status_availability = document.getElementById("status_availability");
const status_ready = document.getElementById("status_ready");

const state_new = document.getElementById("state_new");
const state_used = document.getElementById("state_used");

var checkbox = document.querySelector('#checkbox_guarantee');
var daysField = document.getElementById('guarantee_period');

status_availability.addEventListener('change', function() {
  if (status_availability.checked) {
      status_ready.checked = false;
  }
});


status_ready.addEventListener('change', function() {
  if (status_ready.checked) {
    status_availability.checked = false;
  }
});


state_new.addEventListener('change', function() {
  if (state_new.checked) {
    state_used.checked = false;
  }
});


state_used.addEventListener('change', function() {
  if (state_used.checked) {
    state_new.checked = false;
  }
});


checkbox.addEventListener('change', function() {
  if (checkbox.checked) {
    daysField.style.display = 'block';
  } else {
    daysField.style.display = 'none';
  }
});