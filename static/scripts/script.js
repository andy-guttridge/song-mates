(function(){
    document.addEventListener('DOMContentLoaded', setUp);
    /**
     * Add event listeners and remove any alerts from the DOM after 3 seconds
     */
    function setUp(){
        if(document.querySelector('#id_collabs_only')){
            document.getElementById('id_collabs_only').addEventListener('click', searchSubmit);
        }
        
        // Using setTimeout to automatically dismiss messages adapted from Code Institute Django Blog tutorial
        setTimeout(function() {
            let alertList = document.getElementsByClassName('alert');
            let alertArray = Array.from(alertList);
            alertArray.forEach(function (alert) {
                let anAlert = new bootstrap.Alert(alert);
                anAlert.close();
            });
        }, 3000);
    }

    /**
     * Forces search form to be submitted when user checks or unchecks the collabs only checkbox
     */
    function searchSubmit(){
        document.getElementById('search-profile').submit();
    }
})();