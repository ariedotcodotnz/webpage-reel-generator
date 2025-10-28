#!/usr/bin/env python3
"""
Quick demo script for the Webpage Reel Generator
Tests with a simple webpage
"""

import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from webpage_reel_generator import WebpageReelGenerator

def demo():
    """Run a quick demo"""
    print("🎬 Running Quick Demo")
    print("=" * 60)
    print("This will create a short 10-second reel of example.com")
    print("Perfect for testing if everything works!")
    print("=" * 60)
    print()
    
    # Create a short demo reel
    generator = WebpageReelGenerator(
        url="https://example.com",
        output_file="demo_reel.mp4",
        duration=10,
        fps=30
    )
    
    try:
        generator.generate()
        print()
        print("✨ Demo complete!")
        print("🎥 Check out demo_reel.mp4 to see the result")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print()
        print("💡 Make sure you've run the setup script:")
        print("   bash setup.sh")
        sys.exit(1)

if __name__ == "__main__":
    demo()
