/**
 * SentimentPulse - Multi-Category Review Analytics Platform
 * Advanced Interactive Controller & NLP Visualizer
 */

// Application State
const state = {
  category: "all",
  view: "dashboard", // "dashboard" or "admin"
  sentimentFilter: "all",
  ratingFilter: 0,
  searchQuery: "",
  sortBy: "newest",
  selectedTopic: null,
  offset: 0,
  limit: 20,
  totalReviews: 0,
  selectedModalRating: 5,
  upvotedIds: new Set()
};

// Chart instances
let doughnutChart = null;
let trendChart = null;
let adminBarChart = null;
let adminStackChart = null;

// Category metadata
const CATEGORY_META = {
  all: { name: "All Categories", desc: "Cross-industry consumer sentiment analysis, keyword extractions, and temporal trends.", icon: "layers" },
  products: { name: "Products & Electronics", desc: "Consumer hardware, gadgets, peripherals, and smart devices.", icon: "package" },
  restaurants: { name: "Restaurants & Dining", desc: "Culinary dining experiences, cafes, bistros, and street gastronomy.", icon: "utensils" },
  movies: { name: "Movies & Cinema", desc: "Theatrical blockbusters, indie cinema, streaming features, and reviews.", icon: "film" },
  "mobile-apps": { name: "Mobile Applications", desc: "iOS and Android apps across productivity, finance, health, and utilities.", icon: "smartphone" }
};

// ----------------- Initialization -----------------
document.addEventListener("DOMContentLoaded", () => {
  initLucide();
  setupEventListeners();
  loadCategoryCounts();
  loadCurrentView();
});

function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Fetch Category Counts for Ribbon Badges
async function loadCategoryCounts() {
  try {
    const res = await fetch("/api/categories");
    if (!res.ok) return;
    const data = await res.json();
    let total = 0;
    data.categories.forEach(c => {
      total += c.review_count;
      if (c.slug === "products") document.getElementById("badgeCatProducts").textContent = c.review_count;
      if (c.slug === "restaurants") document.getElementById("badgeCatRestaurants").textContent = c.review_count;
      if (c.slug === "movies") document.getElementById("badgeCatMovies").textContent = c.review_count;
      if (c.slug === "mobile-apps") document.getElementById("badgeCatApps").textContent = c.review_count;
    });
    document.getElementById("badgeCatAll").textContent = total;
  } catch (err) {
    console.error("Error loading category counts:", err);
  }
}

// ----------------- Event Handlers -----------------
function setupEventListeners() {
  // Category tabs navigation
  document.querySelectorAll(".cat-nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-nav-btn").forEach(b => {
        b.classList.remove("active", "bg-indigo-600", "text-white", "shadow-md");
        b.classList.add("text-slate-300");
      });
      btn.classList.add("active", "bg-indigo-600", "text-white", "shadow-md");
      btn.classList.remove("text-slate-300");

      state.category = btn.getAttribute("data-cat");
      state.offset = 0;
      state.selectedTopic = null;
      hideActiveFilter();

      if (state.view === "admin") {
        switchView("dashboard");
      } else {
        loadCategoryDashboard();
      }
    });
  });

  // View toggle tabs (Dashboard vs Admin)
  document.getElementById("viewCategoryTab").addEventListener("click", () => switchView("dashboard"));
  document.getElementById("viewAdminTab").addEventListener("click", () => switchView("admin"));

  // Sentiment Filter buttons
  document.querySelectorAll(".sent-filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".sent-filter-btn").forEach(b => {
        b.classList.remove("active", "bg-dark-700", "text-white");
        b.classList.add("text-slate-400");
      });
      btn.classList.add("active", "bg-dark-700", "text-white");
      btn.classList.remove("text-slate-400");

      state.sentimentFilter = btn.getAttribute("data-sent");
      state.offset = 0;
      loadReviews();
    });
  });

  // Rating Filter select
  document.getElementById("ratingFilterSelect").addEventListener("change", (e) => {
    state.ratingFilter = parseInt(e.target.value) || 0;
    state.offset = 0;
    loadReviews();
  });

  // Sort By select
  document.getElementById("sortBySelect").addEventListener("change", (e) => {
    state.sortBy = e.target.value;
    state.offset = 0;
    loadReviews();
  });

  // Search input with debounce
  let searchTimeout = null;
  document.getElementById("reviewSearchInput").addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.searchQuery = e.target.value.trim();
      state.offset = 0;
      loadReviews();
    }, 300);
  });

  // Clear Active Topic filter
  document.getElementById("clearTopicFilterBtn").addEventListener("click", clearTopicFilter);
  document.getElementById("resetActiveFilterBtn").addEventListener("click", clearTopicFilter);

  // Pagination buttons
  document.getElementById("prevPageBtn").addEventListener("click", () => {
    if (state.offset > 0) {
      state.offset = Math.max(0, state.offset - state.limit);
      loadReviews();
      document.getElementById("reviewsGridContainer").scrollIntoView({ behavior: "smooth" });
    }
  });

  document.getElementById("nextPageBtn").addEventListener("click", () => {
    if (state.offset + state.limit < state.totalReviews) {
      state.offset += state.limit;
      loadReviews();
      document.getElementById("reviewsGridContainer").scrollIntoView({ behavior: "smooth" });
    }
  });

  // Reset database button
  document.getElementById("resetDataBtn").addEventListener("click", async () => {
    if (confirm("Reset database and re-seed with authentic college project mock reviews?")) {
      try {
        const res = await fetch("/api/reset-data", { method: "POST" });
        const data = await res.json();
        showToast(data.message || "Database reset successfully!", "check");
        loadCategoryCounts();
        loadCurrentView();
      } catch (err) {
        showToast("Failed to reset database", "alert-circle");
      }
    }
  });

  // Modal interactions
  const modal = document.getElementById("reviewModal");
  document.getElementById("openReviewModalBtn").addEventListener("click", () => {
    modal.classList.remove("hidden");
    document.getElementById("modalCategory").value = state.category !== "all" ? state.category : "products";
    resetLiveSentiment();
  });

  document.getElementById("closeReviewModalBtn").addEventListener("click", () => modal.classList.add("hidden"));
  document.getElementById("cancelModalBtn").addEventListener("click", () => modal.classList.add("hidden"));

  // Interactive Star Rating in Modal
  document.querySelectorAll(".star-btn").forEach(star => {
    star.addEventListener("click", (e) => {
      const rating = parseInt(e.currentTarget.getAttribute("data-star"));
      setModalRating(rating);
    });
  });

  // Quick Demo Presets in Modal
  document.getElementById("demoPositiveBtn").addEventListener("click", () => {
    document.getElementById("modalItemName").value = "Bose QuietComfort Ultra";
    document.getElementById("modalUsername").value = "David Miller";
    document.getElementById("modalTitle").value = "Absolute masterclass in comfort and audio isolation";
    document.getElementById("modalText").value = "The active noise cancellation is pure magic. Soundstage is wide, battery life easily lasts for days, and the build quality is durable and lightweight.";
    setModalRating(5);
    runLiveNlpAnalysis();
  });

  document.getElementById("demoCriticalBtn").addEventListener("click", () => {
    document.getElementById("modalItemName").value = "SmartClean Robot Vac";
    document.getElementById("modalUsername").value = "Sarah Jenkins";
    document.getElementById("modalTitle").value = "Frequent crashes, terrible battery life and app bugs";
    document.getElementById("modalText").value = "Extremely frustrating device. It constantly disconnects from WiFi, loses stored room maps, and customer service refused to honor the warranty.";
    setModalRating(1);
    runLiveNlpAnalysis();
  });

  // Live NLP Preview typing handlers
  let liveNlpTimeout = null;
  const triggerLiveNlp = () => {
    clearTimeout(liveNlpTimeout);
    liveNlpTimeout = setTimeout(runLiveNlpAnalysis, 200);
  };
  document.getElementById("modalTitle").addEventListener("input", triggerLiveNlp);
  document.getElementById("modalText").addEventListener("input", triggerLiveNlp);

  // Form submission
  document.getElementById("reviewForm").addEventListener("submit", handleReviewSubmit);
}

function switchView(viewName) {
  state.view = viewName;
  const dashBtn = document.getElementById("viewCategoryTab");
  const adminBtn = document.getElementById("viewAdminTab");
  const dashView = document.getElementById("categoryDashboardView");
  const adminView = document.getElementById("adminOverviewView");

  if (viewName === "admin") {
    adminBtn.classList.add("active", "bg-dark-700", "text-white");
    adminBtn.classList.remove("text-slate-400");
    dashBtn.classList.remove("active", "bg-dark-700", "text-white");
    dashBtn.classList.add("text-slate-400");

    dashView.classList.add("hidden");
    adminView.classList.remove("hidden");
    loadAdminDashboard();
  } else {
    dashBtn.classList.add("active", "bg-dark-700", "text-white");
    dashBtn.classList.remove("text-slate-400");
    adminBtn.classList.remove("active", "bg-dark-700", "text-white");
    adminBtn.classList.add("text-slate-400");

    adminView.classList.add("hidden");
    dashView.classList.remove("hidden");
    loadCategoryDashboard();
  }
  initLucide();
}

function loadCurrentView() {
  if (state.view === "admin") {
    loadAdminDashboard();
  } else {
    loadCategoryDashboard();
  }
}

// ----------------- Category Dashboard Loader -----------------
async function loadCategoryDashboard() {
  updateCategoryHeader();
  await Promise.all([
    fetchCategoryAnalytics(),
    loadReviews()
  ]);
}

function updateCategoryHeader() {
  const meta = CATEGORY_META[state.category] || CATEGORY_META["all"];
  document.getElementById("currentCatTitle").textContent = meta.name;
  document.getElementById("currentCatDesc").textContent = meta.desc;

  const iconElem = document.getElementById("currentCatIcon");
  iconElem.setAttribute("data-lucide", meta.icon);
  initLucide();
}

async function fetchCategoryAnalytics() {
  try {
    const res = await fetch(`/api/analytics/category/${state.category}`);
    if (!res.ok) throw new Error("Analytics fetch failed");
    const data = await res.json();

    // 1. Update KPI Cards & Speedometer Needle
    renderKPIs(data.summary, data.sentiment_distribution);

    // 2. Render Sentiment Doughnut Chart
    renderSentimentDoughnut(data.sentiment_distribution);

    // 3. Render Sentiment Trend Chart
    renderSentimentTrend(data.trend);

    // 4. Render Dynamic Word Cloud
    renderWordCloud(data.topics || []);

    // 5. Render Rating Distribution Bars
    renderRatingBars(data.rating_distribution);

  } catch (err) {
    console.error("Error loading category analytics:", err);
  }
}

function renderKPIs(summary, dist) {
  if (!summary) return;

  // Total Reviews
  document.getElementById("kpiTotalReviews").textContent = Number(summary.total_reviews || 0).toLocaleString();

  // Compound Score & Badge & Speedometer Needle
  const compound = summary.avg_sentiment !== null ? summary.avg_sentiment : 0;
  const compoundElem = document.getElementById("kpiAvgCompound");
  const compoundBadge = document.getElementById("kpiCompoundBadge");
  const needle = document.getElementById("speedometerNeedle");

  compoundElem.textContent = (compound >= 0 ? "+" : "") + compound.toFixed(3);

  // Speedometer rotation: -1.0 -> -75deg, 0.0 -> 0deg, +1.0 -> +75deg
  const angle = Math.min(75, Math.max(-75, compound * 75));
  if (needle) {
    needle.style.transform = `rotate(${angle}deg)`;
  }

  if (compound >= 0.05) {
    compoundElem.className = "text-3xl font-extrabold tracking-tight text-emerald-400";
    compoundBadge.className = "text-xs px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider badge-positive";
    compoundBadge.textContent = "Positive (Favorable)";
  } else if (compound <= -0.05) {
    compoundElem.className = "text-3xl font-extrabold tracking-tight text-rose-400";
    compoundBadge.className = "text-xs px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider badge-negative";
    compoundBadge.textContent = "Critical (Unfavorable)";
  } else {
    compoundElem.className = "text-3xl font-extrabold tracking-tight text-amber-400";
    compoundBadge.className = "text-xs px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider badge-neutral";
    compoundBadge.textContent = "Neutral Sentiment";
  }

  // Positive Ratio & Mini Stacked Progress Bar
  const pcts = dist ? dist.percentages : { positive: 0, neutral: 0, negative: 0 };
  document.getElementById("kpiPosRatio").textContent = `${pcts.positive}%`;
  document.getElementById("kpiBarPos").style.width = `${pcts.positive}%`;
  document.getElementById("kpiBarNeu").style.width = `${pcts.neutral}%`;
  document.getElementById("kpiBarNeg").style.width = `${pcts.negative}%`;

  // Average Star Rating
  const avgRating = summary.avg_rating !== null ? summary.avg_rating : 0;
  document.getElementById("kpiAvgRating").textContent = avgRating.toFixed(1);
  renderStarRatingDisplay(avgRating);
}

function renderStarRatingDisplay(rating) {
  const container = document.getElementById("kpiStarsRow");
  container.innerHTML = "";
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rating)) {
      container.innerHTML += `<i data-lucide="star" class="w-4 h-4 fill-amber-400 text-amber-400"></i>`;
    } else if (i - rating <= 0.5) {
      container.innerHTML += `<i data-lucide="star-half" class="w-4 h-4 fill-amber-400 text-amber-400"></i>`;
    } else {
      container.innerHTML += `<i data-lucide="star" class="w-4 h-4 text-slate-700"></i>`;
    }
  }
  initLucide();
}

function renderSentimentDoughnut(dist) {
  const ctx = document.getElementById("sentimentDoughnutChart").getContext("2d");
  const counts = dist ? dist.counts : { positive: 0, neutral: 0, negative: 0 };
  const pcts = dist ? dist.percentages : { positive: 0, neutral: 0, negative: 0 };

  document.getElementById("doughnutCenterPct").textContent = `${pcts.positive}%`;
  document.getElementById("distPosCount").textContent = counts.positive;
  document.getElementById("distPosPct").textContent = `${pcts.positive}%`;
  document.getElementById("distNeuCount").textContent = counts.neutral;
  document.getElementById("distNeuPct").textContent = `${pcts.neutral}%`;
  document.getElementById("distNegCount").textContent = counts.negative;
  document.getElementById("distNegPct").textContent = `${pcts.negative}%`;

  if (doughnutChart) {
    doughnutChart.destroy();
  }

  doughnutChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [{
        data: [counts.positive, counts.neutral, counts.negative],
        backgroundColor: [
          "#10b981", // Emerald
          "#f59e0b", // Amber
          "#f43f5e"  // Rose
        ],
        borderColor: "#070a12",
        borderWidth: 4,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "75%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.95)",
          titleColor: "#fff",
          bodyColor: "#cbd5e1",
          borderColor: "rgba(255, 255, 255, 0.1)",
          borderWidth: 1,
          padding: 12,
          boxPadding: 4,
          usePointStyle: true,
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const val = context.raw;
              const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
              return ` ${context.label}: ${val} reviews (${pct}%)`;
            }
          }
        }
      }
    }
  });
}

function renderSentimentTrend(trends) {
  const ctx = document.getElementById("sentimentTrendChart").getContext("2d");

  if (!trends || trends.length === 0) {
    if (trendChart) trendChart.destroy();
    return;
  }

  const labels = trends.map(t => {
    const d = new Date(t.date_label);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  });

  const sentimentData = trends.map(t => t.avg_sentiment);
  const volumeData = trends.map(t => t.volume);

  if (trendChart) {
    trendChart.destroy();
  }

  // Smooth gradient fill
  const gradient = ctx.createLinearGradient(0, 0, 0, 260);
  gradient.addColorStop(0, "rgba(99, 102, 241, 0.45)");
  gradient.addColorStop(1, "rgba(99, 102, 241, 0.0)");

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Sentiment Compound Score",
          data: sentimentData,
          borderColor: "#6366f1",
          backgroundColor: gradient,
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointBackgroundColor: "#818cf8",
          pointBorderColor: "#070a12",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 7,
          yAxisID: "y"
        },
        {
          label: "Review Volume",
          data: volumeData,
          type: "bar",
          backgroundColor: "rgba(168, 85, 247, 0.28)",
          hoverBackgroundColor: "rgba(168, 85, 247, 0.5)",
          borderRadius: 6,
          borderWidth: 0,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.95)",
          titleColor: "#fff",
          bodyColor: "#cbd5e1",
          borderColor: "rgba(99, 102, 241, 0.3)",
          borderWidth: 1,
          padding: 12
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: { color: "#64748b", font: { size: 11, family: "JetBrains Mono" } }
        },
        y: {
          type: "linear",
          position: "left",
          min: -1.0,
          max: 1.0,
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: {
            color: "#818cf8",
            font: { size: 10, family: "JetBrains Mono" },
            callback: value => (value > 0 ? `+${value.toFixed(1)}` : value.toFixed(1))
          }
        },
        y1: {
          type: "linear",
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: { color: "#c084fc", font: { size: 10, family: "JetBrains Mono" }, stepSize: 5 }
        }
      }
    }
  });
}

// Render Sized & Scented Dynamic Word Cloud
function renderWordCloud(topics) {
  const container = document.getElementById("wordCloudContainer");
  container.innerHTML = "";

  if (!topics || topics.length === 0) {
    container.innerHTML = `<span class="text-xs text-slate-500 italic">No dominant topics extracted for this vertical yet.</span>`;
    return;
  }

  // Find max and min TF-IDF for scaling font size
  const maxScore = Math.max(...topics.map(t => t.tfidf_score || 1));
  const minScore = Math.min(...topics.map(t => t.tfidf_score || 1));
  const range = Math.max(1, maxScore - minScore);

  topics.forEach(t => {
    const isPositive = t.orientation === "positive";
    const isNegative = t.orientation === "negative";

    // Normalized weight 0 to 1
    const norm = (t.tfidf_score - minScore) / range;
    // Font size from 12px to 24px
    const fontSize = 12 + Math.round(norm * 12);
    const fontWeight = norm > 0.6 ? "font-extrabold" : (norm > 0.3 ? "font-bold" : "font-medium");

    let colorStyle = "bg-slate-800/80 text-slate-200 border-slate-700 hover:border-slate-500";
    let badgeClass = "text-slate-400 bg-slate-900";

    if (isPositive) {
      colorStyle = "bg-emerald-950/40 text-emerald-300 border-emerald-500/30 hover:border-emerald-400 hover:bg-emerald-950/60";
      badgeClass = "text-emerald-400 bg-emerald-500/20";
    } else if (isNegative) {
      colorStyle = "bg-rose-950/40 text-rose-300 border-rose-500/30 hover:border-rose-400 hover:bg-rose-950/60";
      badgeClass = "text-rose-400 bg-rose-500/20";
    }

    const isActive = state.selectedTopic === t.keyword;
    if (isActive) {
      colorStyle += " ring-2 ring-indigo-400 border-indigo-400 scale-105";
    }

    const tag = document.createElement("button");
    tag.className = `word-cloud-tag px-3 py-1.5 rounded-xl border flex items-center gap-1.5 transition-all shadow-sm ${colorStyle} ${fontWeight}`;
    tag.style.fontSize = `${fontSize}px`;
    tag.title = `Topic: ${t.keyword} | Frequency: ${t.frequency} reviews | TF-IDF: ${t.tfidf_score} | Sentiment: ${t.avg_sentiment >= 0 ? '+' : ''}${t.avg_sentiment}`;

    tag.innerHTML = `
      <span>${escapeHtml(t.keyword)}</span>
      <span class="text-[10px] px-1.5 py-0.5 rounded-md font-mono ${badgeClass}">${t.frequency}</span>
    `;

    tag.addEventListener("click", () => {
      if (state.selectedTopic === t.keyword) {
        clearTopicFilter();
      } else {
        applyTopicFilter(t.keyword);
      }
    });

    container.appendChild(tag);
  });
}

function applyTopicFilter(keyword) {
  state.selectedTopic = keyword;
  state.searchQuery = keyword;
  document.getElementById("reviewSearchInput").value = keyword;

  const banner = document.getElementById("activeFilterBanner");
  document.getElementById("activeFilterLabel").textContent = `Filtered by topic: "${keyword}"`;
  banner.classList.remove("hidden");
  document.getElementById("clearTopicFilterBtn").classList.remove("hidden");

  state.offset = 0;
  loadReviews();
  fetchCategoryAnalytics();
}

function clearTopicFilter() {
  state.selectedTopic = null;
  state.searchQuery = "";
  document.getElementById("reviewSearchInput").value = "";
  hideActiveFilter();
  state.offset = 0;
  loadReviews();
  fetchCategoryAnalytics();
}

function hideActiveFilter() {
  document.getElementById("activeFilterBanner").classList.add("hidden");
  document.getElementById("clearTopicFilterBtn").classList.add("hidden");
}

function renderRatingBars(ratings) {
  const container = document.getElementById("ratingBarsContainer");
  container.innerHTML = "";

  const total = Object.values(ratings || {}).reduce((a, b) => a + b, 0);

  for (let star = 5; star >= 1; star--) {
    const count = ratings && ratings[star] ? ratings[star] : 0;
    const pct = total > 0 ? ((count / total) * 100).toFixed(0) : 0;

    const row = document.createElement("div");
    row.className = "flex items-center space-x-2 text-xs";
    row.innerHTML = `
      <span class="w-9 text-slate-300 font-mono font-bold flex items-center">${star} <i data-lucide="star" class="w-3 h-3 text-amber-400 fill-amber-400 ml-1"></i></span>
      <div class="flex-1 bg-dark-950 rounded-full h-2.5 overflow-hidden border border-slate-800">
        <div class="bg-gradient-to-r from-amber-500 to-amber-400 h-2.5 rounded-full transition-all duration-500" style="width: ${pct}%"></div>
      </div>
      <span class="w-10 text-right text-slate-400 font-mono text-[11px] font-semibold">${count}</span>
    `;
    container.appendChild(row);
  }
  initLucide();
}

// ----------------- Reviews Explorer Loader -----------------
async function loadReviews() {
  const container = document.getElementById("reviewsGridContainer");
  container.innerHTML = `
    <div class="col-span-full py-12 text-center text-slate-500 flex flex-col items-center justify-center space-y-2">
      <div class="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      <span class="text-xs">Querying reviews repository...</span>
    </div>
  `;

  try {
    const params = new URLSearchParams({
      category: state.category,
      sentiment: state.sentimentFilter,
      rating: state.ratingFilter,
      sort_by: state.sortBy,
      limit: state.limit,
      offset: state.offset
    });

    if (state.searchQuery) {
      params.append("search", state.searchQuery);
    }

    const res = await fetch(`/api/reviews?${params.toString()}`);
    if (!res.ok) throw new Error("Reviews fetch failed");
    const data = await res.json();

    state.totalReviews = data.total;
    document.getElementById("reviewsCountBadge").textContent = data.total;

    // Pagination info
    const start = data.total > 0 ? state.offset + 1 : 0;
    const end = Math.min(state.offset + state.limit, data.total);
    document.getElementById("paginationInfo").textContent = `Showing ${start} - ${end} of ${data.total} reviews`;
    document.getElementById("prevPageBtn").disabled = state.offset === 0;
    document.getElementById("nextPageBtn").disabled = end >= data.total;

    renderReviewsList(data.reviews);

  } catch (err) {
    container.innerHTML = `
      <div class="col-span-full py-8 text-center text-rose-400 text-xs">
        Failed to load reviews. Please verify backend connection.
      </div>
    `;
  }
}

function renderReviewsList(reviews) {
  const container = document.getElementById("reviewsGridContainer");
  container.innerHTML = "";

  if (!reviews || reviews.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-500 glass-card rounded-2xl flex flex-col items-center space-y-2">
        <i data-lucide="inbox" class="w-8 h-8 text-slate-600"></i>
        <p class="text-sm font-semibold text-slate-300">No reviews found matching current filter.</p>
        <p class="text-xs text-slate-500">Try changing keywords or clearing the sentiment filter.</p>
      </div>
    `;
    initLucide();
    return;
  }

  reviews.forEach(rev => {
    const card = document.createElement("div");
    
    // Determine card border & badge
    let cardBorder = "card-border-neu";
    let badgeClass = "badge-neutral";
    let badgeText = "Neutral";
    if (rev.sentiment_label === "positive") {
      cardBorder = "card-border-pos";
      badgeClass = "badge-positive";
      badgeText = "Positive";
    } else if (rev.sentiment_label === "negative") {
      cardBorder = "card-border-neg";
      badgeClass = "badge-negative";
      badgeText = "Critical";
    }

    card.className = `glass-card glass-card-interactive rounded-2xl p-5 flex flex-col justify-between space-y-3.5 border border-slate-800 ${cardBorder}`;

    // Stars HTML
    let starsHtml = "";
    for (let i = 1; i <= 5; i++) {
      if (i <= rev.rating) {
        starsHtml += `<i data-lucide="star" class="w-3.5 h-3.5 fill-amber-400 text-amber-400"></i>`;
      } else {
        starsHtml += `<i data-lucide="star" class="w-3.5 h-3.5 text-slate-700"></i>`;
      }
    }

    const dateStr = new Date(rev.created_at).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric"
    });

    const compoundScore = rev.compound_score !== null ? (rev.compound_score >= 0 ? `+${rev.compound_score.toFixed(3)}` : rev.compound_score.toFixed(3)) : "0.000";

    const posPct = Math.round(rev.pos_score * 100);
    const neuPct = Math.round(rev.neu_score * 100);
    const negPct = Math.round(rev.neg_score * 100);

    const isUpvoted = state.upvotedIds.has(rev.id);

    card.innerHTML = `
      <div>
        <!-- Card Header -->
        <div class="flex items-start justify-between gap-2">
          <div>
            <div class="flex items-center space-x-2">
              <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md bg-dark-950 text-indigo-400 border border-indigo-500/25">
                ${escapeHtml(rev.category_name)}
              </span>
              <span class="text-xs font-bold text-slate-300">&bull; ${escapeHtml(rev.item_name)}</span>
            </div>
            <h3 class="text-sm font-bold text-white mt-1.5 leading-snug">${escapeHtml(rev.title)}</h3>
          </div>

          <!-- Sentiment Badge -->
          <div class="flex flex-col items-end shrink-0">
            <span class="px-2.5 py-1 rounded-lg text-xs font-extrabold ${badgeClass}">
              ${badgeText}
            </span>
            <span class="text-[10px] font-mono text-slate-400 mt-1 font-bold">
              ${compoundScore}
            </span>
          </div>
        </div>

        <!-- Rating & Date -->
        <div class="flex items-center space-x-2.5 mt-2 text-xs">
          <div class="flex items-center space-x-0.5">${starsHtml}</div>
          <span class="text-slate-600">&bull;</span>
          <span class="text-slate-400 text-[11px] font-medium">${dateStr}</span>
        </div>

        <!-- Review Body -->
        <p class="text-xs text-slate-300 leading-relaxed mt-2.5 line-clamp-3">
          ${escapeHtml(rev.text)}
        </p>
      </div>

      <!-- Card Footer: Sub-scores bar & Upvote button -->
      <div class="pt-3 border-t border-slate-800/80 space-y-2.5">
        <!-- Micro Sentiment Bar -->
        <div class="flex items-center justify-between text-[10px] text-slate-400 font-mono">
          <span>VADER Sub-scores:</span>
          <span>Pos ${posPct}% | Neu ${neuPct}% | Neg ${negPct}%</span>
        </div>
        <div class="micro-sentiment-bar" title="Positive: ${posPct}%, Neutral: ${neuPct}%, Negative: ${negPct}%">
          <div style="width: ${posPct}%; background: #10b981;"></div>
          <div style="width: ${neuPct}%; background: #f59e0b;"></div>
          <div style="width: ${negPct}%; background: #f43f5e;"></div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 pt-1">
          <div class="flex items-center space-x-2">
            <div class="w-6 h-6 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-[10px] font-bold text-white uppercase shadow-sm">
              ${rev.username ? rev.username.substring(0, 2) : "CU"}
            </div>
            <span class="font-medium text-slate-300">${escapeHtml(rev.username || "Verified Customer")}</span>
          </div>

          <!-- Interactive Upvote Button -->
          <button class="upvote-btn flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-dark-950 hover:bg-dark-800 border border-slate-800 text-[11px] font-semibold transition ${isUpvoted ? 'upvoted' : ''}" data-review-id="${rev.id}">
            <i data-lucide="thumbs-up" class="w-3.5 h-3.5"></i>
            <span class="helpful-counter">${rev.helpful_count || 0}</span>
          </button>
        </div>
      </div>
    `;

    // Attach upvote click handler
    const upBtn = card.querySelector(".upvote-btn");
    upBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const rid = rev.id;
      if (state.upvotedIds.has(rid)) return;

      try {
        const res = await fetch(`/api/reviews/${rid}/helpful`, { method: "POST" });
        if (res.ok) {
          const resData = await res.json();
          state.upvotedIds.add(rid);
          upBtn.classList.add("upvoted");
          upBtn.querySelector(".helpful-counter").textContent = resData.helpful_count;
        }
      } catch (err) {
        console.error("Upvote failed:", err);
      }
    });

    container.appendChild(card);
  });

  initLucide();
}

// ----------------- Admin Executive View Loader -----------------
async function loadAdminDashboard() {
  try {
    const res = await fetch("/api/analytics/cross-category");
    if (!res.ok) throw new Error("Failed to fetch cross-category stats");
    const data = await res.json();

    const overall = data.overall || {};
    document.getElementById("adminTotalUsers").textContent = Number(overall.total_users || 0).toLocaleString();
    document.getElementById("adminTotalReviews").textContent = Number(overall.total_reviews || 0).toLocaleString();
    const platSent = overall.platform_avg_sentiment !== null ? overall.platform_avg_sentiment : 0;
    document.getElementById("adminPlatformSentiment").textContent = (platSent >= 0 ? "+" : "") + platSent.toFixed(3);

    renderAdminBarChart(data.categories || []);
    renderAdminStackChart(data.categories || []);
    renderAdminTable(data.categories || []);

  } catch (err) {
    console.error("Admin overview error:", err);
  }
}

function renderAdminBarChart(categories) {
  const ctx = document.getElementById("adminComparisonBarChart").getContext("2d");
  const labels = categories.map(c => c.name);
  const sentiments = categories.map(c => c.avg_sentiment);
  const ratings = categories.map(c => c.avg_rating);

  if (adminBarChart) {
    adminBarChart.destroy();
  }

  adminBarChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Sentiment Compound Score (-1 to +1)",
          data: sentiments,
          backgroundColor: "rgba(99, 102, 241, 0.85)",
          hoverBackgroundColor: "rgba(99, 102, 241, 1)",
          borderRadius: 8,
          yAxisID: "y"
        },
        {
          label: "Customer Rating (1 to 5★)",
          data: ratings,
          backgroundColor: "rgba(245, 158, 11, 0.85)",
          hoverBackgroundColor: "rgba(245, 158, 11, 1)",
          borderRadius: 8,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: { color: "#cbd5e1", font: { size: 11, weight: "bold" } }
        },
        y: {
          type: "linear",
          position: "left",
          min: -1.0,
          max: 1.0,
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: { color: "#818cf8", font: { family: "JetBrains Mono" } }
        },
        y1: {
          type: "linear",
          position: "right",
          min: 0,
          max: 5,
          grid: { drawOnChartArea: false },
          ticks: { color: "#fbbf24", font: { family: "JetBrains Mono" } }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#cbd5e1", font: { size: 11 } }
        }
      }
    }
  });
}

function renderAdminStackChart(categories) {
  const ctx = document.getElementById("adminSentimentStackChart").getContext("2d");
  const labels = categories.map(c => c.name);
  const posCounts = categories.map(c => c.positive_count);
  const neuCounts = categories.map(c => c.neutral_count);
  const negCounts = categories.map(c => c.negative_count);

  if (adminStackChart) {
    adminStackChart.destroy();
  }

  adminStackChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Positive",
          data: posCounts,
          backgroundColor: "#10b981",
          borderRadius: 6
        },
        {
          label: "Neutral",
          data: neuCounts,
          backgroundColor: "#f59e0b",
          borderRadius: 6
        },
        {
          label: "Negative",
          data: negCounts,
          backgroundColor: "#f43f5e",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true,
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: { color: "#cbd5e1", font: { size: 10 } }
        },
        y: {
          stacked: true,
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: { color: "#64748b" }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#cbd5e1", font: { size: 11 } }
        }
      }
    }
  });
}

function renderAdminTable(categories) {
  const tbody = document.getElementById("adminTableBody");
  tbody.innerHTML = "";

  categories.forEach(c => {
    const row = document.createElement("tr");
    row.className = "hover:bg-dark-900/40 transition";

    let grade = "B";
    let gradeBadge = "bg-amber-500/10 text-amber-400 border-amber-500/20";
    if (c.avg_sentiment >= 0.30) {
      grade = "A+ (Outstanding)";
      gradeBadge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
    } else if (c.avg_sentiment >= 0.18) {
      grade = "A (Strong)";
      gradeBadge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
    } else if (c.avg_sentiment >= 0.05) {
      grade = "B (Satisfactory)";
      gradeBadge = "bg-blue-500/10 text-blue-400 border-blue-500/20";
    } else {
      grade = "C (Action Required)";
      gradeBadge = "bg-rose-500/10 text-rose-400 border-rose-500/20";
    }

    const compStr = c.avg_sentiment !== null ? (c.avg_sentiment >= 0 ? `+${c.avg_sentiment.toFixed(3)}` : c.avg_sentiment.toFixed(3)) : "0.000";

    row.innerHTML = `
      <td class="py-3 px-4 flex items-center space-x-2 font-bold text-white">
        <i data-lucide="${escapeHtml(c.icon || 'layers')}" class="w-4 h-4 text-indigo-400"></i>
        <span>${escapeHtml(c.name)}</span>
      </td>
      <td class="py-3 px-4 font-mono text-slate-300 font-semibold">${c.total_reviews}</td>
      <td class="py-3 px-4 text-amber-400 font-bold font-mono">${c.avg_rating ? c.avg_rating.toFixed(2) : "0.00"} ★</td>
      <td class="py-3 px-4 font-mono font-extrabold ${c.avg_sentiment >= 0 ? 'text-emerald-400' : 'text-rose-400'}">${compStr}</td>
      <td class="py-3 px-4 text-emerald-400 font-mono font-bold">${c.positive_pct}%</td>
      <td class="py-3 px-4 text-rose-400 font-mono font-bold">${c.negative_pct}%</td>
      <td class="py-3 px-4">
        <span class="px-2.5 py-1 rounded-full text-[11px] font-extrabold border ${gradeBadge}">
          ${grade}
        </span>
      </td>
    `;
    tbody.appendChild(row);
  });
  initLucide();
}

// ----------------- Live NLP Scoring for Modal -----------------
async function runLiveNlpAnalysis() {
  const title = document.getElementById("modalTitle").value.trim();
  const text = document.getElementById("modalText").value.trim();
  const combined = `${title}. ${text}`.trim();

  if (!combined) {
    resetLiveSentiment();
    return;
  }

  try {
    const res = await fetch("/api/nlp/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: combined })
    });
    if (!res.ok) return;
    const data = await res.json();

    const valElem = document.getElementById("liveCompoundValue");
    const badge = document.getElementById("liveSentimentBadge");
    const bar = document.getElementById("liveMeterBar");
    const cuesContainer = document.getElementById("liveCuesContainer");

    const compound = data.compound;
    valElem.textContent = (compound >= 0 ? "+" : "") + compound.toFixed(3);

    const pct = Math.min(100, Math.max(0, ((compound + 1) / 2) * 100));
    bar.style.width = `${pct}%`;

    if (data.label === "positive") {
      badge.textContent = `Positive (${(data.pos * 100).toFixed(0)}%)`;
      badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
      bar.className = "h-2.5 rounded-full bg-emerald-400 transition-all duration-300";
    } else if (data.label === "negative") {
      badge.textContent = `Negative (${(data.neg * 100).toFixed(0)}%)`;
      badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/30";
      bar.className = "h-2.5 rounded-full bg-rose-400 transition-all duration-300";
    } else {
      badge.textContent = `Neutral (${(data.neu * 100).toFixed(0)}%)`;
      badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/20 text-amber-400 border border-amber-500/30";
      bar.className = "h-2.5 rounded-full bg-amber-400 transition-all duration-300";
    }

    cuesContainer.innerHTML = "";
    if (data.sentiment_cues && data.sentiment_cues.length > 0) {
      data.sentiment_cues.forEach(cue => {
        const span = document.createElement("span");
        const isPos = cue.type === "positive";
        span.className = `text-[10px] px-2 py-0.5 rounded-md font-mono font-bold ${isPos ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/15 text-rose-300 border border-rose-500/30'}`;
        span.textContent = `${cue.word} (${cue.valence > 0 ? '+' : ''}${cue.valence.toFixed(1)})`;
        cuesContainer.appendChild(span);
      });
    } else {
      cuesContainer.innerHTML = `<span class="text-slate-500 text-[10px] italic">No prominent emotional valence keywords detected yet.</span>`;
    }

  } catch (err) {
    console.error("Live NLP error:", err);
  }
}

function resetLiveSentiment() {
  document.getElementById("liveCompoundValue").textContent = "0.000";
  document.getElementById("liveSentimentBadge").textContent = "Awaiting input...";
  document.getElementById("liveSentimentBadge").className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 border border-slate-700";
  document.getElementById("liveMeterBar").style.width = "50%";
  document.getElementById("liveMeterBar").className = "h-2.5 rounded-full bg-indigo-500 transition-all duration-300";
  document.getElementById("liveCuesContainer").innerHTML = `<span class="text-slate-600 italic">Type words like "excellent", "flawless", "laggy", "crashed", or "delicious"...</span>`;
}

function setModalRating(val) {
  state.selectedModalRating = val;
  document.getElementById("modalRating").value = val;
  document.querySelectorAll(".star-btn").forEach(btn => {
    const starVal = parseInt(btn.getAttribute("data-star"));
    if (starVal <= val) {
      btn.classList.add("fill-amber-400", "text-amber-400");
      btn.classList.remove("text-slate-600");
    } else {
      btn.classList.remove("fill-amber-400", "text-amber-400");
      btn.classList.add("text-slate-600");
    }
  });
}

// ----------------- Review Submission -----------------
async function handleReviewSubmit(e) {
  e.preventDefault();
  const submitBtn = document.getElementById("submitReviewBtn");
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<div class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div><span>Analyzing NLP...</span>`;

  try {
    const payload = {
      category_slug: document.getElementById("modalCategory").value,
      item_name: document.getElementById("modalItemName").value.trim(),
      username: document.getElementById("modalUsername").value.trim(),
      rating: state.selectedModalRating,
      title: document.getElementById("modalTitle").value.trim(),
      text: document.getElementById("modalText").value.trim()
    };

    const res = await fetch("/api/reviews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to submit review");
    }

    const data = await res.json();
    showToast(`Review published! Classified as ${data.sentiment.label.toUpperCase()} (${data.sentiment.compound >= 0 ? '+' : ''}${data.sentiment.compound})`, "check");

    document.getElementById("reviewModal").classList.add("hidden");
    document.getElementById("reviewForm").reset();
    setModalRating(5);
    resetLiveSentiment();

    loadCategoryCounts();
    loadCurrentView();

  } catch (err) {
    showToast(err.message || "Failed to submit review", "alert-circle");
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = `<i data-lucide="send" class="w-3.5 h-3.5"></i><span>Publish Review</span>`;
    initLucide();
  }
}

// ----------------- Utilities -----------------
function showToast(message, icon = "check-circle") {
  const toast = document.getElementById("toast");
  const msgElem = document.getElementById("toastMsg");
  const iconElem = document.getElementById("toastIcon");

  msgElem.textContent = message;
  iconElem.setAttribute("data-lucide", icon);
  initLucide();

  toast.className = "fixed bottom-6 right-6 z-50 transform transition-all duration-300 flex items-center space-x-2.5 px-5 py-3.5 rounded-2xl shadow-2xl border text-xs font-bold bg-dark-950 text-white border-indigo-500/50 translate-y-0 opacity-100 glow-indigo";

  setTimeout(() => {
    toast.className = "fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none flex items-center space-x-2.5 px-5 py-3.5 rounded-2xl shadow-xl border text-xs font-semibold bg-dark-950 text-white border-indigo-500/40";
  }, 4000);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
