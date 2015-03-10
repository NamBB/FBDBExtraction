jQuery(document).ready(function() {	
	
	// supporting different versions of Font Awesome icons
	var icon_classes = jQuery.parseJSON(mrp_frontend_data.icon_classes);
	
	/**
	 * Saves or updates a rating
	 */
	jQuery(".rating-form .save-rating:button").on("click", function(e) {
	
		var ratingItems = [];
		var customFields = [];
		var btnId = e.currentTarget.id; // btnType-ratingFormid-postId-sequence
		var parts = btnId.split("-"); 
		var ratingFormId = parts[1];
		var postId = parts[2];
		var sequence = parts[3];
		
		var hiddenRatingEntryId = "#ratingEntryId-" + ratingFormId + "-" + postId + "-" + sequence;
		var ratingEntryId = jQuery(hiddenRatingEntryId);
		
		// rating items - hidden inputs are used to find all rating items in the rating form
		jQuery('.rating-form input[type="hidden"].rating-item-' + ratingFormId + '-' + postId + '-' + sequence).each(function(index) {			
			
			var ratingItemId = jQuery(this).val();
			
			// get values for rating items
			var element = jQuery('[name=rating-item-' + ratingItemId + '-' + sequence + ']');
			var value = null;
			if (jQuery(element).is(':radio')) {
				value = jQuery('input[type="radio"][name=rating-item-' + ratingItemId + '-' + sequence + ']:checked').val(); 
			} else if (jQuery(element).is('select')) {
				value = jQuery('select[name=rating-item-' +ratingItemId + '-' + sequence + '] :selected').val(); 
			} else {
				value = jQuery('input[type=hidden][name=rating-item-' + ratingItemId + '-' + sequence + ']').val();
			}
			
			var ratingItem = { 'id' : ratingItemId, 'value' : value };
			ratingItems[index] = ratingItem;
			
		});
		
		var name = jQuery('#mrp-name-' + sequence);
		var email = jQuery('#mrp-email-' + sequence);
		var comment = jQuery('#mrp-comment-' + sequence);
		
		// custom fields - hidden inputs are used to find all custom fields in the rating form
		jQuery('.rating-form input[type="hidden"].custom-field-' + ratingFormId + '-' + postId + '-' + sequence).each(function(index) {			
			
			var customFieldId = jQuery(this).val();
			
			// get values for rating items
			var element = jQuery('[name=custom-field-' + customFieldId + '-' + sequence + ']');
			var value = null;
			var type = null;
			if (jQuery(element).is('textarea')) {
				value = jQuery('textarea[name=custom-field-' + customFieldId + '-' + sequence + ']').val(); 
				type = 'textarea';
			} else {
				value = jQuery('input[name=custom-field-' + customFieldId + '-' + sequence + ']').val(); 
				type = 'input';
			}
			
			var customField = { 'id' : customFieldId, 'value' : value, 'type' :  type };
			customFields[index] = customField;
			
		});
	
		var data = {
				action : "save_rating",
				nonce : mrp_frontend_data.ajax_nonce,
				ratingItems : ratingItems,
				name : (name != undefined) ? name.val() : '',
				email : (email != undefined) ? email.val() : '',
				comment : (comment != undefined) ? comment.val() : '',
				customFields : customFields,
				postId : postId,
				ratingFormId : ratingFormId,
				ratingEntryId : (ratingEntryId != undefined) ? ratingEntryId.val() : '',
				sequence : sequence
		};
		
		var temp = ratingFormId + '-' + postId +'-' + sequence;
		var spinnerId = 'mrp-spinner-' + temp;
		
		jQuery('<i style="margin-left: 10px;" id="' + spinnerId + '" class="' + icon_classes.spinner + '"></i>').insertAfter('input#' + btnId);
	
		jQuery.post(mrp_frontend_data.ajax_url, data, function(response) {
				handle_rating_form_submit_response(response);
		});
		
	});
	
	/**
	 * Deletes an existing rating
	 */
	jQuery(".rating-form .delete-rating:button").on("click", function(e) { 
		
		var btnId = e.currentTarget.id; // btnType-ratingFormid-postId-sequence
		var parts = btnId.split("-"); 
		var ratingFormId = parts[1];
		var postId = parts[2];
		var sequence = parts[3];
		
		var hiddenRatingEntryId = "#ratingEntryId-" + ratingFormId + "-" + postId + "-" + sequence;
		var ratingEntryId = jQuery(hiddenRatingEntryId);
		
		var data = {
				action : "delete_rating",
				nonce : mrp_frontend_data.ajax_nonce,
				postId : postId,
				ratingFormId : ratingFormId,
				ratingEntryId : (ratingEntryId != undefined) ? ratingEntryId.val() : '',
				sequence : sequence
		};
		
		var temp = ratingFormId + '-' + postId +'-' + sequence;
		var spinnerId = 'mrp-spinner-' + temp;
		
		jQuery('<i style="margin-left: 10px;" id="' + spinnerId + '"class="' + icon_classes.spinner + '"></i>').insertAfter('input#saveBtn-' + temp);	
	
		jQuery.post(mrp_frontend_data.ajax_url, data, function(response) {
				handle_rating_form_submit_response(response);
		});
		
	});
	
	/**
	 * Handles rating form submit response
	 */
	function handle_rating_form_submit_response(response) {
		
		var jsonResponse = jQuery.parseJSON(response);
		
		var ratingForm = jQuery("form[name=rating-form-" + jsonResponse.data.rating_form_id + "-" 
				+ jsonResponse.data.post_id + "-" + jsonResponse.data.sequence + "]");
		
		// update rating results if success
		if (jsonResponse.status == 'success') {
			var ratingResult = jQuery(".rating-result-" + jsonResponse.data.rating_form_id + "-" 
					+ jsonResponse.data.post_id).filter(".mrp-filter");
			
			if (ratingResult) {
				ratingResult.replaceWith(jsonResponse.data.html);
			}
		}
		
		// update messages
		if ( (jsonResponse.validation_results && jsonResponse.validation_results.length > 0) || jsonResponse.message ) {
			var messages = '';
			
			if ( jsonResponse.validation_results ) {
				var $index = 0;
				for ($index; $index< jsonResponse.validation_results.length; $index++) {
					messages += '<p class="message ' + jsonResponse.validation_results[$index].severity + '">' 
							+ jsonResponse.validation_results[$index].message + '</p>';
				}
			}
			
			if (jsonResponse.message) {
				messages += '<p class="message ' + jsonResponse.status + '">' 
						+ jsonResponse.message + '</p>';
			}
			
			if (ratingForm && ratingForm.parent().find('.message')) {
				ratingForm.parent().find('.message').remove();
			}
			
			if (ratingForm && ratingForm.parent()) {
				ratingForm.before(messages);
			}
		}
		
		// remove rating form if success
		if ( jsonResponse.status == 'success' && jsonResponse.data.hide_rating_form == true && ratingForm) {
			ratingForm.remove();
		}
		
		var temp = jsonResponse.data.rating_form_id + "-" + jsonResponse.data.post_id + "-" + jsonResponse.data.sequence;
		var spinnerId = 'mrp-spinner-' + temp;
		jQuery("#" + spinnerId).remove();
		
		// if rating has been deleted, update submit button text
		if (jsonResponse.data.submit_btn_text) {
			jQuery("#saveBtn-" + temp).attr('value', jsonResponse.data.submit_btn_text);
			jQuery("#deleteBtn-" + temp).remove();
			jQuery("#entryId-" + temp).remove();
		}
		
	}
	
	
	/**
	 * Selected rating item value on hover and click
	 */
	var ratingItemStatus = {};
	
	var useCustomStarImages = jQuery.parseJSON(mrp_frontend_data.use_custom_star_images);
	
	jQuery(".mrp-star-rating-select .mrp-star-empty, .mrp-star-rating-select .mrp-star-full").on("click", function(e) {
		
		updateRatingItemStatus(this.id, 'clicked');
		
		if (useCustomStarImages == true ) {
			jQuery(this).not('.mrp-minus').removeClass('mrp-custom-empty-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-full-star');
			jQuery(this).prevAll().not('.mrp-minus').removeClass('mrp-custom-empty-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-full-star');
			jQuery(this).nextAll().not('.mrp-minus').removeClass('mrp-custom-full-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-empty-star');
		} else {
			jQuery(this).not('.mrp-minus').removeClass(icon_classes.star_empty + " mrp-star-hover").addClass(icon_classes.star_full);
			jQuery(this).prevAll().not('.mrp-minus').removeClass(icon_classes.star_empty + " mrp-star-hover").addClass(icon_classes.star_full);
			jQuery(this).nextAll().not('.mrp-minus').removeClass(icon_classes.star_full + " mrp-star-hover").addClass(icon_classes.star_empty);
		}
		
		updateSelectedHiddenValue(this);
	});
	
	jQuery(".mrp-star-rating-select .mrp-minus").on("click", function(e) {
		
		updateRatingItemStatus(this.id, '');
		
		if (useCustomStarImages == true) {
			jQuery(this).not('.mrp-minus').removeClass('mrp-custom-empty-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-full-star');
			jQuery(this).prevAll().not('.mrp-minus').removeClass('mrp-custom-empty-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-full-star');
			jQuery(this).nextAll().not('.mrp-minus').removeClass('mrp-custom-full-star mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-empty-star');

		} else {
			jQuery(this).not('.mrp-minus').removeClass(icon_classes.star_empty + " mrp-star-hover").addClass(icon_classes.star_full);
			jQuery(this).prevAll().not('.mrp-minus').removeClass(icon_classes.star_empty + " mrp-star-hover").addClass(icon_classes.star_full);
			jQuery(this).nextAll().not('.mrp-minus').removeClass(icon_classes.star_full + " mrp-star-hover").addClass(icon_classes.star_empty);
		}
		
		updateSelectedHiddenValue(this);
	});
	
	jQuery(".mrp-star-rating-select .mrp-minus, .mrp-star-rating-select .mrp-star-empty, .mrp-star-rating-select .mrp-star-full").on("mouseenter mouseleave", function(e) {

		var elementId = this.id;
		var ratingItemIdSequence = getRatingItemIdSequence(elementId);
		
		if (ratingItemStatus[ratingItemIdSequence] != 'clicked' && ratingItemStatus[ratingItemIdSequence] != undefined) {
			
			updateRatingItemStatus(this.id, 'hovered');
			
			if (useCustomStarImages == true) {
				jQuery(this).not('.mrp-minus').removeClass('mrp-custom-empty-star').addClass('mrp-custom-hover-star mrp-star-hover');
				jQuery(this).prevAll().not('.mrp-minus').removeClass('mrp-custom-empty-star').addClass('mrp-custom-hover-star mrp-star-hover');
				jQuery(this).nextAll().not('.mrp-minus').removeClass('mrp-custom-hover-star mrp-star-hover').addClass('mrp-custom-empty-star');	

			} else {
				jQuery(this).not('.mrp-minus, .exclude-zero').removeClass(icon_classes.star_empty).addClass(icon_classes.star_full + " mrp-star-hover");
				jQuery(this).prevAll().not('.mrp-minus, .exclude-zero').removeClass(icon_classes.star_empty).addClass(icon_classes.star_full + " mrp-star-hover");
				jQuery(this).nextAll().not('.mrp-minus, .exclude-zero').removeClass(icon_classes.star_full + " mrp-star-hover").addClass(icon_classes.star_empty);	
			}
		}
	});
	
	jQuery(".thumbs-select .mrp-thumbs-down-on, .thumbs-select .mrp-thumbs-down-off").click(function(e) {
		jQuery(this).removeClass(icon_classes.down_up_off).addClass(icon_classes.thumbs_down_on);
		jQuery(this).next().removeClass(icon_classes.thumbs_up_on).addClass(icon_classes.thumbs_up_off);
		
		updateSelectedHiddenValue(this);
	});
	
	jQuery(".thumbs-select .mrp-thumbs-up-on, .thumbs-select .mrp-thumbs-up-off").click(function(e) {
		jQuery(this).removeClass(icon_classes.thumbs_up_off).addClass(icon_classes.thumbs_up_on);
		jQuery(this).prev().removeClass(icon_classes.thumbs_down_on).addClass(icon_classes.thumbs_down_off);
		
		updateSelectedHiddenValue(this);
	});
	
	// now cater for touch screen devices
	var touchData = {
		started : null, // detect if a touch event is sarted
		currrentX : 0,
		yCoord : 0,
		previousXCoord : 0,
		previousYCoord : 0,
		touch : null
	};
	
	jQuery(".mrp-star-rating-select .mrp-star-empty, .mrp-star-rating-select .mrp-star-full, .mrp-star-rating-select .mrp-minus, " +
			".thumbs-select .mrp-thumbs-up-on, .thumbs-select .mrp-thumbs-up-off, .thumbs-select .mrp-thumbs-down-on, " +
			".thumbs-select .mrp-thumbs-down-on").on("touchstart", function(e) {
		touchData.started = new Date().getTime();
		var touch = e.originalEvent.touches[0];
		touchData.previousXCoord = touch.pageX;
		touchData.previousYCoord = touch.pageY;
		touchData.touch = touch;
	});
	
	jQuery(".mrp-star-rating-select .mrp-star-empty, .mrp-star-rating-select .mrp-star-full, .mrp-star-rating-select .mrp-minus").on("touchend touchcancel", function(e) {
			var now = new Date().getTime();
			// Detecting if after 200ms if in the same position.
			if ((touchData.started !== null)
					&& ((now - touchData.started) < 200)
					&& (touchData.touch !== null)) {
				var touch = touchData.touch;
				var xCoord = touch.pageX;
				var yCoord = touch.pageY;
				if ((touchData.previousXCoord === xCoord)
						&& (touchData.previousYCoord === yCoord)) {
					
					if (useCustomStarImages == true) {
						jQuery(this).removeClass('mrp-custom-empty-star').addClass('mrp-custom-full-star');
						jQuery(this).prevAll().removeClass('mrp-custom-empty-star').addClass('mrp-custom-full-star');
						jQuery(this).nextAll().removeClass('mrp-custom-full-star').addClass('mrp-custom-empty-star');
					} else {
						jQuery(this).not('.mrp-minus').removeClass(icon_classes.star_empty).addClass(icon_classes.star_full);
						jQuery(this).prevAll().not('.mrp-minus').removeClass(icon_classes.star_empty).addClass(icon_classes.star_full);
						jQuery(this).nextAll().not('.mrp-minus').removeClass(icon_classes.star_full).addClass(icon_classes.star_empty);
					}
					updateSelectedHiddenValue(this);
				}
			}
			touchData.started = null;
			touchData.touch = null;
	});
	jQuery(".thumbs-select .mrp-thumbs-down-off, .thumbs-select .mrp-thumbs-down-on").on( "touchend touchcancel", function(e) {
			var now = new Date().getTime();
			// Detecting if after 200ms if in the same position.
			if ((touchData.started !== null)
					&& ((now - touchData.started) < 200)
					&& (touchData.touch !== null)) {
				var touch = touchData.touch;
				var xCoord = touch.pageX;
				var yCoord = touch.pageY;
				if ((touchData.previousXCoord === xCoord)
						&& (touchData.previousYCoord === yCoord)) {
					
					jQuery(this).removeClass(icon_classes.thumbs_down_off).addClass(icon_classes.thumbs_down_on);
					jQuery(this).next().removeClass(icon_classes.thumbs_up_on).addClass(icon_classes.thumbs_up_off);
					
					updateSelectedHiddenValue(this);
				}
			}
			touchData.started = null;
			touchData.touch = null;
	});
	
	jQuery(".thumbs-select .mrp-thumbs-up-off, .thumbs-select .mrp-thumbs-up-on").on( "touchend touchcancel", function(e) {
			var now = new Date().getTime();
			// Detecting if after 200ms if in the same position.
			if ((touchData.started !== null)
					&& ((now - touchData.started) < 200)
					&& (touchData.touch !== null)) {
				var touch = touchData.touch;
				var xCoord = touch.pageX;
				var yCoord = touch.pageY;
				if ((touchData.previousXCoord === xCoord)
						&& (touchData.previousYCoord === yCoord)) {
					
					jQuery(this).removeClass(icon_classes.thumbs_up_off).addClass(icon_classes.thumbs_up_on);
					jQuery(this).next().removeClass(icon_classes.thumbs_down_on).addClass(icon_classes.thumbs_down_off);
					
					updateSelectedHiddenValue(this);
				}
			}
			touchData.started = null;
			touchData.touch = null;
	});	
	
	/**
	 * Updates the rating item status to either hovered or clicked
	 */
	function updateRatingItemStatus(elementId, status) {
		var ratingItemIdSequence = getRatingItemIdSequence(elementId);
		if (ratingItemIdSequence != null) {
			ratingItemStatus[ratingItemIdSequence] = status;
		}
	}
	
	/**
	 * Retrieves the rating item id sequence used to store the status of a rating item option
	 */
	function getRatingItemIdSequence(elementId) {
		var parts = elementId.split("-"); 
		
		var ratingItemId = parts[4]; /// skip 2: rating-item-
		var sequence = parts[5];
		
		var ratingItemIdSequence = 'rating-item-' + ratingItemId + '-' + sequence;
		return ratingItemIdSequence;
	}
	
	/**
	 * Updates the selected hidden value for a rating item
	 */
	function updateSelectedHiddenValue(element) {
		
		// id is in format "index-3-rating-item-2-1"
		var elementId = element.id;
		
		var parts = elementId.split("-"); 
		var value = parts[1]; // this is the star index
		var ratingItemId = parts[4]; /// skipt 2: rating-item-
		var sequence = parts[5];
		    		
		// update hidden value for storing selected option
		var hiddenValue = '#rating-item-'+ ratingItemId + '-' + sequence;
		
		if (jQuery("#" + elementId).hasClass("exclude-zero") && value == 0) {
			var newElementId = '#index-1-rating-item-' + ratingItemId + '-' + sequence;
			jQuery(newElementId).removeClass(icon_classes.star_empty);
			jQuery(newElementId).addClass(icon_classes.star_full);
			value = 1;
		}
		    		
		jQuery(hiddenValue).val(value);
	}
	
	
	jQuery("#include-rating").change(function() {
		if (this.checked) {
			jQuery("p.mrp-comment-form-field").show("slow", function() {} );
		} else {
			jQuery("p.mrp-comment-form-field").hide("slow", function() {} );
		}
	});
});