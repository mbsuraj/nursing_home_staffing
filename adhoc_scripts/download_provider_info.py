"""
Download CMS Nursing Home Provider Information file

The Provider Info file is available from CMS data.cms.gov
This script attempts to download it from the known URL pattern
"""

import requests
import pandas as pd
from pathlib import Path

print("=" * 70)
print("CMS NURSING HOME PROVIDER INFO DOWNLOAD")
print("=" * 70)

# Create data directory if needed
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Known CMS URLs for nursing home provider data
# These URLs are from the CMS Provider Data Catalog
urls_to_try = [
    # Provider Info from Care Compare/Provider Data Catalog
    "https://data.cms.gov/provider-data/api/1/datastore/query/4pq5-n9py/0/download?format=csv",
    "https://data.cms.gov/provider-data/dataset/4pq5-n9py",
    # Alternative: Direct download link pattern
    "https://data.cms.gov/data-api/v1/dataset/4pq5-n9py/data.csv",
]

print("\nAttempting to download Provider Info file...")
print("This file contains facility metadata including:")
print("- Facility identifiers (PROVNUM)")
print("- Ownership type")
print("- Urban/Rural designation")
print("- Bed count, census")
print("- Chain membership")
print("- Quality ratings")

success = False
for i, url in enumerate(urls_to_try, 1):
    print(f"\nAttempt {i}: {url[:60]}...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Try to parse as CSV
            content = response.content.decode('utf-8')
            if content.startswith('<!DOCTYPE') or content.startswith('<html'):
                print("   ❌ Received HTML instead of CSV")
                continue
            
            # Save to file
            output_path = data_dir / "NH_ProviderInfo.csv"
            with open(output_path, 'w') as f:
                f.write(content)
            
            # Verify it's valid
            df = pd.read_csv(output_path, nrows=5)
            print(f"   ✅ SUCCESS! Downloaded {len(response.content):,} bytes")
            print(f"   Saved to: {output_path}")
            print(f"\n   First few columns: {list(df.columns[:10])}")
            success = True
            break
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if not success:
    print("\n" + "=" * 70)
    print("AUTOMATIC DOWNLOAD FAILED")
    print("=" * 70)
    print("\nMANUAL DOWNLOAD INSTRUCTIONS:")
    print("\n1. Go to: https://data.cms.gov/provider-data/topics/nursing-homes")
    print("2. Look for 'Provider Information' dataset")
    print("3. Click 'Export' → 'CSV'")
    print("4. Save the file as: data/NH_ProviderInfo.csv")
    print("\nAlternatively, search for 'Nursing Home Provider Information' at:")
    print("https://data.cms.gov/provider-data/")
    print("\nThe dataset ID is: 4pq5-n9py")
    print("Direct link: https://data.cms.gov/provider-data/dataset/4pq5-n9py")
else:
    print("\n" + "=" * 70)
    print("ANALYZING DOWNLOADED FILE")
    print("=" * 70)
    
    # Load and analyze
    df = pd.read_csv(data_dir / "NH_ProviderInfo.csv", nrows=1000)
    
    print(f"\nFile shape (first 1000 rows): {df.shape}")
    print(f"\nAll columns ({len(df.columns)} total):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:3d}. {col}")
    
    # Check for key fields
    print("\n" + "=" * 70)
    print("CHECKING FOR LTCCC QUESTION FIELDS")
    print("=" * 70)
    
    # Question 1: Rural/Urban
    urban_cols = [c for c in df.columns if 'urban' in c.lower() or 'rural' in c.lower()]
    print("\n1. Rural/Urban fields:")
    if urban_cols:
        print(f"   ✅ Found: {urban_cols}")
        for col in urban_cols:
            print(f"      Sample values: {df[col].value_counts().to_dict()}")
    else:
        print("   ❌ Not found")
    
    # Question 2: Ownership
    ownership_cols = [c for c in df.columns if 'owner' in c.lower() or 'legal' in c.lower()]
    print("\n2. Ownership fields:")
    if ownership_cols:
        print(f"   ✅ Found: {ownership_cols}")
        for col in ownership_cols:
            if df[col].dtype == 'object':
                print(f"      {col}: {df[col].value_counts().head(10).to_dict()}")
    else:
        print("   ❌ Not found")
    
    # Question 3: Facility identifiers
    facility_cols = [c for c in df.columns if 'prov' in c.lower() or 'federal' in c.lower() or 'ccn' in c.lower()]
    print("\n3. Facility identifier fields:")
    if facility_cols:
        print(f"   ✅ Found: {facility_cols}")
    else:
        print("   ❌ Not found")
    
    # Other useful fields
    print("\n" + "=" * 70)
    print("OTHER USEFUL FIELDS")
    print("=" * 70)
    
    useful_keywords = ['bed', 'resident', 'chain', 'rating', 'star', 'turnover']
    for keyword in useful_keywords:
        cols = [c for c in df.columns if keyword in c.lower()]
        if cols:
            print(f"\n{keyword.upper()}: {cols}")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
