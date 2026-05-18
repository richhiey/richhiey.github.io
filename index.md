---
layout: home
permalink: /
---

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">About me</p>
    <h1 class="hero-title">AI systems, audio ML, and product-minded engineering.</h1>
    <p class="hero-text">
      I build end-to-end machine learning systems with a focus on audio ML, agentic tools, and practical software that ships.
      My work spans data pipelines, real-time modeling, and cloud deployment across Python, TypeScript, and C++.
    </p>
    <div class="hero-actions">
      <a class="button button-primary" href="{{ '/projects' | relative_url }}">View Projects</a>
      <a class="button button-secondary" href="{{ '/publications' | relative_url }}">Read Publications</a>
    </div>
  </div>

  <div class="hero-panel">
    <div class="hero-card">
      <p class="card-label">Focus</p>
      <h2>Audio ML</h2>
      <p>Music transcription, event detection, ASR, and creative ML workflows.</p>
    </div>
    <div class="hero-card">
      <p class="card-label">Stack</p>
      <h2>Production systems</h2>
      <p>AWS, Docker, FastAPI, Flask, PySpark, Airflow, and modern TypeScript tooling.</p>
    </div>
    <div class="hero-card">
      <p class="card-label">Direction</p>
      <h2>Agentic products</h2>
      <p>Interfaces and infrastructure that make AI useful in real workflows.</p>
    </div>
  </div>
</section>

<section class="section-block">
  <div class="section-heading">
    <p class="eyebrow">Overview</p>
    <h2>What I’m working on</h2>
  </div>
  <div class="section-grid">
    <article class="section-card">
      <h3>Projects</h3>
      <p>Selected builds and experiments, including AgentFinder.</p>
      <a href="{{ '/projects' | relative_url }}">Explore projects</a>
    </article>
    <article class="section-card">
      <h3>Blog</h3>
      <p>Writing on AI systems, music technology, and the tools I’m building with.</p>
      <a href="{{ '/blog' | relative_url }}">Read the blog</a>
    </article>
    <article class="section-card">
      <h3>Publications</h3>
      <p>Long-form writing and detailed technical notes, including ERC-8004 registration flows.</p>
      <a href="{{ '/publications' | relative_url }}">Browse publications</a>
    </article>
  </div>
</section>

<section class="section-block">
  <div class="section-heading">
    <p class="eyebrow">Latest</p>
    <h2>Five most recent items</h2>
  </div>

  {%- assign latest_items = site.posts | concat: site.projects | concat: site.publications | sort: "date" | reverse -%}
  <div class="latest-list">
    {%- for item in latest_items limit: 5 -%}
      {%- assign kind = "Blog" -%}
      {%- if item.collection == "projects" -%}
        {%- assign kind = "Project" -%}
      {%- elsif item.collection == "publications" -%}
        {%- assign kind = "Publication" -%}
      {%- endif -%}
      <a class="latest-item" href="{{ item.url | relative_url }}">
        <span class="latest-meta">{{ kind }} · {{ item.date | date: "%b %-d, %Y" }}</span>
        <span class="latest-title">{{ item.title | escape }}</span>
        <span class="latest-arrow">Read</span>
      </a>
    {%- endfor -%}
  </div>
</section>
