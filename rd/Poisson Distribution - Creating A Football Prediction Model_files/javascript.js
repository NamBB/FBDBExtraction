jQuery('document').ready(function(){
	jQuery('a#set_decimal').click(function(){ switch_oddsformat('decimal'); });
	jQuery('a#set_moneyline').click(function(){ switch_oddsformat('moneyline'); });
	jQuery('a#set_fractional').click(function(){ switch_oddsformat('fractional'); });	jQuery('a#set_hongkong').click(function(){ switch_oddsformat('hongkong'); });	jQuery('a#set_indonesian').click(function(){ switch_oddsformat('indonesian'); });	jQuery('a#set_malaysian').click(function(){ switch_oddsformat('malaysian'); });
});

//switcher
function switch_oddsformat(format)
{
	jQuery('a#set_decimal, a#set_moneyline, a#set_fractional, a#set_hongkong, a#set_indonesian, a#set_malaysian').removeClass('active');
	jQuery('a#set_'+format).addClass('active');
	jQuery('span.odds span').hide();
	jQuery('span.odds span.'+format).fadeIn();
	var now = new Date();
	var expireTime = now.getTime() + (24*3600*259200000);
	now.setTime(expireTime);
	document.cookie = 'odds_format='+format+'; expires='+now.toGMTString()+';path=/';
}

//calculator
jQuery('document').ready(function(){
	jQuery('span#span_moneyline').click(function(){ jQuery('input#moneyline').val('+190'); jQuery('input#decimal,input#fractional, input#hongkong, input#indonesian, input#malaysian').val(''); });
	jQuery('span#span_decimal').click(function(){ jQuery('input#decimal').val('2.80'); jQuery('input#hongkong,input#fractional, input#moneyline, input#indonesian, input#malaysian').val(''); });
	jQuery('span#span_fractional').click(function(){ jQuery('input#fractional').val('1/3'); jQuery('input#decimal,input#hongkong, input#moneyline, input#indonesian, input#malaysian').val(''); });
	jQuery('input#moneyline').bind('keyup change', function(){ if(jQuery('input#moneyline').val().length > 0) { jQuery('input#decimal,input#fractional, input#hongkong, input#indonesian, input#malaysian').val(''); } if(jQuery('input#moneyline').val().charAt(0) != '+' && jQuery('input#moneyline').val().charAt(0) != '-' && jQuery('input#moneyline').val().length > 0) { jQuery('input#moneyline').val('+'+jQuery('input#moneyline').val()); } });
	jQuery('input#decimal').bind('keyup change', function(){ if(jQuery('input#decimal').val().length > 0) { jQuery('input#hongkong,input#fractional, input#moneyline, input#indonesian, input#malaysian').val(''); } jQuery('input#decimal').val(jQuery('input#decimal').val().replace(',', '.')); });
	jQuery('input#fractional').bind('keyup change', function(){ if(jQuery('input#fractional').val().length > 0) { jQuery('input#decimal,input#hongkong, input#moneyline, input#indonesian, input#malaysian').val(''); } });			jQuery('input#hongkong').bind('keyup change', function(){ if(jQuery('input#hongkong').val().length > 0) { jQuery('input#decimal,input#fractional, input#moneyline, input#indonesian, input#malaysian').val(''); } });		jQuery('input#indonesian').bind('keyup change', function(){ jQuery('input#decimal,input#fractional, input#moneyline, input#hongkong, input#malaysian').val('');  });		jQuery('input#malaysian').bind('keyup change', function(){ jQuery('input#decimal,input#fractional, input#moneyline, input#hongkong, input#indonesian').val('');  });	
	jQuery('input.odds_button').click(function(){
		
		var decimal = jQuery('input#decimal').val();
		var fractional = jQuery('input#fractional').val();				var moneyline = jQuery('input#moneyline').val();				var hongkong = jQuery('input#hongkong').val();				var indonesian = jQuery('input#indonesian').val();				var malaysian = jQuery('input#malaysian').val();
		if(moneyline.length > 0)
	  	{
			moneyline = moneyline.replace('+', '');
			var allowedchars = '0123456789-';
			var error = 0;
			for (var i = 0; i < moneyline.length; i++) { if(allowedchars.replace(moneyline[i], '') == allowedchars) { error = 1; } }
			if(error == 0)
	 		{
	 			 jQuery.get(document.ajax_url, { val: moneyline, from: 'moneyline', to: 'decimal'}, function(resp){ jQuery('input#decimal').val(resp); });  
	 			 jQuery.get(document.ajax_url, { val: moneyline, from: 'moneyline', to: 'fractional'}, function(resp){ jQuery('input#fractional').val(resp); });  				 				 jQuery.get(document.ajax_url, { val: moneyline, from: 'moneyline', to: 'hongkong'}, function(resp){ jQuery('input#hongkong').val(resp);});				 jQuery.get(document.ajax_url, { val: moneyline, from: 'moneyline', to: 'indonesian'}, function(resp){ jQuery('input#indonesian').val(resp);});				 				 jQuery.get(document.ajax_url, { val: moneyline, from: 'moneyline', to: 'malaysian'}, function(resp){ jQuery('input#malaysian').val(resp);});
			}
			else
			{
				alert('Error: invalid moneyline input.');
			}
		}
		else if(decimal.length > 0)
		{
			var allowedchars = '0123456789.';
			var error = 0;
			for (var i = 0; i < decimal.length; i++) { if(allowedchars.replace(decimal[i], '') == allowedchars) { error = 1; } }
			if(error == 0)
			{
				   
	 			 jQuery.get(document.ajax_url, { val: decimal, from: 'decimal', to: 'fractional'}, function(resp){ jQuery('input#fractional').val(resp); }); 				 				 jQuery.get(document.ajax_url, { val: decimal, from: 'decimal', to: 'moneyline'}, function(resp){ jQuery('input#moneyline').val(resp); });				 				 jQuery.get(document.ajax_url, { val: decimal, from: 'decimal', to: 'hongkong'}, function(resp){ jQuery('input#hongkong').val(resp);});				 jQuery.get(document.ajax_url, { val: decimal, from: 'decimal', to: 'indonesian'}, function(resp){ jQuery('input#indonesian').val(resp);});				 				 jQuery.get(document.ajax_url, { val: decimal, from: 'decimal', to: 'malaysian'}, function(resp){ jQuery('input#malaysian').val(resp);});				 
			}
			else
			{
				alert('Error: invalid decimal input.');
			}
		}								
		else if(fractional.length > 0)
	  	{
			var allowedchars = '0123456789/';	
			var error = 0;
			for (var i = 0; i < fractional.length; i++) { if(allowedchars.replace(fractional[i], '') == allowedchars) { error = 1; } } 
			if(error == 0)
			{
				   
	 			 jQuery.get(document.ajax_url, { val: fractional, from: 'fractional', to: 'decimal'}, function(resp){ jQuery('input#decimal').val(resp); });				 				  jQuery.get(document.ajax_url, { val: fractional, from: 'fractional', to: 'moneyline'}, function(resp){ jQuery('input#moneyline').val(resp); });				 				 jQuery.get(document.ajax_url, { val: fractional, from: 'fractional', to: 'hongkong'}, function(resp){ jQuery('input#hongkong').val(resp);});				 jQuery.get(document.ajax_url, { val: fractional, from: 'fractional', to: 'indonesian'}, function(resp){ jQuery('input#indonesian').val(resp);});				 				 jQuery.get(document.ajax_url, { val: fractional, from: 'fractional', to: 'malaysian'}, function(resp){ jQuery('input#malaysian').val(resp);});				 				 
			}
			else
			{
				alert('Error: invalid fractional input.');
			}
		}
		if(jQuery('input#moneyline').val() == -100) { jQuery('input#moneyline').val('+100'); }
	});
});