from django.shortcuts import render
from django.http import HttpResponse


# from Orders.models import OrderLine


# def move(request):
	
# 	# for stat in OrderLine.objects.using('orders').filter(stat.status="Processing"):
# 	# 	print stat.order_id
# 	query = OrderLine.objects.using("orders").all().values()

# 	print query

# 	for key in query:
# 		 for key['order_id'] in key:
# 		 	if key['status'] in ['processing']
# 		 		status=OrderLine.objects.filter





# # 	for key in query:
# # 		if key.status == 'processing':
# # 			print key.order_id


# # #print query

# # 	# for key in query:
# # 	# 	print key.status
# # 	# #rint query


# 	return render(request,"h1.html")	
# 	 	# if stat.status=="Processing":	
# 	 	# 	print stat.using('order').order_id



# Create your views here.
