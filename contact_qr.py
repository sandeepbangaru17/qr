import qrcode

def create_contact_qr():
    print("=== Contact QR Code Generator ===")
    
    # Get user input
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()
    
    # Create vCard format
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
N:{name};;;;
TEL:{phone}
EMAIL:{email}
END:VCARD"""
    
    # Generate QR code
    qr = qrcode.make(vcard)
    
    # Save file
    filename = f"{name.replace(' ', '_')}_contact.png"
    qr.save(filename)
    
    print(f"\n✅ QR code saved as: {filename}")
    print(f"📱 Scan with your phone to add: {name}")
    print(f"📞 Phone: {phone}")
    print(f"📧 Email: {email}")

if __name__ == "__main__":
    create_contact_qr()
    input("\nPress Enter to exit...")
