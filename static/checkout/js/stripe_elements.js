const stripe = Stripe(stripePublicKey);

const elements = stripe.elements({
    clientSecret: clientSecret
});

// Create Payment Element 
const paymentElement = elements.create("payment");

// Mount the payment
paymentElement.mount("#card-options-container");

// Handle form submit
const form = document.getElementById('payment-form');

form.addEventListener('submit', async function(ev) {
    ev.preventDefault();

    document.getElementById('submit-button').disabled = true;

    const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        redirect: "if_required"  
    });

    if (error) {
        document.getElementById('card-errors').textContent = error.message;
        document.getElementById('submit-button').disabled = false;
    } else {
        form.submit();
    }
});