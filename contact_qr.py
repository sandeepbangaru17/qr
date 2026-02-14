import re

import qrcode


def esc_vcard(value: str) -> str:
    return (
        (value or "")
        .replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .strip()
    )


def safe_filename_part(value: str, default: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", (value or "").strip())
    cleaned = cleaned.strip("_")
    return cleaned or default


def create_contact_qr():
    print("=== Contact QR Code Generator ===")

    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email [optional]: ").strip()

    if not name:
        print("Error: Name is required.")
        return
    if not phone:
        print("Error: Phone Number is required.")
        return

    name_v = esc_vcard(name)
    phone_v = esc_vcard(phone)
    email_v = esc_vcard(email)

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{name_v}",
        f"N:{name_v};;;;",
        f"TEL;TYPE=CELL:{phone_v}",
    ]
    if email_v:
        lines.append(f"EMAIL;TYPE=INTERNET:{email_v}")
    lines.append("END:VCARD")
    vcard = "\n".join(lines)

    qr = qrcode.make(vcard)

    filename = f"{safe_filename_part(name, 'contact')}_contact.png"
    qr.save(filename)

    print(f"\nSaved QR code as: {filename}")
    print(f"Name: {name}")
    print(f"Phone: {phone}")
    if email:
        print(f"Email: {email}")


if __name__ == "__main__":
    create_contact_qr()
    input("\nPress Enter to exit...")
