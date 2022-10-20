document.addEventListener('DOMContentLoaded', addEventListeners);

/**
 * Add event listeners when DOM has loaded
 */
function addEventListeners(){
    if(document.querySelector('#id_collabs_only')){
        document.getElementById('id_collabs_only').addEventListener('click', searchSubmit)
    }
}

/**
 * Forces search form to be submitted when user checks or unchecks the collabs only checkbox
 */
function searchSubmit(){
    document.getElementById('search-profile').submit()
    console.log('Entered searchSubmit')
}