import streamlit.components.v1 as components

PWA_ASSET_VERSION = "20260420"


def inject_pwa_support() -> None:
    components.html(
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
          const pwaAssetVersion = "__PIGILAN_PWA_ASSET_VERSION__";
          const isLocalHost = ["localhost", "127.0.0.1"].includes(parentWindow.location.hostname);

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
            href: `/app/static/manifest.json?v=${pwaAssetVersion}`
          });
          ensureTag("link", {
            rel: "icon",
            type: "image/svg+xml",
            href: `/app/static/icon.svg?v=${pwaAssetVersion}`
          });
          ensureTag("link", {
            rel: "apple-touch-icon",
            href: `/app/static/icon.svg?v=${pwaAssetVersion}`
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

          function clearPigilanCaches() {
            if (!("caches" in parentWindow)) {
              return Promise.resolve();
            }

            return parentWindow.caches.keys().then((keys) =>
              Promise.all(
                keys
                  .filter((key) => key.startsWith("pigilan-static-"))
                  .map((key) => parentWindow.caches.delete(key))
              )
            );
          }

          if ("serviceWorker" in parentWindow.navigator && isLocalHost) {
            parentWindow.navigator.serviceWorker
              .getRegistrations()
              .then((registrations) =>
                Promise.all(
                  registrations
                    .filter((registration) => registration.scope.includes("/app/static/"))
                    .map((registration) => registration.unregister())
                )
              )
              .then(clearPigilanCaches)
              .catch((error) => console.warn("Pigilan local cache cleanup failed", error));
          } else if ("serviceWorker" in parentWindow.navigator) {
            parentWindow.navigator.serviceWorker
              .register(`/app/static/service-worker.js?v=${pwaAssetVersion}`)
              .catch((error) => console.warn("Pigilan service worker registration failed", error));
          }
        })();
        </script>
        """.replace("__PIGILAN_PWA_ASSET_VERSION__", PWA_ASSET_VERSION),
        height=0,
        width=0,
        scrolling=False,
    )
