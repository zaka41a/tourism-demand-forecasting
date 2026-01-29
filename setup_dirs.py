#!/usr/bin/env python3
"""
Setup script to create necessary directories and placeholder files.
Run this after cloning the repository.
"""

import os

def create_directory_structure():
    """Create all necessary directories with .gitkeep files."""

    directories = [
        "data/raw",
        "data/processed",
        "data/test",
        "models",
        "logs",
    ]

    print("Creating directory structure...")

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

        # Create .gitkeep file to preserve empty directories in git
        gitkeep_path = os.path.join(directory, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write("# This file ensures the directory is tracked by git\n")

        print(f"  ✓ Created: {directory}")

    print("\n✅ Directory structure created successfully!")
    print("\nNext steps:")
    print("  1. Place your data CSV file in data/raw/")
    print("  2. Run: python train.py")
    print("  3. Or launch dashboard: streamlit run dashboard/app.py")

if __name__ == "__main__":
    create_directory_structure()
