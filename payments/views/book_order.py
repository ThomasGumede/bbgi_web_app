from campaigns.utils import PaymentStatus
from payments.utilities.yoco_func import headers, decimal_to_str, decimal_to_str
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from payments.ordermodels.storeorder import BookOrder
import requests, logging, json, decimal, base64
from django.urls import reverse

logger = logging.getLogger("payments")

@login_required
def book_payment(request, bookorder_id):
    bookorder = get_object_or_404(BookOrder, id=bookorder_id, paid=False)
    
    if request.method == 'POST':
        
        success_url = request.build_absolute_uri(reverse("payments:book-payment-success", kwargs={"bookorder_id": bookorder.id}))
        cancel_url = request.build_absolute_uri(reverse("payments:book-payment-cancelled", kwargs={"bookorder_id": bookorder.id}))
        fail_url = request.build_absolute_uri(reverse("payments:book-payment-failed", kwargs={"bookorder_id": bookorder.id}))
        str_amount = decimal_to_str(bookorder.amount)

        if bookorder.amount == decimal.Decimal(0.00):
            return redirect("payments:book-payment-success", bookorder.id)
        
        lineitems = [
            {
                "displayName": bookorder.book.title,
                "quantity": 1,
                    "pricingDetails": {
                        "price": int(str_amount)
                    }
            }
        ]
        

        session_data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "failureUrl": fail_url,
            'amount': int(str_amount),
            'currency': 'ZAR',
            'metadata': {
                "checkoutId": f"{bookorder.order_number}"
            },
            "lineItems": lineitems

        }
        data = json.dumps(session_data)
        try:
            response = requests.request("POST", "https://payments.yoco.com/api/checkouts", data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            bookorder.checkout_id = response_data["id"]
            bookorder.status = PaymentStatus.PENDING
            bookorder.save(update_fields=["paid", "checkout_id"])
            return redirect(response_data["redirectUrl"])

        except requests.ConnectionError as err:
            return render(request, "payments/timeout.html", {"err": err})
        
        except requests.HTTPError as err:
            logger.error(f"Yoco - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})
        
        except Exception as err:
            logger.error(f"Yoco - {err}")
            return render(request, "payments/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})
        
    return render(request, 'payments/bbgistore/payment.html', {'order': bookorder})

def book_order_payment_sucessfull(request, bookorder_id):
    bookorder = get_object_or_404(BookOrder, id=bookorder_id)
    return render(request, 'payments/bbgistore/book/order-book-success.html', {'order': bookorder})

def book_order_payment_cancelled(request, bookorder_id):
    bookorder = get_object_or_404(BookOrder, id=bookorder_id)
    return render(request, 'payments/bbgistore/book/order-book-cancelled.html', {'order': bookorder})

def book_order_payment_failed(request, bookorder_id):
    bookorder = get_object_or_404(BookOrder, id=bookorder_id)
    return render(request, 'payments/bbgistore/book/order-book-failed.html', {'order': bookorder})
