#!/usr/bin/env python3
"""
Webpage Reel Video Generator
Creates a scrolling video of a webpage with a dummy search bar overlay
Perfect for social media promotion
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from urllib.parse import urlparse

class WebpageReelGenerator:
    def __init__(self, url, output_file="webpage_reel.mp4", duration=15, fps=30):
        """
        Initialize the reel generator
        
        Args:
            url: The webpage URL to capture
            output_file: Output video filename
            duration: Video duration in seconds
            fps: Frames per second
        """
        self.url = url
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
            
            screenshot_path = '/tmp/webpage_full.png'
            self.driver.save_screenshot(screenshot_path)
            
            print("✓ Webpage captured successfully")
            return screenshot_path, total_height
            
        except Exception as e:
            print(f"✗ Error capturing webpage: {e}")
            raise
            
    def create_search_bar_overlay(self):
        """Create a dummy search bar overlay"""
        # Create search bar image
        search_bar = Image.new('RGBA', (self.width, self.search_bar_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(search_bar)
        
        # Draw search bar background with gradient effect
        for y in range(self.search_bar_height):
            alpha = int(255 * (1 - y / self.search_bar_height * 0.3))
            draw.rectangle([(0, y), (self.width, y + 1)], fill=(255, 255, 255, alpha))
        
        # Draw search box
        padding = 20
        box_height = 60
        box_y = (self.search_bar_height - box_height) // 2
        
        # Search box background
        draw.rounded_rectangle(
            [(padding, box_y), (self.width - padding, box_y + box_height)],
            radius=30,
            fill=(240, 240, 240, 255),
            outline=(200, 200, 200, 255),
            width=2
        )
        
        # Add search icon (simplified)
        icon_x = padding + 20
        icon_y = box_y + box_height // 2
        icon_radius = 12
        draw.ellipse(
            [(icon_x - icon_radius, icon_y - icon_radius),
             (icon_x + icon_radius, icon_y + icon_radius)],
            outline=(100, 100, 100, 255),
            width=3
        )
        draw.line(
            [(icon_x + icon_radius - 3, icon_y + icon_radius - 3),
             (icon_x + icon_radius + 5, icon_y + icon_radius + 5)],
            fill=(100, 100, 100, 255),
            width=3
        )
        
        # Add text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
            
        domain = urlparse(self.url).netloc.replace('www.', '')
        text = f"Search {domain}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = icon_x + 40
        text_y = box_y + (box_height - (text_bbox[3] - text_bbox[1])) // 2
        
        draw.text((text_x, text_y), text, fill=(150, 150, 150, 255), font=font)
        
        return search_bar
        
    def generate_video(self, screenshot_path, page_height):
        """Generate the scrolling video"""
        print("🎬 Generating video...")
        
        # Load the screenshot
        webpage_img = Image.open(screenshot_path)
        search_bar = self.create_search_bar_overlay()
        
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
            
            # Create final frame with search bar
            final_frame = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))
            final_frame.paste(search_bar, (0, 0), search_bar)
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
        print("  output_file  : Output video filename (default: webpage_reel.mp4)")
        print("  duration     : Video duration in seconds (default: 15)")
        print("  fps          : Frames per second (default: 30)")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "webpage_reel.mp4"
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    
    generator = WebpageReelGenerator(url, output_file, duration, fps)
    generator.generate()


if __name__ == "__main__":
    main()
