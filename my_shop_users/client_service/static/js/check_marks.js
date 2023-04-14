const paymentUponReceiptCheckbox = document.getElementById('payment_upon_receipt_checkbox');
const onlinePaymentCheckbox = document.getElementById('online_payment_checkbox');

const iReceiverCheckbox = document.getElementById('i_receiver_checkbox');
const otherPersonCheckbox = document.getElementById('other_person_checkbox');

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