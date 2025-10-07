# 🌿 BioPulse Documentation

A minimalist, science-inspired GitHub contribution visualizer that creates beautiful organic spiral patterns from your coding activity.

## 🎨 What It Does

BioPulse transforms your GitHub contribution history into a living, breathing visualization:

- **Each dot** represents a day of activity
- **Dot size** scales with contribution intensity
- **Color intensity** reflects your coding rhythm
- **Spiral pattern** creates an organic, biomorphic layout
- **Pulse animation** highlights your most active days

## 🚀 Quick Start

### Automatic Generation (Recommended)

The visualization updates automatically every day at midnight UTC via GitHub Actions. You can also trigger it manually:

1. Go to your repository's **Actions** tab
2. Click on **BioPulse** workflow
3. Click **Run workflow**

### Manual Generation (Local Testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Set your GitHub token (optional but recommended to avoid rate limits)
export GITHUB_TOKEN=your_token_here

# Generate the SVG
python generate_biopulse.py
```

The output will be saved to `dist/biopulse.svg`.

## 📊 How It Works

### 1. Data Fetching

The script uses GitHub's GraphQL API to fetch your contribution calendar:

```graphql
{
  user(login: "your_username") {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
```

### 2. Spiral Algorithm

Each day is positioned using a logarithmic spiral:

```python
θ = day_index × 0.15
r = base_radius + (day_index × growth_factor)
x = center_x + r × cos(θ)
y = center_y + r × sin(θ)
```

This creates a natural, organic flow from the center outward.

### 3. Visual Encoding

- **Dot Size**: 1.5px (no activity) → 8px (max activity)
- **Color**: 
  - Inactive: `#102A43` (deep blue)
  - Active: `#00E5FF` (cyan)
  - Highly active: `#7CFCFF` (bright cyan)
- **Opacity**: 0.2 (inactive) → 1.0 (highly active)
- **Animation**: Pulse effect on days with >50% of max contributions

### 4. SVG Optimization

- Uses native SVG `<animate>` elements (no JavaScript)
- Glow effect via `<feGaussianBlur>` filter
- Radial gradient background for depth
- Total file size: ~30-40 KB (well under 50 KB target)

## 🎨 Color Palette

```css
Background:    #0D1117 → #010409 (radial gradient)
Inactive Dots: #102A43 (20% opacity)
Active Dots:   #00E5FF (30-100% opacity)
Highlights:    #7CFCFF (days with 70%+ of max activity)
Text:          #7CFCFF (title) / #00E5FF (subtitle)
```

This palette is optimized for GitHub's dark theme and provides excellent contrast without being harsh.

## 🔧 Customization

### Adjust the Spiral

Edit these parameters in `generate_biopulse.py`:

```python
# Spiral parameters (line ~105)
angle_increment = 0.15   # Smaller = tighter spiral
base_radius = 20         # Starting radius
radius_growth = 0.4      # How fast spiral expands
```

### Change Colors

Update the class constants:

```python
class BioPulseGenerator:
    BG_COLOR = "#0D1117"
    ACTIVE_COLOR = "#00E5FF"
    INACTIVE_COLOR = "#102A43"
    HIGHLIGHT_COLOR = "#7CFCFF"
```

### Modify Animation

Adjust pulse speed (line ~189):

```python
pulse_duration = 3 + (i % 3)  # 3-6 second cycles
```

### Canvas Size

Change SVG dimensions:

```python
WIDTH = 800   # Default: 800px
HEIGHT = 600  # Default: 600px
```

## 📐 Technical Specifications

| Aspect              | Value                                  |
| ------------------- | -------------------------------------- |
| **Language**        | Python 3.11+                           |
| **Dependencies**    | `requests` (only)                      |
| **Output Format**   | SVG (Scalable Vector Graphics)         |
| **File Size**       | ~30-40 KB                              |
| **Data Range**      | Last 365 days                          |
| **Update Frequency**| Daily (00:00 UTC)                      |
| **Animation**       | CSS-based (no JavaScript)              |
| **Responsive**      | Yes (viewBox-based scaling)            |

## 🐛 Troubleshooting

### "Error fetching contributions"

**Cause**: GitHub API rate limit or authentication failure.

**Solution**:
1. Ensure `GITHUB_TOKEN` is set in the workflow (it should be automatic)
2. For local testing, create a Personal Access Token with `read:user` scope
3. The script falls back to dummy data for testing if API fails

### SVG not showing in README

**Cause**: The visualization hasn't been generated yet or the output branch doesn't exist.

**Solution**:
1. Run the workflow manually from the Actions tab
2. Wait for it to complete
3. Refresh your README page (may take a few minutes)
4. Check that the `output` branch exists in your repository

### File size too large

**Cause**: Too many data points or verbose SVG markup.

**Solution**:
1. The current implementation should always be under 50 KB
2. If needed, reduce `angle_increment` to show fewer days
3. Remove animation elements to save ~5 KB

### Colors look wrong in light mode

**Current behavior**: Optimized for dark mode only.

**Future enhancement**: Add media query support:

```svg
<style>
  @media (prefers-color-scheme: light) {
    .dot { filter: invert(1); }
  }
</style>
```

## 🌟 Features & Benefits

✅ **Lightweight**: Pure SVG, no JavaScript dependencies  
✅ **Fast**: Loads instantly, no external requests  
✅ **Elegant**: Minimalist, science-inspired design  
✅ **Informative**: Shows activity patterns at a glance  
✅ **Automated**: Updates daily without manual intervention  
✅ **Accessible**: Includes tooltips on each dot  
✅ **Professional**: Subtle, not distracting  

## 📈 Future Enhancements

Potential additions (not implemented yet):

- **Multiple layouts**: Grid, wave, or radial options
- **Color themes**: Light mode support
- **Interactive mode**: JavaScript version with zoom/pan
- **Stats overlay**: Weekly/monthly aggregates
- **Comparison mode**: Show multiple users
- **Language breakdown**: Color by programming language

## 📝 License

This implementation is part of your personal GitHub profile. Feel free to modify and adapt it to your needs!

## 🙏 Credits

- **Design philosophy**: Inspired by biological rhythms and natural patterns
- **Color palette**: GitHub's dark theme + bioluminescent cyan tones
- **Spiral algorithm**: Based on Archimedean spiral mathematics
- **Implementation**: Custom Python script with minimal dependencies

---

**Generated with ❤️ by BioPulse**  
*Making data visualization feel alive*

