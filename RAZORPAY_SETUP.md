# Quick Setup Guide for Razorpay Integration

## Step 1: Create Razorpay Account
1. Go to https://razorpay.com/
2. Click "Sign Up" and create an account
3. Complete the registration process

## Step 2: Get Your API Keys

### For Testing (Test Mode)
1. Log in to Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Click **Generate Test Key**
4. You'll see:
   - **Key ID**: Starts with `rzp_test_`
   - **Key Secret**: Click "Show" to reveal

### For Production (Live Mode)
1. Complete KYC verification first
2. Go to **Settings** → **API Keys**
3. Click **Generate Live Key**
4. You'll see:
   - **Key ID**: Starts with `rzp_live_`
   - **Key Secret**: Click "Show" to reveal

## Step 3: Configure Your Application

1. Create a `.env` file in your project root (if it doesn't exist):
   ```
   RAZORPAY_KEY_ID=rzp_test_your_key_id_here
   RAZORPAY_KEY_SECRET=your_key_secret_here
   ```

2. Replace the placeholder values with your actual keys from Step 2

3. **IMPORTANT**: Add `.env` to your `.gitignore` file to keep your keys secure:
   ```
   # Add this line to .gitignore
   .env
   ```

## Step 4: Test the Integration

### Using Test Mode
1. Make sure you're using test keys (starting with `rzp_test_`)
2. Go to checkout page and select "Pay Online"
3. Use test payment methods:

#### Test Card Details
- **Card Number**: 4111 1111 1111 1111
- **CVV**: Any 3 digits (e.g., 123)
- **Expiry**: Any future date (e.g., 12/25)
- **Name**: Any name

#### Test UPI
- **UPI ID**: success@razorpay (for successful payment)
- **UPI ID**: failure@razorpay (for failed payment)

#### Test Net Banking
- Select any bank and use the test credentials provided

## Step 5: Verify Payment Flow

After successful payment:
1. ✅ Payment should be verified automatically
2. ✅ Order should be created with status "Confirmed"
3. ✅ Customer should be redirected to order confirmation page
4. ✅ Loyalty points should be awarded (1 point per ₹100)

## Step 6: Check Razorpay Dashboard

1. Go to Razorpay Dashboard → **Transactions** → **Payments**
2. You should see your test payment
3. Click on the payment to see details

## Step 7: Going Live (When Ready)

1. **Complete KYC**: Submit required documents in Razorpay dashboard
2. **Get Live Keys**: Generate live API keys (starting with `rzp_live_`)
3. **Update .env**: Replace test keys with live keys
4. **Enable HTTPS**: Ensure your website uses HTTPS
5. **Test in Production**: Make a small test transaction
6. **Monitor**: Check dashboard regularly for payments

## Common Test Scenarios

### Scenario 1: Successful Payment
1. Select "Pay Online" at checkout
2. Use test card: 4111 1111 1111 1111
3. Complete payment
4. Verify order is created with "Confirmed" status

### Scenario 2: Failed Payment
1. Select "Pay Online" at checkout
2. Use test card: 4111 1111 1111 1234
3. Payment should fail
4. Verify no order is created

### Scenario 3: Payment Cancelled
1. Select "Pay Online" at checkout
2. Click "X" to close payment modal
3. Verify no order is created

## Troubleshooting

### Issue: "Error creating payment order"
**Solution**: Check that your API keys are correct in `.env` file

### Issue: "Payment verification failed"
**Solution**: Ensure you're using the correct Key Secret

### Issue: Payment modal doesn't open
**Solution**: Check browser console for errors. Ensure internet connection is stable.

### Issue: Payment successful but order not created
**Solution**: Check server logs for errors. Verify database connection.

## Support Resources

- **Razorpay Documentation**: https://razorpay.com/docs/
- **Test Cards**: https://razorpay.com/docs/payments/payments/test-card-details/
- **Razorpay Support**: support@razorpay.com
- **Dashboard**: https://dashboard.razorpay.com/

## Security Best Practices

1. ✅ Never commit `.env` file to Git
2. ✅ Never share your Key Secret publicly
3. ✅ Use test keys for development
4. ✅ Use live keys only in production
5. ✅ Enable HTTPS before going live
6. ✅ Regularly check Razorpay dashboard for suspicious activity

## Next Steps

After successful testing:
1. Complete KYC verification
2. Switch to live keys
3. Enable HTTPS on your domain
4. Configure webhook for payment notifications
5. Set up refund policies
6. Train your team on using Razorpay dashboard

---

**Need Help?** Check `RAZORPAY_INTEGRATION.md` for detailed documentation.
