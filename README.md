# BG Remover

Hey there! 👋 Thanks for checking out my background remover tool. I built this during a weekend coding binge when I got tired of using online tools that kept watermarking my images or making me pay for downloads.

## What does it do?

Pretty much what it says on the tin - it removes backgrounds from images! But with some nice extras:

- **Simple drag & drop** - Just drag your image in and watch the magic happen
- **Custom background colors** - Want your product on a bright red background? Easy.
- **Direct downloads** - No annoying "create an account to download" nonsense
- **Clean, dark UI** - Because light mode hurts my eyes at 2am

## Demo

Check out how easy it is to use BG Remover:
https://bg-remover-pc.vercel.app/



<video width="640" height="360" controls>
  <source src="preview.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Getting Started

### The easy way:

1. Download the latest release
2. Run `Run_BG_Remover.bat`
3. That's it. Seriously.

### The nerd way (for devs):

```bash
# Clone the repo
git clone https://github.com/izhan0102/BG_Remover_PC.git

# Install dependencies
pip install -r requirements.txt

# Run it
python hello_world.py  # (yeah I know, weird filename - long story)
```

## Requirements

- Windows 10/11
- At least 4GB RAM (those ML models get hungry)
- Some patience for the first run while it downloads the ML model

## How it works

Behind the scenes, this app uses the awesome [rembg](https://github.com/danielgatis/rembg) library, which uses a U^2-Net model to detect foreground objects. I just wrapped it in a nicer UI so you don't have to touch the command line.

## Known Issues

- Processing large images (>4K) might make things a bit sluggish
- Occasionally struggles with very fine details like hair or fur
- Some transparent PNGs may look odd when background color is applied

## Changelog

### v1.2
- Added color replacement with real-time preview
- Fixed transparency issues in saved images
- Made the UI more compact

### v1.1
- Added drag & drop support
- Improved progress visualization
- Fixed that annoying bug with the save dialog

### v1.0
- Initial release
- Basic functionality

## Got ideas?

If you've got suggestions or found bugs (there are definitely bugs), feel free to:

1. Open an issue
2. Submit a PR if you're feeling brave
3. Connect with me on [LinkedIn](https://www.linkedin.com/in/muhammad-izhan-a404752a6/)

Built with ❤️ by Muhammad Izhan. Enjoy! 
