(function () {
  "use strict";

  function setStatus(el, message) {
    if (el) {
      el.textContent = message;
    }
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    var ok = document.execCommand("copy");
    document.body.removeChild(ta);
    if (!ok) {
      throw new Error("copy failed");
    }
  }

  function initCopy() {
    var button = document.getElementById("copy-prompt");
    var status = document.getElementById("copy-status");
    var targetId = button && button.getAttribute("data-copy-target");
    var target = targetId && document.getElementById(targetId);
    if (!button || !target) {
      return;
    }
    var busy = false;
    button.addEventListener("click", function () {
      if (busy) {
        return;
      }
      busy = true;
      var text = target.textContent || "";
      copyText(text)
        .then(function () {
          setStatus(status, "コピーしました");
        })
        .catch(function () {
          setStatus(status, "コピーに失敗しました");
        })
        .finally(function () {
          window.setTimeout(function () {
            busy = false;
          }, 400);
        });
    });
  }

  function initAccordionControls() {
    var expand = document.getElementById("expand-all");
    var collapse = document.getElementById("collapse-all");
    var root = document.getElementById("agent-responses");
    if (!root) {
      return;
    }
    function setOpen(value) {
      root.querySelectorAll("details").forEach(function (d) {
        d.open = value;
      });
    }
    if (expand) {
      expand.addEventListener("click", function () {
        setOpen(true);
      });
    }
    if (collapse) {
      collapse.addEventListener("click", function () {
        setOpen(false);
      });
    }
  }

  function initGiscus() {
    var button = document.getElementById("load-giscus");
    var container = document.getElementById("giscus-container");
    if (!button || !container) {
      return;
    }
    button.addEventListener("click", function () {
      if (container.getAttribute("data-loaded") === "1") {
        return;
      }
      var script = document.createElement("script");
      script.src = container.getAttribute("data-giscus-src") || "https://giscus.app/client.js";
      script.async = true;
      script.crossOrigin = "anonymous";
      Array.prototype.forEach.call(container.attributes, function (attr) {
        if (attr.name.indexOf("data-") === 0 && attr.name !== "data-giscus-src" && attr.name !== "data-loaded") {
          script.setAttribute(attr.name, attr.value);
        }
      });
      container.hidden = false;
      container.appendChild(script);
      container.setAttribute("data-loaded", "1");
      button.disabled = true;
      button.textContent =
        "コメント領域を表示しました（設定がプレースホルダーの場合は読み込みに失敗します）";
    });
  }

  function byUpdated(a, b) {
    return String(b.updatedAt || "").localeCompare(String(a.updatedAt || "")) || String(b.id).localeCompare(String(a.id));
  }

  function byPublished(a, b) {
    return String(b.publishedAt || "").localeCompare(String(a.publishedAt || "")) || byUpdated(a, b);
  }

  function initHomeList() {
    var list = document.getElementById("article-list");
    if (!list) {
      return;
    }
    var source = list.getAttribute("data-source") || "./data/articles.json";
    var fallback = document.getElementById("list-fallback");
    var empty = document.getElementById("filter-empty");
    var keyword = document.getElementById("filter-keyword");
    var tag = document.getElementById("filter-tag");
    var agent = document.getElementById("filter-agent");
    var sort = document.getElementById("filter-sort");
    var count = document.getElementById("article-count");
    var articles = [];

    function fillSelect(select, values) {
      if (!select) {
        return;
      }
      values.forEach(function (value) {
        var opt = document.createElement("option");
        opt.value = value;
        opt.textContent = value;
        select.appendChild(opt);
      });
    }

    function render() {
      var q = (keyword && keyword.value ? keyword.value : "").trim().toLowerCase();
      var tagValue = tag ? tag.value : "";
      var agentValue = agent ? agent.value : "";
      var sorted = articles.slice().sort(sort && sort.value === "published" ? byPublished : byUpdated);
      var filtered = sorted.filter(function (item) {
        if (tagValue && item.tags.indexOf(tagValue) === -1) {
          return false;
        }
        if (agentValue && item.agents.indexOf(agentValue) === -1) {
          return false;
        }
        if (!q) {
          return true;
        }
        var hay = [item.id, item.title, item.description, item.slug].join(" ").toLowerCase();
        return hay.indexOf(q) !== -1;
      });

      list.textContent = "";
      if (empty) {
        empty.hidden = filtered.length !== 0;
      }
      filtered.forEach(function (item) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.className = "article-card";
        a.href = "." + item.url;

        var h3 = document.createElement("h3");
        h3.textContent = item.title;
        a.appendChild(h3);

        var meta = document.createElement("p");
        meta.textContent =
          item.id +
          " · " +
          item.status +
          " · 更新 " +
          item.updatedAt +
          (item.publishedAt ? " · 公開 " + item.publishedAt : "");
        a.appendChild(meta);

        var desc = document.createElement("p");
        desc.textContent = item.description;
        a.appendChild(desc);

        if (item.tags && item.tags.length) {
          var tags = document.createElement("p");
          tags.textContent = "タグ: " + item.tags.join(", ");
          a.appendChild(tags);
        }

        if (item.agents && item.agents.length) {
          var agents = document.createElement("p");
          agents.textContent = "AI: " + item.agents.join(", ");
          a.appendChild(agents);
        }

        li.appendChild(a);
        list.appendChild(li);
      });
    }

    fetch(source)
      .then(function (res) {
        if (!res.ok) {
          throw new Error("failed to load articles.json");
        }
        return res.json();
      })
      .then(function (data) {
        articles = Array.isArray(data.articles) ? data.articles : [];
        if (count) {
          count.textContent = String(articles.length);
        }
        var tags = {};
        var agents = {};
        articles.forEach(function (item) {
          (item.tags || []).forEach(function (t) {
            tags[t] = true;
          });
          (item.agents || []).forEach(function (name) {
            agents[name] = true;
          });
        });
        fillSelect(tag, Object.keys(tags).sort());
        fillSelect(agent, Object.keys(agents).sort());
        if (fallback) {
          fallback.hidden = true;
        }
        render();
      })
      .catch(function () {
        if (fallback) {
          fallback.textContent =
            "記事一覧の読み込みに失敗しました。data/articles.json を確認するか、ローカルサーバ経由で開いてください。";
        }
      });

    ["input", "change"].forEach(function (evt) {
      [keyword, tag, agent, sort].forEach(function (el) {
        if (el) {
          el.addEventListener(evt, render);
        }
      });
    });
  }

  initCopy();
  initAccordionControls();
  initGiscus();
  initHomeList();
})();
