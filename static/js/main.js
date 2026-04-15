/**
 * main.js — edlynexavier.com
 * Lightweight vanilla JS — no dependencies.
 * Covers: navbar scroll, scroll animations, skill bars, flash messages.
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. Navbar scroll state ─────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    const handleNavScroll = () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', handleNavScroll, { passive: true });
    handleNavScroll(); // run once on load
  }


  // ── 2. Scroll-triggered fade-in animations ─────────────────────────────
  const animatedElements = document.querySelectorAll('[data-animate]');
  if (animatedElements.length && 'IntersectionObserver' in window) {
    const animObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            animObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -48px 0px' }
    );
    animatedElements.forEach((el) => animObserver.observe(el));
  }


  // ── 3. Skill bar animation (paused until visible) ─────────────────────
  const skillBars = document.querySelectorAll('.skill-bar');
  if (skillBars.length && 'IntersectionObserver' in window) {
    // Start all bars paused
    skillBars.forEach((bar) => {
      bar.style.animationPlayState = 'paused';
    });

    const barObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.animationPlayState = 'running';
            barObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    skillBars.forEach((bar) => barObserver.observe(bar));
  }


  // ── 4. Auto-dismiss flash messages ────────────────────────────────────
  const alerts = document.querySelectorAll('.messages-container .alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch (_) {
        // Bootstrap not available or already dismissed
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.4s ease';
        setTimeout(() => alert.remove(), 400);
      }
    }, 5500);
  });


  // ── 5. Active nav link highlighting ───────────────────────────────────
  // Already handled via Django template logic, but ensure mobile state
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach((link) => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });


  // ── 6. Smooth external link handling ──────────────────────────────────
  // Add rel="noopener noreferrer" to any external links missed in templates
  document.querySelectorAll('a[target="_blank"]').forEach((link) => {
    if (!link.rel || !link.rel.includes('noopener')) {
      link.rel = 'noopener noreferrer';
    }
  });


  // ── 7. Form UX improvements ───────────────────────────────────────────
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    const submitBtn = contactForm.querySelector('.btn-submit');

    contactForm.addEventListener('submit', () => {
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Sending…';
      }
    });

    // Real-time validation feedback on blur
    contactForm.querySelectorAll('.form-control').forEach((input) => {
      input.addEventListener('blur', () => {
        if (input.value.trim().length > 0) {
          input.style.borderColor = 'rgba(34, 197, 94, 0.4)';
        }
      });
      input.addEventListener('input', () => {
        input.style.borderColor = ''; // reset on typing
      });
    });
  }


  // ── 8. Project card lazy load fallback ────────────────────────────────
  document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
    img.addEventListener('error', () => {
      img.style.display = 'none';
      const wrap = img.closest('.project-card-img-wrap');
      if (wrap) {
        wrap.style.background = 'var(--clr-bg-card)';
        const placeholder = document.createElement('div');
        placeholder.innerHTML = '<i class="bi bi-image" style="font-size:2.5rem;color:var(--clr-text-faint);display:flex;align-items:center;justify-content:center;height:100%;"></i>';
        placeholder.style.cssText = 'height:100%;display:flex;align-items:center;justify-content:center;';
        wrap.appendChild(placeholder);
      }
    });
  });

});
