const form_checkout = document.getElementById('form-checkout');
const paymentUponReceiptCheckbox = document.getElementById('payment_upon_receipt_checkbox');
const onlinePaymentCheckbox = document.getElementById('online_payment_checkbox');

const iReceiverCheckbox = document.getElementById('i_receiver_checkbox');
const otherPersonCheckbox = document.getElementById('other_person_checkbox');

var checkbox_have_promotion_code = document.querySelector('#have_promotion_code')
var type_promotion_code = document.getElementById('type_promotion_code')

paymentUponReceiptCheckbox.addEventListener('change', function() {
if (paymentUponReceiptCheckbox.checked) {
    onlinePaymentCheckbox.checked = false;
}
});

onlinePaymentCheckbox.addEventListener('change', function() {
if (onlinePaymentCheckbox.checked) {
    paymentUponReceiptCheckbox.checked = false;
}
});

iReceiverCheckbox.addEventListener('change', function() {
  if (iReceiverCheckbox.checked) {
    otherPersonCheckbox.checked = false;
  }
});

otherPersonCheckbox.addEventListener('change', function() {
  if (otherPersonCheckbox.checked) {
    iReceiverCheckbox.checked = false;
  }
});


checkbox_have_promotion_code.addEventListener('change', function() {
  if (checkbox_have_promotion_code) {
    type_promotion_code.style.display = 'block';
  } else {
    type_promotion_code.style.display = 'none';
  }
});


// checking whether all the boxes are checked
form_checkout.addEventListener('submit', function(event) {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const requiredBoxes = [paymentUponReceiptCheckbox, onlinePaymentCheckbox, iReceiverCheckbox, otherPersonCheckbox];
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