// modal edit reply
const replyEditBtns = document.querySelectorAll('.reply-edit-btn');
const modalReplies = document.querySelectorAll('.modal-replyEdit');

replyEditBtns.forEach((replyEditBtn) => {
    replyEditBtn.addEventListener('click', () => {
        const replyId = replyEditBtn.dataset.replyId;
        const modalReply = document.querySelector(`#modal-replyEdit-${replyId}`);
        modalReply.style.display = 'block';

        const closeBtn = modalReply.querySelector('.close-reply');
        closeBtn.addEventListener('click', () => {
            modalReply.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target == modalReply) {
                modalReply.style.display = 'none';
            }
        });
    });
});



// field reply
function ReplyForm(id) 
{
var div = document.getElementById('ReplyForm-' + id);
div.style.display = 'block';
}


// modal edit question
function openModal() {
    btn_open_ques = document.getElementById("modalEditQuestions").style.display = "block";
  }
  
  function closeModal() {
      btn_close_ques = document.getElementById("modalEditQuestions").style.display = "none";
  }       