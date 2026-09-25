const btn = document.getElementById('langBtn');
let lang = 'pt';
function applyLanguage(){
  document.documentElement.lang = lang === 'pt' ? 'pt-BR' : 'en';
  document.querySelectorAll('[data-pt][data-en]').forEach(el=>{
    el.innerHTML = el.dataset[lang];
  });
  btn.textContent = lang === 'pt' ? '🇧🇷 PT' : '🇺🇸 EN';
}
btn.addEventListener('click', ()=>{ lang = lang === 'pt' ? 'en' : 'pt'; applyLanguage(); });
applyLanguage();


// Dynamic real catalog — no API key required.
const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#039;'}[ch]));

function catalogCard(item){
  const kind = item.type === 'series' ? 'SÉRIE' : 'FILME';
  const year = item.year ? ` · ${escapeHtml(item.year)}` : '';
  return `<article class="catalog-card">
    <a href="${escapeHtml(item.source_url || '#')}" target="_blank" rel="noopener noreferrer" class="catalog-poster-wrap" aria-label="${escapeHtml(item.title)}">
      <img class="catalog-poster" src="${escapeHtml(item.image)}" alt="${escapeHtml(item.title)}" loading="lazy">
      <span class="catalog-type">${kind}</span>
    </a>
    <div class="catalog-info"><strong>${escapeHtml(item.title)}</strong><span>${kind}${year}</span></div>
  </article>`;
}

async function loadCatalog(){
  const movieEl = document.getElementById('movieCatalog');
  const seriesEl = document.getElementById('seriesCatalog');
  const movieStatus = document.getElementById('catalogMovieStatus');
  const seriesStatus = document.getElementById('catalogSeriesStatus');
  if (!movieEl || !seriesEl) return;
  try {
    const res = await fetch('/api/catalog', {cache:'no-store'});
    if (!res.ok) throw new Error('catalog request failed');
    const data = await res.json();
    movieEl.innerHTML = data.movies?.length ? data.movies.map(catalogCard).join('') : '<div class="catalog-empty">Nenhum filme encontrado agora.</div>';
    seriesEl.innerHTML = data.series?.length ? data.series.map(catalogCard).join('') : '<div class="catalog-empty">Nenhuma série encontrada agora.</div>';
    const when = data.updated_at ? new Date(data.updated_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}) : '';
    if (movieStatus) movieStatus.textContent = when ? `Atualizado ${when}` : 'Atualizado automaticamente';
    if (seriesStatus) seriesStatus.textContent = when ? `Atualizado ${when}` : 'Atualizado automaticamente';
  } catch (err) {
    movieEl.innerHTML = '<div class="catalog-empty">Não foi possível atualizar o catálogo agora. Tente novamente em instantes.</div>';
    seriesEl.innerHTML = '<div class="catalog-empty">Não foi possível atualizar o catálogo agora. Tente novamente em instantes.</div>';
    if (movieStatus) movieStatus.textContent = 'Temporariamente indisponível';
    if (seriesStatus) seriesStatus.textContent = 'Temporariamente indisponível';
    console.warn(err);
  }
}

loadCatalog();
setInterval(loadCatalog, 30 * 60 * 1000);
