# 🎬 Webpage Reel Video Generator

Automatically create engaging social media reels from any webpage! Perfect for promoting websites, showcasing web apps, or creating demo videos.

## ✨ Features

- 📱 **Social Media Ready**: Generates videos in 9:16 aspect ratio (1080x1920) perfect for Instagram Reels, TikTok, YouTube Shorts
- 🔍 **Dummy Search Bar**: Adds a professional-looking search bar overlay (like those TV ads!)
- 🎯 **Smooth Scrolling**: Automatic smooth scrolling from top to bottom with easing animation
- ⚡ **Easy to Use**: Just provide a URL and get your video!
- 🎨 **Customizable**: Adjust duration, FPS, and output filename

## 📋 Requirements

- Python 3.7+
- Chromium/Chrome browser
- ChromeDriver

## 🚀 Quick Start

### Installation

1. Clone or download the files
2. Run the setup script:
```bash
bash setup.sh
```

Or install manually:
```bash
pip install -r requirements.txt
```

### Basic Usage

Generate a reel from any webpage:
```bash
python3 webpage_reel_generator.py https://example.com
```

### Advanced Usage

Customize output filename, duration, and FPS:
```bash
python3 webpage_reel_generator.py https://example.com my_promo.mp4 20 30
```

**Parameters:**
- `URL` (required): The webpage to capture
- `output_file` (optional): Output video filename (default: webpage_reel.mp4)
- `duration` (optional): Video duration in seconds (default: 15)
- `fps` (optional): Frames per second (default: 30)

## 📖 Examples

### Example 1: Quick 15-second reel
```bash
python3 webpage_reel_generator.py https://www.apple.com
```

### Example 2: Longer promotional video
```bash
python3 webpage_reel_generator.py https://www.shopify.com shopify_demo.mp4 25 30
```

### Example 3: Your own website
```bash
python3 webpage_reel_generator.py https://yourstartup.com startup_promo.mp4 18 60
```

## 🎨 What It Creates

The generator creates a professional-looking video with:

1. **Smooth Scrolling Animation**: The page scrolls smoothly from top to bottom with easing
2. **Search Bar Overlay**: A clean, modern search bar at the top showing the website domain
3. **Social Media Format**: Perfect 9:16 vertical format for mobile viewing
4. **High Quality**: HD resolution (1080x1920) suitable for all platforms

## 💡 Use Cases

- 📱 **Social Media Marketing**: Create eye-catching ads for Instagram, TikTok, or YouTube Shorts
- 🎯 **Product Demos**: Showcase your web application or SaaS product
- 🚀 **Landing Page Promos**: Turn your landing page into a video ad
- 📧 **Email Campaigns**: Embed videos in your marketing emails
- 🎪 **Portfolio Pieces**: Show off your web design work

## ⚙️ How It Works

1. **Capture**: Uses Selenium to load and capture the full webpage
2. **Process**: Creates a smooth scrolling animation with easing
3. **Overlay**: Adds a professional search bar with the site domain
4. **Render**: Generates an MP4 video frame by frame

## 🐛 Troubleshooting

### "Chrome not found" error
Install Chromium or Chrome browser:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install --cask chromium
```

### "ChromeDriver not found" error
Install ChromeDriver:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver
```

### Video quality issues
Increase the FPS for smoother animation:
```bash
python3 webpage_reel_generator.py https://example.com output.mp4 15 60
```

### Very long pages
Increase the duration to allow more time for scrolling:
```bash
python3 webpage_reel_generator.py https://example.com output.mp4 30 30
```

## 🔧 Advanced Configuration

You can modify the script to customize:

- Video dimensions (change `self.width` and `self.height`)
- Search bar design (modify `create_search_bar_overlay()`)
- Scroll speed and easing (adjust in `generate_video()`)
- Color scheme and styling

## 📝 Notes

- Works best with responsive websites
- Pages with animations may need longer load times (adjust sleep in code)
- Very long pages work better with longer durations
- Video file size depends on duration and FPS

## 🎯 Tips for Best Results

1. **Test First**: Try with a 10-second duration first to see the result
2. **Adjust Duration**: Match duration to page length (longer pages = longer duration)
3. **Higher FPS**: Use 60 FPS for ultra-smooth scrolling
4. **Mobile Preview**: Most social platforms prefer vertical video
5. **File Size**: Lower FPS (24-30) for smaller file sizes

## 📄 License

Free to use for any purpose. No attribution required.

## 🤝 Contributing

Feel free to modify and improve the script! Common improvements:
- Add background music
- Add text overlays
- Custom branding
- Multiple page support
- Zoom effects

## 📧 Support

For issues or questions, check:
- Make sure all dependencies are installed
- Verify your internet connection
- Try with a simple webpage first (like example.com)

---

Happy video creating! 🎉
