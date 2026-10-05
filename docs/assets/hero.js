(function(){
const L = 18000;
const BEATS = [
  {t0:0,     t1:3000,  step:-1, words:[["Strategist."],["Writer."],["/"],["Creative"],["lead."],["Teacher.",1]]},
  {t0:3000,  t1:5900,  step:0,  words:[["Start"],["with"],["why.",1]]},
  {t0:5900,  t1:9200,  step:1,  words:[["Go"],["deep",1],["on"],["/"],["the"],["words."]]},
  {t0:9200,  t1:12000, step:2,  words:[["Lead"],["the"],["work.",1]]},
  {t0:12000, t1:14800, step:3,  words:[["Train"],["tomorrow’s",1],["/"],["teams."]]},
  {t0:14800, t1:18000, step:-1, words:[["Range"],["across"],["the"],["room."],["/"],["Depth",1],["where",1],["it",1],["counts.",1]]}
];

const clamp = v => Math.max(0, Math.min(1, v));
const seg = (t, a, b) => clamp((t - a)/(b - a));
const outCubic = x => 1 - Math.pow(1 - x, 3);
const inOut = x => x < .5 ? 4*x*x*x : 1 - Math.pow(-2*x + 2, 3)/2;
const lerp = (a, b, x) => a + (b - a)*x;
const rad = d => d*Math.PI/180;

const GROUND = 440, BAR = 250, SX = 780, X0 = 620, X1 = 940;
const INK = '#1c1c1c', AMBER = '#f0a202', CAST_INK = '#6f6f6f', STONE = '#a8a8a8', HK = 1.3, CK = .95;

const P = {
  STAND: [-90, 106, 100, 74, 80, 100, 95, 80, 85],
  CROUCH:[-62, 125, 80, 112, 68, 28, 122, 40, 130],
  AIR:   [-82, -125, -115, -55, -65, 55, 115, 100, 145],
  LOOK:  [-90, 106, 100, -35, -150, 100, 95, 80, 85],
  DIVE:  [90, 95, 90, 85, 90, -95, -92, -85, -88],
  POINT: [-88, 106, 100, 18, 22, 100, 95, 80, 85],
  REACH: [-86, 106, 100, -40, -32, 100, 95, 80, 85]
};
const blend = (A, B, k) => A.map((a, i) => lerp(a, B[i], k));
function walkPose(ph){
  const s = Math.sin(ph);
  return [-86, 90 + 24*s, 70 + 24*s, 90 - 24*s, 70 - 24*s,
          90 - 26*s, 90 - 26*s + 32*Math.max(0, -s), 90 + 26*s, 90 + 26*s + 32*Math.max(0, s)];
}
function climbPose(ph){
  const s = Math.sin(ph);
  return [-90, -100 - 22*s, -95 - 22*s, -80 + 22*s, -85 + 22*s, 40 + 22*s, 118, 40 - 22*s, 118];
}
const LEN = {tor:32, neck:4, head:12, ua:18, fa:17, th:22, sh:22};
function rig(hx, hy, pose, face, k){
  const A = pose.map(a => face > 0 ? a : 180 - a);
  const d = (x, y, a, l) => [x + Math.cos(rad(a))*l*k, y + Math.sin(rad(a))*l*k];
  const neck = d(hx, hy, A[0], LEN.tor), head = d(...neck, A[0], LEN.neck + LEN.head);
  const eL = d(...neck, A[1], LEN.ua), hL = d(...eL, A[2], LEN.fa);
  const eR = d(...neck, A[3], LEN.ua), hR = d(...eR, A[4], LEN.fa);
  const kL = d(hx, hy, A[5], LEN.th), fL = d(...kL, A[6], LEN.sh);
  const kR = d(hx, hy, A[7], LEN.th), fR = d(...kR, A[8], LEN.sh);
  return {hip:[hx, hy], neck, head, eL, hL, eR, hR, kL, fL, kR, fR, r:LEN.head*k};
}
function footed(x, surface, pose, face, k){
  const r = rig(x, 0, pose, face, k);
  return surface - Math.max(r.fL[1], r.fR[1]) - 2.5*k;
}

const PENCIL_TIP = 50;
function pencilTip(r){
  const mx = (r.hL[0] + r.hR[0])/2, my = (r.hL[1] + r.hR[1])/2, a = Math.atan2(my - r.neck[1], mx - r.neck[0]);
  return [mx + Math.cos(a)*PENCIL_TIP*HK, my + Math.sin(a)*PENCIL_TIP*HK, a];
}
const TIP_OFF = (() => { const r = rig(0, 0, P.DIVE, 1, HK); return pencilTip(r)[1]; })();

function him(t){
  const S = P.STAND, k = HK;
  const on = (x, surf, pose, face = 1, dy = 0) => ({x, y:footed(x, surf, pose, face, k) + dy, pose, face});
  const bob = Math.sin(t/260)*1.2;
  if (t < 3000){
    const look = inOut(seg(t, 1500, 1900))*(1 - inOut(seg(t, 2500, 2900)));
    return on(560, GROUND, blend(S, P.LOOK, look), 1, bob*(1 - look));
  }
  if (t < 3300) return on(560, GROUND, blend(S, P.CROUCH, inOut(seg(t, 3000, 3300))));
  if (t < 3800){
    const u = seg(t, 3300, 3800), a = on(560, GROUND, P.CROUCH), b = on(620, BAR, P.CROUCH);
    return {x:lerp(a.x, b.x, u), y:lerp(a.y, b.y, u) - 70*Math.sin(Math.PI*u), pose:blend(P.CROUCH, P.AIR, Math.sin(Math.PI*u)), face:1};
  }
  if (t < 3950) return on(620, BAR, blend(P.CROUCH, S, inOut(seg(t, 3800, 3950))));
  if (t < 5300){ const x = lerp(620, SX, seg(t, 3950, 5300)); return on(x, BAR, blend(S, walkPose((x - 620)/9), seg(t, 3950, 4100))); }
  if (t < 5700) return on(SX, BAR, blend(S, P.LOOK, inOut(seg(t, 5300, 5500))));
  if (t < 5900) return on(SX, BAR, blend(P.LOOK, P.CROUCH, inOut(seg(t, 5700, 5900))));
  if (t < 6200){
    const u = seg(t, 5900, 6200), base = on(SX, BAR, P.CROUCH).y, apex = BAR - 2 - TIP_OFF;
    return {x:SX, y:lerp(base, apex, outCubic(u)) - 30*Math.sin(Math.PI*u), pose:blend(P.CROUCH, P.DIVE, inOut(u)), face:1};
  }
  if (t < 7400){
    return {x:SX, y:lerp(BAR - 2 - TIP_OFF, GROUND - TIP_OFF, inOut(seg(t, 6200, 7400))), pose:P.DIVE, face:1};
  }
  if (t < 7800){
    const u = inOut(seg(t, 7400, 7800)), b = on(800, GROUND, P.CROUCH);
    return {x:lerp(SX, 800, u), y:lerp(GROUND - TIP_OFF, b.y, u), pose:blend(P.DIVE, P.CROUCH, u), face:1};
  }
  if (t < 8100) return on(800, GROUND, blend(P.CROUCH, S, inOut(seg(t, 7800, 8100))));
  if (t < 9200) return on(800, GROUND, S, 1, bob);
  if (t < 9400){ const x = lerp(800, 760, seg(t, 9200, 9400)); return on(x, GROUND, walkPose((800 - x)/7), -1); }
  if (t < 10500){
    const u = seg(t, 9400, 10500), y0 = on(760, GROUND, S).y;
    return {x:760, y:lerp(y0, BAR - 8, inOut(u)), pose:blend(S, climbPose((t - 9400)/110), seg(t, 9400, 9550)), face:1};
  }
  if (t < 10800){
    const u = inOut(seg(t, 10500, 10800)), b = on(792, BAR, P.CROUCH);
    return {x:lerp(760, 792, u), y:lerp(BAR - 8, b.y, u) - 18*Math.sin(Math.PI*u), pose:blend(climbPose(1100/110), P.CROUCH, u), face:1};
  }
  if (t < 10950) return on(792, BAR, blend(P.CROUCH, S, inOut(seg(t, 10800, 10950))));
  if (t < 11600){ const x = lerp(792, 925, seg(t, 10950, 11600)); return on(x, BAR, walkPose((x - 792)/9)); }
  if (t < 12000) return on(925, BAR, blend(S, P.POINT, inOut(seg(t, 11600, 11800))));
  if (t < 12150) return on(925, BAR, blend(P.POINT, S, inOut(seg(t, 12000, 12150))), t < 12075 ? 1 : -1);
  if (t < 14800){
    const p = blend(S, P.POINT, inOut(seg(t, 12150, 12400))); p[3] += 10*Math.sin(t/220); p[4] += 12*Math.sin(t/220);
    return on(925, BAR, p, -1);
  }
  if (t < 15700){ const x = lerp(925, SX, seg(t, 14800, 15700)); return on(x, BAR, walkPose((925 - x)/9), -1); }
  if (t < 17000) return on(SX, BAR, S, t < 15800 ? -1 : 1, bob*seg(t, 15900, 16200));
  if (t < 17150) return on(SX, BAR, blend(S, P.CROUCH, inOut(seg(t, 17000, 17150))));
  if (t < 17700){
    const u = seg(t, 17150, 17700), a = on(SX, BAR, P.CROUCH), b = on(560, GROUND, P.CROUCH);
    return {x:lerp(a.x, b.x, u), y:lerp(a.y, b.y, u) - 60*Math.sin(Math.PI*u), pose:blend(P.CROUCH, P.AIR, Math.sin(Math.PI*u)), face:-1};
  }
  if (t < 17850) return on(560, GROUND, P.CROUCH, t < 17780 ? -1 : 1);
  return on(560, GROUND, blend(P.CROUCH, S, inOut(seg(t, 17850, 18000))));
}

const CAST = [
  {from:1270, to:1155, t0:10600, t1:11300, faceEnd:-1, fade:[10600, 16900], group:'team'},
  {from:1330, to:985,  t0:10650, t1:11450, faceEnd:1,  fade:[10650, 16900], group:'team'},
  {from:-60,  to:425,  t0:12000, t1:12800, faceEnd:1,  fade:[12000, 16900], group:'students'},
  {from:-120, to:590,  t0:12050, t1:12950, faceEnd:-1, fade:[12050, 16900], group:'students'}
];
const SMALL_T = {team:{x:1070, draw:[11500, 11800, 12100]}, students:{x:508, draw:[13100, 13500, 13900]}};
function castAt(c, t){
  const k = CK, u = seg(t, c.t0, c.t1), x = lerp(c.from, c.to, u), walking = u > 0 && u < 1;
  const dir = Math.sign(c.to - c.from);
  let pose = walking ? walkPose(Math.abs(x - c.from)/7) : P.STAND, face = walking ? dir : c.faceEnd;
  const dr = SMALL_T[c.group].draw;
  if (t > dr[0] - 200 && t < 16900){ pose = blend(P.STAND, P.REACH, inOut(seg(t, dr[0] - 200, dr[0])) * (1 - inOut(seg(t, dr[2] + 100, dr[2] + 400)))); face = c.faceEnd; }
  const opacity = seg(t, c.fade[0], c.fade[0] + 200)*(1 - seg(t, c.fade[1], c.fade[1] + 400));
  return {x, y:footed(x, GROUND, pose, face, k), pose, face, k, opacity};
}

const NS = 'http://www.w3.org/2000/svg', stage = document.getElementById('stage');
const el = (tag, attrs, parent = stage) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
const hairs = el('g', {stroke:'rgba(0,0,0,.06)', 'stroke-width':1});
[400, 800].forEach(x => el('line', {x1:x, y1:-1000, x2:x, y2:1000}, hairs));
el('line', {x1:-1000, y1:250, x2:3000, y2:250}, hairs);
el('line', {x1:-1000, y1:GROUND, x2:3000, y2:GROUND, stroke:INK, 'stroke-width':2.5});
const lineAttrs = (c, w, cap = 'round') => ({stroke:c, 'stroke-width':w, 'stroke-linecap':cap, fill:'none'});
const stem = el('line', lineAttrs(AMBER, 12, 'butt')), barL = el('line', lineAttrs(AMBER, 12, 'butt')), barR = el('line', lineAttrs(AMBER, 12, 'butt'));
const COPY_LINES = [[292, 58], [318, 44], [344, 62], [370, 38], [396, 54]];
const copyLines = COPY_LINES.map(() => el('line', lineAttrs(STONE, 3)));
const smallT = {};
for (const g in SMALL_T){ smallT[g] = {stem:el('line', lineAttrs(STONE, 8, 'butt')), bar:el('line', lineAttrs(STONE, 8, 'butt'))}; }
const mkFig = (ink, w) => { const g = el('g', {fill:'none', stroke:ink, 'stroke-width':w, 'stroke-linecap':'round', 'stroke-linejoin':'round'});
  return {g, p:el('path', {}, g), h:el('circle', {fill:'#ffffff'}, g), e1:el('circle', {fill:ink, stroke:'none'}, g), e2:el('circle', {fill:ink, stroke:'none'}, g)}; };
const castEls = CAST.map(() => mkFig(CAST_INK, 3.4));
const HIM = mkFig(INK, 4.2);
function figPath(r){
  const m = p => p.map(v => v.toFixed(1)).join(' ');
  return `M${m(r.hip)}L${m(r.neck)}M${m(r.neck)}L${m(r.eL)}L${m(r.hL)}M${m(r.neck)}L${m(r.eR)}L${m(r.hR)}M${m(r.hip)}L${m(r.kL)}L${m(r.fL)}M${m(r.hip)}L${m(r.kR)}L${m(r.fR)}`;
}
function drawFig(F, r, face, k){
  F.p.setAttribute('d', figPath(r)); F.h.setAttribute('cx', r.head[0]); F.h.setAttribute('cy', r.head[1]); F.h.setAttribute('r', r.r);
  const ax = r.head[0] - r.neck[0], ay = r.head[1] - r.neck[1], al = Math.hypot(ax, ay) || 1, ux = ax/al, uy = ay/al;
  const fx = -uy*face, fy = ux*face;
  [-1, 1].forEach((sgn, i) => {
    const e = i ? F.e2 : F.e1, off = 3.2*k;
    e.setAttribute('cx', r.head[0] + fx*(2.6*k + sgn*off) + ux*1.5*k); e.setAttribute('cy', r.head[1] + fy*(2.6*k + sgn*off) + uy*1.5*k); e.setAttribute('r', 1.7*k);
  });
}
const TAGS = [
  {txt:'Strategy', x:700, y:280, show:4600},
  {txt:'Copywriting', x:866, y:348, show:7100, anchor:'start'},
  {txt:'Creative direction', x:862, y:280, show:11200},
  {txt:'Team', x:1070, y:470, show:12000},
  {txt:'Students', x:508, y:470, show:13900}
].map(d => Object.assign(d, {e:el('text', {x:d.x, y:d.y, 'text-anchor':d.anchor || 'middle', fill:'#393939', 'font-size':15, 'font-family':'IBM Plex Sans, Helvetica Neue, Arial, sans-serif', 'letter-spacing':'.02em'})}));
TAGS.forEach(d => d.e.textContent = d.txt);
const setLine = (e, x1, y1, x2, y2, show = true) => { e.setAttribute('x1', x1); e.setAttribute('y1', y1); e.setAttribute('x2', x2); e.setAttribute('y2', y2); e.style.display = show ? '' : 'none'; };

const mkProp = (html) => { const g = el('g', {}); g.innerHTML = html; g.style.display = 'none'; return g; };
const SHAPES = {
  telescope:`<rect x="0" y="-3" width="10" height="6" fill="${INK}"/><rect x="10" y="-4.5" width="22" height="9" fill="#4a4a4a"/><rect x="18" y="-4.5" width="3" height="9" fill="${AMBER}"/><rect x="32" y="-6" width="10" height="12" fill="${INK}"/>`,
  pencil:`<rect x="-12" y="-5" width="8" height="10" rx="2" fill="#e8849a"/><rect x="-4" y="-5" width="5" height="10" fill="#9a9a9a"/><rect x="1" y="-5" width="37" height="10" fill="${AMBER}"/><rect x="1" y="-1.2" width="37" height="2.4" fill="#d68b00"/><polygon points="38,-5 50,0 38,5" fill="#f3d9a4"/><polygon points="46,-1.7 50,0 46,1.7" fill="${INK}"/>`,
  megaphone:`<rect x="-5" y="-3" width="6" height="6" fill="${INK}"/><polygon points="1,-4.5 27,-12 27,12 1,4.5" fill="#ffffff" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/><path d="M32 -8 q5 8 0 16 M37 -12 q7 12 0 24" fill="none" stroke="${INK}" stroke-width="2" stroke-linecap="round"/>`,
  mortar:`<rect x="-8" y="-1" width="16" height="7" fill="${INK}"/><polygon points="-18,0 0,-6 18,0 0,6" fill="${INK}"/><polyline points="0,0 14,2 14,13" fill="none" stroke="${AMBER}" stroke-width="2" stroke-linecap="round"/>`,
  pointer:`<line x1="0" y1="0" x2="36" y2="0" stroke="${INK}" stroke-width="2.6" stroke-linecap="round"/>`
};
const PROPS = {}; for (const k in SHAPES) PROPS[k] = mkProp(SHAPES[k]);
const ROW = ['telescope', 'pencil', 'megaphone', 'mortar'].map(k => mkProp(SHAPES[k]));
const popIn = (t, a, b) => { const x = seg(t, a, a + 220), y = seg(t, b - 160, b); return x <= 0 || y >= 1 ? 0 : (1 + 1.6*Math.pow(x - 1, 3) + .6*Math.pow(x - 1, 2))*(1 - y); };
function place(g, x, y, ang, sc, flipY = 1, flipX = 1){
  if (sc <= .001){ g.style.display = 'none'; return; }
  g.style.display = ''; g.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${ang.toFixed(1)}) scale(${(sc*HK*flipX).toFixed(3)} ${(sc*HK*flipY).toFixed(3)})`);
}
function drawProps(t, h, r){
  const deg = a => a*180/Math.PI;
  { const s = popIn(t, 5300, 5760), f = h.face; place(PROPS.telescope, r.head[0] + f*4*HK, r.head[1] - 1*HK, f > 0 ? -8 : 188, s, f > 0 ? 1 : -1); }
  { const s = popIn(t, 5760, 7560), a = pencilTip(r)[2]; const mx = (r.hL[0] + r.hR[0])/2, my = (r.hL[1] + r.hR[1])/2; place(PROPS.pencil, mx, my, deg(a), s); }
  { const s = popIn(t, 11600, 12080), a = Math.atan2(r.hR[1] - r.eR[1], r.hR[0] - r.eR[0]); place(PROPS.megaphone, r.hR[0], r.hR[1], deg(a), s, h.face > 0 ? 1 : -1); }
  { const s = popIn(t, 12150, 14820), f = h.face;
    place(PROPS.mortar, r.head[0], r.head[1] - r.r - 1, 0, s, 1, f);
    const a = Math.atan2(r.hR[1] - r.eR[1], r.hR[0] - r.eR[0]); place(PROPS.pointer, r.hR[0], r.hR[1], deg(a), s); }
  ROW.forEach((g, i) => {
    const s = popIn(t, 15900 + i*120, 16950), cx = h.x + (i - 1.5)*46*HK, cy = r.head[1] - r.r - 36*HK;
    const dx = [-21, -19, -14, 0][i]*HK*.64;
    place(g, cx + dx, cy, 0, s*.8);
  });
}

const steps = [...document.querySelectorAll('#steps button')];
function render(t){
  const h = him(t), r = rig(h.x, h.y, h.pose, h.face, HK);
  drawFig(HIM, r, h.face, HK);
  drawProps(t, h, r);
  const erase = inOut(seg(t, 17000, 17500));
  let xl = t < 3800 ? null : t < 3950 ? 620 : t < 5300 ? h.x : SX;
  if (xl !== null){ const a = lerp(X0, SX, erase); setLine(barL, a, BAR, Math.max(a, xl), BAR, erase < 1 && xl - a > .5); } else barL.style.display = 'none';
  let xr = t < 10950 ? null : t < 11600 ? h.x : lerp(925, X1, outCubic(seg(t, 11600, 11750)));
  if (xr !== null){ const b = lerp(xr, SX, erase); setLine(barR, SX, BAR, b, BAR, erase < 1); } else barR.style.display = 'none';
  let sy = null;
  if (t >= 6200 && t < 7400) sy = Math.min(GROUND, Math.max(BAR, pencilTip(r)[1]));
  else if (t >= 7400) sy = GROUND;
  if (sy !== null){ const y2 = lerp(sy, BAR, erase); setLine(stem, SX, BAR - 6, SX, y2, erase < 1 && y2 > BAR + .5); } else stem.style.display = 'none';
  COPY_LINES.forEach(([y, w], i) => {
    const passT = 6200 + (y - BAR)/(GROUND - BAR)*1200 + 60, g = outCubic(seg(t, passT, passT + 260))*(1 - seg(t, 16900, 17200));
    setLine(copyLines[i], SX + 16, y, SX + 16 + w*g, y, g > 0);
  });
  for (const g in SMALL_T){
    const {x, draw} = SMALL_T[g], half = 55, top = GROUND - 80, e2 = inOut(seg(t, 17000, 17400));
    const b = outCubic(seg(t, draw[0], draw[1]))*(1 - e2), s = inOut(seg(t, draw[1], draw[2]))*(1 - e2);
    setLine(smallT[g].bar, x - half*b, top, x + half*b, top, b > 0);
    setLine(smallT[g].stem, x, top - 4, x, top + 80*s, s > 0);
  }
  CAST.forEach((c, i) => {
    const s = castAt(c, t), E = castEls[i];
    E.g.style.opacity = s.opacity; E.g.style.display = s.opacity > 0 ? '' : 'none';
    if (s.opacity > 0) drawFig(E, rig(s.x, s.y, s.pose, s.face, s.k), s.face, s.k);
  });
  TAGS.forEach(d => { d.e.style.opacity = seg(t, d.show, d.show + 350)*(1 - seg(t, 16900, 17200)); });
  drawCopy(t);
  const b = BEATS.find(b => t >= b.t0 && t < b.t1);
  steps.forEach((s, i) => { const on = b && b.step === i; s.classList.toggle('on', on); s.setAttribute('aria-current', on ? 'step' : 'false'); });
}

const copy = document.getElementById('copy');
const lines = BEATS.map(b => {
  const e = document.createElement('div'); e.className = 'line';
  b.words.forEach(([w, em]) => { if (w === '/'){ e.appendChild(document.createElement('br')); return; } const s = document.createElement('span'); s.className = 'w'; if (em){ s.classList.add('em'); s.innerHTML = `<span class="s">${w}</span><span class="i">${w}</span>`; } else s.textContent = w; e.appendChild(s); });
  copy.appendChild(e); return {e, words:[...e.querySelectorAll('.w')], b};
});
function measureEm(){ document.querySelectorAll('.copy .em').forEach(w => { w.style.width = ''; w._ws = w.firstChild.offsetWidth; w._wi = w.lastChild.offsetWidth; }); }
function drawCopy(t){
  lines.forEach(({e, words, b}) => {
    const live = t >= b.t0 - 50 && t < b.t1; e.style.visibility = live ? 'visible' : 'hidden'; if (!live) return;
    const out = seg(t, b.t1 - 380, b.t1 - 60);
    words.forEach((w, i) => {
      const inn = outCubic(seg(t, b.t0 + 60 + i*90, b.t0 + 540 + i*90));
      w.style.opacity = inn*(1 - out); w.style.transform = `translateY(${(1 - inn)*.5 - out*.25}em)`;
      if (w.classList.contains('em')){ const sw = inOut(seg(t, b.t0 + 1000, b.t0 + 1350)); w.firstChild.style.opacity = 1 - sw; w.lastChild.style.opacity = sw; if (w._ws) w.style.width = lerp(w._ws, w._wi, sw) + 'px'; }
    });
  });
}

const strip = document.getElementById('strip');
function frameView(){
  const w = strip.clientWidth, h = strip.clientHeight; if (!w || !h) return;
  const a = w/h; let vb;
  if (a > 2) vb = [0, 0, 1200, 500];
  else if (a > 1.2){ const vw = 960, vh = vw/a; vb = [250, GROUND - .74*vh, vw, vh]; }
  else { const vw = 770, vh = vw/a; vb = [405, GROUND - .8*vh, vw, vh]; }
  stage.setAttribute('viewBox', vb.join(' '));
}

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let clock = 0, prev = null, raf = null, userPaused = false, onScreen = true;
function frame(now){ if (prev !== null) clock += Math.min(now - prev, 50); prev = now; render(clock % L); raf = requestAnimationFrame(frame); }
const start = () => { if (!raf && !reduce && !userPaused && onScreen){ prev = null; raf = requestAnimationFrame(frame); } };
const stop = () => { if (raf){ cancelAnimationFrame(raf); raf = null; } };
function jump(t){ clock = t; if (!raf) render(clock % L); }
steps.forEach(s => s.addEventListener('click', () => jump(BEATS[+s.dataset.beat].t0 + 80)));

new ResizeObserver(() => { if (!strip.clientWidth) return; frameView(); measureEm(); render(reduce ? 16200 : clock % L); }).observe(strip);
frameView();
(document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
  measureEm();
  render(reduce ? 16200 : 0); start();
});
const btn = strip.querySelector('.pause'), icon = document.getElementById('pi');
btn.addEventListener('click', () => {
  userPaused = !userPaused; userPaused ? stop() : start();
  btn.setAttribute('aria-pressed', String(userPaused));
  btn.setAttribute('aria-label', userPaused ? 'Play animation' : 'Pause animation');
  icon.setAttribute('d', userPaused ? 'M4 2l10 6-10 6z' : 'M4 2h3v12H4zM9 2h3v12H9z');
});
new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; onScreen ? start() : stop(); }).observe(strip);
})();
