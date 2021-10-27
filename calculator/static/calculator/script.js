// Index Page

// change data-bs-target of "x" link on home page card and id of modal to match
$('.editDeleteButtons').each(function(i, obj) {
  var modal = $(this).siblings('.modal')
  var modal_body = modal.find('.modal-body')
  var delete_link = $(this).children('[data-bs-target="#deleteModal"]')
  modal.attr('id', `delete_modal_${i + 1}`)
  delete_link.attr('data-bs-target', `#delete_modal_${i + 1}`)
  $('<p>Are you sure you would like to delete this report?</p>').appendTo(modal_body)

})

// Calculator Page

// validation for forms
$(document).ready(function () {
  // hide prop_photo form field. 
  $('#id_prop_photo').parent().parent().hide();
  // hide down payment 2
  $('.downPayment2').hide();
  if ($('#id_cash_purchase').is(':checked')) {
    $('.toggleLoanDetails').hide();
  }

  $('form').on('submit', function (e) {
    if (!this.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    $(this).addClass('was-validated') 
  });
});

// preview of property image on upload
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      var edit_button = $('.editPhotoButton')
      var delete_button = $('.clearPhotoButton')
      if (edit_button || delete_button) {
        edit_button.remove()
        delete_button.remove()
      }
      if ($('#previewImage')) {
        $('#previewImage').remove()
      }
      $(".imagePlaceholder").removeAttr("style")
      $('.imagePlaceholder').append('<img src="" class="card-img-top" id="previewImage">')
      $('.photoButton').hide()
      $('.imagePlaceholder div').append('<button onclick="addPhoto()" class="editPhotoButton btn btn-sm btn-light me-1">Change</button>')
      $('.editPhotoButton').after('<button onclick="clearPhoto()" class="clearPhotoButton btn btn-sm btn-danger ms-1">Delete</button>')
      $('#previewImage').attr('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

// clicks property photo hidden input
function addPhoto() {
    $('#id_prop_photo').click()
    $('#prop_photo-clear_id').prop('checked', false)
}

// clears the image preview and property photo input 
function clearPhoto() {
  $('.imagePlaceholder').css('border', '1px dashed grey');
  $('.card-img-top').remove();
  $('.photoButton').show()
  $('.editPhotoButton, .clearPhotoButton').remove()
  $('#id_prop_photo').val('')
  if($('#prop_photo-clear_id')) {
    $('#prop_photo-clear_id').prop('checked', true)
  }
}

// wrap form currency inputs with bootstrap formatting
$('.currency input').each(function(i, obj) {
  var invalid_feedback = $(this).siblings('.invalid-feedback')
  $(this).wrap('<div class="input-group"></div>');
  if (invalid_feedback) {
    invalid_feedback.appendTo($(this).parent())
  }
  $(this).before('<span class="input-group-text text-muted bg-transparent border-end-0">$</span>');
})

// wrap form percentage inputs with bootstrap formatting
$('.percentage input').each(function(i, obj) {
  var invalid_feedback = $(this).siblings('.invalid-feedback')
  $(this).wrap('<div class="input-group"></div>');
  if (invalid_feedback) {
    invalid_feedback.appendTo($(this).parent())
  }
  $(this).after('<span class="input-group-text text-muted bg-transparent rounded-right">%</span>');
})

// opens and closes the loan information based on cash purchase box
function toggleLoanInfo() {
  var int_value = $('#id_loan_int_rate').val();
  var loan_term = $('#id_loan_term').val();
  if ($('#id_cash_purchase').is(':checked')) {
    $('.toggleLoanDetails').hide();
    $('#id_loan_int_rate').val(0);
    $('#id_loan_term').val(0);
    $('#id_down_payment_2').val($('#id_purchase_price').val());
  } else {
    $('.toggleLoanDetails').show();
    $('#id_loan_int_rate').val('');
    $('#id_loan_term').val('');
    $('#id_down_payment').val('');
    $('#id_down_payment_2').val('');
    $('#id_points').val('');
  }
}

// toggle between % and $ for down payment calculator
$('.toggleLoanDetails > .btn-group > input').click(function() {
    var ix = $(this).index();
    
    $('.downPayment1').toggle( ix === 0 );
    $('.downPayment2').toggle( ix === 2 );
});



// Report Page

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