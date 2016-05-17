PO={
'head_po' :'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Untitled Document</title>
<link href="/home/bhaskar/Desktop/order-processing/default.css" type="text/css" rel="stylesheet" />

</head>

<body>

<table class="manor_table" >

<tr class="wrapper_manor"  >
		<td >
			<img src="/home/bhaskar/Downloads/trydjango/supplified-cms/manorkart.png" alt="image" width="300" height="150" />
		</td>	

		<td class="manor_add">
			<h3 style="margin:0px; font-size:14px;">%s</h3>
			<p style="font-size: 12px; margin-top: 0px;">K-3/40-A ,West Ghonda<br>		
			Shahdara, New Delhi<br>		
			Delhi-110053<br>
			Contact no :012-3456-7890<br>		
			Email:manorkartretail@gmail.com<br>		
			CIN:U74999DL2015PTC283111		</p>
			</td>			
		</tr>
</div>


</table>
''',
'head_invoice':
'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Untitled Document</title>
<link href="/home/bhaskar/Downloads/trydjango/supplified-cms/default.css" type="text/css" rel="stylesheet" />

</head>

<body>

<table>
<tr>
	<td width="500px">

	<b>Sold by</b>
	</td>		
		<td >
			<img src= alt="image" width="300" height="150" />
		</td>	

				
		</tr>
</div>


</table>''',


'body_invoice':'''			
<div class="purchase" style="width:100%">
INVOICE
</div>



<table style="margin:5px;">				
	<tr>

		<td class='pick_up'>
			Invoice Number : {{ po_date }}<br>
			Invoice Date :{{ created_date }}
		</td>
	</tr>
</table>


<table class="wrap_sup_bill" >

	<td class="bill_wrap">
			<h3 style="margin:0px; font-size:14px;">{{ seller }}</h3>
			<p style="font-size: 12px; margin-top: 0px;">{{ value.0.seller_address }}<br>			
			{{ value.0.seller_city }}<br>
			Contact no :{{ value.0.seller_phone }}<br>		
			Email:{{ value.0.seller_email }}<br>		
			CIN:U74999DL2015PTC283111		</p>
			</td>
	</tr>

</table>

	
<table class="wrap_sup_bill" >

	<tr class="supplier">
			<td class="supplier_details" style="width:214pt;display:inline-block;">

			Bill to
			</td>
			<td class ="supplier_details" style=" display: inline-block; width:350px;" >
			Ship	
			</td>
	</tr>
	<tr style="position: relative;display: block; font-size:12px;">
		<td style="width: 214pt; display: inline-block;">
			<br>
			{{ customer_address }}<br>
			Pincode:  {{ pincode }}<br>
			Contact /Mobile No.:{{ customer_s_phone }}	<br>
			Landline No. {{ user_phone }}			 <br>
			Email :{{ email }}
		</td>

	<td class="bill_wrap" >
			{{ customer_s_address }}					<br>
			{{ customer_s_city}},{{ customer_s_state}}<br>
			{{ customer_s_pincode }}				<br>
			Contact /Mobile No.:{{ 	customer_s_phone }}<br>
			Landline No. {{ user_phone }}		

	</td>
	</tr>

</table>

	<h3 style='background-color:blue;text-align:center;color:white;'>Order Details</h3>

	<table border="1" class="product-detail-table">
		<thead>
			<tr>
				<td>S.NO.</td><td>Code</td>	<td>Product Desc.</td><td>Model No.</td><td>Qty.</td><td>UOM</td><td>Unit Rate</td><td>Tax Type</td><td>Tax Rate %</td><td>Tax Amount</td><td>Amount</td>
			</tr>
		</thead>
		<tbody>
		{% for each in value %}
		<tr>
			<td>S.NO.</td><td>Code</td>	<td>{{ each.product_title }}</td><td>Model No.</td><td>{{ each.product_qty }}</td><td>UOM</td><td>{{ each.unit_price }}</td><td>Tax Type</td><td>{{ each.vat_rate }}%</td><td>{{ each.total_vat }}</td><td>{{ each.subtotal }}</td>
		</tr>
		{% endfor %}
		</tbody>
		
		<tfoot>
			<tr >
			<td colspan="10">Sub-total</td>
			<td> {{ sum }} </td>
			</tr>
			<tr >
			<td colspan="10">Add:Additional Freight</td>
			<td>  </td>
			</tr>
			<tr >
			<td colspan="10">Other Charges</td>
			<td>   </td>
			</tr>
			<tr >
			<td colspan="10">Add:Tax Amount</td>
			<td> {{ total_tax }}  </td>
			</tr>
		
			<tr >
			<td colspan="10">Round-off</td>
			<td> {{ round_off }}</td>
			</tr>
			<tr>
			<td colspan="10">Total Order Value (Inclusive of all Incidental charges and Taxes) In Rupees</td>
			<td>{{ total_value }}</td>
			</tr>
			<tr>
			<td colspan="10">Total Order Value In words</td>
			<td> {{ in_words }}</td>
			</tr>
		</tfoot>

	</table> '''
,

'body_po':
'''
			
<div class="purchase" style="width:100%">
		PURCHASE ORDER
</div>



<table style="margin:5px;">				
	<tr>
		<td class="po_details">
			Order Ref.No.:{{	order_ref }} <br>
			PO Number:   		<br>
			PO Date:{{ po_date }}	<br>
			PO Valid Till:
		</td>

		<td class='pick_up'>
			Pickup Date: {{ pickup_date }}<br>
			PickupTime(Approx.){{ pickup_time }}
		</td>
	</tr>
</table>


<table class="wrap_sup_bill" >

	<tr class="supplier">
			<td class="supplier_details" style="width:214pt;display:inline-block;">
						Supplier Details
			</td>
			<td class ="supplier_details" style=" display: inline-block; width:350px;" >
				BILLING ADDRESS	
			</td>
	</tr>
	<tr style="position: relative;display: block;">
		<td style="width: 214pt; display: inline-block;">
			<br>
			Seller Details : {{	value.0.store_name }}<br>
			Pincode:  {{ pincode }}<br>
			PAN Number:	 			<br>
			Contact /Mobile No.:{{ value.0.seller_phone }}	<br>
			Landline No. 			 <br>
			Email :{{ email }}
		</td>

	<td class="bill_wrap" >
		
			Manor Kart Retail Private Limited		<br>
			Address : Warehouse registered			<br>
			with Vat department						<br>
			New Delhi-11053							<br>
			STATE :									<br>
			PAN : AAJCM8498G 						<br>
			VAT/TIN:								<br>
			CST Number:								<br>
			
	</td>
	</tr>

</table>


	<h3 style='background-color:blue;text-align:center;color:white;'>Order Details</h3>

	<table border="1" class="product-detail-table">
		<thead>
			<tr>
				<td>S.NO.</td><td>Code</td>	<td>Product Desc.</td><td>Model No.</td><td>Qty.</td><td>UOM</td><td>Unit Rate</td><td>Tax Type</td><td>Tax Rate %</td><td>Tax Amount</td><td>Amount</td>
			</tr>
		</thead>
		<tbody>
		{% for each in value %}
		<tr>
			<td>S.NO.</td><td>Code</td>	<td>{{ each.product_title }}</td><td>Model No.</td><td>{{ each.product_qty }}</td><td>UOM</td><td>{{ each.unit_price }}</td><td>Tax Type</td><td>{{ each.vat_rate }}%</td><td>{{ each.total_vat }}</td><td>{{ each.subtotal }}</td>
		</tr>
		{% endfor %}
		</tbody>
		
		<tfoot>
			<tr >
			<td colspan="10">Sub-total</td>
			<td> {{ sum }} </td>
			</tr>
			<tr >
			<td colspan="10">Add:Additional Freight</td>
			<td>  </td>
			</tr>
			<tr >
			<td colspan="10">Other Charges</td>
			<td>   </td>
			</tr>
			<tr >
			<td colspan="10">Add:Tax Amount</td>
			<td> {{ tota_tax }}  </td>
			</tr>
		
			<tr >
			<td colspan="10">Round-off</td>
			<td> {{ round_off }}</td>
			</tr>
			<tr>
			<td colspan="10">Total Order Value (Inclusive of all Incidental charges and Taxes) In Rupees</td>
			<td>{{ total_value }}</td>
			</tr>
			<tr>
			<td colspan="10">Total Order Value In words</td>
			<td> {{ in_words }}</td>
			</tr>
		</tfoot>

	</table>
''',

'foot_invoice':
'''

<div class='para-term'>

*This is a computer generated Invoice.<br>
<pre style="font-size:12px;">

                      			    For Manor Kart Retail Private Limited<br>
					  	(Authorized Signatory)<br>
						  Ordered through:<br>
					  	www.supplified.com/assets/ap <br>
</pre>
Customer Care 999999995, <a href="www.supplified.com"> www.supplified.com</a> <br>



To return an item, visit <a href="www.supplified.com"> www.supplified.com</a> <br>
For more information on your order, visit <a href="www.supplified.com"> www.supplified.com</a><br>








</body>


</html>
''',

'foot_po':
'''
<div class='para-term'>
<b>TERMS & CONDITIONS:</b><br>
This Purchase order, together with standard terms and conditions, and any attachments and exhibits, specifications, drawings, notes, instructions and other information, whether physically attached or incorporated by reference (collectively the "Purchase Order"), constitutes the entire & exclusive agreement between ("PURCHASER") & ("SUPPLIER") as identified in this Purchase Order. Notwithstanding the foregoing, if a master agreement covering procurement of the Products / Material / Goods or Work described in this Purchase Order exists between "SUPPLIER" and "PURCHASER", the terms of such master agreement shall prevail over any inconsistent terms herein.<br>
1. Payment terms 	within 30 days from date of invoice.<br>
2. Quality Standard Compliance to relevant IS / ASTM Standard<br>
3.Road Permit<br>
4.Test Certificate<br>
5.Warranty/Gurantee As per manufacturer's warranty policy.<br>
6.You shall provide only approved quality of material, any inferior quality provided has to be replaced by you at your own risk and cost.<br>
7.In case you fail to supply the material to our requirement, we reserve all rights to withhold your payment and arrange supply from any other agency at your risk and cost.<br>
8.All disputes are to be settled at Delhi jurisdiction.<br>
9.For billing on local vat, only tax invoice is acceptable<br>
10.All the tax liabilities e.g. sales tax, excise duty etc. shall be applicable as per government policy at the time of delivery of material.<br>
11.Billing address has to be given on the bill as shown on top of the purchase order.<br>
12.Manor Kart will return products in all the following cases:-<br>
Size/dimension mismatch in comparison to the ordered materials/products.
Significantly different from the description given by the merchant ( wrong size, color, quality or material related issues)
The packet was empty / some item or accessory was missing
Defective items/malfunctioning materials/products are received.<br>
Not conforming to the specified compliance standard with a test certificate from accredited testing laboratory.<br>
13. Please acknowledge the order by mailing a line of acceptance of the same to manorkartretail@gmail.com for our record purpose.
<br>
14. After acceptance of order the consignment should be kept ready to be picked by our logistics partner.<br></div>
<pre style="width:400px;font-size:12px;">
Prepared by 			Checked by				Approved By
(Operation)				(Taxation)				(Operation)
</pre>'''

}