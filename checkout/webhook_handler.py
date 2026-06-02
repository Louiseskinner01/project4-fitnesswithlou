from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product
from users.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send confirmation email to user"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        username = intent.metadata.username

        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = charge.billing_details
        grand_total = round(charge.amount / 100, 2)

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = billing_details.phone
                    profile.default_street_address1 = billing_details.address.line1
                    profile.default_street_address2 = billing_details.address.line2
                    profile.default_town_or_city = billing_details.address.city
                    profile.default_postcode = billing_details.address.postal_code
                    profile.default_country = billing_details.address.country
                    profile.save()
            except UserProfile.DoesNotExist:
                pass

        # Check if order exists
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                   
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found',
                status=500)

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)