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
    """
    Handle Stripe webhooks.
    This class processes incoming webhook events from Stripe,
    including payment success, payment failure and subscription events.
    """

    def __init__(self, request):
        """Initialise the handler with the incoming HTTP request"""
        self.request = request

    def _send_confirmation_email(self, order):

        """
        Send an order confirmation email to the customer.
        Renders the subject and body from email templates
        and sends via Django's send_mail function.
        """
        customer_email = order.email
        # Render email subject from template
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_subject.txt',
            {'order': order}
        )

        # Render email body from template
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_body.txt',
            {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            }
        )

        # Send the confirmation email
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic, unknown or unexpected webhook event.
        Returns a 200 response to acknowledge receipt without
        any specific processing.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        This fires when a payment is successfully processed.
        Differentiates between subscription payments and product
        order payments using bag metadata, then verifies or creates
        the order in the database.
        """
        intent = event.data.object
        pid = intent.id
        # Check if this is a subscription payment (no bag metadata)
         # Subscription payments don't have bag metadata attached
        bag = getattr(intent.metadata, 'bag', None)
        if not bag:
            # This is a subscription payment, not a product order
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'Subscription payment, skipping order handler'
                ),
                status=200
            )

        # Extract metadata attached to the payment intent
        save_info = intent.metadata.save_info
        username = intent.metadata.username


        # Retrieve the charge object from Stripe to get billing details
        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = charge.billing_details
        grand_total = round(charge.amount / 100, 2)

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(
                    user__username=username
                )
                if save_info:
                    profile.default_phone_number = (
                        billing_details.phone
                    )
                    profile.default_street_address1 = (
                        billing_details.address.line1
                    )
                    profile.default_street_address2 = (
                        billing_details.address.line2
                    )
                    profile.default_town_or_city = (
                        billing_details.address.city
                    )
                    profile.default_postcode = (
                        billing_details.address.postal_code
                    )
                    profile.default_country = (
                        billing_details.address.country
                    )
                    profile.save()
            except UserProfile.DoesNotExist:
                pass

        # Attempt to find the order in the database
        # Retries up to 5 times with 1 second delay to allow for
        # any delay between payment completion and order creation
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
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database'
                ),
                status=200
            )
        else:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'ERROR: Order not found'
                ),
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe.
        This fires when a payment attempt fails.
        Returns a 200 response to acknowledge receipt.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
