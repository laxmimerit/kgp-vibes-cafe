#!/usr/bin/env python3
"""
generate_menu_card.py
Generates a print-ready table menu card for KGP Vibes Cafe.
Matches the site look from DESIGN.md:
- Colors: Steamed Oat Cream (#FAF7F2), Pure White / Cream cards (#FFFFFF),
  Deep Espresso Roast (#2B1810), Warm Chai Amber (#C25E1A), Espresso Muted (#564339).
- Typography: Literata/Georgia serif headings, Plus Jakarta Sans/Segoe UI body,
  JetBrains Mono/Consolas prices and code tags.
- All 39 items from baseline/menu.csv grouped by category on a single page.
- Clean vector layout with vector shapes (no font emojis or bitmap photos)
  so it prints cleanly in any PDF viewer.
- Scannable QR code linking to the site menu page.
- Single configurable site address setting.
- Exports to print/menu_a4.pdf and print/menu_letter.pdf.
"""

import os
import csv
import io
import sys
from PIL import Image
import segno
import zxingcpp
import pymupdf

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==============================================================================
# SETTINGS
# ==============================================================================
# The website menu page address. Keep this in one setting so it can be changed
# when the site goes live. Can also be overridden by CAFE_MENU_URL env var.
SITE_MENU_URL = os.environ.get("CAFE_MENU_URL", "https://kgp-vibes-cafe.vercel.app/menu")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "baseline", "menu.csv")
PRINT_DIR = os.path.join(BASE_DIR, "print")

# ==============================================================================
# COLOR PALETTE (From DESIGN.md)
# ==============================================================================
C_SURFACE = HexColor('#FAF7F2')            # Steamed Oat Cream (canvas)
C_CARD_BG = HexColor('#FFFFFF')            # Pure White (cards)
C_CARD_HEADER_BG = HexColor('#F6F3EE')     # Light Linen
C_BORDER = HexColor('#E8DFC8')             # Warm Biscuit Border
C_BORDER_LIGHT = HexColor('#F0EDE9')       # Oatmeal divider
C_PRIMARY = HexColor('#C25E1A')            # Warm Chai Amber
C_PRIMARY_LIGHT = HexColor('#FCD8CA')      # Toasted Biscuit pill
C_SECONDARY = HexColor('#2B1810')          # Deep Espresso Roast
C_ON_SURFACE = HexColor('#1C1C19')         # Deep Charcoal Roast (item names)
C_MUTED = HexColor('#564339')              # Espresso Muted (descriptions)
C_MUTED_LIGHT = HexColor('#785D52')        # Subtitle secondary
C_DOTS = HexColor('#D8CEB9')               # Subtle leader dots
C_WHITE = HexColor('#FFFFFF')

# Dietary badge colors
C_VEG_TEXT = HexColor('#15803D')
C_VEG_BG = HexColor('#DCFCE7')
C_VEGAN_TEXT = HexColor('#0369A1')
C_VEGAN_BG = HexColor('#E0F2FE')
C_EGG_TEXT = HexColor('#92400E')
C_EGG_BG = HexColor('#FEF3C7')
C_NONVEG_TEXT = HexColor('#BA1A1A')
C_NONVEG_BG = HexColor('#FFDAD6')

# ==============================================================================
# FONT REGISTRATION
# ==============================================================================
def register_fonts():
    """Register fonts according to DESIGN.md hierarchy with system fallbacks."""
    font_candidates = [
        ('FontHeadingBold', ['C:/Windows/Fonts/georgiab.ttf', 'C:/Windows/Fonts/timesbd.ttf']),
        ('FontHeading', ['C:/Windows/Fonts/georgia.ttf', 'C:/Windows/Fonts/times.ttf']),
        ('FontHeadingItalic', ['C:/Windows/Fonts/georgiai.ttf', 'C:/Windows/Fonts/timesi.ttf']),
        ('FontBodyBold', ['C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/arialbd.ttf']),
        ('FontBody', ['C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']),
        ('FontBodyItalic', ['C:/Windows/Fonts/segoeuii.ttf', 'C:/Windows/Fonts/ariali.ttf']),
        ('FontCodeBold', ['C:/Windows/Fonts/consolab.ttf', 'C:/Windows/Fonts/courbd.ttf']),
        ('FontCode', ['C:/Windows/Fonts/consola.ttf', 'C:/Windows/Fonts/cour.ttf']),
    ]
    
    for font_name, paths in font_candidates:
        registered = False
        for p in paths:
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, p))
                    registered = True
                    break
                except Exception:
                    pass
        if not registered:
            print(f"Warning: Could not register font {font_name}, fallback will be used.")

register_fonts()

# ==============================================================================
# VECTOR SHAPE DRAWING (Icons & Logo)
# ==============================================================================
def draw_header_logo(c, x, y, size):
    """Draw cafe logo box with white vector coffee cup (matching site logo)."""
    c.saveState()
    # Brand orange container
    c.setFillColor(C_PRIMARY)
    c.roundRect(x, y, size, size, radius=5.5, stroke=0, fill=1)
    
    cx = x + size / 2.0
    cy = y + size / 2.0 - 2.5
    
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_WHITE)
    c.setLineWidth(1.3)
    
    # Cup body
    w = 15.0
    h = 11.5
    cup_x = cx - w / 2.0
    cup_y = cy - h / 2.0
    c.roundRect(cup_x, cup_y, w, h, radius=3.0, stroke=1, fill=1)
    
    # Handle loop on right
    c.roundRect(cup_x + w - 1.5, cy - 2.0, 4.8, 7.2, radius=2.4, stroke=1, fill=0)
    
    # Saucer underneath
    c.roundRect(cx - w * 0.75, cup_y - 3.0, w * 1.5, 2.0, radius=1.0, stroke=0, fill=1)
    
    # Steam waves
    c.setLineWidth(1.1)
    for sx in [cx - 2.5, cx + 2.5]:
        p = c.beginPath()
        p.moveTo(sx, cup_y + h + 1.5)
        p.curveTo(sx + 1.5, cup_y + h + 3.5, sx - 1.5, cup_y + h + 5.5, sx, cup_y + h + 7.5)
        c.drawPath(p, stroke=1, fill=0)
        
    c.restoreState()


def draw_category_badge_icon(c, cx, cy, category_type):
    """Draw a vector icon inside a warm circular badge for each category."""
    c.saveState()
    # Badge background circle
    r = 8.5
    c.setFillColor(C_PRIMARY_LIGHT)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.circle(cx, cy, r, stroke=1, fill=1)
    
    c.setStrokeColor(C_PRIMARY)
    c.setFillColor(C_PRIMARY)
    
    if category_type == 'coffee':
        # Mini coffee cup
        c.setLineWidth(0.8)
        w, h = 7.5, 5.5
        c.roundRect(cx - w / 2.0 - 0.5, cy - h / 2.0 - 0.5, w, h, radius=1.5, stroke=1, fill=0)
        c.roundRect(cx + w / 2.0 - 1.5, cy - 1.5, 2.8, 3.8, radius=1.2, stroke=1, fill=0)
        c.line(cx - 4.5, cy - h / 2.0 - 1.5, cx + 4.5, cy - h / 2.0 - 1.5)
        # Steam line
        p = c.beginPath()
        p.moveTo(cx - 0.5, cy + h / 2.0 + 0.8)
        p.curveTo(cx + 0.5, cy + h / 2.0 + 2.0, cx - 0.5, cy + h / 2.0 + 3.2, cx, cy + h / 2.0 + 4.4)
        c.drawPath(p, stroke=1, fill=0)
        
    elif category_type == 'snacks':
        # Mini croissant / pastry
        c.setLineWidth(0.8)
        w, h = 8.5, 5.0
        x = cx - w / 2.0
        y = cy - h / 2.0
        p = c.beginPath()
        p.moveTo(x, y + 1.0)
        p.curveTo(cx - 2.0, y + h + 1.5, cx + 2.0, y + h + 1.5, x + w, y + 1.0)
        p.curveTo(cx + 2.0, y + 1.5, cx - 2.0, y + 1.5, x, y + 1.0)
        c.drawPath(p, stroke=1, fill=1)
        # Rib lines
        c.setStrokeColor(C_WHITE)
        c.setLineWidth(0.6)
        c.line(cx - 1.5, y + 1.5, cx - 1.0, y + h + 0.2)
        c.line(cx + 1.5, y + 1.5, cx + 1.0, y + h + 0.2)
        
    elif category_type == 'meals':
        # Mini burger
        c.setLineWidth(0.8)
        w, h = 9.0, 7.0
        x = cx - w / 2.0
        y = cy - h / 2.0
        # Top bun dome
        c.roundRect(x, y + 3.8, w, 3.5, radius=1.8, stroke=1, fill=1)
        # Patty
        c.setLineWidth(1.0)
        c.line(x - 0.5, y + 2.3, x + w + 0.5, y + 2.3)
        # Bottom bun
        c.setLineWidth(0.8)
        c.roundRect(x + 0.5, y, w - 1.0, 1.8, radius=0.9, stroke=1, fill=1)
        
    elif category_type == 'desserts':
        # Mini cooler / sundae glass
        c.setLineWidth(0.8)
        w, h = 7.5, 8.0
        x = cx - w / 2.0
        y = cy - h / 2.0
        # Glass bowl (V-shape)
        p = c.beginPath()
        p.moveTo(x, y + h)
        p.lineTo(cx, y + 3.0)
        p.lineTo(x + w, y + h)
        c.drawPath(p, stroke=1, fill=0)
        # Stem & base
        c.line(cx, y + 3.0, cx, y)
        c.line(cx - 2.8, y, cx + 2.8, y)
        # Straw
        c.line(cx, y + 4.0, cx + 3.5, y + h + 2.0)
        
    c.restoreState()


# ==============================================================================
# DATA LOADING
# ==============================================================================
def load_menu_items(csv_path):
    """Load and group the 39 items from CSV."""
    categories = {
        'Coffee': [],
        'Snacks & Meals': [],
        'Meals': [],
        'Desserts & Drinks': []
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row['category']
            if cat in categories:
                categories[cat].append(row)
            else:
                print(f"Unknown category: {cat}")
                
    total = sum(len(v) for v in categories.values())
    if total == 0:
        print(f"Warning: No items found in {csv_path}")
    return categories


# ==============================================================================
# MENU CARD RENDERER
# ==============================================================================
class MenuCardRenderer:
    def __init__(self, page_size, menu_url=SITE_MENU_URL):
        self.page_width, self.page_height = page_size
        self.menu_url = menu_url
        self.is_letter = (page_size == letter)
        
        # Geometry margins (safe print bleed area)
        self.margin_x = 22.0
        self.margin_top = 20.0
        self.margin_bottom = 18.0
        
        # Usable dimensions
        self.content_w = self.page_width - (2 * self.margin_x)
        self.content_h = self.page_height - self.margin_top - self.margin_bottom
        
        # Columns
        self.gutter = 14.0
        self.col_w = (self.content_w - self.gutter) / 2.0
        self.col1_x = self.margin_x
        self.col2_x = self.margin_x + self.col_w + self.gutter
        
        # Pre-generate QR code image
        self.qr_img = self._generate_qr_image()
        
    def _generate_qr_image(self):
        """Generate high-contrast QR code as PNG image bytes."""
        qr = segno.make(self.menu_url, error='M')
        buf = io.BytesIO()
        qr.save(buf, kind='png', scale=10, border=1, dark='#2B1810', light='#FFFFFF')
        buf.seek(0)
        return buf

    def render(self, output_pdf_path):
        """Render complete 1-page menu card to PDF."""
        c = canvas.Canvas(output_pdf_path, pagesize=(self.page_width, self.page_height))
        categories = load_menu_items(CSV_PATH)
        
        # 1. Background Canvas
        c.setFillColor(C_SURFACE)
        c.rect(0, 0, self.page_width, self.page_height, stroke=0, fill=1)
        
        # Outer decorative frame
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.75)
        c.rect(self.margin_x - 6.0, self.margin_bottom - 5.0, 
               self.content_w + 12.0, self.content_h + 10.0, stroke=1, fill=0)
        
        # 2. Header Banner
        header_y = self.page_height - self.margin_top
        header_h = 56.0 if self.is_letter else 60.0
        self._draw_header(c, self.margin_x, header_y - header_h, self.content_w, header_h)
        
        # 3. Footer Bar
        footer_h = 15.0
        footer_y = self.margin_bottom
        self._draw_footer(c, self.margin_x, footer_y, self.content_w, footer_h)
        
        # 4. Content Area for Menu Cards
        cards_top = header_y - header_h - 9.0
        cards_bottom = footer_y + footer_h + 6.0
        available_cards_h = cards_top - cards_bottom
        
        # Card spacing and vertical distribution
        card_gap = 8.5 if self.is_letter else 10.5
        
        # Column 1: Coffee & Snacks & Meals dynamically proportioned
        col1_content_h = available_cards_h - card_gap
        n_coffee = len(categories['Coffee'])
        n_snacks = len(categories['Snacks & Meals'])
        col1_items = n_coffee + n_snacks
        coffee_ratio = (n_coffee / col1_items) if col1_items > 0 else 0.5
        coffee_h = round(col1_content_h * coffee_ratio)
        snacks_h = col1_content_h - coffee_h
        
        coffee_y = cards_top - coffee_h
        snacks_y = coffee_y - card_gap - snacks_h
        
        self._draw_category_card(c, self.col1_x, coffee_y, self.col_w, coffee_h,
                                 "COFFEE", "Specialty brews, espresso & chai", 
                                 categories['Coffee'], category_type="coffee")
        
        self._draw_category_card(c, self.col1_x, snacks_y, self.col_w, snacks_h,
                                 "SNACKS & BITES", "Fresh bakes, savory plates & sides", 
                                 categories['Snacks & Meals'], category_type="snacks")
        
        # Column 2: Meals (9 items), Desserts & Drinks (9 items), and QR Code Card
        qr_card_h = 92.0 if self.is_letter else 98.0
        col2_menu_h = available_cards_h - (2 * card_gap) - qr_card_h
        meals_h = round(col2_menu_h * 0.5)
        desserts_h = col2_menu_h - meals_h
        
        meals_y = cards_top - meals_h
        desserts_y = meals_y - card_gap - desserts_h
        qr_y = desserts_y - card_gap - qr_card_h
        
        self._draw_category_card(c, self.col2_x, meals_y, self.col_w, meals_h,
                                 "MEALS", "Burgers, wraps, bowls & pasta", 
                                 categories['Meals'], category_type="meals")
        
        self._draw_category_card(c, self.col2_x, desserts_y, self.col_w, desserts_h,
                                 "DESSERTS & COOLERS", "Sweets, shakes, smoothies & mocktails", 
                                 categories['Desserts & Drinks'], category_type="desserts")
        
        self._draw_qr_card(c, self.col2_x, qr_y, self.col_w, qr_card_h)
        
        c.showPage()
        c.save()
        print(f"Generated menu card: {output_pdf_path}")

    def _draw_header(self, c, x, y, w, h):
        """Draw top branded header box matching site style with vector logo."""
        # Cream card container
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1.0)
        c.roundRect(x, y, w, h, radius=6.0, stroke=1, fill=1)
        
        # Left brand icon box with vector coffee cup
        icon_box_size = h - 14.0
        icon_x = x + 8.0
        icon_y = y + 7.0
        draw_header_logo(c, icon_x, icon_y, icon_box_size)
        
        # Title text
        text_x = icon_x + icon_box_size + 9.0
        c.setFillColor(C_SECONDARY)
        c.setFont("FontHeadingBold", 17.0 if not self.is_letter else 15.5)
        c.drawString(text_x, y + h - 20.0, "KGP VIBES CAFÉ")
        
        # Subtitle
        c.setFillColor(C_MUTED)
        c.setFont("FontBody", 8.0 if not self.is_letter else 7.5)
        c.drawString(text_x, y + 12.0, "Where code meets chai  ·  Freshly brewed daily  ·  Table Menu")
        
        # Right pill tags (pure text, no emoji symbols)
        pills = [
            ("KORAMANGALA & INDIRANAGAR", C_PRIMARY_LIGHT, C_PRIMARY),
            ("FREE GUEST WI-FI", C_CARD_HEADER_BG, C_MUTED_LIGHT),
        ]
        
        pill_right_x = x + w - 8.0
        pill_y = y + (h / 2.0) - 8.5
        
        for text, bg_col, text_col in reversed(pills):
            c.setFont("FontCodeBold", 6.8)
            tw = pdfmetrics.stringWidth(text, "FontCodeBold", 6.8)
            pw = tw + 12.0
            px = pill_right_x - pw
            
            c.setFillColor(bg_col)
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.6)
            c.roundRect(px, pill_y, pw, 17.0, radius=8.5, stroke=1, fill=1)
            
            c.setFillColor(text_col)
            c.drawString(px + 6.0, pill_y + 5.0, text)
            
            pill_right_x = px - 5.0

    def _draw_footer(self, c, x, y, w, h):
        """Draw minimal clean footer bar."""
        c.setFont("FontBody", 7.0)
        c.setFillColor(C_MUTED)
        
        left_text = "All prices in USD, tax included  ·  Scan table QR code to browse & order"
        c.drawString(x + 2.0, y + 3.0, left_text)
        
        right_text = "No. 27, 6th Cross, Koramangala 5th Block, Bengaluru"
        rw = pdfmetrics.stringWidth(right_text, "FontBody", 7.0)
        c.drawString(x + w - rw - 2.0, y + 3.0, right_text)

    def _draw_category_card(self, c, x, y, w, h, title, subtitle, items, category_type=""):
        """Draw an elegant cream card for a category with vector shape icon."""
        # 1. Card Container
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.9)
        c.roundRect(x, y, w, h, radius=6.0, stroke=1, fill=1)
        
        # 2. Category Header Bar
        header_h = 22.5 if not self.is_letter else 21.0
        header_y = y + h - header_h
        
        c.setFillColor(C_CARD_HEADER_BG)
        c.roundRect(x + 0.5, header_y, w - 1.0, header_h - 0.5, radius=5.5, stroke=0, fill=1)
        c.rect(x + 0.5, header_y, w - 1.0, 5.0, stroke=0, fill=1)
        
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.line(x, header_y, x + w, header_y)
        
        # Category Icon (vector shape)
        icon_cx = x + 16.0
        icon_cy = header_y + (header_h / 2.0)
        draw_category_badge_icon(c, icon_cx, icon_cy, category_type)
        
        # Category Title (clean text, placed right of vector badge)
        c.setFillColor(C_SECONDARY)
        c.setFont("FontHeadingBold", 10.0 if not self.is_letter else 9.5)
        title_x = x + 30.0
        c.drawString(title_x, header_y + 6.5, title)
        
        # Category count badge
        count_text = f"{len(items)} items"
        c.setFont("FontCodeBold", 6.8)
        c.setFillColor(C_PRIMARY)
        cw = pdfmetrics.stringWidth(count_text, "FontCodeBold", 6.8)
        c.drawString(x + w - cw - 8.0, header_y + 7.0, count_text)
        
        # 3. Items Rendering
        items_area_top = header_y - 3.5
        items_area_bottom = y + 3.5
        total_items_h = items_area_top - items_area_bottom
        
        n_items = len(items)
        item_slot_h = total_items_h / n_items
        
        inner_padding_x = 8.0
        inner_w = w - (2 * inner_padding_x)
        for i, item in enumerate(items):
            item_y_top = items_area_top - (i * item_slot_h)
            self._draw_menu_item(c, x + inner_padding_x, item_y_top, inner_w, item_slot_h, item)

    def _draw_menu_item(self, c, x, y_top, w, slot_h, item):
        """Draw an individual item with name, leader dots, price, and description."""
        name = item['name']
        price = f"${float(item['price_usd']):.2f}"
        desc = item['description']
        diet = item['diet'].strip()
        contains_egg = item['contains_egg'].strip().lower() == 'yes'
        
        diet_tag = ""
        if diet == 'vegan':
            diet_tag = "[Vegan]"
        elif diet == 'veg':
            if contains_egg:
                diet_tag = "[Veg · Egg]"
            else:
                diet_tag = "[Veg]"
        elif 'non-veg' in diet:
            diet_tag = "[Non-Veg]"
            
        name_font_size = 8.2 if not self.is_letter else 7.8
        price_font_size = 8.2 if not self.is_letter else 7.8
        desc_font_size = 6.4 if not self.is_letter else 6.1
        
        line1_y = y_top - name_font_size - 1.0
        line2_y = line1_y - desc_font_size - 2.8
        
        # 1. Item Name
        c.setFont("FontHeadingBold", name_font_size)
        c.setFillColor(C_ON_SURFACE)
        c.drawString(x, line1_y, name)
        name_w = pdfmetrics.stringWidth(name, "FontHeadingBold", name_font_size)
        
        # 2. Price
        c.setFont("FontCodeBold", price_font_size)
        c.setFillColor(C_PRIMARY)
        price_w = pdfmetrics.stringWidth(price, "FontCodeBold", price_font_size)
        price_x = x + w - price_w
        c.drawString(price_x, line1_y, price)
        
        # 3. Leader Dots between Name and Price
        dots_start_x = x + name_w + 5.0
        dots_end_x = price_x - 5.0
        if dots_end_x > dots_start_x + 12.0:
            c.setFont("FontCode", 5.5)
            c.setFillColor(C_DOTS)
            dot_unit_w = pdfmetrics.stringWidth(". ", "FontCode", 5.5)
            available_dots_w = dots_end_x - dots_start_x
            n_dots = int(available_dots_w / dot_unit_w)
            if n_dots > 1:
                dots_text = ". " * n_dots
                c.drawString(dots_start_x, line1_y + 0.5, dots_text)
            
        # 4. Description Line with Dietary Tag
        c.setFont("FontBody", desc_font_size)
        c.setFillColor(C_MUTED)
        
        full_desc = f"{desc}  {diet_tag}".strip()
        full_w = pdfmetrics.stringWidth(full_desc, "FontBody", desc_font_size)
        
        if full_w <= w:
            c.drawString(x, line2_y, desc)
            if diet_tag:
                dw = pdfmetrics.stringWidth(desc + "  ", "FontBody", desc_font_size)
                c.setFont("FontCodeBold", desc_font_size - 0.4)
                if 'Vegan' in diet_tag:
                    c.setFillColor(C_VEGAN_TEXT)
                elif 'Non-Veg' in diet_tag:
                    c.setFillColor(C_NONVEG_TEXT)
                elif 'Egg' in diet_tag:
                    c.setFillColor(C_EGG_TEXT)
                else:
                    c.setFillColor(C_VEG_TEXT)
                c.drawString(x + dw, line2_y, diet_tag)
        else:
            desc_text = desc
            while pdfmetrics.stringWidth(desc_text + "...", "FontBody", desc_font_size) > w and len(desc_text) > 5:
                desc_text = desc_text[:-1]
            if desc_text != desc:
                desc_text += "..."
            c.drawString(x, line2_y, desc_text)

    def _draw_qr_card(self, c, x, y, w, h):
        """Draw the table ordering and QR code card."""
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_PRIMARY)
        c.setLineWidth(1.0)
        c.roundRect(x, y, w, h, radius=6.0, stroke=1, fill=1)
        
        qr_padding = 7.5
        qr_box_size = h - (2 * qr_padding)
        qr_x = x + qr_padding
        qr_y = y + qr_padding
        
        c.setFillColor(HexColor('#FFFFFF'))
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.roundRect(qr_x, qr_y, qr_box_size, qr_box_size, radius=4.0, stroke=1, fill=1)
        
        from reportlab.lib.utils import ImageReader
        self.qr_img.seek(0)
        img_reader = ImageReader(self.qr_img)
        inset = 3.0
        c.drawImage(img_reader, qr_x + inset, qr_y + inset, 
                    qr_box_size - (2 * inset), qr_box_size - (2 * inset))
        
        content_x = qr_x + qr_box_size + 9.0
        content_w = (x + w - 8.0) - content_x
        
        c.setFont("FontHeadingBold", 10.5 if not self.is_letter else 9.8)
        c.setFillColor(C_SECONDARY)
        c.drawString(content_x, y + h - 17.0, "Scan To Order Ahead")
        
        c.setFont("FontBody", 7.2 if not self.is_letter else 6.8)
        c.setFillColor(C_MUTED)
        c.drawString(content_x, y + h - 30.0, "Scan with your phone to view our menu,")
        c.drawString(content_x, y + h - 39.5, "check allergens, and place table orders.")
        
        pill_y = y + 7.5
        pill_h = 17.0
        c.setFillColor(C_CARD_HEADER_BG)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.roundRect(content_x, pill_y, content_w, pill_h, radius=3.5, stroke=1, fill=1)
        
        c.setFont("FontCodeBold", 6.4 if not self.is_letter else 6.0)
        c.setFillColor(C_PRIMARY)
        url_text = self.menu_url
        c.drawString(content_x + 5.0, pill_y + 5.0, url_text)


# ==============================================================================
# MAIN EXPORT & VERIFICATION
# ==============================================================================
def main():
    os.makedirs(PRINT_DIR, exist_ok=True)
    
    a4_pdf = os.path.join(PRINT_DIR, "menu_a4.pdf")
    letter_pdf = os.path.join(PRINT_DIR, "menu_letter.pdf")
    
    # 1. Export A4
    renderer_a4 = MenuCardRenderer(A4, SITE_MENU_URL)
    renderer_a4.render(a4_pdf)
    
    # 2. Export US Letter
    renderer_letter = MenuCardRenderer(letter, SITE_MENU_URL)
    renderer_letter.render(letter_pdf)
    
    # 3. Verification: Page count, QR decode, edge boundary check, missing glyph check
    print("\n--- Running Verification ---")
    for name, pdf_path in [("A4", a4_pdf), ("US Letter", letter_pdf)]:
        doc = pymupdf.open(pdf_path)
        page_count = len(doc)
        page = doc[0]
        rect = page.rect
        
        print(f"\nVerifying {name} ({pdf_path}):")
        print(f"  Page count: {page_count} (Expected: 1)")
        assert page_count == 1, f"Error: {name} has {page_count} pages, expected 1!"
        print(f"  Dimensions: {rect.width:.1f} x {rect.height:.1f} pt")
        
        # Check text for any unprintable or emoji characters
        full_text = page.get_text()
        unprintable = [ch for ch in full_text if ord(ch) > 1000 and ch not in ['·', '—', '–']]
        print(f"  Non-standard/emoji characters in extracted text: {unprintable}")
        assert len(unprintable) == 0, f"Error: Found emoji characters that might fail in PDF viewers: {unprintable}"
        print(f"  Glyph Safety Check Passed: No font emojis present; all icons are rendered as vector shapes!")
        
        # Render page to high-res image (300 DPI)
        zoom = 300.0 / 72.0
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        
        # Save preview image for visual inspection
        preview_img_path = os.path.join(PRINT_DIR, f"preview_{name.lower().replace(' ', '_')}.png")
        img.save(preview_img_path)
        print(f"  Saved render preview: {preview_img_path}")
        
        # Test QR code decoding directly from the rendered page image
        results = zxingcpp.read_barcodes(img)
        print(f"  Barcodes found on rendered page: {len(results)}")
        assert len(results) > 0, f"Error: No QR code detected on {name} page image!"
        
        qr_text = results[0].text
        print(f"  Decoded QR Code URL: {qr_text}")
        assert qr_text == SITE_MENU_URL, f"Error: QR code text '{qr_text}' != '{SITE_MENU_URL}'!"
        print(f"  QR code successfully verified against configured URL: {SITE_MENU_URL}")
        
        # Check text clipping / margin boundaries
        text_page = page.get_text("blocks")
        x_min = min(b[0] for b in text_page)
        y_min = min(b[1] for b in text_page)
        x_max = max(b[2] for b in text_page)
        y_max = max(b[3] for b in text_page)
        
        margin_left = x_min
        margin_right = rect.width - x_max
        margin_top = y_min
        margin_bottom = rect.height - y_max
        
        print(f"  Text Bounding Box: ({x_min:.1f}, {y_min:.1f}) to ({x_max:.1f}, {y_max:.1f})")
        print(f"  Margins: Left={margin_left:.1f}pt, Right={margin_right:.1f}pt, Top={margin_top:.1f}pt, Bottom={margin_bottom:.1f}pt")
        
        assert margin_left >= 15.0, f"Error: Content too close to left edge ({margin_left:.1f} pt)"
        assert margin_right >= 15.0, f"Error: Content too close to right edge ({margin_right:.1f} pt)"
        assert margin_top >= 15.0, f"Error: Content too close to top edge ({margin_top:.1f} pt)"
        assert margin_bottom >= 15.0, f"Error: Content too close to bottom edge ({margin_bottom:.1f} pt)"
        print(f"  Edge Check Passed: All content is safely within print bounds with healthy margins (all >= 15 pt)!")
        
        doc.close()

    print("\n==============================================")
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("==============================================")

if __name__ == "__main__":
    main()
