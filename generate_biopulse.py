#!/usr/bin/env python3
"""
BioPulse - Minimalist GitHub Contribution Visualizer
Generates an organic, spiral-based SVG visualization of GitHub activity.
"""

import os
import math
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class BioPulseGenerator:
    """Generate a biomorphic SVG visualization of GitHub contributions."""
    
    # Color palette (dark-mode friendly)
    BG_COLOR = "#0D1117"
    ACTIVE_COLOR = "#00E5FF"
    INACTIVE_COLOR = "#102A43"
    HIGHLIGHT_COLOR = "#7CFCFF"
    
    # SVG dimensions
    WIDTH = 800
    HEIGHT = 600
    CENTER_X = 400
    CENTER_Y = 300
    
    def __init__(self, username: str, token: str = None):
        self.username = username
        self.token = token
        self.contributions = []
        
    def fetch_contributions(self) -> List[Dict]:
        """Fetch contribution data from GitHub GraphQL API."""
        url = "https://api.github.com/graphql"
        
        # GraphQL query to fetch last year of contributions
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
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
        """
        
        headers = {
            "Authorization": f"Bearer {self.token}" if self.token else "",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "variables": {"username": self.username}
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract contribution days
            weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            days = []
            for week in weeks:
                for day in week["contributionDays"]:
                    days.append({
                        "date": day["date"],
                        "count": day["contributionCount"]
                    })
            
            return days
            
        except Exception as e:
            print(f"Error fetching contributions: {e}")
            # Return dummy data for testing
            return self._generate_dummy_data()
    
    def _generate_dummy_data(self) -> List[Dict]:
        """Generate dummy data for testing when API fails."""
        days = []
        start_date = datetime.now() - timedelta(days=365)
        for i in range(365):
            date = start_date + timedelta(days=i)
            days.append({
                "date": date.strftime("%Y-%m-%d"),
                "count": max(0, int(math.sin(i / 10) * 5 + 5))
            })
        return days
    
    def calculate_spiral_position(self, index: int, total: int, contribution_count: int) -> Tuple[float, float, float]:
        """
        Calculate position and size for a dot in a spiral pattern.
        Returns (x, y, radius).
        """
        # Spiral parameters
        angle_increment = 0.15  # Tighter spiral
        base_radius = 20
        radius_growth = 0.4
        
        # Calculate spiral coordinates
        theta = index * angle_increment
        r = base_radius + (index * radius_growth)
        
        x = self.CENTER_X + r * math.cos(theta)
        y = self.CENTER_Y + r * math.sin(theta)
        
        # Dot size based on contribution count
        # Scale: 0 contributions = 1px, max contributions = 8px
        max_contributions = max([d["count"] for d in self.contributions]) if self.contributions else 1
        if max_contributions == 0:
            max_contributions = 1
        
        normalized = contribution_count / max_contributions
        dot_radius = 1.5 + (normalized * 6.5)
        
        return x, y, dot_radius
    
    def get_dot_color(self, contribution_count: int) -> str:
        """Determine dot color based on contribution count."""
        if contribution_count == 0:
            return self.INACTIVE_COLOR
        
        # Calculate intensity
        max_contributions = max([d["count"] for d in self.contributions]) if self.contributions else 1
        if max_contributions == 0:
            return self.ACTIVE_COLOR
        
        intensity = contribution_count / max_contributions
        
        # Interpolate between active and highlight colors
        if intensity > 0.7:
            return self.HIGHLIGHT_COLOR
        else:
            return self.ACTIVE_COLOR
    
    def get_dot_opacity(self, contribution_count: int) -> float:
        """Calculate opacity based on contribution count."""
        if contribution_count == 0:
            return 0.2
        
        max_contributions = max([d["count"] for d in self.contributions]) if self.contributions else 1
        if max_contributions == 0:
            return 0.8
        
        intensity = contribution_count / max_contributions
        return 0.3 + (intensity * 0.7)
    
    def generate_svg(self) -> str:
        """Generate the complete SVG markup."""
        self.contributions = self.fetch_contributions()
        
        svg_parts = [
            f'<svg width="{self.WIDTH}" height="{self.HEIGHT}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.WIDTH} {self.HEIGHT}">',
            
            # Define filters for glow effect
            '<defs>',
            '<filter id="glow">',
            '<feGaussianBlur stdDeviation="2" result="coloredBlur"/>',
            '<feMerge>',
            '<feMergeNode in="coloredBlur"/>',
            '<feMergeNode in="SourceGraphic"/>',
            '</feMerge>',
            '</filter>',
            
            # Radial gradient for subtle background
            '<radialGradient id="bgGradient" cx="50%" cy="50%" r="50%">',
            '<stop offset="0%" style="stop-color:#0D1117;stop-opacity:1" />',
            '<stop offset="100%" style="stop-color:#010409;stop-opacity:1" />',
            '</radialGradient>',
            '</defs>',
            
            # Background
            f'<rect width="{self.WIDTH}" height="{self.HEIGHT}" fill="url(#bgGradient)"/>',
            
            # Title
            '<text x="400" y="30" font-family="\'Segoe UI\', Arial, sans-serif" font-size="24" '
            'font-weight="300" fill="#7CFCFF" text-anchor="middle" opacity="0.9">',
            'BioPulse',
            '</text>',
            
            '<text x="400" y="55" font-family="\'Segoe UI\', Arial, sans-serif" font-size="12" '
            'fill="#00E5FF" text-anchor="middle" opacity="0.6">',
            f'GitHub Activity · {self.username}',
            '</text>',
        ]
        
        # Generate dots for each day
        total_days = len(self.contributions)
        for i, day in enumerate(self.contributions):
            x, y, radius = self.calculate_spiral_position(i, total_days, day["count"])
            color = self.get_dot_color(day["count"])
            opacity = self.get_dot_opacity(day["count"])
            
            # Create circle with optional pulse animation for active days
            circle_parts = [
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" '
                f'fill="{color}" opacity="{opacity:.2f}" filter="url(#glow)">'
            ]
            
            # Add tooltip
            circle_parts.append(f'<title>{day["date"]}: {day["count"]} contributions</title>')
            
            # Add pulse animation for highly active days
            if day["count"] > 0:
                max_contributions = max([d["count"] for d in self.contributions])
                if day["count"] >= max_contributions * 0.5:
                    pulse_duration = 3 + (i % 3)  # Vary animation timing
                    circle_parts.append(
                        f'<animate attributeName="opacity" values="{opacity:.2f};{min(1, opacity * 1.3):.2f};{opacity:.2f}" '
                        f'dur="{pulse_duration}s" repeatCount="indefinite"/>'
                    )
            
            circle_parts.append('</circle>')
            svg_parts.extend(circle_parts)
        
        # Footer with stats
        total_contributions = sum(d["count"] for d in self.contributions)
        active_days = sum(1 for d in self.contributions if d["count"] > 0)
        
        svg_parts.extend([
            '<text x="400" y="580" font-family="\'Segoe UI\', Arial, sans-serif" font-size="11" '
            'fill="#00E5FF" text-anchor="middle" opacity="0.5">',
            f'{total_contributions} contributions · {active_days} active days · Last 365 days',
            '</text>',
            '</svg>'
        ])
        
        return '\n'.join(svg_parts)
    
    def save(self, output_path: str = "dist/biopulse.svg"):
        """Generate and save the SVG to a file."""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate SVG
        svg_content = self.generate_svg()
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"✅ BioPulse generated successfully: {output_path}")
        print(f"📊 Total contributions: {sum(d['count'] for d in self.contributions)}")
        print(f"📅 Active days: {sum(1 for d in self.contributions if d['count'] > 0)}")
        print(f"💾 File size: {len(svg_content)} bytes ({len(svg_content) / 1024:.1f} KB)")


def main():
    """Main entry point."""
    # Get username from environment or default
    username = os.getenv("GITHUB_ACTOR", "rm2thaddeus")
    
    # Get GitHub token from environment (optional but recommended)
    token = os.getenv("GITHUB_TOKEN")
    
    print(f"🌿 Generating BioPulse for {username}...")
    
    # Create generator and save
    generator = BioPulseGenerator(username, token)
    generator.save("dist/biopulse.svg")
    
    print("✨ Done!")


if __name__ == "__main__":
    main()

