"""
Quick script to assess data availability for LTCCC questions
Run this to see what fields we have access to
"""

import pandas as pd
from pathlib import Path

print("=" * 70)
print("LTCCC DATA AVAILABILITY CHECK")
print("=" * 70)

# Current panel
panel_path = Path("data/panel.csv")
if panel_path.exists():
    print("\n✅ Current panel.csv found")
    panel = pd.read_csv(panel_path)
    print(f"   Shape: {panel.shape}")
    print(f"   Columns: {list(panel.columns)}")
    print(f"   Ownership types: {panel['ownership'].unique().tolist()}")
else:
    print("\n❌ panel.csv not found")

# Check for Provider Info file
provider_paths = [
    "edq_journal/cache/NH_ProviderInfo.csv",
    "../edq_journal/cache/NH_ProviderInfo.csv",
    "data/NH_ProviderInfo.csv",
]

provider_found = False
for path_str in provider_paths:
    path = Path(path_str)
    if path.exists():
        print(f"\n✅ Provider Info found at: {path}")
        provider_found = True
        
        # Load and inspect
        provider = pd.read_csv(path, nrows=5)
        print(f"   Shape: {provider.shape}")
        print(f"\n   Available columns:")
        for i, col in enumerate(provider.columns, 1):
            print(f"   {i:3d}. {col}")
        
        # Check for specific fields
        print("\n   KEY FIELDS FOR LTCCC QUESTIONS:")
        
        # Question 1: Rural/Urban
        urban_cols = [c for c in provider.columns if 'urban' in c.lower() or 'rural' in c.lower()]
        if urban_cols:
            print(f"   ✅ Rural/Urban field(s): {urban_cols}")
        else:
            print("   ❌ No obvious rural/urban field found")
        
        # Question 2: Ownership subtypes
        ownership_cols = [c for c in provider.columns if 'owner' in c.lower() or 'legal' in c.lower()]
        if ownership_cols:
            print(f"   ✅ Ownership field(s): {ownership_cols}")
        else:
            print("   ❌ No ownership subtype fields found")
        
        # Question 3: Facility identifiers
        facility_cols = [c for c in provider.columns if 'prov' in c.lower() or 'ccn' in c.lower() or 'federal' in c.lower()]
        if facility_cols:
            print(f"   ✅ Facility ID field(s): {facility_cols}")
        else:
            print("   ❌ No facility identifier found")
        
        break

if not provider_found:
    print("\n❌ Provider Info file NOT found in expected locations:")
    for path_str in provider_paths:
        print(f"   - {path_str}")
    print("\n   ACTION: You need to locate or re-download NH_ProviderInfo.csv")

# Check for raw PBJ files (for facility-level rebuild)
print("\n" + "=" * 70)
print("RAW PBJ DATA CHECK (for facility-level analysis)")
print("=" * 70)

pbj_paths = [
    "edq_journal/cache/",
    "../edq_journal/cache/",
]

pbj_found = False
for path_str in pbj_paths:
    path = Path(path_str)
    if path.exists() and path.is_dir():
        pbj_files = list(path.glob("PBJ_*.csv"))
        if pbj_files:
            print(f"\n✅ PBJ files found in: {path}")
            print(f"   Number of files: {len(pbj_files)}")
            print(f"   Example files:")
            for f in sorted(pbj_files)[:3]:
                print(f"   - {f.name}")
            pbj_found = True
            break

if not pbj_found:
    print("\n❌ PBJ employee detail files NOT found")
    print("   These are needed for facility-level analysis")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("\nQuestion 1 (Rural vs Urban):")
if provider_found and urban_cols:
    print("   🟢 READY - Can add to panel immediately")
elif provider_found:
    print("   🟡 PARTIAL - Provider file exists, need to find urban field")
else:
    print("   🔴 BLOCKED - Need Provider Info file")

print("\nQuestion 2 (Ownership Subtypes):")
if provider_found and ownership_cols:
    print("   🟢 READY - Ownership fields available")
elif provider_found:
    print("   🟡 PARTIAL - Provider file exists, need to check ownership detail")
else:
    print("   🔴 BLOCKED - Need Provider Info file")

print("\nQuestion 3 (Facility-Level Risk):")
if pbj_found:
    print("   🟡 FEASIBLE - Have raw data, needs major pipeline rebuild")
else:
    print("   🔴 BLOCKED - Need raw PBJ files for facility-level data")

print("\n" + "=" * 70)
