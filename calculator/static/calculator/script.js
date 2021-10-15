// validation for forms
$(document).ready(function () {
  $('form').on('submit', function (e) {
    if (!this.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    $(this).addClass('was-validated') 
  });
});

// toggle between expenses and income pie chart on report
$('.btn-group > input').click(function() {
    var ix = $(this).index();
    
    $('.expenses-pie-chart').toggle( ix === 0 );
    $('.income-pie-chart').toggle( ix === 2 );
});

// for popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})