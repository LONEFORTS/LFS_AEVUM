/* ================================================================
   AEVUM — Legendary Interaction Engine
   Immersive scroll, reveal-on-view, timer, active nav, copy, forms.
   ================================================================ */
(function(){
  'use strict';

  // ---------- SVG icon library ----------
  const ICONS = {
    home:'<path stroke-linecap="round" stroke-linejoin="round" d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
    note:'<path stroke-linecap="round" stroke-linejoin="round" d="M5 4h11l4 4v12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/><path stroke-linecap="round" d="M15 4v5h5M8 13h8M8 17h6"/>',
    assign:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 4h6l1 2h3a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h3z"/><path stroke-linecap="round" d="m9 14 2 2 4-4"/>',
    task:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h10M4 12h16M4 18h7"/><circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/>',
    event:'<rect x="3" y="5" width="18" height="16" rx="2"/><path stroke-linecap="round" d="M3 10h18M8 3v4M16 3v4"/>',
    att:'<path stroke-linecap="round" stroke-linejoin="round" d="M8 4h8a2 2 0 0 1 2 2v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V6a2 2 0 0 1 2-2z"/><path stroke-linecap="round" d="M9 3h6v3H9zM9 12h6M9 16h4"/>',
    news:'<path stroke-linecap="round" stroke-linejoin="round" d="M3 11v4a2 2 0 0 0 2 2h4l6 4V5L9 9H5a2 2 0 0 0-2 2z"/><path stroke-linecap="round" d="M19 8a5 5 0 0 1 0 8"/>',
    code:'<path stroke-linecap="round" stroke-linejoin="round" d="m8 8-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>',
    focus:'<circle cx="12" cy="13" r="8"/><path stroke-linecap="round" d="M12 9v4l2 2M9 3h6"/>',
    search:'<circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="m20 20-4-4"/>',
    user:'<circle cx="12" cy="8" r="4"/><path stroke-linecap="round" d="M4 21a8 8 0 0 1 16 0"/>',
    share:'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path stroke-linecap="round" d="m8.6 10.6 6.8-4.2M8.6 13.4l6.8 4.2"/>',
    plus:'<path stroke-linecap="round" d="M12 5v14M5 12h14"/>',
    edit:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 20h4l10-10-4-4L4 16zM14 6l4 4"/>',
    trash:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 7h16M9 7V4h6v3M6 7l1 13a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1l1-13M10 11v6M14 11v6"/>',
    check:'<path stroke-linecap="round" stroke-linejoin="round" d="m5 12 5 5 9-11"/>',
    x:'<path stroke-linecap="round" d="M6 6l12 12M18 6 6 18"/>',
    arrow:'<path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 5l7 7-7 7"/>',
    play:'<path stroke-linecap="round" stroke-linejoin="round" d="M6 4v16l14-8z"/>',
    save:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 0 1 1-1h11l4 4v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path stroke-linecap="round" d="M8 4v5h7M8 21v-6h8v6"/>',
    star:'<path stroke-linecap="round" stroke-linejoin="round" d="m12 3 2.9 6 6.6.9-4.8 4.6 1.2 6.5-6-3.2-6 3.2 1.2-6.5L2.5 9.9 9 9z"/>',
    fire:'<path stroke-linecap="round" stroke-linejoin="round" d="M12 3s6 5 6 11a6 6 0 0 1-12 0c0-2 1-4 2-5 0 3 2 4 2 4s-1-3 2-10z"/>',
    github:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 19c-4 1-4-2-6-2m12 4v-3.5c0-1-.1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6 0-1.3-.4-2.4-1.2-3.3.4-.6.5-2-.2-3.3 0 0-1-.3-3.5 1.2a12 12 0 0 0-6.2 0C6.4 3 5.4 3.4 5.4 3.4c-.7 1.3-.6 2.7-.2 3.3A4.6 4.6 0 0 0 4 10c0 4.6 2.7 5.7 5.5 6-.4.5-.5 1-.5 2V21"/>',
    lightning:'<path stroke-linecap="round" stroke-linejoin="round" d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    chart:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
    sparkle:'<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
    logout:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h4M16 17l5-5-5-5M9 12h12"/>',
    alert:'<path stroke-linecap="round" stroke-linejoin="round" d="M12 3 2 21h20zM12 10v5M12 18v.5"/>',
    check2:'<circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="m8 12 3 3 5-6"/>',
    upload:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2M12 3v13M6 9l6-6 6 6"/>',
    download:'<path stroke-linecap="round" stroke-linejoin="round" d="M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2M12 3v13M6 11l6 6 6-6"/>',
    external:'<path stroke-linecap="round" stroke-linejoin="round" d="M14 4h6v6M20 4 10 14M20 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h5"/>',
    send:'<path stroke-linecap="round" stroke-linejoin="round" d="m4 12 17-8-7 18-3-8z"/>',
    tag:'<path stroke-linecap="round" stroke-linejoin="round" d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="8" cy="8" r="1.5"/>',
    clock:'<circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 7v5l3 2"/>',
    pin:'<path stroke-linecap="round" stroke-linejoin="round" d="M12 17v5M8 4h8v6l3 3H5l3-3z"/>',
    copy:'<rect x="8" y="8" width="12" height="12" rx="2"/><path stroke-linecap="round" d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
    globe:'<circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    palette:'<path stroke-linecap="round" stroke-linejoin="round" d="M12 3a9 9 0 1 0 0 18c1 0 2-1 2-2s-1-1-1-2 1-2 2-2h2a4 4 0 0 0 0-8 9 9 0 0 0-5-4z"/><circle cx="7" cy="12" r="1"/><circle cx="9" cy="7" r="1"/><circle cx="14" cy="6" r="1"/><circle cx="17" cy="10" r="1"/>'
  };

  function svg(name){
    const p = ICONS[name] || '';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">${p}</svg>`;
  }
  window.Aevum = window.Aevum || {};
  window.Aevum.svg = svg;

  // ---------- Icon injection ----------
  function injectIcons(){
    document.querySelectorAll('[data-i]').forEach(el=>{
      if(el.dataset._done)return;
      el.dataset._done='1';
      el.innerHTML = svg(el.dataset.i) + (el.innerHTML.trim()? ' '+el.innerHTML : '');
    });
    document.querySelectorAll('[data-icon]').forEach(el=>{
      if(el.dataset._doneI)return;
      el.dataset._doneI='1';
      el.innerHTML = svg(el.dataset.icon);
    });
  }

  // ---------- Form autoclass ----------
  function styleForms(){
    document.querySelectorAll('input:not([type=color]):not([type=checkbox]):not([type=radio]):not([type=file]):not(.no-auto), textarea:not(.no-auto), select:not(.no-auto)').forEach(el=>{
      if(el.tagName==='SELECT') el.classList.add('form-select');
      else el.classList.add('form-control');
    });
  }

  // ---------- Active nav highlight ----------
  function activeNav(){
    const here = window.location.pathname;
    document.querySelectorAll('.nav-x a, .mobile-nav-x a').forEach(a=>{
      const href = a.getAttribute('href'); if(!href||href==='#')return;
      const base = href.split('?')[0];
      if(base==='/dashboard/' && here==='/dashboard/'){a.classList.add('active');return;}
      if(base!=='/dashboard/' && base.length>1 && here.startsWith(base)) a.classList.add('active');
    });
  }

  // ---------- Reveal on scroll ----------
  function revealOnView(){
    if(!('IntersectionObserver' in window))return;
    const io = new IntersectionObserver(entries=>{
      entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }});
    },{threshold:.15});
    document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
  }

  // ---------- Immersive scroll (hide topbar/mobile-nav on scroll, show on scroll up) ----------
  function immersiveScroll(){
    let lastY = window.scrollY;
    let ticking = false;
    let idleTimer;
    const body = document.body;

    function onScroll(){
      const y = window.scrollY;
      const dy = y - lastY;
      lastY = y;

      // Enter immersive on scroll down past threshold, exit when scrolling up
      if(y > 60 && dy > 4){
        body.classList.add('is-immersive');
      } else if(dy < -4 || y < 40){
        body.classList.remove('is-immersive');
      }

      // Also exit after idle (no scroll for 1.5s)
      clearTimeout(idleTimer);
      idleTimer = setTimeout(()=>{ body.classList.remove('is-immersive'); }, 1500);

      ticking = false;
    }

    window.addEventListener('scroll', ()=>{
      if(!ticking){ requestAnimationFrame(onScroll); ticking = true; }
    }, {passive:true});
  }

  // ---------- Gate: starfield + shooting stars ----------
  function initStarfield(){
    const holder = document.querySelector('.starfield');
    if(!holder) return;
    const w = holder.offsetWidth || window.innerWidth;
    const h = holder.offsetHeight || window.innerHeight;
    const count = Math.min(120, Math.floor((w*h)/12000));
    let frag = '';
    for(let i=0;i<count;i++){
      const size = Math.random()*1.6 + .4;
      const x = Math.random()*100;
      const y = Math.random()*100;
      const dur = 2 + Math.random()*5;
      const delay = Math.random()*6;
      const op = .35 + Math.random()*.55;
      frag += `<span class="star" style="left:${x}%;top:${y}%;width:${size}px;height:${size}px;--dur:${dur}s;--delay:${delay}s;--maxOp:${op}"></span>`;
    }
    for(let i=0;i<3;i++){
      const top = Math.random()*40;
      const left = Math.random()*40;
      const dur = 6 + Math.random()*6;
      const delay = 2 + Math.random()*8;
      frag += `<span class="shooting-star" style="top:${top}%;left:${left}%;--dur:${dur}s;--delay:${delay}s"></span>`;
    }
    holder.innerHTML = frag;
  }

  // ---------- Pomodoro timer ----------
  window.startTimer = function(){
    const input = document.querySelector('#id_minutes');
    const display = document.getElementById('timerDisplay');
    if(!input||!display) return;
    let seconds = (parseInt(input.value||25,10))*60;
    display.textContent = fmt(seconds);
    if(window.__t) clearInterval(window.__t);
    window.__t = setInterval(()=>{
      seconds--;
      display.textContent = fmt(seconds);
      if(seconds<=0){
        clearInterval(window.__t);
        display.textContent = '00:00';
        try{ navigator.vibrate && navigator.vibrate([180,80,180]); }catch(e){}
        alert('Focus session finished. Tap Save Completed Session.');
      }
    },1000);
  };
  function fmt(t){const m=String(Math.floor(t/60)).padStart(2,'0');const s=String(t%60).padStart(2,'0');return `${m}:${s}`;}

  // ---------- Copy ----------
  window.copyText = function(el){
    const txt = el.getAttribute('data-copy') || el.innerText;
    if(!navigator.clipboard) return;
    navigator.clipboard.writeText(txt).then(()=>{
      const orig = el.dataset._orig || el.innerText;
      el.dataset._orig = orig;
      el.innerText = 'Copied to clipboard';
      setTimeout(()=>{ el.innerText = orig; }, 1400);
    });
  };

  // ---------- Boot ----------
  function boot(){
    injectIcons();
    styleForms();
    activeNav();
    revealOnView();
    immersiveScroll();
    initStarfield();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
