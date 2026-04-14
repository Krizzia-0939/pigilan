import streamlit as st


def inject_pwa_support() -> None:
    st.iframe(
        """
        <style>
        html, body {
          margin: 0;
          padding: 0;
          width: 0;
          height: 0;
          overflow: hidden;
          background: transparent;
        }
        </style>
        <script>
        (function () {
          const frame = window.frameElement;
          if (frame) {
            frame.style.width = "0px";
            frame.style.minWidth = "0";
            frame.style.height = "0px";
            frame.style.minHeight = "0";
            frame.style.border = "0";
            frame.style.display = "block";
          }

          const parentWindow = window.parent;
          const parentDocument = parentWindow.document;

          function ensureTag(tagName, attrs) {
            const selector = Object.entries(attrs)
              .map(([key, value]) => `[${key}="${value}"]`)
              .join("");
            let element = parentDocument.head.querySelector(`${tagName}${selector}`);
            if (!element) {
              element = parentDocument.createElement(tagName);
              Object.entries(attrs).forEach(([key, value]) => {
                element.setAttribute(key, value);
              });
              parentDocument.head.appendChild(element);
            }
            return element;
          }

          ensureTag("link", {
            rel: "manifest",
            href: "/app/static/manifest.json"
          });
          ensureTag("link", {
            rel: "icon",
            type: "image/svg+xml",
            href: "/app/static/icon.svg"
          });
          ensureTag("link", {
            rel: "apple-touch-icon",
            href: "/app/static/icon.svg"
          });
          ensureTag("meta", {
            name: "theme-color",
            content: "#2f6f3e"
          });
          ensureTag("meta", {
            name: "apple-mobile-web-app-capable",
            content: "yes"
          });
          ensureTag("meta", {
            name: "apple-mobile-web-app-status-bar-style",
            content: "default"
          });

          if ("serviceWorker" in parentWindow.navigator) {
            parentWindow.navigator.serviceWorker
              .register("/app/static/service-worker.js")
              .catch((error) => console.warn("Pigilan service worker registration failed", error));
          }
        })();
        </script>
        """,
        height="content",
        width="content",
        tab_index=-1,
    )
