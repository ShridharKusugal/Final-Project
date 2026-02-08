# Razorpay Payment Gateway Integration

## Overview
This document describes the Razorpay payment gateway integration for NK Automobiles website, which provides automatic payment verification for online payments.

## Features
- **Multiple Payment Methods**: UPI, Credit/Debit Cards, Net Banking, and Wallets
- **Automatic Verification**: Payments are verified automatically using Razorpay's signature verification
- **Secure Transactions**: All payments are processed through Razorpay's secure payment gateway
- **Order Status**: Orders are automatically marked as "Confirmed" after successful payment
- **Loyalty Points**: Customers earn loyalty points (1 point per ₹100) on successful payments

## Setup Instructions

### 1. Install Dependencies
```bash
pip install razorpay python-dotenv
```

### 2. Get Razorpay Credentials
1. Sign up at https://razorpay.com/
2. Go to Dashboard → Settings → API Keys
3. Generate API keys (Key ID and Key Secret)
4. For production, activate your account and use live keys

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```
RAZORPAY_KEY_ID=your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_here
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret_here  # Optional
```

**Important**: Never commit the `.env` file to version control. Add it to `.gitignore`.

### 4. Database Schema
The integration uses the existing `orders` table. Razorpay payments are stored with:
- `payment_method`: 'Razorpay'
- `transaction_id`: Razorpay payment ID
- `status`: 'Confirmed' (automatically set after payment verification)

## How It Works

### Payment Flow
1. **Customer Checkout**: Customer fills shipping details and selects "Pay Online" option
2. **Order Creation**: System creates a Razorpay order with the total amount
3. **Payment Modal**: Razorpay checkout modal opens with multiple payment options
4. **Payment Processing**: Customer completes payment using their preferred method
5. **Signature Verification**: System verifies payment signature for security
6. **Order Creation**: After successful verification, order is created in database
7. **Confirmation**: Customer is redirected to order confirmation page

### API Endpoints

#### 1. Create Razorpay Order
**Endpoint**: `POST /create-razorpay-order`
**Purpose**: Creates a Razorpay order for payment
**Request**:
```json
{
  "amount": "1500.00"
}
```
**Response**:
```json
{
  "success": true,
  "order_id": "order_xxxxxxxxxxxxx",
  "amount": 150000,
  "currency": "INR",
  "key_id": "rzp_test_xxxxxxxxxxxxx"
}
```

#### 2. Verify Payment
**Endpoint**: `POST /verify-razorpay-payment`
**Purpose**: Verifies payment signature and creates order in database
**Request**:
```json
{
  "razorpay_order_id": "order_xxxxxxxxxxxxx",
  "razorpay_payment_id": "pay_xxxxxxxxxxxxx",
  "razorpay_signature": "signature_string",
  "order_details": {
    "full_name": "John Doe",
    "phone_number": "9876543210",
    ...
  }
}
```
**Response**:
```json
{
  "success": true,
  "order_id": 123
}
```

#### 3. Webhook Handler (Optional)
**Endpoint**: `POST /razorpay-webhook`
**Purpose**: Handles Razorpay webhook events for additional processing
**Events Supported**: 
- `payment.captured`
- `payment.failed`
- `order.paid`

## Testing

### Test Mode
1. Use test API keys from Razorpay dashboard
2. Test card numbers: https://razorpay.com/docs/payments/payments/test-card-details/
3. Test UPI: Use `success@razorpay` as VPA

### Test Cards
- **Success**: 4111 1111 1111 1111
- **Failure**: 4111 1111 1111 1234
- CVV: Any 3 digits
- Expiry: Any future date

### Test UPI
- **Success**: `success@razorpay`
- **Failure**: `failure@razorpay`

## Security Features

1. **Signature Verification**: All payments are verified using HMAC SHA256 signature
2. **HTTPS Required**: Razorpay requires HTTPS in production
3. **PCI Compliance**: Razorpay is PCI DSS compliant
4. **No Card Storage**: Card details are never stored on your server

## Going Live

### Checklist
1. ✅ Complete KYC verification on Razorpay
2. ✅ Replace test keys with live keys in `.env`
3. ✅ Enable HTTPS on your website
4. ✅ Test all payment methods in production
5. ✅ Set up webhook URL in Razorpay dashboard
6. ✅ Configure payment methods you want to accept
7. ✅ Set up email notifications for failed payments

### Webhook Setup
1. Go to Razorpay Dashboard → Webhooks
2. Add webhook URL: `https://yourdomain.com/razorpay-webhook`
3. Select events to track
4. Copy webhook secret and add to `.env`

## Troubleshooting

### Common Issues

**1. Payment fails but money is deducted**
- Razorpay automatically refunds failed payments within 5-7 business days
- Check payment status in Razorpay dashboard

**2. Signature verification fails**
- Ensure you're using the correct API secret
- Check that the order_id, payment_id, and signature are being passed correctly

**3. Webhook not receiving events**
- Verify webhook URL is accessible publicly
- Check webhook signature verification
- Review webhook logs in Razorpay dashboard

**4. Payment modal not opening**
- Ensure Razorpay checkout.js script is loaded
- Check browser console for JavaScript errors
- Verify API key is correct

## Support

- **Razorpay Documentation**: https://razorpay.com/docs/
- **Razorpay Support**: https://razorpay.com/support/
- **Integration Guide**: https://razorpay.com/docs/payments/payment-gateway/web-integration/

## Advantages over Manual UPI

1. **Automatic Verification**: No manual verification needed
2. **Multiple Payment Options**: Cards, UPI, Net Banking, Wallets
3. **Better User Experience**: Professional checkout interface
4. **Instant Confirmation**: Orders confirmed immediately after payment
5. **Reduced Fraud**: Built-in fraud detection
6. **Better Tracking**: Detailed payment analytics in dashboard
7. **Refund Management**: Easy refund processing through dashboard

## Migration Notes

The integration replaces the manual UPI payment system with:
- Razorpay's automated payment processing
- Automatic payment verification
- Instant order confirmation
- Professional payment interface

COD (Cash on Delivery) option remains available for customers who prefer it.
