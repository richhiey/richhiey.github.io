---
layout: page
title: Blog
permalink: /blog/
---

<div class="section-list">
  {%- assign posts = site.posts -%}
  {%- for post in posts -%}
    <article class="section-card section-card--wide">
      <p class="card-label">{{ post.date | date: "%b %-d, %Y" }}</p>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>
      <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
