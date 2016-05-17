
$(document).ready(function() {

	$("<style type='text/css'> .datepicker th, .datepicker td{ cursor: pointer;} </style>").appendTo("head");
	
	$('span.search-filters').append('<input  type="text" id="datepickers" placeholder="PickUpDate" />');
	
	$('span.search-filters').append("<input type= 'hidden'  id='pick_request'  />"); 
	
	var date=$('#datepickers').datetimepicker({timepicker:false,format:'20y-m-d 00:00:00' ,defaultDate:false});

	console.log(date);
	$('select[data-name="pickup_date"]').remove();
	$("#datepickers").on('change',function(){

		 $('#datepickers').attr("name","pickup_date__gte");
				 $('#pick_request').attr("name","pickup_date__lt");

		django_date=$(this).val();
		console.log(django_date);

		arr=django_date.split('-');

		date_value=parseInt(arr[2])+1;
		console.log(arr);
		if (arr[2].length==1)
		{
		}
		else
		{

		date_actual=arr[0]+'-'+arr[1]+'-'+date_value+" 00:00:00";	
		}

		console.log(date_actual);
		
	$('#pick_request').val(date_actual) ; 		
	});


	$.urlParam = function(name){
	    var results = new RegExp('[\&]' + name + '=([^&#]*)').exec(window.location.href);
	    console.log(results);
	    if (results==null){
	       return " ";
	    }
	    else{	
	       return results[1] || 0;
	    }
	}

	fetched=decodeURIComponent($.urlParam('pickup_date__gte')); 
	console.log($.urlParam('pickup_date__gte'));
	console.log(fetched,'==========fetcjed');
	fetched=fetched.replace('+',' ');	
	console.log(fetched);
	$('#datepickers').css('cursor', 'hand');

		$('#datepickers').val(fetched);


});