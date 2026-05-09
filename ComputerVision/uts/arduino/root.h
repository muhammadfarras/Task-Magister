#ifndef HOME_PAGE_H
#define HOME_PAGE_H

#include <Arduino.h>

String getHomePage() {
    String html = "";

    html += "<!doctype html>\n";
    html += "<meta charset='utf-8'>\n";
    html += "<title>Home</title>\n";
    html += "<style>\n";
    html += ":root{--bg1:#0f172a;--bg2:#0b3a5b;--accent:#7dd3fc}\n";
    html += "*{box-sizing:border-box;margin:0;padding:0}\n";
    html += "html,body{height:100%}\n";
    html += "body{\n";
    html += "  font-family:system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;\n";
    html += "  background:linear-gradient(135deg,var(--bg1),var(--bg2));\n";
    html += "  display:flex;align-items:center;justify-content:center;\n";
    html += "  -webkit-font-smoothing:antialiased;color:#e6f7ff;\n";
    html += "}\n";
    html += ".card{\n";
    html += "  padding:2.2rem 2.6rem;\n";
    html += "  border-radius:18px;\n";
    html += "  backdrop-filter:blur(8px) saturate(.9);\n";
    html += "  box-shadow:0 8px 30px rgba(2,6,23,.6),inset 0 1px 0 rgba(255,255,255,.02);\n";
    html += "  background:linear-gradient(180deg,rgba(255,255,255,.03),rgba(255,255,255,.01));\n";
    html += "  text-align:center;transform:translateY(0);\n";
    html += "  animation:float 4s ease-in-out infinite;\n";
    html += "  border:1px solid rgba(125,211,252,.09);\n";
    html += "}\n";
    html += "h1{\n";
    html += "  font-size:2.1rem;letter-spacing:.06em;margin-bottom:.35rem;\n";
    html += "  text-transform:lowercase;\n";
    html += "}\n";
    html += "p{margin:0;font-size:.95rem;opacity:.9;}\n";
    html += ".logo{\n";
    html += "  width:56px;height:56px;margin:0 auto 14px;border-radius:12px;\n";
    html += "  display:grid;place-items:center;\n";
    html += "  background:conic-gradient(from 90deg at 50% 50%,var(--accent),transparent 60%);\n";
    html += "  box-shadow:0 6px 18px rgba(7,18,36,.45);\n";
    html += "  border:1px solid rgba(125,211,252,.12);\n";
    html += "}\n";
    html += "@keyframes float{0%{transform:translateY(0)}50%{transform:translateY(-8px)}100%{transform:translateY(0)}}\n";
    html += "</style>\n";
    html += "<body>\n";
    html += "<div class='card' role='main' aria-label='home'>\n";
    html += "<div class='logo' aria-hidden='true'>🏠</div>\n";
    html += "<h1>this is home</h1>\n";
    html += "<p>welcome — cozy and simple.</p>\n";
    html += "</div>\n";
    html += "</body>\n";

    return html;
}

#endif
