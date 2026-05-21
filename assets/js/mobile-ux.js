/* ============================================================
   tamj-residence - mobile UX (drawer + lightbox)
   ============================================================
   - <button class="nav-toggle"> をタップ → ドロワー開閉
   - <figure class="photo-figure"> や <table>, <svg.chart-svg> や
     <.finance-pl-wrap> をタップ → 全画面で拡大表示
   - 全画面表示中はピンチズーム可能 (touch-action: none を解除)
   依存: なし (vanilla JS)
   ============================================================ */
(function () {
  'use strict';

  // ===== Drawer =====
  function initDrawer() {
    var toggle = document.querySelector('.nav-toggle');
    var drawer = document.querySelector('.nav-drawer');
    var backdrop = document.querySelector('.nav-drawer-backdrop');
    if (!toggle || !drawer) return;

    function open() {
      drawer.classList.add('open');
      if (backdrop) backdrop.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      document.documentElement.style.overflow = 'hidden';
    }
    function close() {
      drawer.classList.remove('open');
      if (backdrop) backdrop.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      document.documentElement.style.overflow = '';
    }
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      if (drawer.classList.contains('open')) close(); else open();
    });
    if (backdrop) backdrop.addEventListener('click', close);
    // 内部リンクをタップしたら閉じる
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', close);
    });
    // ESC で閉じる
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) close();
    });
  }

  // ===== Lightbox =====
  // 動的に作成 (HTML側に書かなくて良い)
  function ensureLightbox() {
    var lb = document.getElementById('lb-overlay');
    if (lb) return lb;
    lb = document.createElement('div');
    lb.id = 'lb-overlay';
    lb.className = 'lb-overlay';
    lb.innerHTML =
      '<button class="lb-close" aria-label="閉じる">&times;</button>' +
      '<div class="lb-stage"><div class="lb-content"></div></div>' +
      '<div class="lb-hint">ピンチで拡大 / ダブルタップで初期サイズ / 背景タップで閉じる</div>';
    document.body.appendChild(lb);

    var closeBtn = lb.querySelector('.lb-close');
    closeBtn.addEventListener('click', closeLightbox);
    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.classList.contains('lb-stage')) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('open')) closeLightbox();
    });
    return lb;
  }

  function openLightbox(node, kind) {
    var lb = ensureLightbox();
    var content = lb.querySelector('.lb-content');
    content.className = 'lb-content lb-kind-' + kind;
    content.innerHTML = '';
    // ノードのディープクローンを追加 (元DOMを動かさない)
    var clone = node.cloneNode(true);
    // クローン側の余計な属性削除 (id 重複防止)
    clone.removeAttribute('id');
    clone.querySelectorAll('[id]').forEach(function (el) { el.removeAttribute('id'); });
    clone.classList.add('lb-cloned');
    content.appendChild(clone);
    lb.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
  }

  function closeLightbox() {
    var lb = document.getElementById('lb-overlay');
    if (!lb) return;
    lb.classList.remove('open');
    document.documentElement.style.overflow = '';
  }

  // ===== Triggers =====
  function initLightboxTriggers() {
    // タップ可能化のためのクラス付与
    document.querySelectorAll('figure.photo-figure img').forEach(function (img) {
      img.classList.add('lb-trigger');
      img.dataset.lbKind = 'image';
      img.addEventListener('click', function (e) {
        e.preventDefault();
        openLightbox(img, 'image');
      });
    });
    document.querySelectorAll('.finance-table-wrap, .finance-pl-wrap').forEach(function (wrap) {
      wrap.classList.add('lb-trigger');
      wrap.addEventListener('click', function (e) {
        // テーブル内のリンクは普通に動かす
        if (e.target.tagName === 'A') return;
        openLightbox(wrap, 'table');
      });
    });
    document.querySelectorAll('.finance-chart .chart-svg').forEach(function (svg) {
      svg.classList.add('lb-trigger');
      svg.addEventListener('click', function (e) {
        e.preventDefault();
        // figure ごとクローンしてタイトルも一緒に出す
        var fig = svg.closest('figure') || svg;
        openLightbox(fig, 'chart');
      });
    });
  }

  // 起動
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initDrawer();
      initLightboxTriggers();
    });
  } else {
    initDrawer();
    initLightboxTriggers();
  }
})();
