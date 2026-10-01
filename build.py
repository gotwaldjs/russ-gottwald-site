#!/usr/bin/env python3
"""Build Russ Gottwald's portfolio as plain static pages.

Edit the CONTENT section, then run:  python3 build.py
Output goes to ./public  (upload that folder to any static host).
Images: run  python3 fetch_images.py  once to download originals from Cargo into ./public/images.
"""
import html, json, os, re, shutil

# ════════════════════════════════════════════════════════════════
# SETTINGS
# ════════════════════════════════════════════════════════════════
NAME = 'Russ Gottwald'
EMAIL = 'rl.gottwald@gmail.com'              # [replace]
LINKEDIN = 'hhttps://www.linkedin.com/in/rlgottwald/'  # [replace]
LOCATION = '[Richmond, VA]'
SITE_URL = 'https://russgottwald.com'          # e.g. 'https://russgottwald.com' — enables link-preview images
SHOW_PROMPTS = False    # True: missing pieces show as [bracketed prompts]. False: left out.
CARGO = 'https://payload.cargocollective.com/1/18/592383/'
ROLES = ['Strategy', 'Copywriting', 'Creative direction', 'Teaching']

# ════════════════════════════════════════════════════════════════
# CONTENT
# media items: an image filename (from that project's Cargo folder) or 'vimeo:ID'
# ════════════════════════════════════════════════════════════════
def seq(fmt, nums): return [fmt.format(n) for n in nums]

PROJECTS = [
  dict(slug='nipsco', cargo='13958411', client='NIPSCO', title='Energy efficiency programs', year='2019–2020',
       agency='PACO Collective', kind='Integrated campaign', roles=['Strategy', 'Copywriting'],
       tags=['Copywriting', 'Strategy', 'Strategy direction'], cover='NIPSCO_OOH_EE_14x48.png',
       summary='Folks in Northern Indiana could save money and energy with energy efficiency programs from NIPSCO – but not enough knew about it. So they hired PACO Collective to help spread the word.',
       sections=[
         dict(h='Creative strategy', p=['(Note: the red line is the good one.)'], media=['NIPSCOCreativeStrategy.png']),
         dict(h='Media strategy', media=['NIPSCOMediaStrategy.png']),
         dict(h='Video', p=['“Driver” was featured in the December 2019 Lürzer’s Archive and won a Bronze Telly in 2020 for Craft: Use of Humor.',
                            '“Griller” won a Silver Telly in 2020 for Craft: Use of Humor.'],
              media=['vimeo:364287200', 'vimeo:364286717']),
         dict(h='OOH: sequential billboards', media=seq('NIPSCO_OOH_Sequential_416x1504_IN-374-2_0{}.jpg', [1, 2, 3])),
         dict(h='OOH: standard billboards', media=['NIPSCO_OOH_EE_14x48.png', 'NIPSCO_OOH_Digital_Heating-AC_400x1400_60051.jpg', 'NIPSCO_OOH_Digital_CI_416x1504_IN-137-1.jpg'], layout='one'),
       ]),
  dict(slug='illinois-dhs', cargo='14488767', client='Illinois Department of Human Services', title='COVID awareness in five languages',
       year='2021', agency='[Agency]', kind='Public health campaign', roles=['Strategy'], tags=['Brand strategy', 'Strategy direction'],
       cover='IDHS1.png',
       summary='“We’re not saving lives” is one of the oldest jokes in advertising. But sometimes, we get a chance to.',
       intro=['In 2021, the Illinois Department of Human Services wanted help raising COVID awareness among immigrant and refugee populations – specifically speakers of Arabic, Mandarin, Polish, Spanish, and Urdu.',
              'We had to not only determine the most relevant messages for each group, but also make sure that they were conveyed in an authentic manner.'],
       intro_media=['IDHS1.png', 'IDHS2.png'],
       sections=[
         dict(h='Arabic and Urdu', p=['Messaging stressed that it was important to get diagnosed early and that there was no shame in getting COVID.'],
              media=['IDHSArabic1.png', 'IDHSUrdu1.png', 'Screenshot-2023-10-22-at-5.46.21-PM.png', 'Screenshot-2023-10-22-at-5.46.44-PM.png']),
         dict(h='Mandarin, Polish, and Spanish', p=['Messaging focused on how gatherings can spread the disease as well as the importance of early diagnosis.'],
              placeholder='Mandarin, Polish, and Spanish executions (images to come)'),
       ]),
  dict(slug='pork-and-mindys', cargo='13959231', client='Pork & Mindy’s', title='Brand refinement and retail packaging', year='[Year]',
       agency='[Agency]', kind='Brand and packaging', roles=['Strategy', 'Copywriting', 'Creative direction'],
       tags=['Strategy', 'Copywriting', 'Creative direction'], cover='PnM_Sauce-Labels_MockUp_V2-R1_Sweet1.png',
       summary='Pork & Mindy’s is a barbecue restaurant in Chicago that’s the brainchild of “Sandwich King” Jeff Mauro.',
       intro=['We were asked to maintain their brash, entertainingly in-your-face personality while refining the brand, opening new locations, and introducing new package designs for retail products.'],
       sections=[
         dict(h='Barbecue sauce labels', p=['New labels feature pairing options and fold-out recipes.'],
              media=['PnM_Sauce-Labels_MockUp_V2-R1_Sweet1.png', 'PnM_Sauce-Labels_MockUp_V2-R1_Sweet2.png', 'PnM_Sauce-Labels_MockUp_V2-R1_SweetHeat2.png']),
         dict(h='Sauce packets', p=['Designed for sale with co-branded quick-prep meals.'], media=['Packet1-Sweet.png', 'Packet2-SweetHeat.png']),
         dict(h='Bo Jackson’s Pig Candy', media=['BosSweetPC.jpg', 'BosSweetHeatPC.jpg']),
         dict(h='Brand book', p=['The Brand Book was an opportunity to show future users the P&M brand even as we explained how to use it. Here are a few pages to give the idea.'],
              media=seq('BrandBook{}.png', [1, 2, 3, 5, 6, 12, 16, 30, 34])),
       ]),
  dict(slug='cazo-de-oro', cargo='13959228', client='Cazo de Oro', title='“Dale chicharron.”', year='[Year]', agency='[Agency]',
       kind='Brand campaign', roles=['Copywriting'], tags=['Copywriting'], cover='1-Tia.jpg',
       summary='Literally: “Give him the pork rind.” In Mexican slang: “Take him out.”',
       intro=['Using this expression in a mix of Spanish and Spanglish ties the Cazo de Oro brand to its roots while introducing it to today’s Southern California Latinos as the solution to life’s everyday frustrations.'],
       sections=[
         dict(h='Posters', media=['1-Tia.jpg', '2-Goalie.jpg', '3-Diet.jpg', 'DaleChicharron_POP-Branding_R2_V6.jpg']),
         dict(h='Social: recipe sharing', media=['Social3-Thai.jpg', 'Social1-GrilledCheese.jpg', 'Social2-Mac-Chicharron.jpg']),
       ]),
  dict(slug='big-lots', cargo='9404576', client='Big Lots!', title='Outdoor furniture for Latina shoppers', year='[Year]',
       agency='PACO Collective', kind='Consumer research', roles=['Strategy'],
       tags=['Strategy', 'Qual research', 'Quant research', 'Consumer journey'], cover='Slide1.png',
       summary='Big Lots! wanted to market outdoor furniture to Latinas. PACO was there to help them understand who they were trying to engage.',
       sections=[dict(h='The research', media=seq('Slide{}.png', [1] + list(range(3, 36))))]),
  dict(slug='burger-bach', cargo='13961117', client='Burger Bach', title='Brand review before franchising', year='[Year]',
       agency='[Agency]', kind='Brand strategy', roles=['Strategy'], tags=['Strategy'], cover='BBRecsPres001.png',
       summary='Burger Bach, a Richmond restaurant serving New Zealand beach cuisine, wanted to take a look at their brand before expanding into new markets with franchises.',
       sections=[dict(h='The review', media=[('BBRecsPres.008.png' if n == 8 else f'BBRecsPres{n:03d}.png') for n in range(1, 20)])]),
  dict(slug='usc-student-work', cargo='14488764', client='University of South Carolina', title='Student work, with awards',
       year='2021–2024', agency='', kind='Instructor portfolio', roles=['Teaching', 'Creative direction', 'Strategy'],
       tags=['Creative direction', 'Strategy direction'], cover='CityLarge.jpg', prompts=False,
       summary='Here is some of the work my students have done; awards and accolades where noted.',
       sections=[
         dict(h='Tampax', p=['2024 YoungOnes Finalist (OOH & Print/Promotional) and Shortlist (Art Direction); Gold ADDY and Best in Show (AAF Midlands and AAF District 3); Silver ADDY (AAF National).',
                             'Sophia McKowen and Abby Mondello'],
              media=['BusStop.jpg', 'AirportBillboard.jpg', 'CityLarge.jpg', 'MallSign.png']),
         dict(h='Fanta', p=['2024 YoungOnes Finalist (Integrated Campaign) and Shortlist (Experiential/Immersive).',
                            'Lizzie Batten, Ben Crispin, Katie Hall, and Katie Jameson'], media=['vimeo:968786329']),
         dict(h='Diablo IV', p=['2023 YoungOnes Shortlist (Print).', 'Koby Anderson, Allie Horres, Trent King, and Victoria Lynch'],
              media=seq('Screenshot-2023-10-23-at-9.{}-AM.png', ['48.06', '49.00', '51.14', '51.32', '51.49', '52.24', '49.30', '50.07', '50.26', '50.52'])),
         dict(h='Pernod Ricard', p=['2022 Effie Collegiate Finalist. Creative executions on slides 21–31.',
                                    'Sarah Corry, Gabrielle Loughlin, Elizabeth Messier, and Alyssa Ross'],
              media=['vimeo:877151975'] + seq('Spring-2022-Effies---Stallion---Drip_Page_{:02d}.png', range(1, 37))),
         dict(h='Bose', p=['2021 Effie Collegiate Semifinalist. Creative executions on slides 12–14.',
                           'Logan Ingram, Katie Marino, Summer Shinn, and Sarah Turner'],
              media=seq('Group-3-Plansbook_Page_{:02d}.png', range(1, 19))),
       ]),
  dict(slug='usc-more-student-work', cargo='14488885', client='University of South Carolina', title='More student work',
       year='2022–2024', agency='', kind='Instructor portfolio', roles=['Teaching', 'Creative direction', 'Strategy'],
       tags=['Creative direction', 'Strategy direction'], cover='Crocs-1.jpg', prompts=False,
       summary='Here are a few more samples of the work my students have done.',
       sections=[
         dict(h='Crocs', p=['Concept Development, Spring 2024.', 'Madison Enslow and Emily Gencarelli'],
              media=seq('Crocs-{}.jpg', [1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 21, 22, 32, 33, 34, 35, 28, 29, 30, 31, 42, 23, 47, 51, 57, 58, 59, 60])),
         dict(h='Pop-Tarts', p=['Integrated Campaigns, Fall 2022.', 'Art direction: Trent King'], media=['Screenshot-2023-10-23-at-11.33.02-AM.png']),
         dict(h='Chuck E. Cheese’s', p=['Concept Development, Spring 2023.', 'Rosie Cline and Mallory Tingen'],
              media=seq('317-Chuck-E.-Cheese-Final_Page_{:02d}.png', [1, 3, 4, 5, 6, 7, 26])),
         dict(h='Criterion', p=['Concept Development, Fall 2022.', 'Isabel Borja and Dan Zigelbaum'],
              media=seq('Slide{}.png', [1, 2, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 6])),
       ]),
  dict(slug='second-showing', cargo='10199980', client='VCU Brandcenter', title='Second Showing', year='[Year]', agency='',
       kind='Brandcenter project', roles=['Strategy'], tags=['Strategy', 'Brandcenter'], cover='Second-Showing.001.jpg',
       summary='[One sentence on what Second Showing is and what your part was.]',
       sections=[dict(h='The deck', media=seq('Second-Showing.{:03d}.jpg', range(1, 16))),
                 dict(h='The film', media=['vimeo:51654614'])]),
  dict(slug='campaigns-that-might-have-been', cargo='10199864', client='Spec work', title='Campaigns that might have been…but never were',
       year='[Year]', agency='', kind='Spec campaigns', roles=['Copywriting'], tags=['Copywriting', 'Art direction'],
       cover='NavyPier_FunHappens_OOH_Image.png', summary='[One line on why these exist.]',
       sections=[
         dict(h='CPS Energy: Find the Power', media=seq('-CPS{}.png', [1, 2, 3, 4])),
         dict(h='Navy Pier: Don’t Plan', p=[
           'Radio, “On the Clock”',
           'VINCE VAUGHN: I tell folks I’m going to Navy Pier, first thing they do is ask what I have planned. Like I wanna plan things when there’s a cornucopia of options around me.',
           'I’m Vince Vaughn. I live in the real world my dude, with work, with schedules: be here, be there, be on time, don’t be late, don’t miss your appointments. I get paid to live on a schedule, this is my time.',
           'So I’m gonna follow where fate leads me. Food, music, plays, art, tours, or maybe just a spectacular view of this beautiful town…it’s all up to that fickle lady’s fancy.',
           'I don’t wanna make plans. So I go somewhere I don’t have to.',
           'VO: Don’t plan your trip to Navy Pier.']),
         dict(h='Navy Pier: digital, Instagram, and OOH',
              media=seq('NavyPier_FunHappens_Digital_300x250_R1_F{}.jpg', range(1, 7)) +
                    ['NavyPier_FunHappens_Instagram_Kids_Mockup.png', 'NavyPier_FunHappens_Instagram_ShakespeareTheatre_Mockup.png', 'NavyPier_FunHappens_OOH_Image.png']),
         dict(h='The Smith & Wesson Model 29', p=['Just a thing I did when I heard Dirty Harry’s revolver was having its 60th birthday the same year as another American icon.'],
              media=['S-W29.003.jpg']),
       ]),
  dict(slug='turkeysb4trees', cargo='13961146', client='Spec work', title='#turkeysb4trees', year='[Year]', agency='',
       kind='Spec TV spot', roles=['Copywriting'], tags=['Copywriting'], cover='1.jpg',
       summary='Every year, Christmas marketing comes earlier. It takes away from the joy of the true holiday season, and it intrudes on that most American of holidays: Thanksgiving! One of my fondest dreams is striking back…',
       sections=[
         dict(h='The script', p=[
           'SCENE: A radiant autumn day in New England. Every hue of red, yellow, and orange is visible on the leaves that cover the ground – as well as those still on the trees that line a wide path through the woods.',
           'A Pilgrim walks his horse on the right hand side of the path, towards the camera, taking in the beauty of his surroundings.',
           'AVO: Some people have a deep, abiding respect…',
           'The Pilgrim hears a faint noise, and turns to the left. The noise grows louder and is distinguishable as the jingling of bells. The camera blurs.',
           'AVO: …for the most American of holidays.',
           'Camera blurs back in to show a passing sleigh, pulled by reindeer and driven by a fat, white-bearded man in a red suit. He casually lobs two gift-wrapped packages out of the side of the sleigh as it passes by the Pilgrim.',
           'AVO: And some people don’t.',
           'The packages land at the Pilgrim’s feet.',
           'JOLLY FAT MAN (VO): Ho, ho, ho!',
           'The Pilgrim looks up from the packages at his feet to face the camera. The camera zooms in on his right eye, from which a single tear trickles down his cheek.',
           'AVO: People start holiday marketing too early. People can stop it.',
           'Fade to end card.']),
         dict(h='The boards', p=['These boards reflect a straighter play on the Ad Council’s spot with Iron Eyes Cody; I’m wondering if a stop-motion visual style à la Burl Ives’ Rudolph might not be a better (i.e. more seasonal) fit.'],
              media=seq('{}.jpg', range(1, 7))),
       ]),
]

RESUME = dict(
  experience=[
    dict(role='[Strategy Director]', org='[Agency], [City]', dates='[Year]–present', body='[What you owned and at what scale: clients, teams, budgets, outcomes.]'),
    dict(role='[Title]', org='PACO Collective, [City]', dates='[Year]–[Year]', body='[Scope. Clients on the site from PACO include NIPSCO and Big Lots!]'),
    dict(role='Associate Creative Director', org='[Agency], [City]', dates='[Year]–[Year]', body='[Teams led, accounts run, the work that came out of it.]'),
    dict(role='Copywriter', org='[Agency], [City]', dates='[Year]–[Year]', body='[Brands written for and the work worth naming.]'),
  ],
  teaching=[dict(role='[Instructor title]', org='University of South Carolina', dates='[2021]–[2024]',
                 body='Courses include Concept Development and Integrated Campaigns. Student teams have been YoungOnes finalists, Effie Collegiate finalists and semifinalists, and Gold ADDY and Best in Show winners.')],
  education=[dict(role='[Degree]', org='[School]', dates='[Year]')],
  recognition=['Silver Telly, Craft: Use of Humor, NIPSCO “Griller,” 2020',
               'Bronze Telly, Craft: Use of Humor, NIPSCO “Driver,” 2020',
               'Lürzer’s Archive, NIPSCO “Driver,” December 2019'],
  skills='Brand strategy, copywriting, creative direction, qualitative and quantitative research, consumer journey mapping, teaching and mentoring',
)

ABOUT = [
  'I’ve had to approach this business from a lot of angles. BUT: all of that has made me a better strategist and strategy director. Briefing a creative team and justifying to clients when and how to push the envelope of an assignment are different matters when one’s run a marathon or three in a copywriter’s or creative director’s shoes. And I doubt I’d have ever had to manage 47 integrated teams at once in an agency setting.',
  'So I have a certain sympathy to…well, call it “counter-conventional wisdom”. For challenger audiences, not just challenger brands. For the rest of us who’ve zigged (zug?) when the world told us we were supposed to zag.',
  'Can I get my hands dirty? You bet. I’ll do it with glee. But I’ll also make your team and their work sharper. And I’ll help your clients solve the problems that keep them awake at night – the ones that conventional approaches failed to work on.',
]

# ════════════════════════════════════════════════════════════════
# RENDERING
# ════════════════════════════════════════════════════════════════
E = lambda s: html.escape(str(s), quote=True)
def T(s):
    s = str(s)
    return f'<span class="placeholder">{E(s)}</span>' if re.fullmatch(r'\[.*\]', s.strip()) else E(s)
def plain(s): return re.sub(r'\s+', ' ', re.sub(r'\[.*?\]', '', str(s))).strip()

T_MARK = '<svg viewBox="0 0 20 20" aria-hidden="true"><rect x="1" y="2" width="18" height="4" fill="#f0a202"/><rect x="8" y="2" width="4" height="16" fill="#f0a202"/></svg>'

def page(path, title, desc, body, nav, scripts=(), og_image=None):
    depth = path.count('/')
    r = '../' * depth
    canon = f'{SITE_URL}/{path.replace("index.html", "")}' if SITE_URL else ''
    meta = [f'<meta name="description" content="{E(desc)}">',
            f'<meta property="og:title" content="{E(title)}">',
            f'<meta property="og:description" content="{E(desc)}">',
            '<meta property="og:type" content="website">']
    if canon: meta += [f'<link rel="canonical" href="{E(canon)}">', f'<meta property="og:url" content="{E(canon)}">']
    if SITE_URL and og_image: meta.append(f'<meta property="og:image" content="{E(SITE_URL + "/" + og_image)}">')
    links = [('Work', 'index.html', 'home'), ('About', 'about/index.html', 'about'), ('Resume', 'resume/index.html', 'resume')]
    cur = ' aria-current="page"'
    navhtml = ''.join('<a href="%s%s"%s>%s</a>' % (r, h, cur if k == nav else '', l) for l, h, k in links)
    js = ''.join(f'<script src="{r}assets/{s}" defer></script>' for s in scripts)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
{chr(10).join(meta)}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect x='1' y='2' width='18' height='4' fill='%23f0a202'/%3E%3Crect x='8' y='2' width='4' height='16' fill='%23f0a202'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&family=IBM+Plex+Serif:ital,wght@1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/site.css">
{js}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <a class="mark" href="{r}index.html">{T_MARK}<span>{E(NAME)}</span></a>
  <nav class="site-nav" aria-label="Main">{navhtml}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <p class="ask">Got a problem conventional approaches haven’t solved?</p>
  <ul class="ways"><li><a href="mailto:{E(EMAIL)}">{E(EMAIL)}</a></li><li><a href="{E(LINKEDIN)}" rel="noopener">LinkedIn</a></li></ul>
  <small>© 2026 {E(NAME)}</small>
</footer>
</body>
</html>
'''

def img_path(p, f): return f'images/{p["slug"]}/{f}'

def media_block(p, items, r, label):
    out, imgs = [], [m for m in items if not m.startswith('vimeo:')]
    for m in items:
        if m.startswith('vimeo:'):
            vid = m.split(':', 1)[1]
            out.append(f'<div class="video"><iframe src="https://player.vimeo.com/video/{vid}?dnt=1" title="{E(label)} video" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>')
    if imgs:
        n = len(imgs)
        tags = [f'<img src="{r}{img_path(p, f)}" alt="{E(label)}, image {i + 1} of {n}" loading="lazy" decoding="async">' for i, f in enumerate(imgs)]
        if n > 6:
            out.append(f'<div class="deck" tabindex="0" role="region" aria-label="{E(label)}, {n} images, scrolls sideways">{"".join(tags)}</div><p class="deck-hint">{n} images. Scroll sideways.</p>')
        else:
            out.append(f'<div class="shots{" two" if n > 1 else ""}">{"".join(tags)}</div>')
    return ''.join(out)

def project_page(p, i):
    r = '../../'
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    prompts = SHOW_PROMPTS and p.get('prompts', True)
    show = lambda v: v or prompts
    paras = lambda a: ''.join(f'<p>{T(x)}</p>' for x in (a or []))
    facts = [(k, v) for k, v in [('Client', p['client']), ('Year', p['year']), ('Agency', p.get('agency')), ('Type of work', p['kind']), ('Disciplines', ', '.join(p['tags']))] if v]
    hero = f'<img src="{r}{img_path(p, p["cover"])}" alt="{E(p["title"])}">' if p.get('cover') else '<div class="ph" style="aspect-ratio:16/9"><span>Hero image, 16:9</span></div>'
    secs = []
    for s in p['sections']:
        m = media_block(p, s.get('media', []), r, s['h'])
        if s.get('placeholder'): m = f'<div class="ph" style="aspect-ratio:16/9"><span>{E(s["placeholder"])}</span></div>'
        wide = '<div class="wide">' + m + '</div>' if m else ''
        secs.append('<div class="sec"><div class="stem prose"><h2>' + E(s['h']) + '</h2>' + paras(s.get('p')) + '</div>' + wide + '</div>')
    credits = p.get('credits') or [('[Role]', '[Name]'), ('[Role]', '[Name]')]
    intro = ''
    if p.get('intro'):
        im = media_block(p, p.get('intro_media', []), r, p['title'])
        intro = '<div class="sec"><div class="stem prose">' + paras(p['intro']) + '</div>' + ('<div class="wide">' + im + '</div>' if im else '') + '</div>'
    line = '<blockquote class="the-line"><p>' + E(p.get('line') or '[The line that sold it.]') + '</p></blockquote>' if show(p.get('line')) else ''
    result = '<div class="stem prose"><h2>What happened</h2><p>' + T(p.get('result') or '[What happened. A number if you have one; recognition and what the client did next count too.]') + '</p></div>' if show(p.get('result')) else ''
    cred = '<div class="stem prose"><h2>Credits</h2><dl class="credits">' + ''.join('<dt>%s</dt><dd>%s</dd>' % (T(a), T(b)) for a, b in credits) + '</dl></div>' if show(p.get('credits')) else ''
    factsh = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(k), T(v)) for k, v in facts)
    body = f'''<article>
  <div class="stem"><a class="back" href="{r}index.html">Back to all work</a></div>
  <header class="stem p-head">
    <p class="p-client">{T(p["client"])}</p>
    <h1>{E(p["title"])}</h1>
    <p class="p-sum">{T(p["summary"])}</p>
  </header>
  <div class="wide p-hero">{hero}</div>
  <div class="wide"><dl class="t-bar facts" style="--n:{len(facts)}">{factsh}</dl></div>
  <div class="p-body">
    {intro}
    {line}
    {''.join(secs)}
    {result}
    {cred}
  </div>
  <nav class="stem next" aria-label="Next project"><a href="{r}work/{nxt["slug"]}/index.html"><span class="lbl">Next project</span><span class="ttl">{E(nxt["title"])}</span></a></nav>
</article>'''
    return page(f'work/{p["slug"]}/index.html', f'{plain(p["title"])} | {NAME}', plain(p['summary']) or plain(p['title']), body, 'home',
                og_image=img_path(p, p['cover']) if p.get('cover') else None)

def home():
    hero_markup = open(os.path.join(HERE, 'src', 'hero.html')).read()
    cards = ''.join(f'''<li class="work-item{" feature" if i == 0 else ""}" data-roles="{E("|".join(p["roles"]))}">
  <a href="work/{p["slug"]}/index.html">
    <div class="cover"><img src="{img_path(p, p["cover"])}" alt="" loading="{"eager" if i < 3 else "lazy"}" decoding="async"></div>
    <p class="client">{E(p["client"])}</p>
    <h3>{E(p["title"])}</h3>
    <p class="kind">{E(p["kind"])}. {E(", ".join(p["roles"]))}.</p>
  </a>
</li>''' for i, p in enumerate(PROJECTS))
    filt = ''.join(f'<button type="button" data-role="{E(r) if i else ""}" aria-pressed="{"true" if i == 0 else "false"}">{E(r)}</button>' for i, r in enumerate(['All work'] + ROLES))
    body = f'''<h1 class="sr">{E(NAME)}: strategist, copywriter, associate creative director, and teacher.</h1>
{hero_markup}
<div class="stem intro center">
  <p class="lede">Strategist, copywriter, creative director and teacher. I make teams and their work sharper, and help clients solve the problems conventional approaches haven’t.</p>
  <p class="intro-links"><a class="btn" href="about/index.html">About me</a><a class="btn" href="resume/index.html">Resume</a></p>
</div>
<section class="wide" aria-labelledby="work-h">
  <div class="work-head">
    <h2 id="work-h">Selected work</h2>
    <p class="note">I can’t show you everything here: current clients aren’t too keen on sharing a ton of details on websites. But I’ll be happy to discuss broad outlines, methodologies, and results.</p>
    <div class="filters" id="filters" role="group" aria-label="Filter work by role">{filt}</div>
  </div>
  <ul class="work-list" id="work-list">{cards}</ul>
  <p class="empty" id="work-empty" hidden>No projects tagged with this role yet.</p>
  <p class="sr" id="filter-status" aria-live="polite"></p>
</section>'''
    return page('index.html', NAME, 'Strategist, copywriter, associate creative director, and teacher.', body, 'home',
                scripts=('site.js', 'hero.js'), og_image=img_path(PROJECTS[0], PROJECTS[0]['cover']))

def about():
    body = f'''<header class="stem page-head center">
  <div class="portrait"><div class="ph" style="aspect-ratio:4/5"><span>Portrait, 4:5</span></div></div>
  <h1>We’re all supposed to be <span style="white-space:nowrap">hyper-specialized</span> these days.</h1>
  <p class="sub">My career didn’t turn out that way, and I’m grateful for it.</p>
</header>
<div class="wide"><ul class="t-bar pairs" aria-label="Roles held"><li>Strategist and copywriter</li><li>Agency and academia</li><li>Practitioner and mentor</li></ul></div>
<div class="stem prose">
  {''.join(f'<p>{E(x)}</p>' for x in ABOUT)}
  <div class="about-actions"><a class="btn" href="../resume/index.html">See the resume</a><a class="btn" href="mailto:{E(EMAIL)}">Email Russ</a></div>
</div>'''
    return page('about/index.html', f'About | {NAME}', 'We’re all supposed to be hyper-specialized these days. My career didn’t turn out that way, and I’m grateful for it.', body, 'about')

def resume():
    def entry(e):
        b = f'<p class="r-body">{T(e["body"])}</p>' if e.get('body') else ''
        return f'<div class="r-entry"><div class="r-dates">{T(e["dates"])}</div><div><h3>{T(e["role"])}</h3><p class="r-org">{T(e["org"])}</p>{b}</div></div>'
    R = RESUME
    body = f'''<header class="stem r-head">
  <h1>{E(NAME)}</h1>
  <p class="sub">Strategy, copywriting, creative direction, teaching</p>
  <p class="contact">{T(LOCATION)} &nbsp;/&nbsp; <a href="mailto:{E(EMAIL)}">{E(EMAIL)}</a></p>
  <button class="btn no-print" type="button" id="print">Print or save as PDF</button>
</header>
<div class="stem resume">
  <section class="r-sec"><h2>Experience</h2>{''.join(map(entry, R["experience"]))}</section>
  <section class="r-sec"><h2>Teaching</h2>{''.join(map(entry, R["teaching"]))}</section>
  <section class="r-sec"><h2>Education</h2>{''.join(map(entry, R["education"]))}</section>
  <section class="r-sec"><h2>Recognition</h2><ul class="r-list">{''.join(f'<li>{T(x)}</li>' for x in R["recognition"])}</ul></section>
  <section class="r-sec"><h2>Skills</h2><p style="margin:0">{T(R["skills"])}</p></section>
</div>'''
    return page('resume/index.html', f'Resume | {NAME}', f'Resume of {NAME}: strategy, copywriting, creative direction, teaching.', body, 'resume', scripts=('site.js',))

HERE = os.path.dirname(os.path.abspath(__file__))
def build():
    out = os.path.join(HERE, 'public')
    keep_images = os.path.join(out, 'images')
    for name in os.listdir(out) if os.path.isdir(out) else []:
        if name != 'images':
            pth = os.path.join(out, name)
            shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
    os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
    for f in ('site.css', 'site.js', 'hero.js'): shutil.copy(os.path.join(HERE, 'src', f), os.path.join(out, 'assets', f))
    pages = {'index.html': home(), 'about/index.html': about(), 'resume/index.html': resume()}
    for i, p in enumerate(PROJECTS): pages[f'work/{p["slug"]}/index.html'] = project_page(p, i)
    for path, htm in pages.items():
        full = os.path.join(out, path); os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'w', encoding='utf-8').write(htm)
    # image manifest for fetch_images.py
    manifest = []
    for p in PROJECTS:
        files = set([p['cover']] + p.get('intro_media', []) + [m for s in p['sections'] for m in s.get('media', []) if not m.startswith('vimeo:')])
        manifest += [{'url': CARGO + p['cargo'] + '/' + f, 'path': img_path(p, f)} for f in sorted(files)]
    json.dump(manifest, open(os.path.join(HERE, 'images.json'), 'w'), indent=1)
    print(f'Built {len(pages)} pages into public/ ; {len(manifest)} images listed in images.json')

if __name__ == '__main__':
    build()
