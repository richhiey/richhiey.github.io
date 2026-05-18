---
layout: page
title: Blog
permalink: /blog/
show_title: false
---

<section class="page-intro">
  <p class="eyebrow">Blog</p>
  <h1 class="page-title">Notes, experiments, and technical essays.</h1>
  <p class="page-lead">A chronological archive of posts on AI systems, music technology, and product work.</p>
</section>

<div class="section-list">
  {%- assign posts = site.posts -%}
  {%- for post in posts -%}
    <article class="list-card">
      <div class="list-card__meta">
        <span>Blog</span>
        <span>{{ post.date | date: "%b %-d, %Y" }}</span>
      </div>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>
      <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
