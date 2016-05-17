
$(document).ready(function() {


	$form1=$('<form method="post" action="http://'+window.location.href.split("/")[2]+'/admin/orders/get_check" name="form1" id="form1"></form>')
	$form1.insertBefore('#changelist-search');
	$form1.append('<input type="submit" name="po" id="PO" value="PDF"/>');

	$('<input>', {
    type: 'hidden',
    id: 'request',
    name: 'hidden',
    value: 'hide'
}).appendTo($form1);
	$('#form1').css({'position':"absolute","right":"300px","display":"inline-block"});

	$('#PO').css({"background-color": "#5bb75b","border":" none","text-shadow": "2px 1px #000000","line-height":"15px","color": "white","padding":"7px","text-align": "center","text-decoration": "none","display": "inline-block","font-size": "16px","border-radius":"7px",	"border":"1px solid rgb(dark-black)"});

	$("#PO").click(function (){
		console.log('start');
		objects={};
		objects['selected_val']= [];
		$(".action-checkbox").find("input").each(function(){
		if ($(this).prop('checked')==true){
			objects['selected_val'].push($(this).val());
			
			}

	});
		console.log(objects['selected_val']);
		$('#request').val(objects['selected_val']);
					

		
	});
$form2=$('<form method="post" action="http://'+window.location.href.split("/")[2]+'/admin/orders/get_check" name="form2" id="form1"></form>')
$form2.insertBefore('#changelist-search');
		
$form2.append('<input type="submit" name="doc" id="doc_button" value="DOC"/>');
	
$('<input>', {
    type: 'hidden',
    id: 'doc_request',
    name: 'hidden_doc',
    value: 'hide'
}).appendTo($form2);
	$('#form2').css({'position':"absolute","display":"inline-block"});
	$('input[name="doc"]').css({"position":"absolute","line-height":"15px","right":"239px","background-color": "#5bb75b","border":"1px solid rgb(black)","color": "white","padding":"7px","text-align": "center","text-decoration": "none","display": "inline-block","font-size": "16px","border-radius":"7px","width":"50px"});
	$("#doc_button").click(function (){
		console.log('start');
		objects={};
		objects['selected_val']= [];
		$(".action-checkbox").find("input").each(function(){
		if ($(this).prop('checked')==true){
			objects['selected_val'].push($(this).val());
			
			}

	});
		$('#doc_request').val(objects['selected_val']);
					

		
	});

	


});