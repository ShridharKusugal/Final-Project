from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_pdf(filename="NK_Automobiles_Presentation.pdf"):
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # --- Slide Helper ---
    def add_slide(title, content_list=None):
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 1.5*inch, title)
        
        c.setFont("Helvetica", 14)
        y = height - 2.5 * inch
        
        if content_list:
            for item in content_list:
                for line in item.split('\n'):
                     c.drawString(1.0*inch, y, line)
                     y -= 0.3 * inch
        
        c.showPage() # Create new page for next slide

    # --- Title Slide ---
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height / 2 + 0.5*inch, "NK Automobiles")
    
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height / 2 - 0.5*inch, "Comprehensive E-Commerce Platform for Bike Spare Parts")
    c.drawCentredString(width / 2, height / 2 - 1.0*inch, "Project Presentation")
    c.showPage()

    # --- Introduction ---
    add_slide("Introduction", [
        "NK Automobiles is a dedicated e-commerce web application designed to simplify",
        "the process of purchasing genuine two-wheeler spare parts online.",
        "",
        "Key Goals:",
        "- Bridge the gap between bike owners and authentic suppliers.",
        "- Provide a seamless online shopping experience.",
        "- Offer secure payment options and reliable tracking."
    ])

    # --- Problem Statement ---
    add_slide("Problem Statement", [
        "Current Challenges in the Market:",
        "- Difficulty in finding genuine spare parts for specific bike models.",
        "- Uncertainty about product quality and authenticity.",
        "- Lack of transparent pricing and inventory information.",
        "- Inconvenient offline purchasing requiring physical store visits."
    ])

    # --- Solution: Key Features ---
    add_slide("Solution & Key Features", [
        "For Users:",
        "- Extensive Product Catalog: Categorized by brand and part type.",
        "- Smart Search & Filters: Easily find parts by bike model or price.",
        "- Secure Authentication: User registration, login, and profile.",
        "- Interactive Shopping: Wishlist, Shopping Cart, and Reviews.",
        "",
        "For Admins:",
        "- Product Management: Add, edit, delete products & stock.",
        "- Order Management: View orders and update status.",
        "- Analytics Dashboard: Track sales, user growth, and revenue."
    ])

    # --- Technology Stack ---
    add_slide("Technology Stack", [
        "Frontend:",
        "- HTML5, CSS3, Bootstrap 5 (Responsive)",
        "- JavaScript (Interactive elements)",
        "",
        "Backend:",
        "- Python (Core Logic)",
        "- Flask (Web Framework)",
        "",
        "Database:",
        "- MySQL (Relational Data Storage)"
    ])

    # --- Secure Payment Workflow ---
    add_slide("Secure Payment Workflow", [
        "Hybrid Payment System:",
        "1. UPI QR Code Integration:",
        "   - Users scan a dynamic QR code for the exact amount.",
        "   - Mandatory Transaction ID entry for verification.",
        "   - Server-side check for duplicate transaction IDs.",
        "",
        "2. Cash on Delivery (COD):",
        "   - Traditional option for user trust and convenience."
    ])

    # --- Database Schema (ER Diagram) ---
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 1.5*inch, "Database Schema (ER Relationships)")
    
    # Draw simple boxes for ER Diagram representation
    c.setFont("Helvetica", 10)
    
    # User Box
    c.rect(1*inch, height - 4*inch, 2*inch, 1*inch)
    c.drawString(1.2*inch, height - 3.5*inch, "USERS")
    c.drawString(1.2*inch, height - 3.7*inch, "(PK: user_id)")

    # Order Box
    c.rect(4*inch, height - 4*inch, 2*inch, 1.5*inch)
    c.drawString(4.2*inch, height - 3.5*inch, "ORDERS")
    c.drawString(4.2*inch, height - 3.7*inch, "(PK: order_id)")
    c.drawString(4.2*inch, height - 3.9*inch, "(FK: user_id)")
    
    # Product Box
    c.rect(7*inch, height - 4*inch, 2*inch, 1.5*inch)
    c.drawString(7.2*inch, height - 3.5*inch, "PRODUCTS")
    c.drawString(7.2*inch, height - 3.7*inch, "(PK: product_id)")
    c.drawString(7.2*inch, height - 3.9*inch, "(FK: category_id)")

    # Lines representing relationships
    c.line(3*inch, height - 3.5*inch, 4*inch, height - 3.5*inch) # User <-> Order
    c.drawString(3.2*inch, height - 3.4*inch, "1 ---- N")

    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 6*inch, "Key Tables & Relationships:")
    c.drawString(1*inch, height - 6.3*inch, "- Users Place Orders (1-to-Many)")
    c.drawString(1*inch, height - 6.5*inch, "- Orders Contain Order Items (1-to-Many)")
    c.drawString(1*inch, height - 6.7*inch, "- Products belong to Categories (Many-to-1)")
    c.drawString(1*inch, height - 6.9*inch, "- Users Write Reviews for Products (Many-to-Many)")
    
    c.showPage()

    # --- User Workflow (Flowchart) ---
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 1.5*inch, "User Workflow (Flowchart)")
    
    y_start = height - 2.5*inch
    steps = ["Start (Home Page)", "Browse / Search Products", "Add to Cart / View Details", 
             "Login / Register", "Checkout (Address)", "Payment (UPI/COD)", "Order Confirmed"]
    
    c.setFont("Helvetica", 12)
    for i, step in enumerate(steps):
        # Draw Box
        x = 1.5*inch + (i * 1.3*inch)
        y = height/2
        
        # Simple text representation since drawing boxes dynamically is tricky
        c.rect(x, y, 1.2*inch, 0.6*inch)
        # Center text in box somewhat roughly
        c.setFont("Helvetica", 8)
        # Split step text into lines if needed
        words = step.split(' ')
        if len(words) > 2:
            c.drawCentredString(x + 0.6*inch, y + 0.35*inch, ' '.join(words[:2]))
            c.drawCentredString(x + 0.6*inch, y + 0.15*inch, ' '.join(words[2:]))
        else:
            c.drawCentredString(x + 0.6*inch, y + 0.25*inch, step)
            
        # Draw Arrow
        if i < len(steps) - 1:
            c.line(x + 1.2*inch, y + 0.3*inch, x + 1.3*inch, y + 0.3*inch)

    c.setFont("Helvetica", 14)
    c.drawString(1*inch, height - 5*inch, "Step-by-Step Flow:")
    c.drawString(1*inch, height - 5.3*inch, "1. Visitor explores the product catalog.")
    c.drawString(1*inch, height - 5.5*inch, "2. Adds desired items to cart.")
    c.drawString(1*inch, height - 5.7*inch, "3. Authenticates to proceed (Login/Signup).")
    c.drawString(1*inch, height - 5.9*inch, "4. Enters delivery details and selects payment.")
    c.drawString(1*inch, height - 6.1*inch, "5. Completes purchase -> System updates Inventory.")

    c.showPage()

    # --- Future Enhancements ---
    add_slide("Future Enhancements", [
        "- Mobile Application Development (Android/iOS).",
        "- AI-Powered Recommendation System for spare parts.",
        "- Integration with Razorpay/Stripe Payment Gateways.",
        "- Live Chat Customer Support.",
        "- Multi-language interface for wider accessibility."
    ])

    # --- Conclusion ---
    add_slide("Conclusion", [
        "NK Automobiles successfully addresses the market need for a reliable",
        "online spare parts store.",
        "",
        "By combining a user-friendly interface with robust backend management,",
        "it ensures efficient operations and customer satisfaction."
    ])
    
    # --- Thank You ---
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(width / 2, height / 2, "Thank You")
    c.setFont("Helvetica", 24)
    c.drawCentredString(width / 2, height / 2 - 1.0*inch, "Questions & Answers")
    c.showPage()

    c.save()
    print(f"PDF Presentation saved as {filename}")

if __name__ == "__main__":
    create_pdf()
