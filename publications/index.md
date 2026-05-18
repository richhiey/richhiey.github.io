---
layout: page
title: Publications
permalink: /publications/
show_title: false
---

<section class="page-intro">
  <p class="eyebrow">Publications</p>
  <h1 class="page-title">Long-form writing and detailed technical notes.</h1>
  <p class="page-lead">Entries here keep the full context intact, including the ERC-8004 write-up.</p>
</section>

<div class="section-list">
  {%- assign publications = site.publications | sort: "date" | reverse -%}
  {%- for publication in publications -%}
    <article class="list-card">
      <div class="list-card__meta">
        <span>Publication</span>
        <span>{{ publication.date | date: "%b %-d, %Y" }}</span>
      </div>
      <h2><a href="{{ publication.url | relative_url }}">{{ publication.title | escape }}</a></h2>
      <p>{{ publication.summary | default: publication.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
