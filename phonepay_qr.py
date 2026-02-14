import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from urllib.parse import quote

import qrcode


def parse_amount(amount_str: str) -> Decimal:
    try:
        amount = Decimal(amount_str)
    except InvalidOperation as exc:
        raise ValueError("Invalid amount. Use a number like 150 or 150.50") from exc

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def safe_filename_part(value: str, default: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", (value or "").strip())
    cleaned = cleaned.strip("_")
    return cleaned or default


def create_upi_payment_qr():
    print("=== UPI Payment QR Code Generator ===")

    upi_id = input("Enter UPI ID (pa): ").strip()
    name = input("Enter Payee Name (pn) [optional]: ").strip()
    amount_str = input("Enter Amount (INR) [optional, ex: 150.50]: ").strip()
    note = input("Enter Note (tn) [optional]: ").strip()

    if not upi_id:
        print("Error: UPI ID is required.")
        return

    amount = None
    if amount_str:
        try:
            amount = parse_amount(amount_str)
        except ValueError as err:
            print(f"Error: {err}")
            return

    # pa = payee address (UPI ID), pn = payee name, am = amount, cu = currency, tn = note
    uri = f"upi://pay?pa={quote(upi_id)}"

    if name:
        uri += f"&pn={quote(name)}"
    if note:
        uri += f"&tn={quote(note)}"
    if amount is not None:
        uri += f"&am={amount}"

    uri += "&cu=INR"

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    safe_upi = safe_filename_part(upi_id.replace("@", "_at_"), "upi")
    safe_amt = str(amount).replace(".", "_") if amount is not None else "any_amount"
    filename = f"upi_{safe_upi}_{safe_amt}.png"
    img.save(filename)

    print(f"\nUPI payment QR saved as: {filename}")
    print(f"Encoded UPI URI: {uri}")
    if amount is not None:
        print(f"Amount: INR {amount} (fixed)")
    else:
        print("Amount: Not fixed (payer can enter)")


if __name__ == "__main__":
    create_upi_payment_qr()
    input("\nPress Enter to exit...")
