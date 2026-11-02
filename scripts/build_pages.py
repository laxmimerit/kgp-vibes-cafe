"""
build_pages.py
Generates KGP Vibes Cafe pages keeping:
- The LOOK from DESIGN.md: Warm Terminal Roast colors, Literata / Plus Jakarta Sans / JetBrains Mono fonts,
  spacing, rounded cards, and 390px phone layout.
- The PLAIN COPY & SCOPE from AGENTS.md & .agents/rules/site-look.md:
  * Plain headlines, buttons, and section names.
  * NO telemetry ticker, NO Wi-Fi SSID/PSK/ping details, NO coding pods / table booking, NO payment options.
  * All prices in USD ($X.XX), demo-only pickup flow, zero dates/years.
  * Single unified checkout inside cart.html, all checkout links point there.
  * Plain cream placeholders for food photos until custom photos are provided.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, "site")

TAILWIND_CONFIG = '''
<script src="https://cdn.tailwindcss.com"></script>
<script id="tailwind-config">
tailwind.config={
  darkMode:"class",
  theme:{
    extend:{
      colors:{
        "surface-bright":"#fcf9f4",
        "on-secondary-fixed":"#2a170f",
        "surface-container-low":"#f6f3ee",
        "inverse-on-surface":"#f3f0eb",
        "surface-tint":"#9c4400",
        "on-secondary-fixed-variant":"#5a4137",
        "tertiary-fixed":"#a4f3ca",
        "on-primary-fixed-variant":"#773300",
        "primary":"#984300",
        "primary-container":"#ba5814",
        "background":"#fcf9f4",
        "on-background":"#1c1c19",
        "inverse-primary":"#ffb68e",
        "on-surface-variant":"#564339",
        "on-error-container":"#93000a",
        "tertiary-container":"#348260",
        "surface-container-high":"#ebe8e3",
        "on-secondary":"#ffffff",
        "surface-container-highest":"#e5e2dd",
        "secondary-fixed-dim":"#e2bfb2",
        "secondary-container":"#fcd8ca",
        "surface-variant":"#e5e2dd",
        "on-primary-fixed":"#331200",
        "secondary":"#73584e",
        "secondary-fixed":"#ffdbcd",
        "error":"#ba1a1a",
        "error-container":"#ffdad6",
        "surface-container-lowest":"#ffffff",
        "tertiary-fixed-dim":"#88d6af",
        "on-tertiary-container":"#f5fff6",
        "on-error":"#ffffff",
        "on-secondary-container":"#785d52",
        "on-primary":"#ffffff",
        "on-tertiary-fixed-variant":"#005236",
        "primary-fixed-dim":"#ffb68e",
        "outline-variant":"#ddc1b3",
        "inverse-surface":"#31302d",
        "on-primary-container":"#fffbff",
        "on-tertiary-fixed":"#002113",
        "primary-fixed":"#ffdbca",
        "surface-dim":"#dcdad5",
        "surface-container":"#f0ede9",
        "on-surface":"#1c1c19",
        "outline":"#897267",
        "on-tertiary":"#ffffff",
        "surface":"#fcf9f4",
        "tertiary":"#136948"
      },
      borderRadius:{
        "DEFAULT":"0.25rem",
        "lg":"0.5rem",
        "xl":"0.75rem",
        "full":"9999px"
      },
      spacing:{
        "gutter-desktop":"2rem",
        "margin-tablet":"2rem",
        "gutter":"1.25rem",
        "margin-desktop":"3.5rem",
        "space-md":"1rem",
        "margin":"1rem",
        "space-lg":"1.5rem",
        "space-sm":"0.5rem",
        "space-xs":"0.25rem",
        "space-xl":"2.5rem"
      },
      fontFamily:{
        "headline-md":["Literata"],
        "display-hero":["Literata"],
        "body-md":["Plus Jakarta Sans"],
        "display-hero-mobile":["Literata"],
        "body-sm":["Plus Jakarta Sans"],
        "headline-sm":["Literata"],
        "body-lg":["Plus Jakarta Sans"],
        "headline-lg":["Literata"],
        "code-pill":["JetBrains Mono"],
        "headline-lg-mobile":["Literata"],
        "label-md":["Plus Jakarta Sans"],
        "label-sm":["JetBrains Mono"]
      },
      fontSize:{
        "headline-md":["26px",{"lineHeight":"34px","letterSpacing":"-0.01em","fontWeight":"500"}],
        "display-hero":["56px",{"lineHeight":"64px","letterSpacing":"-0.02em","fontWeight":"600"}],
        "body-md":["15px",{"lineHeight":"24px","fontWeight":"400"}],
        "display-hero-mobile":["36px",{"lineHeight":"42px","letterSpacing":"-0.01em","fontWeight":"600"}],
        "body-sm":["13px",{"lineHeight":"20px","fontWeight":"400"}],
        "headline-sm":["20px",{"lineHeight":"28px","fontWeight":"500"}],
        "body-lg":["18px",{"lineHeight":"28px","fontWeight":"400"}],
        "headline-lg":["36px",{"lineHeight":"44px","letterSpacing":"-0.015em","fontWeight":"600"}],
        "code-pill":["12px",{"lineHeight":"16px","letterSpacing":"0.02em","fontWeight":"500"}],
        "headline-lg-mobile":["28px",{"lineHeight":"34px","letterSpacing":"-0.01em","fontWeight":"600"}],
        "label-md":["14px",{"lineHeight":"20px","fontWeight":"600"}],
        "label-sm":["11px",{"lineHeight":"14px","letterSpacing":"0.04em","fontWeight":"400"}]
      }
    }
  }
};
</script>
'''

def get_header(active_tab="home"):
    h_cls = 'bg-secondary-container text-on-secondary-container font-label-md rounded-full shadow-sm' if active_tab == 'home' else 'text-on-surface-variant hover:text-on-surface'
    a_cls = 'bg-secondary-container text-on-secondary-container font-label-md rounded-full shadow-sm' if active_tab == 'about' else 'text-on-surface-variant hover:text-on-surface'
    m_cls = 'bg-secondary-container text-on-secondary-container font-label-md rounded-full shadow-sm' if active_tab == 'menu' else 'text-on-surface-variant hover:text-on-surface'
    c_cls = 'bg-secondary-container text-on-secondary-container font-label-md rounded-full shadow-sm' if active_tab == 'cart' else 'text-on-surface-variant hover:text-on-surface'

    return f'''
  <!-- Site Header (Clean, plain customer navigation) -->
  <header class="fixed top-0 left-0 right-0 z-50 bg-surface/90 backdrop-blur-md shadow-[0_4px_20px_-4px_rgba(43,24,16,0.06)] border-b border-outline-variant/30">
    <div class="h-20 max-w-[1280px] mx-auto px-gutter-desktop flex items-center justify-between gap-space-md">
      <a href="index.html" class="flex items-center gap-space-md shrink-0 cursor-pointer" aria-label="KGP Vibes Cafe Home">
        <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm text-xl font-bold">
          ☕
        </div>
        <div class="flex flex-col">
          <span class="font-headline-sm text-headline-sm text-on-surface leading-tight brand-title">KGP Vibes Cafe</span>
          <span class="font-label-sm text-label-sm text-secondary tracking-normal">Where code meets chai</span>
        </div>
      </a>
      
      <!-- Desktop Navigation Links -->
      <nav class="hidden lg:flex items-center gap-space-xs bg-surface-container-low px-space-xs py-space-xs rounded-full shadow-[0_1px_4px_rgba(43,24,16,0.04)]">
        <a href="index.html" class="px-space-md py-space-xs transition-colors flex items-center gap-space-xs font-label-md {h_cls}">Home</a>
        <a href="about.html" class="px-space-md py-space-xs transition-colors flex items-center gap-space-xs font-label-md rounded-full {a_cls}">About</a>
        <a href="menu.html" class="px-space-md py-space-xs rounded-full font-label-md transition-colors flex items-center gap-space-xs {m_cls}">
          Menu
          <span class="font-code-pill text-code-pill bg-secondary-fixed text-on-secondary-fixed px-space-xs py-0.5 rounded-full leading-none">39 Items</span>
        </a>
        <a href="cart.html" class="px-space-md py-space-xs rounded-full font-label-md transition-colors flex items-center gap-space-xs {c_cls}">
          <span>🛒 Order Ahead</span>
          <span class="cart-badge font-code-pill text-code-pill bg-primary text-on-primary px-space-xs py-0.5 rounded-full leading-none">0</span>
        </a>
      </nav>
      
      <div class="flex items-center gap-space-md shrink-0">
        <a href="cart.html" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-lg py-space-sm rounded-full shadow-sm transition-all duration-200 flex items-center gap-space-xs">
          <span>Order Ahead</span>
        </a>
      </div>
    </div>
  </header>
'''

def get_bottom_nav(active_tab="home"):
    h_c = 'text-primary font-bold' if active_tab == 'home' else 'text-on-surface-variant'
    a_c = 'text-primary font-bold' if active_tab == 'about' else 'text-on-surface-variant'
    m_c = 'text-primary font-bold' if active_tab == 'menu' else 'text-on-surface-variant'
    c_c = 'text-primary font-bold' if active_tab == 'cart' else 'text-on-surface-variant'

    return f'''
  <!-- Mobile Bottom Navigation Bar (Phone layout: 390px) -->
  <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-50 pb-safe bg-surface/95 backdrop-blur-xl shadow-[0_-2px_12px_rgba(43,24,16,0.06)] border-t border-outline-variant/30">
    <div class="flex items-center justify-around h-16 px-space-xs max-w-md mx-auto">
      <a href="index.html" class="flex flex-col items-center justify-center min-w-[56px] min-h-[44px] gap-0.5 transition-colors {h_c}">
        <span class="material-symbols-outlined text-[24px]">home</span>
        <span class="font-label-sm text-[11px]">Home</span>
      </a>
      <a href="about.html" class="flex flex-col items-center justify-center min-w-[56px] min-h-[44px] gap-0.5 transition-colors {a_c}">
        <span class="material-symbols-outlined text-[24px]">info</span>
        <span class="font-label-sm text-[11px]">About</span>
      </a>
      <a href="menu.html" class="flex flex-col items-center justify-center min-w-[56px] min-h-[44px] gap-0.5 transition-colors {m_c}">
        <span class="material-symbols-outlined text-[24px]">restaurant_menu</span>
        <span class="font-label-sm text-[11px]">Menu</span>
      </a>
      <a href="cart.html" class="relative flex flex-col items-center justify-center min-w-[56px] min-h-[44px] gap-0.5 transition-colors {c_c}">
        <span class="material-symbols-outlined text-[24px]">shopping_cart</span>
        <span class="font-label-sm text-[11px]">Order Ahead</span>
        <span class="cart-badge absolute top-1 right-2 w-4 h-4 rounded-full bg-primary text-on-primary text-[10px] font-bold flex items-center justify-center">0</span>
      </a>
    </div>
  </nav>
'''

def get_footer():
    return '''
  <!-- Plain Customer Footer (No dates, no years, no Wi-Fi credentials) -->
  <footer class="w-full bg-surface-container-low text-on-surface-variant mt-space-xl pb-20 lg:pb-0 border-t border-outline-variant/30">
    <div class="max-w-[1280px] mx-auto px-gutter-desktop py-space-xl">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-space-xl">
        <div class="md:col-span-2 flex flex-col gap-space-sm">
          <div class="flex items-center gap-space-sm">
            <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-on-primary font-bold text-base">
              ☕
            </div>
            <span class="font-headline-sm text-headline-sm text-on-surface">KGP Vibes Cafe</span>
          </div>
          <p class="font-body-md text-body-md text-on-surface-variant max-w-sm">
            Where code meets chai. Handcrafted brews, collegiate hospitality, and wholesome food open daily from 8:00 AM to 10:00 PM.
          </p>
        </div>
        <div>
          <h4 class="font-label-md text-label-md text-on-surface font-semibold mb-space-sm">Explore</h4>
          <ul class="flex flex-col gap-space-xs font-body-sm text-body-sm">
            <li><a href="index.html" class="hover:text-primary transition-colors">Home</a></li>
            <li><a href="about.html" class="hover:text-primary transition-colors">About Us</a></li>
            <li><a href="menu.html" class="hover:text-primary transition-colors">Our Menu</a></li>
            <li><a href="cart.html" class="hover:text-primary transition-colors">Order Ahead</a></li>
          </ul>
        </div>
        <div>
          <h4 class="font-label-md text-label-md text-on-surface font-semibold mb-space-sm">Outlets</h4>
          <ul class="flex flex-col gap-space-xs font-body-sm text-body-sm">
            <li><strong class="text-on-surface">Koramangala</strong> (Open Daily)</li>
            <li class="text-xs text-outline">No. 27, 6th Cross, 5th Block</li>
            <li class="mt-2"><strong class="text-on-surface">Indiranagar</strong> (Opening Soon)</li>
            <li class="text-xs text-outline">100 Feet Road</li>
          </ul>
        </div>
      </div>
      <div class="mt-space-xl pt-space-md border-t border-outline-variant/30 flex flex-wrap items-center justify-between gap-space-sm font-label-sm text-label-sm text-secondary">
        <span>KGP Vibes Cafe. All rights reserved.</span>
        <span>Daily 8:00 AM – 10:00 PM</span>
      </div>
    </div>
  </footer>
'''

def build_home():
    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>KGP Vibes Cafe - Where Code Meets Chai</title>
  <meta name="description" content="KGP Vibes Cafe: artisanal chai, specialty coffee, and cafe favorites in Koramangala and now Indiranagar.">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  {TAILWIND_CONFIG}
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-background font-body-md text-on-surface antialiased">
  {get_header("home")}

  <main class="w-full pt-20 bg-background min-h-[calc(100vh-20rem)]">
    
    <!-- Hero Section with Masala Chai & Chocolate Brownie Photo -->
    <section class="relative w-full overflow-hidden border-b border-outline-variant/20 min-h-[520px] lg:min-h-[580px] flex items-center">
      <!-- Background Hero Image -->
      <img src="images/hero.jpg" alt="Handcrafted Masala Chai and Chocolate Brownie on cafe table" class="absolute inset-0 w-full h-full object-cover object-right md:object-center select-none" priority="high">
      
      <!-- Gradient Overlays for Readability: Cream gradient on left for desktop, protective scrim on mobile -->
      <div class="absolute inset-0 bg-gradient-to-t sm:bg-gradient-to-r from-surface-bright/95 via-surface-bright/90 md:via-surface-bright/80 to-surface-bright/40 md:to-transparent"></div>

      <!-- Hero Content over the empty space on the left -->
      <div class="relative w-full max-w-[1280px] mx-auto px-gutter-desktop py-space-xl lg:py-space-2xl z-10">
        <div class="max-w-xl lg:max-w-2xl flex flex-col gap-space-md bg-surface-bright/60 sm:bg-transparent backdrop-blur-xs sm:backdrop-blur-none p-space-sm sm:p-0 rounded-2xl">
          <div class="inline-flex items-center gap-space-xs self-start px-space-md py-space-xs rounded-full bg-secondary-container/95 text-on-secondary-container font-label-md text-xs shadow-sm backdrop-blur-sm">
            <span>☕ Freshly Brewed Daily</span>
            <span class="opacity-60">·</span>
            <span>Koramangala &amp; Indiranagar</span>
          </div>

          <h1 class="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface leading-tight tracking-tight">
            Where code meets chai: now open in Indiranagar
          </h1>

          <p class="font-body-lg text-body-lg text-on-surface-variant max-w-xl leading-relaxed">
            An approachable neighborhood sanctuary for builders, students, and thinkers. Enjoy handcrafted Kulhad Chai, artisanal coffee, and comforting bites.
          </p>

          <div class="flex flex-wrap items-center gap-space-sm pt-space-xs">
            <a href="cart.html" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-xl py-space-sm rounded-full shadow-md transition-all duration-200">
              Order Ahead
            </a>
            <a href="menu.html" class="bg-surface-container-high/90 hover:bg-surface-container-highest text-on-surface font-label-md text-label-md px-space-lg py-space-sm rounded-full transition-all duration-200 border border-outline-variant/40 backdrop-blur-sm">
              Browse Menu
            </a>
          </div>

          <div class="grid grid-cols-3 gap-space-sm pt-space-md max-w-lg border-t border-outline-variant/30">
            <div>
              <span class="font-headline-sm text-primary font-bold block">39 Items</span>
              <span class="font-body-sm text-xs text-on-surface-variant">Chai, Coffee &amp; Food</span>
            </div>
            <div>
              <span class="font-headline-sm text-primary font-bold block">15-Min</span>
              <span class="font-body-sm text-xs text-on-surface-variant">Quick Pickup Slots</span>
            </div>
            <div>
              <span class="font-headline-sm text-primary font-bold block">2 Outlets</span>
              <span class="font-body-sm text-xs text-on-surface-variant">Open Daily 8 AM - 10 PM</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 1: The Spirit of KGP Vibes -->
    <section class="py-space-xl bg-surface">
      <div class="max-w-[1280px] mx-auto px-gutter-desktop">
        <div class="text-center max-w-2xl mx-auto mb-space-xl">
          <span class="font-label-sm text-primary uppercase tracking-wider font-semibold">Our Philosophy</span>
          <h2 class="font-headline-lg text-headline-lg text-on-surface mt-1">The Spirit of KGP Vibes</h2>
          <p class="font-body-md text-on-surface-variant mt-2">
            Born from late-night college discussions and a craving for honest, comforting chai, KGP Vibes is an unpretentious home away from home.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-space-lg">
          <div class="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
            <div class="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
              🫖
            </div>
            <h3 class="font-headline-sm text-headline-sm text-on-surface">Authentic Kulhad Chai</h3>
            <p class="font-body-sm text-on-surface-variant">Simmered with whole cardamom, crushed fresh ginger, and rich Assam tea leaves in natural earthen clay.</p>
          </div>

          <div class="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
            <div class="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
              🌱
            </div>
            <h3 class="font-headline-sm text-headline-sm text-on-surface">Mindful &amp; Wholesome Food</h3>
            <p class="font-body-sm text-on-surface-variant">From hearty breakfast bowls and signature burgers to vegan bites and fresh sourdough snacks.</p>
          </div>

          <div class="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
            <div class="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
              🤝
            </div>
            <h3 class="font-headline-sm text-headline-sm text-on-surface">Welcoming Community</h3>
            <p class="font-body-sm text-on-surface-variant">A peaceful place where you can study, read a novel, meet collaborators, or just take a breather.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: Cafe Favorites -->
    <section class="py-space-xl bg-surface-container-low border-y border-outline-variant/20">
      <div class="max-w-[1280px] mx-auto px-gutter-desktop">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-space-md mb-space-lg">
          <div>
            <span class="font-label-sm text-primary uppercase tracking-wider font-semibold">Campus Specials</span>
            <h2 class="font-headline-lg text-headline-lg text-on-surface mt-1">Cafe Favorites</h2>
            <p class="font-body-md text-on-surface-variant mt-1">Our most beloved drinks and bites, ready for order-ahead pickup.</p>
          </div>
          <a href="menu.html" class="font-label-md text-primary hover:underline flex items-center gap-1 font-semibold">
            View full menu (39 items) &rarr;
          </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-lg">
          <!-- Favorite 1: Talkie Chai -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">Talkie Chai</h3>
                <span class="font-headline-sm font-bold text-primary">$2.00</span>
              </div>
              <span class="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
              <p class="font-body-sm text-on-surface-variant">Signature masala chai brewed in an authentic clay kulhad with crushed ginger and aromatic green cardamom.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-coffee-01',name:'Talkie Chai',price:2.00,category:'Chai'}},1)">+ Add to Order</button>
            </div>
          </div>

          <!-- Favorite 2: Byte Brownie -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">Byte Brownie</h3>
                <span class="font-headline-sm font-bold text-primary">$2.50</span>
              </div>
              <span class="inline-block bg-secondary-fixed text-on-secondary-fixed text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Egg</span>
              <p class="font-body-sm text-on-surface-variant">Rich fudgy dark chocolate brownie baked fresh every morning with a crisp crackly crust.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-pastry-01',name:'Byte Brownie',price:2.50,category:'Snacks'}},1)">+ Add to Order</button>
            </div>
          </div>

          <!-- Favorite 3: Filter Coffee -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">Filter Coffee</h3>
                <span class="font-headline-sm font-bold text-primary">$2.50</span>
              </div>
              <span class="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
              <p class="font-body-sm text-on-surface-variant">Traditional South Indian brass filter coffee made with chicory blend and frothed steamed milk.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-coffee-02',name:'Filter Coffee',price:2.50,category:'Coffee'}},1)">+ Add to Order</button>
            </div>
          </div>

          <!-- Favorite 4: KGP Maggi Bowl -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">KGP Maggi Bowl</h3>
                <span class="font-headline-sm font-bold text-primary">$3.00</span>
              </div>
              <span class="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
              <p class="font-body-sm text-on-surface-variant">Double masala street-style noodles tossed with crisp onions, bell peppers, sweet corn, and a squeeze of fresh lime.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-food-02',name:'KGP Maggi Bowl',price:3.00,category:'Snacks'}},1)">+ Add to Order</button>
            </div>
          </div>

          <!-- Favorite 5: Startup Burger -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">Startup Burger</h3>
                <span class="font-headline-sm font-bold text-primary">$4.00</span>
              </div>
              <span class="inline-block bg-secondary-container text-on-secondary-container text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Non-Veg</span>
              <p class="font-body-sm text-on-surface-variant">Grilled herb patty with melted cheddar, crisp lettuce, spicy chipotle mayo on a toasted brioche bun.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-food-01',name:'Startup Burger',price:4.00,category:'Snacks'}},1)">+ Add to Order</button>
            </div>
          </div>

          <!-- Favorite 6: Stack Overflow Nachos -->
          <div class="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
            <div class="p-space-lg">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">Stack Overflow Nachos</h3>
                <span class="font-headline-sm font-bold text-primary">$3.50</span>
              </div>
              <span class="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
              <p class="font-body-sm text-on-surface-variant">Crisp tortilla chips piled high with warm queso cheese sauce, fresh salsa, jalapeños, and sour cream.</p>
            </div>
            <div class="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
              <button type="button" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all" onclick="Cart.addToCart({{id:'kv-food-03',name:'Stack Overflow Nachos',price:3.50,category:'Snacks'}},1)">+ Add to Order</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 3: Our Outlets -->
    <section class="py-space-xl bg-surface">
      <div class="max-w-[1280px] mx-auto px-gutter-desktop">
        <div class="text-center max-w-2xl mx-auto mb-space-xl">
          <span class="font-label-sm text-primary uppercase tracking-wider font-semibold">Locations</span>
          <h2 class="font-headline-lg text-headline-lg text-on-surface mt-1">Our Outlets</h2>
          <p class="font-body-md text-on-surface-variant mt-2">Find a comfortable table near you or order ahead for quick pickup.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-space-lg max-w-4xl mx-auto">
          <div class="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-headline-sm text-headline-sm text-on-surface">Koramangala</h3>
              <span class="bg-tertiary-fixed text-on-tertiary-fixed text-xs px-2.5 py-0.5 rounded-full font-semibold">Open Daily</span>
            </div>
            <p class="font-body-sm text-on-surface-variant mb-3">No. 27, 6th Cross, 5th Block · Daily 8:00 AM – 10:00 PM</p>
            <p class="font-body-sm text-sm text-on-surface-variant mb-4">Our flagship cafe featuring outdoor patio seating, comfortable spaces, and warm campus energy.</p>
            <a href="cart.html" class="inline-block bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-2 rounded-full transition-all">
              Order Ahead for Koramangala
            </a>
          </div>

          <div class="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-headline-sm text-headline-sm text-on-surface">Indiranagar</h3>
              <span class="bg-secondary-container text-on-secondary-container text-xs px-2.5 py-0.5 rounded-full font-semibold">Opening Soon</span>
            </div>
            <p class="font-body-sm text-on-surface-variant mb-3">100 Feet Road · Daily 8:00 AM – 10:00 PM</p>
            <p class="font-body-sm text-sm text-on-surface-variant mb-4">Our newest location bringing comfortable study corners and artisanal chai closer to office commuters.</p>
            <a href="menu.html" class="inline-block bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label-md text-xs px-space-md py-2 rounded-full transition-all border border-outline-variant/40">
              Explore Launch Specials
            </a>
          </div>
        </div>
      </div>
    </section>

  </main>

  {get_footer()}
  {get_bottom_nav("home")}

  <script src="js/cart.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Built site/index.html with cream placeholder & Warm Terminal Roast style")

def build_menu():
    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Menu - KGP Vibes Cafe</title>
  <meta name="description" content="Explore our full menu of artisanal chai, specialty coffee, and cafe snacks.">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  {TAILWIND_CONFIG}
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-background font-body-md text-on-surface antialiased">
  {get_header("menu")}

  <main class="w-full pt-20 bg-background min-h-[calc(100vh-20rem)] py-space-xl">
    <div class="max-w-[1280px] mx-auto px-gutter-desktop">
      
      <!-- Menu Header -->
      <div class="flex flex-col max-w-2xl mb-space-lg">
        <span class="font-label-sm text-primary uppercase tracking-wider font-semibold">Freshly Prepared</span>
        <h1 class="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface tracking-tight mt-1">Our Menu</h1>
        <p class="font-body-lg text-body-lg text-on-surface-variant mt-2 leading-relaxed">
          Explore our handcrafted chai, single-origin coffee, wholesome food, and bakery treats.
        </p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="flex flex-col gap-space-sm mb-space-xl">
        <div class="relative w-full max-w-md">
          <span class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-outline">
            <span class="material-symbols-outlined text-lg">search</span>
          </span>
          <input id="menu-search" class="w-full bg-surface-container-lowest border border-outline-variant/50 rounded-full pl-11 pr-4 py-2.5 font-body-md text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary shadow-sm" placeholder="Search menu by name, ingredient, or tag...">
        </div>

        <div class="flex items-center gap-space-xs overflow-x-auto pb-space-xs no-scrollbar" id="category-pills">
          <button data-category="all" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-secondary-container text-on-secondary-container font-semibold shadow-sm transition-all duration-150 active" type="button">All Items (39)</button>
          <button data-category="Coffee" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-all duration-150" type="button">Coffee (12)</button>
          <button data-category="Chai" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-all duration-150" type="button">Chai</button>
          <button data-category="Snacks" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-all duration-150" type="button">Bites &amp; Snacks</button>
          <button data-category="Bakery" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-all duration-150" type="button">Bakery &amp; Desserts</button>
          <button data-category="Cold Brew" class="category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-all duration-150" type="button">Cold Brews &amp; Coolers</button>
        </div>

        <div class="flex flex-wrap items-center gap-space-xs font-label-sm text-xs text-on-surface-variant">
          <span class="opacity-70">Dietary Filter:</span>
          <button data-diet="all" class="diet-pill px-space-sm py-0.5 rounded-full bg-primary/10 text-primary font-semibold">All Diets</button>
          <button data-diet="vegetarian" class="diet-pill px-space-sm py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container">Veg</button>
          <button data-diet="vegan" class="diet-pill px-space-sm py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container">Vegan</button>
          <button data-diet="egg-free" class="diet-pill px-space-sm py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container">Egg-Free</button>
          <span id="menu-items-count" class="ml-auto text-xs text-secondary opacity-75">Loading items...</span>
        </div>
      </div>

      <!-- Dynamic Menu Items Grid -->
      <div id="menu-items-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-space-lg">
        <!-- Rendered by js/menu-page.js with food photos & plain labels -->
      </div>

    </div>
  </main>

  {get_footer()}
  {get_bottom_nav("menu")}

  <script src="js/menu-data.js"></script>
  <script src="js/menu-loader.js"></script>
  <script src="js/cart.js"></script>
  <script src="js/menu-page.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(SITE_DIR, "menu.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Built site/menu.html with plain headlines & Warm Terminal Roast style")

def build_cart():
    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Your Order &amp; Checkout - KGP Vibes Cafe</title>
  <meta name="description" content="Review your items, schedule a pickup time, and place your order ahead at KGP Vibes Cafe.">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  {TAILWIND_CONFIG}
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-background font-body-md text-on-surface antialiased">
  {get_header("cart")}

  <main class="w-full pt-20 bg-background min-h-[calc(100vh-20rem)] py-space-xl">
    <div class="max-w-[1280px] mx-auto px-gutter-desktop">
      
      <!-- Page Title -->
      <div class="mb-space-lg">
        <h1 class="font-headline-lg text-headline-lg text-on-surface">Review Your Order &amp; Checkout</h1>
        <p class="font-body-md text-on-surface-variant mt-1">Review your items, choose an outlet and pickup time, and place your order ahead.</p>
      </div>

      <!-- Empty Cart State -->
      <div id="empty-cart-state" class="bg-surface-container-lowest rounded-xl shadow-sm p-space-xl text-center flex flex-col items-center justify-center gap-space-md border border-outline-variant/30" style="display: none;">
        <div class="w-20 h-20 rounded-full bg-surface-container flex items-center justify-center text-primary text-4xl">
          ☕
        </div>
        <h2 class="font-headline-md text-headline-md text-on-surface">Your cart is empty</h2>
        <p class="font-body-md text-body-md text-on-surface-variant max-w-md">
          Add your favorite brews, bites, or sweet treats from our menu to schedule a pickup.
        </p>
        <a href="menu.html" class="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-lg py-space-sm rounded-full shadow-sm transition-all duration-200 inline-flex items-center gap-space-xs">
          Browse the Menu
        </a>
      </div>

      <!-- Active Cart Layout (Single Checkout View) -->
      <div id="active-cart-layout" class="grid grid-cols-1 lg:grid-cols-12 gap-space-lg lg:gap-gutter-desktop items-start">
        
        <!-- Left: Cart Items List -->
        <div class="lg:col-span-7 flex flex-col gap-space-lg min-w-0">
          <div class="bg-surface-container-lowest rounded-xl shadow-sm p-space-md lg:p-space-lg flex flex-col gap-space-md border border-outline-variant/30">
            <div class="flex items-center justify-between pb-space-sm border-b border-outline-variant/20">
              <div class="flex items-center gap-space-xs">
                <span class="font-headline-sm text-headline-sm text-on-surface">Your Selected Items</span>
                <span id="total-count-badge" class="font-code-pill text-xs bg-secondary-container text-on-secondary-container px-space-sm py-0.5 rounded-full font-medium">
                  0 items
                </span>
              </div>
              <button id="clear-all-btn" type="button" class="font-label-sm text-xs text-secondary hover:text-error transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">delete</span>
                Clear Cart
              </button>
            </div>

            <!-- Cart Table -->
            <table class="cart-table w-full">
              <tbody id="cart-items-body">
                <!-- Dynamically populated by js/checkout.js -->
              </tbody>
            </table>

            <div class="pt-space-sm flex justify-between items-center text-sm border-t border-outline-variant/20">
              <a href="menu.html" class="font-label-md text-primary hover:underline flex items-center gap-1 font-semibold">
                <span class="material-symbols-outlined text-sm">add_circle</span>
                + Add more items from menu
              </a>
            </div>
          </div>
        </div>

        <!-- Right: Pickup Details & Customer Form (Single Integrated Checkout) -->
        <div class="lg:col-span-5 flex flex-col gap-space-lg">
          <div class="bg-surface-container-lowest rounded-xl shadow-md p-space-lg flex flex-col gap-space-md border border-outline-variant/30">
            <h2 class="font-headline-sm text-headline-sm text-on-surface pb-space-xs border-b border-outline-variant/20">Customer Details</h2>

            <form id="checkout-form" class="flex flex-col gap-space-md">
              
              <!-- 1. Outlet Selection -->
              <div class="flex flex-col gap-space-xs">
                <label class="font-label-md text-sm text-on-surface font-semibold">1. Choose Pickup Outlet</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-space-sm mt-1">
                  <label class="radio-card selected relative flex flex-col p-space-sm rounded-xl bg-secondary-container text-on-secondary-container cursor-pointer transition-all border border-primary/30">
                    <input type="radio" name="outlet" value="koramangala" checked class="sr-only">
                    <span class="font-label-md text-sm font-bold flex items-center justify-between">
                      Koramangala
                      <span class="material-symbols-outlined text-primary text-base">check_circle</span>
                    </span>
                    <span class="font-body-sm text-[11px] opacity-90 mt-0.5">Open Daily · 8:00 AM – 10:00 PM</span>
                  </label>
                  <label class="radio-card relative flex flex-col p-space-sm rounded-xl bg-surface-container-low text-on-surface-variant hover:bg-surface-container cursor-pointer transition-all border border-outline-variant/20">
                    <input type="radio" name="outlet" value="indiranagar" class="sr-only">
                    <span class="font-label-md text-sm font-semibold flex items-center justify-between">
                      Indiranagar
                      <span class="text-[10px] bg-tertiary-fixed text-on-tertiary-fixed px-1.5 py-0.5 rounded-full font-bold">Opening Soon</span>
                    </span>
                    <span class="font-body-sm text-[11px] opacity-80 mt-0.5">100 Feet Road</span>
                  </label>
                </div>
              </div>

              <!-- 2. Pickup Time Selection -->
              <div class="flex flex-col gap-space-xs">
                <label class="font-label-md text-sm text-on-surface font-semibold" for="pickup-time-input">2. Choose Pickup Time</label>
                <p class="font-body-sm text-xs text-on-surface-variant">Pickup times are in 15-minute slots from 8:00 AM to 9:45 PM.</p>

                <div id="cafe-closed-notice" class="closed-notice bg-error-container text-on-error-container p-space-sm rounded-lg font-body-sm text-sm" style="display: none;" role="status">
                  We're closed right now. Pickup starts at 8:00 AM.
                </div>

                <!-- Quick Presets -->
                <div class="flex gap-space-xs mt-1" id="preset-chips-container">
                  <button type="button" class="time-chip active bg-secondary-container text-on-secondary-container px-space-md py-1 rounded-full font-label-md text-xs font-semibold" data-minutes="15">+15 Mins</button>
                  <button type="button" class="time-chip bg-surface-container-low text-on-surface-variant hover:bg-surface-container px-space-md py-1 rounded-full font-label-md text-xs" data-minutes="30">+30 Mins</button>
                  <button type="button" class="time-chip bg-surface-container-low text-on-surface-variant hover:bg-surface-container px-space-md py-1 rounded-full font-label-md text-xs" data-minutes="45">+45 Mins</button>
                </div>

                <div class="mt-2 max-w-[240px]">
                  <select id="pickup-time-input" class="form-select w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 font-body-md text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary" aria-label="Selected pickup time">
                    <!-- Populated dynamically -->
                  </select>
                </div>

                <div id="time-alert" class="alert-box bg-error-container text-on-error-container p-2 rounded-lg text-xs mt-1" style="display: none;">
                  Please select a valid future pickup time.
                </div>
              </div>

              <!-- 3. Customer Contact Fields -->
              <div class="flex flex-col gap-space-xs pt-space-xs border-t border-outline-variant/20">
                <span class="font-label-md text-sm text-on-surface font-semibold">3. Your Contact Information</span>
                
                <div>
                  <label class="font-label-sm text-xs text-on-surface-variant" for="customer-name">
                    Your Name <span class="text-error">*</span>
                  </label>
                  <input type="text" id="customer-name" class="form-input w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5" placeholder="e.g. Alex Developer" required minlength="2">
                  <span class="font-body-sm text-[11px] text-outline">Printed on your cup and pickup ticket.</span>
                </div>

                <div class="mt-1">
                  <label class="font-label-sm text-xs text-on-surface-variant" for="customer-phone">
                    Phone Number <span class="text-xs text-outline">(Optional)</span>
                  </label>
                  <input type="tel" id="customer-phone" class="form-input w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5" placeholder="e.g. 9876543210">
                  <span class="font-body-sm text-[11px] text-outline">Used only if our baristas need to clarify your order.</span>
                </div>

                <div class="mt-1">
                  <label class="font-label-sm text-xs text-on-surface-variant" for="special-notes">
                    Special Instructions <span class="text-xs text-outline">(Optional)</span>
                  </label>
                  <textarea id="special-notes" class="form-textarea w-full bg-surface-container-lowest border border-outline-variant/50 rounded-lg px-3 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary mt-0.5" rows="2" placeholder="e.g. Extra hot, oat milk"></textarea>
                </div>
              </div>

              <!-- Order Summary -->
              <div class="bg-surface-container-low rounded-xl p-space-md flex flex-col gap-space-xs border border-outline-variant/20 mt-space-xs">
                <div class="flex justify-between text-sm">
                  <span class="text-on-surface-variant">Items</span>
                  <span id="cart-count-summary" class="font-code-pill font-medium">0 items</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-on-surface-variant">Subtotal</span>
                  <span id="cart-subtotal" class="font-code-pill font-semibold">$0.00</span>
                </div>
                <div class="flex justify-between text-xs text-outline">
                  <span>Taxes</span>
                  <span>Included in price</span>
                </div>
                <div class="pt-space-xs border-t border-outline-variant/30 flex justify-between items-baseline">
                  <span class="font-headline-sm text-headline-sm text-on-surface">Total Amount</span>
                  <span id="cart-total" class="font-headline-sm text-headline-sm text-primary font-bold">$0.00</span>
                </div>
              </div>

              <!-- Demo Notice & Submit -->
              <div class="text-xs text-on-surface-variant bg-surface-container-low p-2 rounded-lg text-center">
                This is a demo checkout. No payment details are needed online.
              </div>

              <button type="submit" id="btn-place-order" class="w-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md py-space-sm px-space-lg rounded-full shadow-md transition-all duration-200 flex items-center justify-center gap-space-xs">
                <span>Place Demo Order</span>
              </button>

            </form>

          </div>
        </div>

      </div>

    </div>
  </main>

  {get_footer()}
  {get_bottom_nav("cart")}

  <script src="js/cart.js"></script>
  <script src="js/checkout.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(SITE_DIR, "cart.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Built site/cart.html with single integrated checkout & Warm Terminal Roast style")

def build_checkout():
    # Keep one single checkout inside cart.html, and redirect checkout.html directly to cart.html
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=cart.html">
  <title>Redirecting to Order Checkout - KGP Vibes Cafe</title>
  <script>window.location.replace("cart.html");</script>
</head>
<body class="bg-background font-body-md text-on-surface p-8 text-center">
  <p>Redirecting to <a href="cart.html" class="text-primary underline font-semibold">Order Checkout</a>...</p>
</body>
</html>
'''
    with open(os.path.join(SITE_DIR, "checkout.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Built site/checkout.html as direct redirect to cart.html")

def build_confirmation():
    # Build clean confirmation.html without Wi-Fi passwords, status strip, or "Compiled Menu"
    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Order Confirmed - KGP Vibes Cafe</title>
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  {TAILWIND_CONFIG}
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-background font-body-md text-on-surface antialiased">
  {get_header("cart")}

  <main class="w-full pt-20 bg-background min-h-[calc(100vh-20rem)] flex items-center justify-center py-space-xl">
    <div class="max-w-xl w-full mx-auto px-margin">
      
      <div class="bg-surface-container-lowest rounded-2xl shadow-xl p-space-xl border border-outline-variant/30 flex flex-col gap-space-md text-center relative overflow-hidden">
        
        <div class="w-16 h-16 rounded-full bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center mx-auto text-3xl shadow-sm">
          ✓
        </div>

        <div>
          <span class="font-label-sm text-xs uppercase tracking-wider text-primary font-semibold">Order Received</span>
          <h1 class="font-headline-lg text-headline-lg text-on-surface mt-1">Order Confirmed!</h1>
          <p class="font-body-md text-on-surface-variant mt-1">Your order is being prepared fresh by our baristas.</p>
        </div>

        <!-- Ticket Receipt Box -->
        <div class="bg-surface-container-low rounded-xl p-space-lg text-left border border-outline-variant/20 flex flex-col gap-space-sm font-code-pill text-sm">
          <div class="flex justify-between items-center pb-space-xs border-b border-outline-variant/20">
            <span class="text-outline">Order Ticket</span>
            <span id="ticket-number" class="text-primary font-bold text-base">KV-0000</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-outline">Customer</span>
            <span id="ticket-customer" class="text-on-surface font-semibold">-</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-outline">Pickup Time</span>
            <span id="ticket-pickup-time" class="text-tertiary font-bold">-</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-outline">Outlet</span>
            <span id="ticket-outlet" class="text-on-surface font-semibold">-</span>
          </div>

          <div id="ticket-address" class="text-xs text-outline text-right">
            -
          </div>

          <ul id="ticket-items-container" class="flex flex-col gap-1 py-1 border-y border-outline-variant/20 text-xs text-on-surface">
          </ul>

          <div id="ticket-notes" class="text-xs text-secondary italic pt-1 border-t border-outline-variant/20" style="display: none;">
          </div>

          <div class="pt-space-xs border-t border-outline-variant/30 flex justify-between items-baseline">
            <span class="font-label-md font-bold text-on-surface">Total</span>
            <span id="ticket-total" class="font-headline-sm text-primary font-bold">$0.00</span>
          </div>
        </div>

        <div class="flex flex-col sm:row gap-space-sm mt-space-sm">
          <a href="menu.html" id="btn-another-order" class="flex-1 bg-primary hover:bg-primary-container text-on-primary font-label-md text-sm py-2.5 rounded-full shadow-sm transition-all text-center">
            Order Something Else
          </a>
          <a href="index.html" class="flex-1 bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md text-sm py-2.5 rounded-full transition-all text-center">
            Back to Home
          </a>
        </div>

      </div>

    </div>
  </main>

  {get_footer()}
  {get_bottom_nav("cart")}

  <script src="js/cart.js"></script>
  <script src="js/confirmation.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(SITE_DIR, "confirmation.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Built site/confirmation.html with clean plain ticket & no Wi-Fi status strip")

def main():
    build_home()
    build_menu()
    build_cart()
    build_checkout()
    build_confirmation()

if __name__ == "__main__":
    main()
