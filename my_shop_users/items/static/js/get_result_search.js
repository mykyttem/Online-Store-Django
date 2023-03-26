const div_search = document.querySelector('.block_search_item');

const divContainer_sort_chp_to_exp = document.querySelector('.main_block_sort_chp_to_exp')
const div_exp_to_chp = document.querySelector('.main_block_sort_exp_to_chp')

const div_newItem = document.querySelector('.main_block_newItem')
const div_review = document.querySelector('.main_block_more_review')

const div_filter_price = document.querySelector('.main_block_filter_price')

let isCliked = localStorage.getItem('isClicked') === 'true';


// від дешевого до дорого
let showOrhideChptoExp = function(){
    if(isCliked){
        div_search.style.display = 'none';
        divContainer_sort_chp_to_exp.style.display = 'block'
        isCliked = false;
    } else {
        div_search.style.display = 'block';
        isCliked = true;            
    }
    localStorage.setItem('isClicked', isCliked);
}

if(isCliked){
    div_search.style.display = 'none';
    divContainer_sort_chp_to_exp.style.display = 'block'
} else {
    div_search.style.display = 'block';
}


// від дорого до дешевого
let showExp_or_Chp = function(){
    if(isCliked){
        div_search.style.display = 'none';
        div_exp_to_chp.style.display = 'block'
        isCliked = false;
    } else {
        div_search.style.display = 'block';
        isCliked = true;            
    }
    localStorage.setItem('isClicked', isCliked);
}

if(isCliked){
    div_search.style.display = 'none';
    div_exp_to_chp.style.display = 'block'
} else {
    div_search.style.display = 'block';
}


// new ones first
let newItem = function(){
    if(isCliked){
        div_search.style.display = 'none';
        div_newItem.style.display = 'block'
        isCliked = false;
    } else {
        div_search.style.display = 'block';
        isCliked = true;            
    }
    localStorage.setItem('isClicked', isCliked);
}

if(isCliked){
    div_search.style.display = 'none';
    div_newItem.style.display = 'block'
} else {
    div_search.style.display = 'block';
}

// review item sorting
let moreReview = function(){
    if(isCliked){
        div_search.style.display = 'none';
        div_review.style.display = 'block'
        isCliked = false;
    } else {
        div_search.style.display = 'block';
        isCliked = true;            
    }
    localStorage.setItem('isClicked', isCliked);
}

if(isCliked){
    div_search.style.display = 'none';
    div_review.style.display = 'block'
} else {
    div_search.style.display = 'block';
}


// filter price
let filter_price = function(){
    if(isCliked){
        div_search.style.display = 'none';
        div_filter_price.style.display = 'block'
        isCliked = false;
    } else {
        div_search.style.display = 'block';
        isCliked = true;            
    }
    localStorage.setItem('isClicked', isCliked);
}

if(isCliked){
    div_search.style.display = 'none';
    div_filter_price.style.display = 'block'
} else {
    div_search.style.display = 'block';
}


