# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Rationale

The primary goal of testing was to ensure that the FWL - Fitness With Lou application performs consistently across multiple devices and screen sizes, maintaining both functionality and a smooth user experience.
Testing focused on performance, accessibility, responsiveness and the integrity of all e-commerce, booking and subscription features.

## Approach
Testing was carried out to verify that the website functions as intended, is fully responsive, and provides an intuitive user experience.
All tests were conducted manually using a combination of Google Chrome DevTools, validation tools, and live user interaction testing on both local and deployed Heroku environments.

## Methods

| Method | Description | Tools Used |
| --- | --- | --- |
| **Manual Testing** | Each feature and button was manually tested to verify correct functionality. This included checking form submissions, Stripe payments, class bookings, subscription management, product CRUD operations and email confirmations. | Google Chrome |
| **Responsive Testing** | Tested using Chrome DevTools' built-in device emulation. Ensured the layout adapts correctly to different screen widths and orientations. | Chrome DevTools |
| **Cross-Browser Compatibility Testing** | Tested in multiple browsers to ensure consistent design, colour rendering, and interactivity. | Chrome, Firefox, Safari, Edge |
| **Validation Testing** | Used validation tools to check that the HTML, CSS and Python are free from syntax errors and follow best practices. | [W3C HTML Validator](https://validator.w3.org/), [W3C CSS Validator](https://jigsaw.w3.org/css-validator/), [PEP8 CI](https://pep8ci.herokuapp.com/) |
| **Accessibility Testing** | Checked colour contrast, font readability, tab navigation, and proper use of ARIA and semantic tags where applicable. | Chrome Lighthouse, manual checks |
| **Performance Testing** | Evaluated page load speed and responsiveness using Chrome Lighthouse and Page Speed Insights. | Chrome DevTools Lighthouse |

### Manual Tests (Defensive Programming)

- Users cannot submit an empty form (add the `required` attribute)
- Users must enter valid field types (ensure the correct input `type=""` is used)
- Users cannot brute-force a URL to navigate to a restricted page
- Non-superusers cannot access product management pages
- Users cannot subscribe to more than one plan at a time
- Users cannot double book a class if they are already booked onto it

| Feature Tested | Test Description | Expected Outcome | Pass/Fail | Screenshot |
| --- | --- | --- | --- | --- |
| Signup (valid) | Create a new account with valid username, email and password | Account created, verification email sent, user redirected to verify email page | ✅ Works | ![screenshot](documentation/testing/features/test-f-signup-email.JPG) <br> ![screenshot](documentation/testing/features/test-f-signup-confim-email.JPG) <br> ![screenshot](documentation/testing/features/test-f-signup-email-confirmed.JPG) |
| Signup (duplicate username) | Attempt to sign up using an existing username | Form displays error and prevents account creation | ✅ Works | ![screenshot](documentation/testing/features/test-f-signup-existing-details.png) <br> ![screenshot](documentation/testing/features/test-f-user-exists-terminal.png) |
| Signup (password mismatch) | Enter two different passwords in password fields | Validation error shown and account not created | ✅ Works | ![screenshot](documentation/testing/features/test-f-password-missmatch.png) |
| Signup (weak password) | Enter a weak password e.g. 123 | Error message displayed stating password requirements | ✅ Works | ![screenshot](documentation/testing/features/test-f-password-too-short.png) |
| Email verification | Click verification link in confirmation email | Account verified and user can log in | ✅ Works | ![screenshot](documentation/testing/features/test-f-signup-confim-email.JPG) |
| Login (valid) | Log in with correct username/email and password | User is authenticated and redirected to home page | ✅ Works | ![screenshot](documentation/testing/features/test-f-login-required.png) <br> ![screenshot](documentation/testing/features/test-f-login-page.png) |
| Login (invalid) | Attempt login with incorrect password | Error message shown and login denied | ✅ Works | ![screenshot](documentation/testing/features/test-f-incorrect-password.png) |
| Logout | Click logout while logged in | User is logged out and redirected; restricted pages no longer accessible | ✅ Works | ![screenshot](documentation/testing/features/test-f-loggedout.png) |
| Brute-force URL testing | Visit restricted pages without being logged in | User redirected to login page | ✅ Works | ![screenshot](documentation/testing/features/test-f-login-required.png)|
| Browse products | View all products on the products page | All products display with images, names and prices | ✅ Works | ![screenshot](documentation/images/existing_features/features_product_list.png) |
| Product detail | Click on a product to view its detail page | Product detail page loads with description, price, size selector and quantity input | ✅ Works | ![screenshot](documentation/images/existing_features/features_products_details.png) |
| Add to cart | Add a product to the cart | Product appears in cart with correct quantity and price | ✅ Works | ![screenshot](documentation/testing/features/test-f-add-to-cart.png) |
| Update cart quantity | Increase/decrease quantity in cart | Total updates correctly | ✅ Works | ![screenshot](documentation/testing/features/test-f-cart-updated.png) |
| Remove from cart | Click remove on a cart item | Item is removed and totals update | ✅ Works | ![screenshot](documentation/testing/features/test-f-remove-item.png) |
| Empty cart message | View cart with no items | Friendly message displayed with link to shop | ✅ Works | ![screenshot](documentation/testing/features/test-f-cart-empty.png) |
| Stripe checkout (valid) | Complete checkout with test card `4242 4242 4242 4242` | Order created, confirmation email sent, redirected to success page | ✅ Works | ![screenshot](documentation/images/existing_features/features_stripe_payment.png) <br> ![screenshot](documentation/images/existing_features/features_success.png) <br> ![screenshot](documentation/images/existing_features/features_success_email.png)  |
| Stripe checkout (invalid card) | Enter invalid card details | Error message displayed and order not created | ✅ Works | ![screenshot](documentation/testing/features/test-f-stripe-invalid.png) |
| Order confirmation email | Complete a purchase | Confirmation email received with order details | ✅ Works | ![screenshot](documentation/images/existing_features/features_success_email.png) |
| Order history | View profile after purchase | Order appears in order history with correct details | ✅ Works | ![screenshot](documentation/testing/features/test-f-order-history.png) |
| View class timetable | Navigate to class schedule | All classes display with instructor, date, time and capacity | ✅ Works | ![screenshot](documentation/images/existing_features/features_classes.png) |
| Book a class | Click book on an available class | Booking confirmed, success toast displayed | ✅ Works | ![screenshot](documentation/testing/features/test-f-booking-toast-confirmation.png) |
| Cancel a class | Cancel an existing booking | Booking removed, capacity updated | ✅ Works | ![screenshot](documentation/images/existing_features/features_class_cancelled.png) |
| Duplicate booking (defensive) | Attempt to book the same class twice | Warning message displayed, duplicate booking prevented | ✅ Works | ![screenshot](documentation/manual-testing/duplicate-booking.png) |
| Full class (defensive) | Attempt to book a class at capacity | Error message displayed, booking prevented | ✅ Works | ![screenshot](documentation/manual-testing/full-class.png) |
| View subscription plans | Navigate to subscriptions page | All three plans display with prices and descriptions | ✅ Works | ![screenshot](documentation/images/existing_features/features_subscriptions.png) |
| Subscribe to a plan | Select a plan and complete Stripe checkout | Subscription activated, confirmation email sent | ✅ Works | ![screenshot](documentation/images/existing_features/features_subscription_confirmed.png) <br> ![screenshot](documentation/images/existing_features/features_subscription_email.png) |
| Duplicate subscription (defensive) | Attempt to subscribe while already subscribed | Error message displayed, prevented from subscribing to second plan | ✅ Works | ![screenshot](documentation/testing/features/test-f-duplicate-subscription.png) |
| Cancel subscription | Click cancel subscription on profile | Subscription cancels at end of billing period, status updated | ✅ Works | ![screenshot](documentation/images/existing_features/features_subscription_cancelled.png) |
| Subscription confirmation email | Subscribe to a plan | Confirmation email received with subscription details | ✅ Works | ![screenshot](documentation/testing/features/test-f-subscription-confirmation-email.png) |
| Add product (superuser) | Add a new product via admin | Product appears in catalogue | ✅ Works |**New product details**![screenshot](documentation/testing/features/test-f-add-new-prduct.png) <br> **New product added**![screenshot](documentation/testing/features/test-f-add-product-successful.png) |
| Edit product (superuser) | Edit an existing product | Changes saved and displayed correctly | ✅ Works |**Existing data** ![screenshot](documentation/testing/features/test-f-edit-orginal-details.png)  <br>  **New details for existing product** ![screenshot](documentation/testing/features/test-f-edit-new-details.png) <br> **Existing item with updated details** ![screenshot](documentation/testing/features/test-f-edit-updated.png)|
| Delete product (superuser) | Delete a product with confirmation prompt | Product removed from catalogue | ✅ Works | ![screenshot](documentation/testing/features/test-f-delete.png) <br> ![screenshot](documentation/testing/features/test-f-delete-confirm.png) <br> ![screenshot](documentation/testing/features/test-f-deleted-product.png)|
| Non-superuser product management (defensive) | Attempt to access edit/delete product URLs as regular user | Access denied, user redirected | ✅ Works | ![screenshot](documentation/testing/features/test-f-defence.png) |
| Newsletter signup | Submit email via newsletter form | Success message displayed, email saved to database | ✅ Works | ![screenshot](documentation/images/existing_features/features_news_letter.png) |
| Job application | Submit job application form with CV upload | Success page displayed, application saved to database | ✅ Works | ![screenshot](documentation/images/existing_features/features_job_application.png) |
| Toast notifications | Trigger various actions (add to cart, book class, etc.) | Appropriate toast message displayed for each action | ✅ Works | ![screenshot](documentation/images/existing_features/features_toast_msg.png) |
| Navigation (burger icon) | Resize screen and click burger icon on mobile | Navbar collapses on small screens and expands correctly | ✅ Works | ![screenshot](documentation/testing/features/test-f-navbar-burger.png)<br>![screenshot](documentation/testing/features/test-f-navbar-expand.png) |
| Navbar conditional links | Compare navbar logged out vs logged in | Correct links shown/hidden based on auth state | ✅ Works | **Unauthenticated User**![screenshot](documentation/testing/features/test-f-unauthenticated-user.png) <br> **Authenticated User**![screenshot](documentation/testing/features/test-f-authenticated-user.png) |
| Custom 404 page | Visit non-existent URL e.g. `/test` | Custom 404 page displays with navigation link | ✅ Works | ![screenshot](documentation/testing/features/test-f-404.png) |
| Custom 403 page | Attempt to access forbidden URL | Custom 403 page displays with navigation link | ✅ Works | ![screenshot](documentation/testing/features/test-f-403.png) |

### User Story Testing

| User Story Tested | Test Description | Expected Outcome | Pass/Fail |
| --- | --- | --- | --- |
| As a user, I would like to create an account | Submit signup form with valid details | Account created and verification email sent | ✅ Pass |
| As a user, I would like to log in and out of my account | Enter valid credentials and click logout | User authenticated and securely logged out | ✅ Pass |
| As a user, I would like to view a list of fitness apparel products | Navigate to products page | All products display with images and prices | ✅ Pass |
| As a user, I would like to view individual product details | Click on a product | Detail page loads with full product information | ✅ Pass |
| As a user, I would like to add products to my shopping cart | Click add to cart | Product appears in cart with correct totals | ✅ Pass |
| As a user, I would like to adjust the quantity of items in my cart | Update quantity in cart | Totals recalculate correctly | ✅ Pass |
| As a user, I would like to remove items from my cart | Click remove on cart item | Item removed and totals updated | ✅ Pass |
| As a user, I would like to securely pay for my order using Stripe | Complete checkout with test card | Order created and confirmation email sent | ✅ Pass |
| As a user, I would like to receive a confirmation email after purchase | Complete a purchase | Confirmation email received with order details | ✅ Pass |
| As a user, I would like to view my order history on my profile | View profile page | All previous orders displayed correctly | ✅ Pass |
| As a user, I would like to view a class timetable | Navigate to class schedule | All classes displayed with correct details | ✅ Pass |
| As a user, I would like to book a class | Click book on an available class | Booking confirmed with success toast | ✅ Pass |
| As a user, I would like to cancel a class booking | Cancel a booked class | Booking removed and capacity updated | ✅ Pass |
| As a user, I would like to subscribe to a membership plan | Select and pay for a plan | Subscription activated and email sent | ✅ Pass |
| As a user, I would like to cancel my subscription | Click cancel subscription | Subscription cancels at end of billing period | ✅ Pass |
| As a user, I would like to view my active subscription on my profile | View profile page | Active subscription displayed with plan details | ✅ Pass |
| As a superuser, I would like to upload, edit and delete products | Use product management pages | Full CRUD operations work correctly | ✅ Pass |
| As a user, I would like to upload my CV when applying for a job | Submit job application form | Application saved, success page displayed | ✅ Pass |
| As a user, I would like to sign up to the newsletter | Submit newsletter form | Success message displayed, email stored | ✅ Pass |
| As a user, I want access to a simple and clean navbar | Navigate using the navbar | All links work correctly and adapt to auth state | ✅ Pass |

### Responsiveness

Google Chrome DevTools was used extensively to simulate various device viewports, including popular smartphones, tablets, and desktop resolutions. This allowed for a controlled testing environment to verify that the layout, interactive elements, and overall responsiveness behaved as intended under different conditions.

Particular attention was given to:
- **Responsive design**: Ensuring all elements (buttons, images, forms and text) resize and reposition correctly.
- **Touch interactions**: Confirming buttons and inputs respond properly on smaller screens.
- **Visual consistency**: Checking that colours, fonts, containers and spacing remain aligned with the intended design across all viewports.

| Page | Mobile | Tablet | Laptop | Desktop |
| --- | --- | --- | --- | --- |
| Home | ![screenshot](documentation/responsiveness/mobile/home.png) | ![screenshot](documentation/responsiveness/tablet/home.png) | ![screenshot](documentation/responsiveness/laptop/home.png) | ![screenshot](documentation/responsiveness/desktop/home.png) |
| Products | ![screenshot](documentation/responsiveness/mobile/products.png) | ![screenshot](documentation/responsiveness/tablet/products.png) | ![screenshot](documentation/responsiveness/laptop/products.png) | ![screenshot](documentation/responsiveness/desktop/products.png) |
| Product Detail | ![screenshot](documentation/responsiveness/mobile/product-detail.png) | ![screenshot](documentation/responsiveness/tablet/product-detail.png) | ![screenshot](documentation/responsiveness/laptop/product-detail.png) | ![screenshot](documentation/responsiveness/desktop/product-detail.png) |
| Cart | ![screenshot](documentation/responsiveness/mobile/cart.png) | ![screenshot](documentation/responsiveness/tablet/cart.png) | ![screenshot](documentation/responsiveness/laptop/cart.png) | ![screenshot](documentation/responsiveness/desktop/cart.png) |
| Checkout | ![screenshot](documentation/responsiveness/mobile/checkout.png) | ![screenshot](documentation/responsiveness/tablet/checkout.png) | ![screenshot](documentation/responsiveness/laptop/checkout.png) | ![screenshot](documentation/responsiveness/desktop/checkout.png) |
| Class Timetable | ![screenshot](documentation/responsiveness/mobile/timetable.png) | ![screenshot](documentation/responsiveness/tablet/timetable.png) | ![screenshot](documentation/responsiveness/laptop/timetable.png) | ![screenshot](documentation/responsiveness/desktop/timetable.png) |
| Subscription Plans | ![screenshot](documentation/responsiveness/mobile/subscriptions.png) | ![screenshot](documentation/responsiveness/tablet/subscriptions.png) | ![screenshot](documentation/responsiveness/laptop/subscriptions.png) | ![screenshot](documentation/responsiveness/desktop/subscriptions.png) |
| Profile | ![screenshot](documentation/responsiveness/mobile/profile.png) | ![screenshot](documentation/responsiveness/tablet/profile.png) | ![screenshot](documentation/responsiveness/laptop/profile.png) | ![screenshot](documentation/responsiveness/desktop/profile.png) |
| Login | ![screenshot](documentation/responsiveness/mobile/login.png) | ![screenshot](documentation/responsiveness/tablet/login.png) | ![screenshot](documentation/responsiveness/laptop/login.png) | ![screenshot](documentation/responsiveness/desktop/login.png) |
| Sign Up | ![screenshot](documentation/responsiveness/mobile/signup.png) | ![screenshot](documentation/responsiveness/tablet/signup.png) | ![screenshot](documentation/responsiveness/laptop/signup.png) | ![screenshot](documentation/responsiveness/desktop/signup.png) |
| 404 | ![screenshot](documentation/responsiveness/mobile/404.png) | ![screenshot](documentation/responsiveness/tablet/404.png) | ![screenshot](documentation/responsiveness/laptop/404.png) | ![screenshot](documentation/responsiveness/desktop/404.png) |

## Testing Summaries

### Cross-Browser Compatibility

To ensure a consistent and accessible user experience across all devices and browsers, the project was thoroughly tested using Google Chrome DevTools and multiple browsers. Cross-browser compatibility testing was performed manually in the following browsers:
- Chrome
- Firefox
- Safari
- Edge
- Opera

**Summary**: The FWL web application displays and functions without any issues across all major web browsers.

| Page | Chrome | Firefox | Safari | Edge | Opera |
| --- | --- | --- | --- | --- | --- |
| Home | ![screenshot](documentation/browser-compatibility/chrome/home.png) | ![screenshot](documentation/browser-compatibility/firefox/home.png) | ![screenshot](documentation/browser-compatibility/safari/home.png) | ![screenshot](documentation/browser-compatibility/edge/home.png) | ![screenshot](documentation/browser-compatibility/opera/home.png) |
| Products | ![screenshot](documentation/browser-compatibility/chrome/products.png) | ![screenshot](documentation/browser-compatibility/firefox/products.png) | ![screenshot](documentation/browser-compatibility/safari/products.png) | ![screenshot](documentation/browser-compatibility/edge/products.png) | ![screenshot](documentation/browser-compatibility/opera/products.png) |
| Cart | ![screenshot](documentation/browser-compatibility/chrome/cart.png) | ![screenshot](documentation/browser-compatibility/firefox/cart.png) | ![screenshot](documentation/browser-compatibility/safari/cart.png) | ![screenshot](documentation/browser-compatibility/edge/cart.png) | ![screenshot](documentation/browser-compatibility/opera/cart.png) |
| Checkout | ![screenshot](documentation/browser-compatibility/chrome/checkout.png) | ![screenshot](documentation/browser-compatibility/firefox/checkout.png) | ![screenshot](documentation/browser-compatibility/safari/checkout.png) | ![screenshot](documentation/browser-compatibility/edge/checkout.png) | ![screenshot](documentation/browser-compatibility/opera/checkout.png) |
| Class Timetable | ![screenshot](documentation/browser-compatibility/chrome/timetable.png) | ![screenshot](documentation/browser-compatibility/firefox/timetable.png) | ![screenshot](documentation/browser-compatibility/safari/timetable.png) | ![screenshot](documentation/browser-compatibility/edge/timetable.png) | ![screenshot](documentation/browser-compatibility/opera/timetable.png) |
| Subscription Plans | ![screenshot](documentation/browser-compatibility/chrome/subscriptions.png) | ![screenshot](documentation/browser-compatibility/firefox/subscriptions.png) | ![screenshot](documentation/browser-compatibility/safari/subscriptions.png) | ![screenshot](documentation/browser-compatibility/edge/subscriptions.png) | ![screenshot](documentation/browser-compatibility/opera/subscriptions.png) |
| Profile | ![screenshot](documentation/browser-compatibility/chrome/profile.png) | ![screenshot](documentation/browser-compatibility/firefox/profile.png) | ![screenshot](documentation/browser-compatibility/safari/profile.png) | ![screenshot](documentation/browser-compatibility/edge/profile.png) | ![screenshot](documentation/browser-compatibility/opera/profile.png) |
| Login | ![screenshot](documentation/browser-compatibility/chrome/login.png) | ![screenshot](documentation/browser-compatibility/firefox/login.png) | ![screenshot](documentation/browser-compatibility/safari/login.png) | ![screenshot](documentation/browser-compatibility/edge/login.png) | ![screenshot](documentation/browser-compatibility/opera/login.png) |
| Sign Up | ![screenshot](documentation/browser-compatibility/chrome/signup.png) | ![screenshot](documentation/browser-compatibility/firefox/signup.png) | ![screenshot](documentation/browser-compatibility/safari/signup.png) | ![screenshot](documentation/browser-compatibility/edge/signup.png) | ![screenshot](documentation/browser-compatibility/opera/signup.png) |
| 404 | ![screenshot](documentation/browser-compatibility/chrome/404.png) | ![screenshot](documentation/browser-compatibility/firefox/404.png) | ![screenshot](documentation/browser-compatibility/safari/404.png) | ![screenshot](documentation/browser-compatibility/edge/404.png) | ![screenshot](documentation/browser-compatibility/opera/404.png) |

### Validation Summary

#### PEP8

I have used [PEP8 CI](https://pep8ci.herokuapp.com/) to validate my Python files.

| App | File | Errors/Warnings | Passed ✅ |
| --- | --- | --- | --- |
| checkout | views.py | ![screenshot](documentation/validation/pep8/checkout-views1.png) | ![screenshot](documentation/validation/pep8/checkout-views2.png) |
| checkout | webhook_handler.py | ![screenshot](documentation/validation/pep8/checkout-webhook-handler1.png) | ![screenshot](documentation/validation/pep8/checkout-webhook-handler2.png) |
| checkout | webhooks.py | ![screenshot](documentation/validation/pep8/checkout-webhooks1.png) | ![screenshot](documentation/validation/pep8/checkout-webhooks2.png) |
| checkout | models.py | ![screenshot](documentation/validation/pep8/checkout-models1.png) | ![screenshot](documentation/validation/pep8/checkout-models2.png) |
| checkout | forms.py | ![screenshot](documentation/validation/pep8/checkout-forms1.png) | ![screenshot](documentation/validation/pep8/checkout-forms2.png) |
| cart | contexts.py | ![screenshot](documentation/validation/pep8/cart-contexts1.png) | ![screenshot](documentation/validation/pep8/cart-contexts2.png) |
| cart | views.py | ![screenshot](documentation/validation/pep8/cart-views1.png) | ![screenshot](documentation/validation/pep8/cart-views2.png) |
| cart | models.py | ![screenshot](documentation/validation/pep8/cart-models1.png) | ![screenshot](documentation/validation/pep8/cart-models2.png) |
| products | views.py | ![screenshot](documentation/validation/pep8/products-views1.png) | ![screenshot](documentation/validation/pep8/products-views2.png) |
| products | models.py | ![screenshot](documentation/validation/pep8/products-models1.png) | ![screenshot](documentation/validation/pep8/products-models2.png) |
| products | forms.py | ![screenshot](documentation/validation/pep8/products-forms1.png) | ![screenshot](documentation/validation/pep8/products-forms2.png) |
| bookings | views.py | ![screenshot](documentation/validation/pep8/bookings-views1.png) | ![screenshot](documentation/validation/pep8/bookings-views2.png) |
| bookings | models.py | ![screenshot](documentation/validation/pep8/bookings-models1.png) | ![screenshot](documentation/validation/pep8/bookings-models2.png) |
| subscriptions | views.py | ![screenshot](documentation/validation/pep8/subscriptions-views1.png) | ![screenshot](documentation/validation/pep8/subscriptions-views2.png) |
| subscriptions | models.py | ![screenshot](documentation/validation/pep8/subscriptions-models1.png) | ![screenshot](documentation/validation/pep8/subscriptions-models2.png) |
| subscriptions | webhook_handler.py | ![screenshot](documentation/validation/pep8/subscriptions-webhook1.png) | ![screenshot](documentation/validation/pep8/subscriptions-webhook2.png) |
| users | views.py | ![screenshot](documentation/validation/pep8/users-views1.png) | ![screenshot](documentation/validation/pep8/users-views2.png) |
| users | models.py | ![screenshot](documentation/validation/pep8/users-models1.png) | ![screenshot](documentation/validation/pep8/users-models2.png) |
| main | views.py | ![screenshot](documentation/validation/pep8/main-views1.png) | ![screenshot](documentation/validation/pep8/main-views2.png) |
| main | models.py | ![screenshot](documentation/validation/pep8/main-models1.png) | ![screenshot](documentation/validation/pep8/main-models2.png) |
| fwl | settings.py | ![screenshot](documentation/validation/pep8/settings1.png) | ![screenshot](documentation/validation/pep8/settings2.png) |

#### HTML

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

| Page | Screenshot | Passed |
| --- | --- | --- |
| Home | ![screenshot](documentation/validation/html/home.png) | ✅ Pass |
| Products | ![screenshot](documentation/validation/html/products.png) | ✅ Pass |
| Product Detail | ![screenshot](documentation/validation/html/product-detail.png) | ✅ Pass |
| Cart | ![screenshot](documentation/validation/html/cart.png) | ✅ Pass |
| Checkout | ![screenshot](documentation/validation/html/checkout.png) | ✅ Pass |
| Class Timetable | ![screenshot](documentation/validation/html/timetable.png) | ✅ Pass |
| Subscription Plans | ![screenshot](documentation/validation/html/subscriptions.png) | ✅ Pass |
| Profile | ![screenshot](documentation/validation/html/profile.png) | ✅ Pass |
| Login | ![screenshot](documentation/validation/html/login.png) | ✅ Pass |
| Sign Up | ![screenshot](documentation/validation/html/signup.png) | ✅ Pass |
| 404 | ![screenshot](documentation/validation/html/404.png) | ✅ Pass |

#### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

| File | Screenshot | Passed |
| --- | --- | --- |
| base.css | ![screenshot](documentation/validation/css/base-css.png) | ✅ Pass |
| checkout.css | ![screenshot](documentation/validation/css/checkout-css.png) | ✅ Pass |
| hero.css | ![screenshot](documentation/validation/css/hero-css.png) | ✅ Pass |
| variables.css | ![screenshot](documentation/validation/css/variables-css.png) | ✅ Pass |

## Performance

### Performance Testing

I've tested my deployed project using the Page Speed Insights tool and Chrome Lighthouse to check for any major performance issues.

| Page | Mobile | Desktop |
| --- | --- | --- |
| Home | ![screenshot](documentation/performance-testing/home-mobile.png) | ![screenshot](documentation/performance-testing/home-desktop.png) |
| Products | ![screenshot](documentation/performance-testing/products-mobile.png) | ![screenshot](documentation/performance-testing/products-desktop.png) |
| Login | ![screenshot](documentation/performance-testing/login-mobile.png) | ![screenshot](documentation/performance-testing/login-desktop.png) |
| Sign Up | ![screenshot](documentation/performance-testing/signup-mobile.png) | ![screenshot](documentation/performance-testing/signup-desktop.png) |

### Accessibility Summary

| Test | Result |
| --- | --- |
| The web app follows WCAG 2.1 standards | ✅ |
| Text size and spacing adjustable | ✅ |
| Interactive elements clearly labeled and accessible via keyboard | ✅ |
| ARIA labels provided where appropriate | ✅ |
| Colour contrast meets accessibility standards | ✅ |
| Orientation and responsiveness maintained for screen readers | ✅ |

## Bugs / Fixes

| Bug | Fix |
| --- | --- |
| Webhook 400 errors — signing secret mismatch between ngrok CLI and Stripe dashboard | Updated `STRIPE_WH_SECRET` in `env.py` to use the correct Stripe dashboard signing secret |
| Images not persisting on Heroku after dyno restart | Integrated Cloudinary for permanent media file storage |
| `django_site` table missing on Heroku causing 500 error on login | Ran `python manage.py migrate sites` and created Site object via Django shell |
| Stripe `charges` attribute deprecated in newer API version | Replaced `intent.charges.data[0]` with `stripe.Charge.retrieve(intent.latest_charge)` |
| Custom widget not rendering — crispy forms overriding widget | Rendered image field manually using `{{ field }}` outside of `{{ form|crispy }}` |
| Cart totals not updating after quantity adjustment | Fixed `cart/contexts.py` to calculate totals dynamically from `product.price * quantity` |
| Allauth templates not found — incorrect folder structure | Moved templates from `templates/allauth/account/` to `templates/account/` |
| `STATICFILES_STORAGE` error with Django 6 and cloudinary-storage | Replaced deprecated setting with new `STORAGES` dictionary format |

### Known/Existing Issues

| Issue | Screenshot |
| --- | --- |
| Stripe payment method dropdown slightly clipped on very small mobile screens due to Shadow DOM CSS isolation | ![screenshot](documentation/known-issues/stripe-mobile.png) |