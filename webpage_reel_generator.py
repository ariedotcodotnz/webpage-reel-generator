#!/usr/bin/env python3
"""
Webpage Reel Video Generator
Creates a scrolling video of a webpage with a dummy search bar overlay
Perfect for social media promotion
"""

import os
import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from urllib.parse import urlparse


class WebpageReelGenerator:
    def __init__(self, url, output_file=None, duration=15, fps=30):
        """
        Initialize the reel generator

        Args:
            url: The webpage URL to capture
            output_file: Output video filename (default: uses website domain name)
            duration: Video duration in seconds
            fps: Frames per second
        """
        self.url = url

        # Generate filename from URL if not provided
        if output_file is None:
            domain = urlparse(url).netloc.replace('www.', '')
            # Clean domain name for filename (remove special chars)
            clean_domain = ''.join(c if c.isalnum() or c in '.-' else '_' for c in domain)
            output_file = f"{clean_domain}_reel.mp4"

        self.output_file = output_file
        self.duration = duration
        self.fps = fps
        self.width = 1080  # Instagram/TikTok reel width
        self.height = 1920  # Instagram/TikTok reel height
        self.search_bar_height = 120

    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--window-size={self.width},{self.height * 3}')
        chrome_options.add_argument('--hide-scrollbars')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Chrome WebDriver initialized")
        except Exception as e:
            print(f"✗ Error initializing Chrome: {e}")
            print("Installing ChromeDriver...")
            raise

    def capture_webpage(self):
        """Capture the full webpage as a screenshot"""
        print(f"📸 Capturing webpage: {self.url}")

        try:
            self.driver.get(self.url)
            time.sleep(3)  # Wait for page to load

            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")

            print(f"   Page height: {total_height}px")

            # Capture full page screenshot
            self.driver.set_window_size(self.width, total_height)
            time.sleep(1)

            # Use cross-platform temp directory
            temp_dir = tempfile.gettempdir()
            screenshot_path = os.path.join(temp_dir, 'webpage_full.png')
            self.driver.save_screenshot(screenshot_path)

            print("✓ Webpage captured successfully")
            return screenshot_path, total_height

        except Exception as e:
            print(f"✗ Error capturing webpage: {e}")
            raise

    def create_browser_address_bar(self):
        """Create a browser-style address bar overlay"""
        # Create address bar image
        address_bar = Image.new('RGBA', (self.width, self.search_bar_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(address_bar)

        # Draw address bar background with gradient effect (darker, more browser-like)
        for y in range(self.search_bar_height):
            alpha = int(255 * (1 - y / self.search_bar_height * 0.2))
            # Slightly darker gray for browser chrome look
            gray_value = 245 - int(y / self.search_bar_height * 10)
            draw.rectangle([(0, y), (self.width, y + 1)], fill=(gray_value, gray_value, gray_value, alpha))

        # Draw address/URL box
        padding = 15
        box_height = 55
        box_y = (self.search_bar_height - box_height) // 2

        # Address box background (white with subtle border)
        draw.rounded_rectangle(
            [(padding, box_y), (self.width - padding, box_y + box_height)],
            radius=8,
            fill=(255, 255, 255, 255),
            outline=(220, 220, 220, 255),
            width=1
        )

        # Draw lock icon (for HTTPS)
        lock_x = padding + 20
        lock_y = box_y + box_height // 2
        lock_size = 10

        # Lock body
        draw.rounded_rectangle(
            [(lock_x - lock_size // 2, lock_y - 2),
             (lock_x + lock_size // 2, lock_y + lock_size // 2)],
            radius=2,
            fill=(100, 180, 100, 255)
        )

        # Lock shackle
        draw.arc(
            [(lock_x - lock_size // 2 + 1, lock_y - lock_size),
             (lock_x + lock_size // 2 - 1, lock_y)],
            start=180,
            end=0,
            fill=(100, 180, 100, 255),
            width=2
        )

        # Add URL text
        try:
            # Try different font paths for different operating systems
            font_paths = [
                "C:\\Windows\\Fonts\\Arial.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Linux alt
            ]

            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 20)
                    break

            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Display the actual URL
        url_text = self.url
        # Truncate if too long
        text_bbox = draw.textbbox((0, 0), url_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        max_width = self.width - padding * 2 - 120  # Leave space for lock icon and refresh button

        if text_width > max_width:
            # Truncate URL if too long
            while text_width > max_width and len(url_text) > 10:
                url_text = url_text[:-4] + "..."
                text_bbox = draw.textbbox((0, 0), url_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]

        text_x = lock_x + 25
        text_y = box_y + (box_height - (text_bbox[3] - text_bbox[1])) // 2

        draw.text((text_x, text_y), url_text, fill=(60, 60, 60, 255), font=font)

        # Draw refresh/menu icons on the right (simple dots for menu)
        right_x = self.width - padding - 30
        dot_y = box_y + box_height // 2

        # Three vertical dots (menu icon)
        for i in range(3):
            dot_offset = (i - 1) * 8
            draw.ellipse(
                [(right_x - 2, dot_y + dot_offset - 2),
                 (right_x + 2, dot_y + dot_offset + 2)],
                fill=(120, 120, 120, 255)
            )

        return address_bar

    def generate_video(self, screenshot_path, page_height):
        """Generate the scrolling video"""
        print("🎬 Generating video...")

        # Load the screenshot
        webpage_img = Image.open(screenshot_path)
        browser_bar = self.create_browser_address_bar()

        # Calculate scroll parameters
        total_frames = self.duration * self.fps
        scroll_distance = page_height - self.height + self.search_bar_height

        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            self.output_file,
            fourcc,
            self.fps,
            (self.width, self.height)
        )

        print(f"   Creating {total_frames} frames at {self.fps} FPS...")

        for frame_num in range(total_frames):
            # Calculate scroll position with easing
            progress = frame_num / total_frames
            # Ease in-out cubic
            eased_progress = progress ** 2 * (3 - 2 * progress)
            scroll_y = int(eased_progress * scroll_distance)

            # Crop the webpage at current scroll position
            frame = webpage_img.crop((
                0,
                scroll_y,
                self.width,
                scroll_y + self.height - self.search_bar_height
            ))

            # Convert to RGBA if needed
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')

            # Create final frame with browser address bar
            final_frame = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))
            final_frame.paste(browser_bar, (0, 0), browser_bar)
            final_frame.paste(frame, (0, self.search_bar_height))

            # Convert to OpenCV format
            frame_cv = cv2.cvtColor(np.array(final_frame.convert('RGB')), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

            # Progress indicator
            if (frame_num + 1) % (self.fps * 2) == 0:
                print(f"   Progress: {int((frame_num + 1) / total_frames * 100)}%")

        out.release()
        print(f"✓ Video saved to: {self.output_file}")

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def generate(self):
        """Main generation process"""
        try:
            print("=" * 60)
            print("🎥 Webpage Reel Generator")
            print("=" * 60)

            self.setup_driver()
            screenshot_path, page_height = self.capture_webpage()
            self.generate_video(screenshot_path, page_height)

            print("=" * 60)
            print("✨ Reel generated successfully!")
            print(f"📁 Output: {os.path.abspath(self.output_file)}")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise
        finally:
            self.cleanup()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python webpage_reel_generator.py <URL> [output_file] [duration] [fps]")
        print("\nExample:")
        print("  python webpage_reel_generator.py https://example.com")
        print("  python webpage_reel_generator.py https://example.com my_reel.mp4 20 30")
        print("\nParameters:")
        print("  URL          : The webpage URL to capture (required)")
        print("  output_file  : Output video filename (default: uses website domain name)")
        print("  duration     : Video duration in seconds (default: 15)")
        print("  fps          : Frames per second (default: 30)")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30

    generator = WebpageReelGenerator(url, output_file, duration, fps)
    generator.generate()


if __name__ == "__main__":
    main()