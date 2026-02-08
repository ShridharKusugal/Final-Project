# ✅ Razorpay Integration Checklist

## Pre-Integration (Completed ✓)
- [x] Install Razorpay SDK (`pip install razorpay`)
- [x] Install python-dotenv (`pip install python-dotenv`)
- [x] Update requirements.txt
- [x] Add Razorpay configuration to app.py
- [x] Create payment routes in app.py
- [x] Update checkout.html with Razorpay integration
- [x] Create .env.example template
- [x] Create .gitignore file
- [x] Create documentation files

## Your Next Steps

### Step 1: Razorpay Account Setup
- [ ] Go to https://razorpay.com/
- [ ] Click "Sign Up" and create account
- [ ] Verify your email address
- [ ] Complete basic profile information

### Step 2: Get Test API Keys
- [ ] Log in to Razorpay Dashboard
- [ ] Navigate to Settings → API Keys
- [ ] Click "Generate Test Key"
- [ ] Copy the Key ID (starts with `rzp_test_`)
- [ ] Click "Show" and copy the Key Secret
- [ ] Save these keys securely (you'll need them next)

### Step 3: Configure Your Application
- [ ] Create a `.env` file in project root
- [ ] Add the following lines to `.env`:
  ```
  RAZORPAY_KEY_ID=rzp_test_your_key_id_here
  RAZORPAY_KEY_SECRET=your_key_secret_here
  ```
- [ ] Replace the placeholder values with your actual keys
- [ ] Save the file
- [ ] Verify `.env` is listed in `.gitignore`

### Step 4: Test the Integration

#### Test 1: Successful Payment
- [ ] Start your Flask application
- [ ] Go to the website and add a product to cart
- [ ] Proceed to checkout
- [ ] Fill in shipping details
- [ ] Select "Pay Online (Razorpay)" as payment method
- [ ] Click "Place Order"
- [ ] Razorpay modal should open
- [ ] Select "Card" as payment method
- [ ] Enter test card: `4111 1111 1111 1111`
- [ ] CVV: `123`, Expiry: `12/25`, Name: `Test User`
- [ ] Click "Pay"
- [ ] Verify you're redirected to order confirmation page
- [ ] Check that order status is "Confirmed" (not "Payment Pending")
- [ ] Verify loyalty points were awarded

#### Test 2: UPI Payment
- [ ] Repeat checkout process
- [ ] Select "Pay Online (Razorpay)"
- [ ] In Razorpay modal, select "UPI"
- [ ] Enter UPI ID: `success@razorpay`
- [ ] Complete payment
- [ ] Verify order is created successfully

#### Test 3: Failed Payment
- [ ] Repeat checkout process
- [ ] Use test card: `4111 1111 1111 1234`
- [ ] Payment should fail
- [ ] Verify no order is created in database
- [ ] Verify customer sees error message

#### Test 4: Cancelled Payment
- [ ] Start checkout process
- [ ] Open Razorpay modal
- [ ] Click "X" to close modal
- [ ] Verify no order is created
- [ ] Verify customer can try again

### Step 5: Verify in Razorpay Dashboard
- [ ] Go to Razorpay Dashboard
- [ ] Navigate to Transactions → Payments
- [ ] Verify your test payments appear
- [ ] Click on a payment to see details
- [ ] Verify payment status is "Captured"
- [ ] Check transaction details match your order

### Step 6: Test Edge Cases

#### Test with Coupon
- [ ] Apply a coupon code at checkout
- [ ] Complete Razorpay payment
- [ ] Verify discount is applied correctly
- [ ] Verify final amount matches discounted total

#### Test Direct Buy
- [ ] Click "Buy Now" on a product (not "Add to Cart")
- [ ] Complete checkout with Razorpay
- [ ] Verify order is created correctly

#### Test COD (Should Still Work)
- [ ] Go to checkout
- [ ] Select "Cash on Delivery"
- [ ] Complete order
- [ ] Verify COD orders still work as before

### Step 7: Review Documentation
- [ ] Read `RAZORPAY_SETUP.md` for detailed setup
- [ ] Review `RAZORPAY_INTEGRATION.md` for technical details
- [ ] Check `RAZORPAY_QUICK_REFERENCE.md` for quick tips
- [ ] Open `razorpay_payment_flow.html` in browser to see flow diagram

### Step 8: Security Check
- [ ] Verify `.env` file is NOT committed to Git
- [ ] Check `.gitignore` includes `.env`
- [ ] Ensure API keys are not hardcoded in any files
- [ ] Verify HTTPS is planned for production

## Going Live (When Ready)

### Step 9: KYC Verification
- [ ] Go to Razorpay Dashboard → Account & Settings
- [ ] Click on "Complete KYC"
- [ ] Upload required documents:
  - [ ] PAN Card
  - [ ] Business Registration (if applicable)
  - [ ] Bank Account Details
  - [ ] Address Proof
- [ ] Submit for verification
- [ ] Wait for approval (usually 24-48 hours)

### Step 10: Get Live API Keys
- [ ] After KYC approval, go to Settings → API Keys
- [ ] Click "Generate Live Key"
- [ ] Copy the Live Key ID (starts with `rzp_live_`)
- [ ] Copy the Live Key Secret
- [ ] Keep these keys extremely secure

### Step 11: Production Configuration
- [ ] Update `.env` file with live keys:
  ```
  RAZORPAY_KEY_ID=rzp_live_your_live_key_id
  RAZORPAY_KEY_SECRET=your_live_key_secret
  ```
- [ ] Ensure website is running on HTTPS
- [ ] Test with a small real transaction (₹1-10)
- [ ] Verify payment is captured successfully

### Step 12: Configure Payment Settings
- [ ] Go to Razorpay Dashboard → Settings → Payment Methods
- [ ] Enable/disable payment methods as needed:
  - [ ] UPI
  - [ ] Credit Cards
  - [ ] Debit Cards
  - [ ] Net Banking
  - [ ] Wallets
- [ ] Set payment limits if required
- [ ] Configure auto-refund settings

### Step 13: Set Up Webhooks (Optional but Recommended)
- [ ] Go to Razorpay Dashboard → Webhooks
- [ ] Click "Add Webhook"
- [ ] Enter webhook URL: `https://yourdomain.com/razorpay-webhook`
- [ ] Select events to track:
  - [ ] payment.captured
  - [ ] payment.failed
  - [ ] order.paid
- [ ] Copy webhook secret
- [ ] Add to `.env`: `RAZORPAY_WEBHOOK_SECRET=your_webhook_secret`
- [ ] Test webhook by making a payment

### Step 14: Final Testing in Production
- [ ] Make a test purchase with real payment
- [ ] Verify order is created correctly
- [ ] Check Razorpay dashboard for payment
- [ ] Verify email/SMS notifications work
- [ ] Test refund process (if needed)

### Step 15: Monitoring & Maintenance
- [ ] Set up daily dashboard checks
- [ ] Monitor payment success rate
- [ ] Review failed payments regularly
- [ ] Set up alerts for unusual activity
- [ ] Keep API keys secure and rotate if needed

## Troubleshooting Checklist

If something doesn't work:
- [ ] Check `.env` file exists and has correct keys
- [ ] Verify API keys are correct (no extra spaces)
- [ ] Check browser console for JavaScript errors
- [ ] Review server logs for Python errors
- [ ] Ensure internet connection is stable
- [ ] Verify Razorpay services are operational
- [ ] Check database connection is working
- [ ] Ensure Flask app is running without errors

## Support Resources

If you need help:
- [ ] Check `RAZORPAY_SETUP.md` for setup issues
- [ ] Review `RAZORPAY_INTEGRATION.md` for technical details
- [ ] Visit Razorpay Documentation: https://razorpay.com/docs/
- [ ] Contact Razorpay Support: support@razorpay.com
- [ ] Check Razorpay Status: https://status.razorpay.com/

## Success Criteria

Your integration is successful when:
- [x] Razorpay SDK is installed
- [x] Code changes are implemented
- [ ] API keys are configured in `.env`
- [ ] Test payments work successfully
- [ ] Orders are created with "Confirmed" status
- [ ] Loyalty points are awarded
- [ ] Payment verification is automatic
- [ ] All payment methods work (UPI, Cards, etc.)
- [ ] COD still works as before
- [ ] No errors in browser console or server logs

## Completion Status

- **Integration Code**: ✅ Complete
- **Documentation**: ✅ Complete
- **Dependencies**: ✅ Installed
- **Configuration**: ⏳ Pending (Need your API keys)
- **Testing**: ⏳ Pending (After configuration)
- **Production**: ⏳ Pending (After KYC)

---

## Quick Start Summary

**Right Now:**
1. Create Razorpay account → Get test keys
2. Create `.env` file → Add your keys
3. Test with card `4111 1111 1111 1111`

**Before Going Live:**
1. Complete KYC verification
2. Get live keys → Update `.env`
3. Enable HTTPS
4. Test in production

---

**Current Status**: Integration code is complete! Follow steps 1-8 to test with your Razorpay account.

**Estimated Time**: 
- Setup & Testing: 30-45 minutes
- KYC Approval: 24-48 hours
- Going Live: 1-2 hours

Good luck! 🚀
