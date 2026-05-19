---
layout: page
title: Blog
permalink: /blog/
show_title: false
---

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
