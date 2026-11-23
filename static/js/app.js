/* ═══════════════════════════════════════════════════════════════════════════
   Living Ink — Frontend Application
   Handles upload, style selection, API calls, and result display.
   ═══════════════════════════════════════════════════════════════════════════ */

;(function () {
  'use strict';

  // ---------------------------------------------------------------- DOM refs
  const $ = (s) => document.querySelector(s);
  const uploadZone    = $('#upload-zone');
  const fileInput     = $('#file-input');
  const preview       = $('#preview');
  const previewImg    = $('#preview-img');
  const previewName   = $('#preview-filename');
  const removeBtn     = $('#remove-btn');
  const styleSection  = $('#style-section');
  const styleGrid     = $('#style-grid');
  const transformBtn  = $('#transform-btn');
  const loadingSection= $('#loading-section');
  const loadingStep   = $('#loading-step');
  const resultsSection= $('#results-section');
  const resultImg     = $('#result-img');
  const compOriginal  = $('#comparison-original');
  const compBefore    = $('#comparison-before');
  const compSlider    = $('#comparison-slider');
  const compHandle    = $('#comparison-handle');
  const resultLabel   = $('#result-style-label');
  const analysisGrid  = $('#analysis-grid');
  const poetryText    = $('#poetry-text');
  const downloadBtn   = $('#download-btn');
  const tryAnotherBtn = $('#try-another-btn');
  const newImageBtn   = $('#new-image-btn');

  // ---------------------------------------------------------------- state
  let selectedFile  = null;
  let selectedStyle = 'tattoo';

  // ================================================================ UPLOAD
  // Click to upload
  uploadZone.addEventListener('click', () => fileInput.click());

  // File selected
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFile(e.target.files[0]);
  });

  // Drag & drop
  uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
  });
  uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
  });
  uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });

  function handleFile(file) {
    // Validate
    const allowed = ['image/png','image/jpeg','image/webp','image/bmp','image/tiff'];
    if (!allowed.includes(file.type)) {
      toast('Unsupported format. Use PNG, JPG, or WebP.', true);
      return;
    }
    if (file.size > 16 * 1024 * 1024) {
      toast('File too large. Max 16 MB.', true);
      return;
    }

    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (ev) => {
      previewImg.src = ev.target.result;
      previewName.textContent = file.name;
      preview.style.display = 'block';
      uploadZone.style.display = 'none';

      // Show style section
      styleSection.style.display = 'block';
      styleSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

      // Hide results if visible
      resultsSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  // Remove image
  removeBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    preview.style.display = 'none';
    uploadZone.style.display = 'block';
    styleSection.style.display = 'none';
    resultsSection.style.display = 'none';
  });

  // ================================================================ STYLE SELECTION
  styleGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.style-card');
    if (!card) return;

    // Toggle active
    styleGrid.querySelectorAll('.style-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    selectedStyle = card.dataset.style;
  });

  // ================================================================ TRANSFORM
  transformBtn.addEventListener('click', () => {
    if (!selectedFile) {
      toast('Please upload an image first.', true);
      return;
    }
    processImage();
  });

  async function processImage() {
    // Show loading
    styleSection.style.display = 'none';
    preview.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    loadingSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Animate loading steps
    const steps = [
      'Analyzing organic patterns…',
      'Extracting living geometry…',
      'Mapping flow and rhythm…',
      'Applying ink transformation…',
      'Composing poetic description…',
      'Finalizing your artwork…',
    ];
    let stepIdx = 0;
    const stepTimer = setInterval(() => {
      stepIdx = (stepIdx + 1) % steps.length;
      loadingStep.textContent = steps[stepIdx];
    }, 2200);

    // Build form data
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('style', selectedStyle);

    try {
      const res = await fetch('/api/process', { method: 'POST', body: formData });
      const data = await res.json();
      clearInterval(stepTimer);

      if (!res.ok || data.error) {
        throw new Error(data.error || 'Processing failed.');
      }

      displayResults(data);
    } catch (err) {
      clearInterval(stepTimer);
      loadingSection.style.display = 'none';
      uploadZone.style.display = 'block';
      preview.style.display = 'block';
      styleSection.style.display = 'block';
      toast(err.message || 'Something went wrong.', true);
    }
  }

  // ================================================================ RESULTS
  function displayResults(data) {
    loadingSection.style.display = 'none';

    // Set images (add cache-bust)
    const bust = '?t=' + Date.now();
    resultImg.src = data.artwork_url + bust;
    compOriginal.src = data.original_url + bust;

    // Label
    resultLabel.textContent = data.style_name;

    // Reset slider
    compSlider.value = 50;
    compBefore.style.width = '50%';
    compHandle.style.left = '50%';

    // Analysis grid
    renderAnalysis(data.analysis);

    // Poetry
    poetryText.textContent = data.poetry;

    // Download link
    const artFilename = data.artwork_url.split('/').pop();
    downloadBtn.href = '/api/download/' + artFilename;

    // Show
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderAnalysis(a) {
    const items = [
      { label: 'Dominant Patterns', value: a.dominant_patterns.join(', ') },
      { label: 'Complexity',        value: (a.complexity * 100).toFixed(0) + '%', bar: a.complexity },
      { label: 'Flow Direction',    value: a.flow_direction },
      { label: 'Density',           value: a.density },
      { label: 'Branching Score',   value: (a.branching_score * 100).toFixed(0) + '%', bar: a.branching_score },
      { label: 'Texture Frequency', value: a.texture_frequency },
      { label: 'Contour Count',     value: a.contour_count.toLocaleString() },
      { label: 'Edge Density',      value: (a.edge_density * 100).toFixed(1) + '%', bar: Math.min(a.edge_density * 5, 1) },
    ];

    analysisGrid.innerHTML = items.map(it => {
      let barHTML = '';
      if (it.bar !== undefined) {
        barHTML = `<div class="analysis-item__bar"><div class="analysis-item__bar-fill" style="width:${(it.bar * 100).toFixed(0)}%"></div></div>`;
      }
      return `
        <div class="analysis-item">
          <span class="analysis-item__label">${it.label}</span>
          <span class="analysis-item__value">${it.value}</span>
          ${barHTML}
        </div>`;
    }).join('');
  }

  // ================================================================ COMPARISON SLIDER
  compSlider.addEventListener('input', (e) => {
    const val = e.target.value;
    compBefore.style.width = val + '%';
    compHandle.style.left = val + '%';
  });

  // ================================================================ ACTION BUTTONS
  tryAnotherBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    preview.style.display = 'block';
    styleSection.style.display = 'block';
    styleSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  newImageBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    resultsSection.style.display = 'none';
    preview.style.display = 'none';
    styleSection.style.display = 'none';
    uploadZone.style.display = 'block';
    uploadZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  // ================================================================ TOAST
  function toast(message, isError = false) {
    // Remove existing
    document.querySelectorAll('.toast').forEach(t => t.remove());

    const el = document.createElement('div');
    el.className = 'toast' + (isError ? ' error' : '');
    el.textContent = message;
    document.body.appendChild(el);

    requestAnimationFrame(() => {
      requestAnimationFrame(() => el.classList.add('show'));
    });

    setTimeout(() => {
      el.classList.remove('show');
      setTimeout(() => el.remove(), 400);
    }, 3500);
  }

})();
