import os
import csv
import hashlib
import exifread
from PIL import Image

def get_sha256(filepath):
    """Calculates the SHA-256 cryptographic hash of the image."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def convert_to_degrees(value):
    """Converts raw EXIF fraction data (Degrees, Minutes, Seconds) into Decimal Degrees."""
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def log_to_csv(data_dict):
    """Saves the clean extracted data to a CSV ledger."""
    csv_file = "evidence_log.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data_dict.keys())
        if not file_exists:
            writer.writeheader()  
        writer.writerow(data_dict)
    print(f"\n[+] Successfully logged clean data to {csv_file}")

def analyze_image(filepath):
    """Extracts metadata, computes GPS coordinates, logs clean data, and dumps raw data."""
    print(f"\n🔍 Analyzing Evidence: {filepath}")
    print("-" * 50)
    
    # 1. Setup our dictionary for the clean CSV logger
    report_data = {
        "File Name": os.path.basename(filepath),
        "SHA-256": get_sha256(filepath),
        "Resolution": "Unknown",
        "File Format": "Unknown",
        "Date Taken": "Not Found",
        "Camera Make": "Not Found",
        "Camera Model": "Not Found",
        "Coordinates": "Not Found",
        "Google Maps Link": "Not Found"
    }
    print(f"[*] SHA-256 Hash: {report_data['SHA-256']}")
    
    # 2. Extract resolution and format
    try:
        with Image.open(filepath) as img:
            report_data["Resolution"] = f"{img.width}x{img.height} pixels"
            report_data["File Format"] = img.format
            print(f"[*] Resolution:   {report_data['Resolution']}")
            print(f"[*] File Format:  {report_data['File Format']}")
    except Exception as e:
        pass

    # 3. Extract EXIF and GPS
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            
            report_data["Date Taken"] = str(tags.get('EXIF DateTimeOriginal', 'Not Found'))
            report_data["Camera Make"] = str(tags.get('Image Make', 'Not Found')).strip()
            report_data["Camera Model"] = str(tags.get('Image Model', 'Not Found')).strip()
            
            print(f"[*] Date Taken:   {report_data['Date Taken']}")
            print(f"[*] Camera Make:  {report_data['Camera Make']}")
            print(f"[*] Camera Model: {report_data['Camera Model']}")
            
            # 4. Clean GPS Conversion for the CSV
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = convert_to_degrees(tags['GPS GPSLatitude'])
                lat_ref = tags['GPS GPSLatitudeRef'].values
                if lat_ref != 'N': lat = -lat
                
                lon = convert_to_degrees(tags['GPS GPSLongitude'])
                lon_ref = tags['GPS GPSLongitudeRef'].values
                if lon_ref != 'E': lon = -lon
                
                report_data["Coordinates"] = f"{lat}, {lon}"
                report_data["Google Maps Link"] = f"https://www.google.com/maps?q={lat},{lon}"
                
                print(f"[*] Coordinates:  {report_data['Coordinates']}")
                print(f"[*] Maps Link:    {report_data['Google Maps Link']}")
            else:
                print("[*] Coordinates:  No GPS Data Found")
                print("[*] Maps Link:    No GPS Data Found")

            # 5. RAW DATA DUMP (Prints to terminal, does NOT go into the CSV)
            gps_tags = {key: val for key, val in tags.items() if key.startswith('GPS')}
            if gps_tags:
                print("\n[!] RAW GPS DATA DUMP (For Investigator Review):")
                for key, val in gps_tags.items():
                    print(f"    -> {key}: {val}")
            else:
                # NEW FEATURE: Explicitly tell the user why there is no raw data
                print("\n[!] RAW GPS DATA DUMP: None found (Device location was off or data was stripped).")
                
    except Exception as e:
        print(f"[!] Error reading EXIF: {e}")
        
    print("-" * 50)
    log_to_csv(report_data)

# Make sure to update the filename here to match your test image!
if __name__ == "__main__":
    analyze_image("test_img/1000139754.jpg")