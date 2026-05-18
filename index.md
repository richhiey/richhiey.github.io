---
layout: home
permalink: /
---

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">About me</p>
    <h1 class="hero-title">
      AI systems,<br>
      audio ML,<br>
      and product-minded<br>
      engineering.
    </h1>
    <p class="hero-text">
      I build end-to-end machine learning systems with a focus on audio ML, agentic tools, and practical software that ships.
      My work spans data pipelines, real-time modeling, and cloud deployment across Python, TypeScript, and C++.
    </p>
    <div class="hero-actions">
      <a class="button button-primary" href="{{ '/projects' | relative_url }}">Projects</a>
      <a class="button button-secondary" href="{{ '/publications' | relative_url }}">Publications</a>
      <a class="button button-secondary" href="{{ '/blog' | relative_url }}">Blog</a>
    </div>
  </div>

  <div class="hero-panel">
    <article class="hero-card">
      <p class="card-label">Focus</p>
      <h2>Audio ML</h2>
      <p>Music transcription, event detection, ASR, and creative ML workflows.</p>
    </article>
    <article class="hero-card">
      <p class="card-label">Stack</p>
      <h2>Production systems</h2>
      <p>AWS, Docker, FastAPI, Flask, PySpark, Airflow, and modern TypeScript tooling.</p>
    </article>
    <article class="hero-card">
      <p class="card-label">Direction</p>
      <h2>Agentic products</h2>
      <p>Interfaces and infrastructure that make AI useful in real workflows.</p>
    </article>
  </div>
</section>

<section class="latest-block">
  <div class="section-heading">
    <p class="eyebrow">Latest</p>
    <h2>Five recent items</h2>
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
        <span class="latest-kind">{{ kind }}</span>
        <span class="latest-title">{{ item.title | escape }}</span>
        <span class="latest-date">{{ item.date | date: "%b %-d, %Y" }}</span>
      </a>
    {%- endfor -%}
  </div>
</section>
