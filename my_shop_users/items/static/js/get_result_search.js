const div_search = document.querySelector('.block_search_item');
const divContainer_sort_chp_to_exp = document.querySelector('.main_block_sort_chp_to_exp');
const div_exp_to_chp = document.querySelector('.main_block_sort_exp_to_chp');
const div_newItem = document.querySelector('.main_block_newItem');
const div_review = document.querySelector('.main_block_more_review');
const div_filter_price = document.querySelector('.main_block_filter_price');


let isClicked_chp_to_exp = localStorage.getItem('isClicked_chp_to_exp') === 'true';
let isClicked_exp_to_chp = localStorage.getItem('isClicked_exp_to_chp') === 'true';
let isClicked_newItem = localStorage.getItem('isClicked_newItem') === 'true';
let isCliked = localStorage.getItem('isClicked_moreReview') === 'true';
let isCliked_filter_price = localStorage.getItem('isClicked_filter_price') === 'true';


// від дешевого до дорого
let showOrhideChptoExp = function() {
  if (isClicked_chp_to_exp) {
    div_search.style.display = 'none';
    divContainer_sort_chp_to_exp.style.display = 'block';
    isClicked_chp_to_exp = false;
  } else {
    div_search.style.display = 'block';
    isClicked_chp_to_exp = true;
  }
  localStorage.setItem('isClicked_chp_to_exp', isClicked_chp_to_exp);
};

if (isClicked_chp_to_exp) {
  div_search.style.display = 'none';
  divContainer_sort_chp_to_exp.style.display = 'block';
} else {
  div_search.style.display = 'block';
}


// від дорого до дешевого
let showExp_or_Chp = function() {
  if (isClicked_exp_to_chp) {
    div_search.style.display = 'none';
    div_exp_to_chp.style.display = 'block';
    isClicked_exp_to_chp = false;
  } else {
    div_search.style.display = 'block';
    isClicked_exp_to_chp = true;
  }
  localStorage.setItem('isClicked_exp_to_chp', isClicked_exp_to_chp);
};

if (isClicked_exp_to_chp) {
  div_search.style.display = 'none';
  div_exp_to_chp.style.display = 'block';
} else {
  div_search.style.display = 'block';
}

// review item sorting
let moreReview = function() {
  if (isCliked) {
    div_search.style.display = 'none';
    div_review.style.display = 'block';
    isCliked = false;
  } else {
    div_search.style.display = 'block';
    isCliked = true;
  }
  localStorage.setItem('isClicked_moreReview', isCliked);
};

if (isCliked) {
  div_search.style.display = 'none';
  div_review.style.display = 'block';
} else {
  div_search.style.display = 'block';
}

// filter price
let filter_price = (function() {
  let isClicked = false;

  return function() {
    if (!isClicked) {
      div_search.style.display = 'none';
      div_filter_price.style.display = 'block';
      isClicked = true;
      localStorage.setItem('isClicked_filter_price', isClicked);
    }
  };
})();


// Reset filters
let reset_filters = function() {
  // Reset price filter values
  document.querySelector('input[name="first_price"]').value = 0;
  document.querySelector('input[name="last_price"]').value = 0;

  // Reset local storage 
  localStorage.setItem('isClicked_filter_price', 'false');
  location.reload();
};