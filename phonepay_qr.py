import qrcode
from urllib.parse import quote

def create_upi_payment_qr():
    print("=== UPI Payment QR Code Generator ===")

    upi_id = input("Enter UPI ID (pa): ").strip()
    name = input("Enter Payee Name (pn) [optional]: ").strip()
    amount_str = input("Enter Amount (INR) [optional, ex: 150.50]: ").strip()

    if not upi_id:
        print("❌ UPI ID is required.")
        return

    # Validate/format amount (optional)
    amount_param = ""
    if amount_str:
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            amount_param = f"&am={amount:.2f}"
        except ValueError:
            print("❌ Invalid amount. Use a number like 150 or 150.50")
            return

    # Build UPI URI
    # pa = payee address (UPI ID), pn = payee name, am = amount, cu = currency, tn = transaction note
    uri = f"upi://pay?pa={quote(upi_id)}"

    if name:
        uri += f"&pn={quote(name)}"

    uri += f"{amount_param}&cu=INR"

    # Generate QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save
    safe_upi = upi_id.replace("@", "_at_").replace(".", "_").replace(" ", "_")
    safe_amt = amount_str.replace(".", "_") if amount_str else "any_amount"
    filename = f"upi_{safe_upi}_{safe_amt}.png"
    img.save(filename)

    print("\n✅ UPI Payment QR saved as:", filename)
    print("🔗 Encoded UPI URI:", uri)
    if amount_str:
        print(f"💰 Amount: ₹{float(amount_str):.2f} (fixed)")
    else:
        print("💰 Amount: Not fixed (payer can enter)")

if __name__ == "__main__":
    create_upi_payment_qr()
    input("\nPress Enter to exit...")
