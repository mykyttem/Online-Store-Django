const form_create_item = document.getElementById('form-create-item');

const status_availability = document.getElementById("status_availability");
const status_ready = document.getElementById("status_ready");

const state_new = document.getElementById("state_new");
const state_used = document.getElementById("state_used");

var checkbox_guarantee = document.querySelector('#checkbox_guarantee');
var daysField = document.getElementById('guarantee_period');

var checkbox_promotion_code = document.querySelector('#checkbox_promotion_code')
var type_promotion_code = document.getElementById('promotion_code')
var amount_users_type = document.getElementById('amount_users_type')
var at_what_price = document.getElementById('at_what_price')
var validity_period_promocode = document.getElementById('validity_period_promocode')
var text_data = document.getElementById('hint-text')

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


checkbox_guarantee.addEventListener('change', function() {
  if (checkbox_guarantee.checked) {
    daysField.style.display = 'block';
  } else {
    daysField.style.display = 'none';
    document.getElementById("guarantee_period").value = '';
  }
});


checkbox_promotion_code.addEventListener('change', function() {
  if (checkbox_promotion_code.checked) {

    type_promotion_code.style.display = 'block';
    amount_users_type.style.display = 'block';
    at_what_price.style.display = 'block';
    validity_period_promocode.style.display = 'block'
    text_data.style.display = 'block'

    const random_promotion_code = Math.random().toString(36).substring(2, 8);
    document.getElementById("promotion_code").value = random_promotion_code;
  } else {
    
    type_promotion_code.style.display = 'none';
    amount_users_type.style.display = 'none';
    at_what_price.style.display = 'none';
    validity_period_promocode.style.display = 'none'
    text_data.style.display = 'none'

    document.getElementById("promotion_code").value = '';
  }
});


// checking whether all the boxes are checked
form_create_item.addEventListener('submit', function(event) {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const requiredBoxes = [status_availability, status_ready, state_new, state_used]
  let numRequiredChecked = 0;

  for (let i = 0; i < requiredBoxes.length; i++) {
    if (requiredBoxes[i].checked && checkedBoxes.includes(requiredBoxes[i])) {
      numRequiredChecked++;
    }
  }

  if (numRequiredChecked < 2) {
    alert('Ви натиснули не всі галочки');
    event.preventDefault();
  }
});